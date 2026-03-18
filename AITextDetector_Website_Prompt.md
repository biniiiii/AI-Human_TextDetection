# AI-Generated Text Detection Website — Full Prompt

## Project Overview

Building a full-stack web application called **"VeritAI"** — an AI-generated text detection platform powered by a fine-tuned BERT model. The system allows users to paste or upload text and instantly receive a classification result (AI-Generated or Human-Written) with a confidence score.

**Stack:**
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python), Hugging Face Transformers (BERT), PyTorch
- **Database:** SQLite (dev) / PostgreSQL (prod) via SQLAlchemy
- **Auth:** NextAuth.js (for admin role)

---

## Design System

**Aesthetic:** Utilitarian-editorial. Clinical precision meets document authenticity. Think forensic lab meets academic journal — sharp, no-nonsense, trustworthy. No gradients.

**Color Palette (CSS Variables):**
```css
--bg-primary: #F5F2EB;        /* Aged paper / warm off-white */
--bg-surface: #FFFFFF;
--bg-dark: #111111;
--accent: #C8102E;            /* Deep institutional red */
--accent-muted: #8B0000;
--text-primary: #1A1A1A;
--text-secondary: #5C5C5C;
--text-muted: #9E9E9E;
--border: #D4CFBF;
--border-dark: #2E2E2E;
--human: #1B4332;             /* Forest green — human */
--ai: #7B1D1D;                /* Deep red — AI */
--human-bg: #D8F3DC;
--ai-bg: #FCE4EC;
```

**Typography:**
- Display: `DM Serif Display` (headings, hero)
- Body: `IBM Plex Mono` (results, metrics, code-like data)
- UI: `Sora` (buttons, labels, nav)

**No gradients. No rounded pill buttons. Use sharp borders, monospace data displays, and stamp-like result badges.**

---

## Pages & Routes

### 1. `/` — Home / Landing Page

**Purpose:** Introduce the tool; drive users to try it.

**Layout:**
- Fixed top navbar: Logo "VeritAI" (left), nav links: Detect · About · History · Admin (right)
- Hero section:
  - Large serif headline: `"Is it real, or rendered?"` — left-aligned, 72px
  - Subheadline: `"BERT-powered AI text detection. Trained on 44,000+ samples. Built for academic integrity."`
  - Two stats blocks below headline (no animation needed): `44,552 Training Samples` | `99% Baseline Accuracy` | `3 Use Cases`
  - A single CTA button: `[ Analyze Text → ]` — sharp rectangle, black fill, white text
- Three use case cards below (sharp bordered cards, no shadow blur):
  1. 🎓 **Academic Integrity** — "Detect AI-written assignments in academic settings, including non-native English submissions."
  2. 🛡️ **Anti-Spam Bots** — "Filter AI-generated spam content used by automated bots."
  3. 📰 **Disinformation Filtering** — "Flag AI-generated news and propaganda on social media platforms."
- Footer: University name, team members, supervisor — monospaced, muted

---

### 2. `/detect` — Main Detection Page

**Purpose:** Core feature. User submits text, gets result.

**Layout:**

**Left panel (60% width):**
- Label: `TEXT INPUT` in small caps, monospaced
- Large `<textarea>` — full height, paper-white bg, 1px border, monospaced font, placeholder: `"Paste your text here. Minimum 50 words recommended for accurate classification."`
- Word count live counter below textarea: `Words: 0 / 512 (BERT token limit)`
- A toggle: `[ Preprocessing: ON | OFF ]` — shows what preprocessing will be applied
- Submit button: `[ RUN DETECTION ]` — full width, black, sharp, uppercase Sora font

**Right panel (40% width):**
- Before submission: Empty state — a dotted border box with text: `"Result will appear here"`
- After submission — Result Card:
  - Large stamp-style label: `AI-GENERATED` (red bg, white text) or `HUMAN-WRITTEN` (green bg, white text) — uppercase, bold, bordered like a physical stamp
  - Confidence meter: Horizontal bar (no animation), split into Human % and AI % — labeled with exact percentages
  - Two probability rows:
    - `Human Probability: 0.9985`
    - `AI Probability: 0.0015`
  - Timestamp: `Analyzed: 2026-03-11 14:32:07`
  - Processing time: `Inference time: 1.24s`
  - Feedback section below result:
    - Label: `Was this result correct?`
    - Two buttons: `[ ✓ Correct ]` `[ ✗ Incorrect ]` — outline style
    - Optional comment field that appears on "Incorrect" click

**Loading State:**
- Replace button with: `[ ANALYZING... ]` — monospaced blinking cursor animation
- Right panel shows: Scanning animation — text lines appearing one by one (CSS only)

**Error States:**
- Text too short: Inline red message below textarea: `"Text too short. Minimum 20 words required."`
- Server error: Red bordered box in result panel

---

### 3. `/history` — Detection History Page

**Purpose:** View past detection results. Filter and search.

**Layout:**
- Page title: `DETECTION LOG` — large, serif
- Filter bar (top):
  - Search input (monospaced)
  - Filter by label: `[ All ] [ AI-Generated ] [ Human-Written ]`
  - Date range picker
  - Sort: Latest First / Oldest First
- Table view (not cards):
  - Columns: `#` | `Text Preview` | `Label` | `Confidence` | `Date` | `Feedback`
  - Label column uses stamp-style badge
  - Confidence shown as exact decimal: `0.9912`
  - Clicking a row expands it inline to show full text and full metrics
- Pagination at bottom: `< Prev | Page 1 of 4 | Next >`
- Empty state: `"No detection history yet. Run your first analysis."`

---

### 4. `/about` — About the Project

**Purpose:** Technical transparency and academic context.

**Layout:**
- Two-column layout (text left, stats right)
- Section: **The Problem** — Detection bias against non-native English writers, paraphrasing evasion
- Section: **Our Approach** — BERT-base-uncased, 44,552 samples, Hugging Face Trainer
- Section: **Model Architecture** — a text-based architecture diagram (monospaced ASCII or SVG block diagram):
  ```
  Input Text → Preprocessing → WordPiece Tokenizer → BERT Encoder (12 layers) → [CLS] Token → Classification Head → Label + Confidence
  ```
- Section: **Metrics** — Table showing Precision / Recall / F1 for class 0 and class 1 (from the report: all 0.99)
- Section: **Limitations** — Honest acknowledgment: overfitting risk, limited OOD testing, paraphrased text gaps
- Section: **Team** — Four member cards: name + roll number. Supervisor listed separately.
- Section: **References** — numbered list in academic style

---

### 5. `/admin` — Admin Dashboard (Protected)

**Purpose:** Admin can monitor usage, manage models, view feedback.

**Auth:** Protected by NextAuth.js. Redirect to `/login` if unauthenticated.

**Layout:**
- Sidebar navigation: Dashboard · Submissions · Feedback · Models · Settings
- **Dashboard tab:**
  - 4 stat cards: Total Submissions | AI-Generated Count | Human Count | Avg Confidence
  - Bar chart (using Recharts or Chart.js): Submissions per day (last 14 days)
  - Pie chart: AI vs Human split
- **Submissions tab:**
  - Full table of all submissions with text, label, confidence, feedback status
  - Export to CSV button
- **Feedback tab:**
  - Table of user feedback: Text preview | Model prediction | User said | Comment
  - Flag samples for retraining
- **Models tab:**
  - Current model version displayed: `bert-base-uncased v1.0 (Feb 2026)`
  - Upload new model weights button
  - Model performance metrics table
- **Settings tab:**
  - Toggle: Enable/disable public submissions
  - Set min/max text length
  - API key management

---

## FastAPI Backend — Endpoints

```
POST   /api/detect              → Run detection on submitted text
GET    /api/history             → Get paginated detection history
GET    /api/history/{id}        → Get single detection result
POST   /api/feedback            → Submit feedback on a result
GET    /api/stats               → Aggregate stats (for admin dashboard)
GET    /api/admin/submissions   → All submissions (admin only)
GET    /api/admin/feedback      → All feedback entries (admin only)
POST   /api/admin/model/upload  → Upload new model weights (admin only)
DELETE /api/admin/submissions/{id} → Delete a submission (admin only)
```

**`POST /api/detect` — Request body:**
```json
{
  "text": "string",
  "apply_preprocessing": true
}
```

**`POST /api/detect` — Response:**
```json
{
  "id": "uuid",
  "label": "AI-Generated" | "Human-Written",
  "confidence": 0.9985,
  "human_prob": 0.0015,
  "ai_prob": 0.9985,
  "word_count": 134,
  "inference_time_ms": 1240,
  "timestamp": "2026-03-11T14:32:07Z",
  "preprocessed_text": "string (optional)"
}
```

**FastAPI model loading (startup):**
```python
from transformers import BertForSequenceClassification, BertTokenizer
import torch

model = BertForSequenceClassification.from_pretrained("./saved_model")
tokenizer = BertTokenizer.from_pretrained("./saved_model")
model.eval()
```

**Inference pipeline:**
1. Receive raw text
2. If `apply_preprocessing=true`: lowercase, remove digits/punctuation/stop words
3. Tokenize with `BertTokenizer` — max_length=512, truncation=True, padding=True
4. Run `model(**inputs)` → logits
5. Apply softmax → probabilities
6. Return label (argmax) + both class probabilities

**Database schema (SQLAlchemy):**
```python
class Detection(Base):
    id: UUID (primary key)
    raw_text: Text
    preprocessed_text: Text (nullable)
    label: String  # "AI-Generated" or "Human-Written"
    ai_prob: Float
    human_prob: Float
    confidence: Float
    inference_time_ms: Integer
    created_at: DateTime
    feedback_correct: Boolean (nullable)
    feedback_comment: String (nullable)
```

---

## Frontend Component Structure (Next.js)

```
app/
├── layout.tsx              (global fonts, navbar, footer)
├── page.tsx                (Landing)
├── detect/
│   └── page.tsx            (Detection page)
├── history/
│   └── page.tsx            (History log)
├── about/
│   └── page.tsx            (About)
├── admin/
│   ├── layout.tsx          (Sidebar + auth guard)
│   └── page.tsx            (Dashboard)
├── login/
│   └── page.tsx

components/
├── Navbar.tsx
├── Footer.tsx
├── TextInput.tsx           (textarea + word counter + toggle)
├── ResultCard.tsx          (stamp label + confidence bar + feedback)
├── HistoryTable.tsx        (expandable rows)
├── StatsCard.tsx
├── ModelInfo.tsx
├── FeedbackButtons.tsx
├── LoadingScanner.tsx      (CSS animation)
├── UseCaseCard.tsx

lib/
├── api.ts                  (fetch wrappers for FastAPI)
├── types.ts                (TypeScript interfaces)
```

---

## Key Interaction Details

**Word count + token warning:**
- Show live word count as user types
- Warn at >400 words: `"Text will be truncated to BERT's 512-token limit"`

**Preprocessing toggle:**
- When ON: Show a small preview of what the cleaned text looks like before sending
- When OFF: Send raw text directly to model

**Stamp animation on result:**
- CSS only: Result badge "stamps" into view with a scale transform from 1.3 → 1.0 + opacity 0 → 1, duration 200ms

**History expandable rows:**
- Click row → inline expansion (no modal) showing full text and a mini confidence breakdown

**Feedback flow:**
- After getting result, user sees: `Was this correct? [ ✓ Yes ] [ ✗ No ]`
- On "No": Text input appears: `"What should it be? (optional comment)"`
- Feedback stored and flagged for admin review

---

## Non-Functional Requirements (from report)

- Classification result must appear within **15 seconds** of submission
- System must achieve **≥95% accuracy** on validation set
- Interface must be usable with **minimal technical knowledge**
- Deployable on standard laptops (CPU inference supported, just slower)
- Submitted text must **not be used without user consent** — add a privacy notice on detect page: `"Your submitted text is stored locally for history. It will not be used for retraining without your explicit consent."`

---

## Styling Notes

- Use `border: 1px solid var(--border)` everywhere — no box shadows that blur
- Buttons: `border: 2px solid var(--text-primary)`, no border-radius (or max 2px)
- Result stamp: Bold uppercase, 2px solid border, no border-radius
- Tables: No zebra striping — use top/bottom border per row only
- All numbers/metrics: `font-family: 'IBM Plex Mono'`
- Section headers: Small caps, letter-spacing 0.15em, color: `var(--text-secondary)`
- Hover states: Background shifts to `#EDEAE0` (slightly darker paper) — no color change
- Focus states: `outline: 2px solid var(--accent)` — red, no offset

---

## Deployment Notes

- FastAPI: Run with `uvicorn main:app --host 0.0.0.0 --port 8000`
- Next.js: `next build && next start` on port 3000
- CORS: FastAPI must allow `http://localhost:3000` during dev
- Model files: Store in `/backend/saved_model/` — mounted as volume in Docker
- Environment variables needed:
  - `NEXT_PUBLIC_API_URL=http://localhost:8000`
  - `NEXTAUTH_SECRET=...`
  - `DATABASE_URL=sqlite:///./detections.db`
