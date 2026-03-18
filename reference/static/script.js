// State Management
let isAnalyzing = false;

// DOM Elements
const analyzeBtn = document.getElementById('analyzeBtn');
const textInput = document.getElementById('textInput');
const initialState = document.getElementById('initialState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');
const errorNotification = document.getElementById('errorNotification');
const errorMessage = document.getElementById('errorMessage');
const errorClose = document.getElementById('errorClose');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners
    analyzeBtn.addEventListener('click', handleAnalyze);
    if (errorClose) {
        errorClose.addEventListener('click', hideError);
    }
});

// Show Error Notification
function showError(message) {
    errorMessage.textContent = message;
    errorNotification.classList.add('show');
}

// Hide Error Notification
function hideError() {
    errorNotification.classList.remove('show');
}

// Handle Analyze Button Click
async function handleAnalyze() {
    const text = textInput.value.trim();
    
    // Validation
    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    if (text.split(/\s+/).length < 50) {
        showError('Please enter at least 50 words for accurate analysis.');
        return;
    }
    
    // Hide error if validation passes
    hideError();
    
    if (isAnalyzing) {
        return;
    }
    
    isAnalyzing = true;
    analyzeBtn.disabled = true;
    analyzeBtn.style.opacity = '0.6';
    
    // Show loading state
    showLoading();
    
    try {
        // Call Flask API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed. Please try again.');
        }
        
        const data = await response.json();
        
        // Simulate loading progress
        await simulateProgress();
        
        // Show results
        showResult(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred. Please try again.');
        showInitial();
    } finally {
        isAnalyzing = false;
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = '1';
    }
}

// Show Loading State
function showLoading() {
    initialState.classList.remove('active');
    resultState.classList.remove('active');
    loadingState.classList.add('active');
    
    // Reset loading percentage
    const spinnerPercent = document.querySelector('.spinner-percent');
    if (spinnerPercent) {
        animateValue(spinnerPercent, 0, 100, 2000, '%');
    }
}

// Simulate Progress
function simulateProgress() {
    return new Promise(resolve => {
        setTimeout(resolve, 2000);
    });
}

// Show Result State
function showResult(data) {
    loadingState.classList.remove('active');
    resultState.classList.add('active');
    
    // Extract data
    const probability = Math.round(data.probability * 100);
    const confidence = Math.round(data.confidence * 100);
    const isAI = data.label === 'AI-Generated' || data.label === 1;
    
    // Update result elements
    const resultPercent = document.getElementById('resultPercent');
    const resultLabel = document.getElementById('resultLabel');
    const resultTitle = document.getElementById('resultTitle');
    const resultDescription = document.getElementById('resultDescription');
    const confidencePercent = document.getElementById('confidencePercent');
    const confidenceFill = document.getElementById('confidenceFill');
    const resultCircle = document.getElementById('resultCircle');
    
    // Set label and colors first
    resultLabel.textContent = isAI ? 'AI-Generated' : 'Human-Written';
    
    // Set title and description
    if (isAI) {
        resultTitle.textContent = 'AI-Generated Content Detected';
        resultDescription.textContent = 'The text exhibits patterns characteristic of AI-generated content.';
        resultCircle.style.stroke = '#ef4444';
    } else {
        resultTitle.textContent = 'Human-Written Content';
        resultDescription.textContent = 'The text shows characteristics of human-written content.';
        resultCircle.style.stroke = '#10b981';
    }
    
    // Animate percentage text
    animateValue(resultPercent, 0, probability, 1000, '%');
    
    // Animate circle progress synchronized with percentage
    animateCircle(resultCircle, probability, 1000);
    
    // Animate confidence
    confidencePercent.textContent = confidence + '%';
    confidenceFill.style.width = confidence + '%';
}

// Show Initial State
function showInitial() {
    loadingState.classList.remove('active');
    resultState.classList.remove('active');
    initialState.classList.add('active');
}

// Animate Circle Progress
function animateCircle(element, endPercentage, duration) {
    const circumference = 2 * Math.PI * 60;
    const startOffset = circumference; // Start at 0%
    const endOffset = circumference - (endPercentage / 100) * circumference; // End at target %
    
    const range = endOffset - startOffset;
    const increment = range / (duration / 16);
    let current = startOffset;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= endOffset) || (increment < 0 && current <= endOffset)) {
            current = endOffset;
            clearInterval(timer);
        }
        element.style.strokeDashoffset = current;
    }, 16);
}

// Animate Number Value
function animateValue(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, 16);
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// DEMO MODE
const DEMO_MODE = false;

if (DEMO_MODE) {
    const originalHandleAnalyze = handleAnalyze;
    handleAnalyze = async function() {
        const text = textInput.value.trim();
        
        if (!text) {
            showError('Please enter some text to analyze.');
            return;
        }
        
        if (isAnalyzing) return;
        
        isAnalyzing = true;
        analyzeBtn.disabled = true;
        analyzeBtn.style.opacity = '0.6';
        
        showLoading();
        
        await simulateProgress();
        
        // Demo data
        const demoData = {
            label: Math.random() > 0.5 ? 'AI-Generated' : 'Human-Written',
            probability: 0.75 + Math.random() * 0.24,
            confidence: 0.85 + Math.random() * 0.14
        };
        
        showResult(demoData);
        
        isAnalyzing = false;
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = '1';
    };
}
