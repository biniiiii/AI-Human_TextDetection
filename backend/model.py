import os
import math
from pathlib import Path
import numpy as np
import torch
from transformers import pipeline, GPT2LMHeadModel, GPT2TokenizerFast
# from lime.lime_text import LimeTextExplainer

MODEL_MAX_LENGTH = int(os.getenv("MODEL_MAX_LENGTH", "350"))
MODEL_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "distilbert-base-uncased_length_set_balanced")
LEGACY_MODEL_PATH = os.getenv("MODEL_PATH", DEFAULT_MODEL_NAME)


def _is_local_model_dir(path: Path) -> bool:
    has_tokenizer = (path / "tokenizer.json").exists() or (path / "tokenizer_config.json").exists()
    return path.is_dir() and (path / "config.json").exists() and has_tokenizer


def _discover_model_paths() -> dict[str, str]:
    discovered: dict[str, str] = {}

    for child in MODEL_DIR.iterdir():
        if _is_local_model_dir(child):
            discovered[child.name] = str(child)

    legacy_path = Path(LEGACY_MODEL_PATH)
    if not legacy_path.is_absolute():
        legacy_path = (MODEL_DIR / legacy_path).resolve()

    if legacy_path.exists():
        discovered.setdefault(legacy_path.name, str(legacy_path))
    elif not discovered:
        # Keep support for remote Hugging Face model IDs when no local model folders exist.
        discovered[DEFAULT_MODEL_NAME] = LEGACY_MODEL_PATH

    return dict(sorted(discovered.items()))


AVAILABLE_MODELS = _discover_model_paths()
albert_model = os.getenv("ALBERT_MODEL_NAME")
if albert_model:
    AVAILABLE_MODELS[albert_model] = albert_model


def _resolve_default_model_name() -> str:
    if DEFAULT_MODEL_NAME in AVAILABLE_MODELS:
        return DEFAULT_MODEL_NAME

    legacy_name = Path(LEGACY_MODEL_PATH).name
    if legacy_name in AVAILABLE_MODELS:
        return legacy_name

    return next(iter(AVAILABLE_MODELS))


DEFAULT_SELECTED_MODEL = _resolve_default_model_name()

_classifier_cache: dict[str, object] = {}
_label_map_cache: dict[str, dict[str, int]] = {}

# # GPT-2 for perplexity calculation
# _ppl_model_id = "gpt2"
# _ppl_tokenizer = GPT2TokenizerFast.from_pretrained(_ppl_model_id)
# _ppl_model = GPT2LMHeadModel.from_pretrained(_ppl_model_id)
# _ppl_model.eval()

# GPT-2 for perplexity calculation (lazy loaded)
_ppl_model_id = "gpt2"
_ppl_tokenizer = None
_ppl_model = None

# LIME explainer (class 0 = Human, class 1 = AI)
# explainer = LimeTextExplainer(class_names=["Human-Written", "AI-Generated"])
_explainer = None

def get_explainer():
    global _explainer
    if _explainer is None:
        from lime.lime_text import LimeTextExplainer
        _explainer = LimeTextExplainer(class_names=["Human-Written", "AI-Generated"])
    return _explainer


def _label_to_id_map(classifier) -> dict[str, int]:
    mapping = getattr(classifier.model.config, "label2id", None) or {}
    normalized: dict[str, int] = {}
    for label, index in mapping.items():
        try:
            normalized[str(label)] = int(index)
        except (TypeError, ValueError):
            continue
    return normalized


def get_available_models() -> list[str]:
    return list(AVAILABLE_MODELS.keys())


def get_default_model_name() -> str:
    return DEFAULT_SELECTED_MODEL


def resolve_model_name(model_name: str | None) -> str:
    requested = (model_name or "").strip()
    if not requested:
        return DEFAULT_SELECTED_MODEL

    if requested not in AVAILABLE_MODELS:
        available = ", ".join(AVAILABLE_MODELS.keys())
        raise ValueError(f"Unknown model '{requested}'. Available models: {available}")

    return requested


def _get_classifier_and_labels(model_name: str):
    if model_name not in _classifier_cache:
        model_path = AVAILABLE_MODELS[model_name]
        classifier = pipeline("text-classification", model=model_path, tokenizer=model_path)
        _classifier_cache[model_name] = classifier
        _label_map_cache[model_name] = _label_to_id_map(classifier)

    return _classifier_cache[model_name], _label_map_cache[model_name]


def _scores_to_probs(scores: list[dict], label_to_id: dict[str, int]) -> tuple[float, float]:
    human_prob = None
    ai_prob = None

    for item in scores:
        label = str(item["label"])
        score = float(item["score"])
        label_upper = label.upper()

        if label_upper in {"REAL", "HUMAN", "HUMAN-WRITTEN", "LABEL_0"}:
            human_prob = score
            continue
        if label_upper in {"FAKE", "AI", "AI-GENERATED", "LABEL_1"}:
            ai_prob = score
            continue

        mapped_index = label_to_id.get(label)
        if mapped_index == 0:
            human_prob = score
        elif mapped_index == 1:
            ai_prob = score

    if human_prob is None or ai_prob is None:
        raise ValueError("Unable to map model output labels to human/AI probabilities.")

    return human_prob, ai_prob


def _predict_proba(texts: list[str], model_name: str) -> np.ndarray:
    """Return (n_samples, 2) array of [human_prob, ai_prob] for LIME."""
    classifier, label_to_id = _get_classifier_and_labels(model_name)
    results = classifier(list(texts), top_k=None, truncation=True, max_length=MODEL_MAX_LENGTH)
    if results and isinstance(results, list) and results and isinstance(results[0], dict):
        results = [results]

    probs = []
    for scores in results:
        human, ai = _scores_to_probs(scores, label_to_id)
        probs.append([human, ai])
    return np.array(probs)


def predict_text(text: str, model_name: str | None = None) -> dict:
    resolved_model = resolve_model_name(model_name)
    classifier, label_to_id = _get_classifier_and_labels(resolved_model)

    raw_scores = classifier(text, top_k=None, truncation=True, max_length=MODEL_MAX_LENGTH)
    if isinstance(raw_scores, list) and raw_scores and isinstance(raw_scores[0], list):
        scores = raw_scores[0]
    else:
        scores = raw_scores

    human_prob, ai_prob = _scores_to_probs(scores, label_to_id)
    confidence = max(human_prob, ai_prob)
    label = "Human-Written" if human_prob >= ai_prob else "AI-Generated"
    return {
        "label": label,
        "confidence": round(confidence, 6),
        "human_prob": round(human_prob, 6),
        "ai_prob": round(ai_prob, 6),
        "model_name": resolved_model,
    }



# def compute_perplexity(text: str) -> float:
#     """Compute perplexity of text using GPT-2. Lower = more predictable (likely AI)."""
#     encodings = _ppl_tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
#     input_ids = encodings.input_ids
#     with torch.no_grad():
#         outputs = _ppl_model(input_ids, labels=input_ids)
#         neg_log_likelihood = outputs.loss
#     return round(math.exp(neg_log_likelihood.item()), 2)
def compute_perplexity(text: str) -> float:
    global _ppl_tokenizer, _ppl_model
    if _ppl_tokenizer is None:
        _ppl_tokenizer = GPT2TokenizerFast.from_pretrained(_ppl_model_id)
        _ppl_model = GPT2LMHeadModel.from_pretrained(_ppl_model_id)
        _ppl_model.eval()
    encodings = _ppl_tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    input_ids = encodings.input_ids
    with torch.no_grad():
        outputs = _ppl_model(input_ids, labels=input_ids)
        neg_log_likelihood = outputs.loss
    return round(math.exp(neg_log_likelihood.item()), 2)
def explain_text(
    text: str,
    num_features: int = 10,
    num_samples: int = 200,
    model_name: str | None = None,
) -> list[dict]:
    """Run LIME explanation and return top feature words with weights."""
    
    resolved_model = resolve_model_name(model_name)

    explainer = get_explainer()

    exp = explainer.explain_instance(
        text,
        lambda texts: _predict_proba(texts, resolved_model),
        num_features=num_features,
        num_samples=num_samples,
    )

    return [{"word": word, "weight": round(weight, 6)} for word, weight in exp.as_list()]

    # exp = explainer.explain_instance(
    #     text,
    #     lambda texts: _predict_proba(texts, resolved_model),
    #     num_features=num_features,
    #     num_samples=num_samples,
    # )
    # exp.as_list() returns [(word, weight), ...] where positive = class 1 (AI)
    