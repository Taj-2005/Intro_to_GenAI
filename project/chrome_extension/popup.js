/**
 * Popup script for Chrome extension.
 */
const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultsDiv = document.getElementById('results');
const noDataDiv = document.getElementById('no-data');
const analyzeBtn = document.getElementById('analyze-btn');
const refreshBtn = document.getElementById('refresh-btn');

// Get current tab
async function getCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
}

// Extract job data from current page
async function extractJobData() {
    const tab = await getCurrentTab();
    
    try {
        const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractJobData' });
        if (response && response.success) {
            return response.data;
        }
    } catch (error) {
        console.error('Error extracting job data:', error);
    }
    
    // Fallback: try to get from storage
    const stored = await chrome.storage.local.get('extractedJobData');
    return stored.extractedJobData || null;
}

// Analyze job posting
async function analyzeJobPosting(jobData) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_title: jobData.job_title || '',
                company_name: jobData.company_name || '',
                salary: jobData.salary || '',
                description: jobData.description || '',
                source: jobData.source || 'unknown'
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error analyzing job:', error);
        throw error;
    }
}

// Display results
function displayResults(jobData, analysisResult) {
    // Hide other sections
    loadingDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    noDataDiv.classList.add('hidden');
    resultsDiv.classList.remove('hidden');

    // Update prediction
    const predictionText = document.getElementById('prediction-text');
    const predictionBadge = document.getElementById('prediction-badge');
    const confidenceValue = document.getElementById('confidence-value');
    const confidenceLabel = document.getElementById('confidence-label');

    const isFake = analysisResult.prediction === 'FAKE';
    predictionText.textContent = isFake ? '⚠️ High Risk Scam' : '✅ Likely Genuine';
    predictionBadge.className = `prediction-badge ${isFake ? 'fake' : 'real'}`;
    
    const trustScore = isFake ? (100 - analysisResult.confidence) : analysisResult.confidence;
    confidenceValue.textContent = `${trustScore}%`;
    confidenceLabel.textContent = isFake ? 'likely scam' : 'trust score';

    // Update reasons
    const reasonsList = document.getElementById('reasons-list');
    reasonsList.innerHTML = '';
    analysisResult.reasons.forEach(reason => {
        const li = document.createElement('li');
        li.textContent = reason;
        reasonsList.appendChild(li);
    });

    // Update job info
    document.getElementById('job-title').textContent = jobData.job_title || 'N/A';
    document.getElementById('company-name').textContent = jobData.company_name || 'N/A';
}

// Display error
function displayError(message) {
    loadingDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    noDataDiv.classList.add('hidden');
    errorDiv.classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
}

// Show no data message
function showNoData() {
    loadingDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    noDataDiv.classList.remove('hidden');
}

// Main analyze function
async function analyze() {
    // Show loading
    loadingDiv.classList.remove('hidden');
    errorDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    noDataDiv.classList.add('hidden');

    try {
        // Extract job data
        const jobData = await extractJobData();
        
        if (!jobData || !jobData.description || jobData.description.length < 50) {
            showNoData();
            return;
        }

        // Analyze
        const analysisResult = await analyzeJobPosting(jobData);
        
        // Display results
        displayResults(jobData, analysisResult);
    } catch (error) {
        displayError(`Error: ${error.message}. Make sure the backend server is running at ${API_BASE_URL}`);
    }
}

// Refresh data
async function refresh() {
    const tab = await getCurrentTab();
    try {
        await chrome.tabs.sendMessage(tab.id, { action: 'extractJobData' });
        analyze();
    } catch (error) {
        console.error('Error refreshing:', error);
        analyze(); // Try anyway
    }
}

// Event listeners
analyzeBtn.addEventListener('click', analyze);
refreshBtn.addEventListener('click', refresh);

// Auto-analyze on load
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(analyze, 500);
});
