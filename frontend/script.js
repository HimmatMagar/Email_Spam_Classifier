// Configuration
const API_URL = 'http://127.0.0.1:8000/predict';

// DOM Elements
const emailInput = document.getElementById('emailInput');
const predictBtn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');
const btnText = predictBtn.querySelector('.btn-text');
const spinner = predictBtn.querySelector('.spinner');
const resultSection = document.getElementById('resultSection');
const resultCard = document.getElementById('resultCard');
const resultIcon = document.getElementById('resultIcon');
const resultTitle = document.getElementById('resultTitle');
const resultMessage = document.getElementById('resultMessage');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
predictBtn.addEventListener('click', handlePredict);
clearBtn.addEventListener('click', handleClear);

// Allow Ctrl+Enter to submit
emailInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        handlePredict();
    }
});

/**
 * Handle prediction request
 */
async function handlePredict() {
    const emailText = emailInput.value.trim();

    // Validation
    if (!emailText) {
        showError('Please enter some email content to classify.');
        return;
    }

    if (emailText.length < 5) {
        showError('Email content is too short. Please enter more text.');
        return;
    }

    // Reset UI
    hideError();
    hideResult();
    setLoading(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: emailText }),
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('API Response:', data);

        displayResult(data);

    } catch (error) {
        console.error('Prediction error:', error);
        if (error.message.includes('Failed to fetch')) {
            showError(
                'Cannot connect to the prediction server. ' +
                'Make sure the FastAPI server is running at http://127.0.0.1:8000'
            );
        } else {
            showError(`Error: ${error.message}`);
        }
    } finally {
        setLoading(false);
    }
}

/**
 * Display prediction result
 * Adjust the logic below based on your API's response format.
 */
function displayResult(data) {
    // Try to extract prediction and confidence from various possible formats
    let isSpam = false;
    let confidence = 0;

    // Handle different possible response formats
    if (typeof data.prediction === 'string') {
        isSpam = data.prediction.toLowerCase() === 'spam';
    } else if (typeof data.prediction === 'number') {
        isSpam = data.prediction === 1;
    } else if (typeof data.label === 'string') {
        isSpam = data.label.toLowerCase() === 'spam';
    } else if (typeof data.result === 'string') {
        isSpam = data.result.toLowerCase() === 'spam';
    }

    // Extract confidence/probability
    if (typeof data.confidence === 'number') {
        confidence = data.confidence;
    } else if (typeof data.probability === 'number') {
        confidence = data.probability;
    } else if (typeof data.score === 'number') {
        confidence = data.score;
    } else if (data.probabilities && typeof data.probabilities === 'object') {
        // e.g. { spam: 0.95, ham: 0.05 }
        const spamProb = data.probabilities.spam ?? data.probabilities.SPAM ?? 0;
        const hamProb = data.probabilities.ham ?? data.probabilities.HAM ?? 0;
        confidence = isSpam ? spamProb : hamProb;
    }

    // Convert to percentage if needed
    if (confidence > 0 && confidence <= 1) {
        confidence = confidence * 100;
    }

    // Fallback if no confidence was found
    if (confidence === 0) {
        confidence = isSpam ? 95 : 90; // placeholder
    }

    confidence = Math.round(confidence);

    // Update UI
    resultCard.classList.remove('spam', 'ham');
    
    if (isSpam) {
        resultCard.classList.add('spam');
        resultIcon.textContent = '⚠️';
        resultTitle.textContent = 'Spam Detected';
        resultMessage.textContent = 'This email appears to be spam. Be cautious!';
    } else {
        resultCard.classList.add('ham');
        resultIcon.textContent = '✅';
        resultTitle.textContent = 'Not Spam';
        resultMessage.textContent = 'This email appears to be legitimate.';
    }

    confidenceValue.textContent = `${confidence}%`;
    confidenceFill.style.width = '0%';
    resultSection.classList.remove('hidden');

    // Animate confidence bar
    setTimeout(() => {
        confidenceFill.style.width = `${confidence}%`;
    }, 100);
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

function hideError() {
    errorSection.classList.add('hidden');
}

function hideResult() {
    resultSection.classList.add('hidden');
}

/**
 * Set loading state
 */
function setLoading(isLoading) {
    predictBtn.disabled = isLoading;
    if (isLoading) {
        btnText.textContent = 'Classifying...';
        spinner.classList.remove('hidden');
    } else {
        btnText.textContent = 'Classify Email';
        spinner.classList.add('hidden');
    }
}

/**
 * Clear input and results
 */
function handleClear() {
    emailInput.value = '';
    hideResult();
    hideError();
    emailInput.focus();
}