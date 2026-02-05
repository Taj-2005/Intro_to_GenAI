# User Manual

## Fake Job Posting Detection System

### Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Chrome Extension](#using-the-chrome-extension)
4. [Using the Web Dashboard](#using-the-web-dashboard)
5. [Understanding Results](#understanding-results)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Introduction

The Fake Job Posting Detection System helps you identify potentially fraudulent job postings using AI-powered analysis. The system can be used in two ways:

1. **Chrome Extension:** Automatically analyze job postings while browsing LinkedIn, Indeed, or Naukri
2. **Web Dashboard:** Manually paste and analyze job descriptions

### Key Features

- ✅ Automatic job posting analysis
- ✅ Trust score (0-100%)
- ✅ Explainable reasons for predictions
- ✅ History of analyzed jobs
- ✅ Analytics and scam pattern detection

---

## Getting Started

### Prerequisites

- Chrome browser (for extension)
- Internet connection
- Backend server running (for API access)

### Installation

#### Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome_extension` folder
5. The extension icon should appear in your toolbar

#### Web Dashboard

1. Navigate to the deployed dashboard URL (or `http://localhost:3000` for local development)
2. No installation required - works in any modern browser

---

## Using the Chrome Extension

### Step 1: Navigate to a Job Posting

Visit a job posting page on one of these platforms:
- LinkedIn (linkedin.com/jobs)
- Indeed (indeed.com)
- Naukri (naukri.com)

### Step 2: Open the Extension

1. Click the extension icon in your Chrome toolbar
2. The extension will automatically extract job details from the page

### Step 3: Analyze

1. Click the "Analyze Job Posting" button
2. Wait a few seconds for analysis
3. View the results in the popup

### Step 4: Review Results

The popup will show:
- **Prediction:** "Likely Genuine" or "High Risk Scam"
- **Trust Score:** Percentage indicating confidence
- **Key Reasons:** List of factors that influenced the decision
- **Job Information:** Title and company name

### Refreshing Data

If the extension doesn't extract data correctly:
1. Click "Refresh Data" button
2. Wait a moment for re-extraction
3. Click "Analyze Job Posting" again

---

## Using the Web Dashboard

### Accessing the Dashboard

1. Open your web browser
2. Navigate to the dashboard URL
3. You'll see three tabs: Analyze, History, and Analytics

### Analyze Tab

#### Manual Analysis

1. **Enter Job Information (Optional):**
   - Job Title
   - Company Name
   - Salary

2. **Paste Job Description:**
   - Copy the full job description from any source
   - Paste it into the "Job Description" text area
   - *Required field*

3. **Analyze:**
   - Click "Analyze Job Posting" button
   - Wait for analysis (usually 2-5 seconds)

4. **View Results:**
   - Prediction badge (Likely Genuine / High Risk Scam)
   - Trust score percentage
   - List of key reasons

#### Tips for Best Results

- Include the complete job description
- Copy text directly (avoid images)
- Include salary information if available
- Include company name if mentioned

### History Tab

View all previously analyzed jobs:

1. Click the "History" tab
2. See list of recent analyses with:
   - Job title and company
   - Prediction result
   - Confidence score
   - Analysis timestamp

3. Jobs are sorted by most recent first

### Analytics Tab

View system-wide statistics:

1. Click the "Analytics" tab
2. View metrics:
   - **Total Analyzed:** Total number of jobs analyzed
   - **Fake Jobs:** Count and percentage of fake jobs detected
   - **Real Jobs:** Count and percentage of legitimate jobs

3. **Common Scam Patterns:**
   - See most frequently detected scam indicators
   - Helps identify common tactics used by scammers

---

## Understanding Results

### Prediction Types

#### ✅ Likely Genuine
- The job posting appears legitimate
- Low risk indicators detected
- Trust score typically 70%+

#### ⚠️ High Risk Scam
- Multiple suspicious indicators detected
- Exercise caution before applying
- Trust score typically <70%

### Trust Score

The trust score (0-100%) indicates confidence in the prediction:
- **90-100%:** Very high confidence
- **70-89%:** High confidence
- **50-69%:** Moderate confidence
- **0-49%:** Low confidence

**Note:** For "High Risk Scam" predictions, the score shows "likely scam" percentage (inverse of confidence).

### Key Reasons

The system provides explainable reasons for its decision:

#### Common Reasons for Fake Jobs:
- "Use of urgency-based language detected"
- "Emotional manipulation tactics identified"
- "Personal email domain detected instead of company email"
- "Missing or suspicious company information"
- "Suspicious keywords related to financial scams detected"
- "Unrealistic salary claims with low requirements"
- "Unusually short job description"

#### Common Reasons for Real Jobs:
- "Company information provided"
- "Detailed job description provided"
- "No urgency-based language detected"
- "No suspicious keywords detected"

### Interpreting Results

**Important Considerations:**

1. **AI-Based Predictions:** Results are based on machine learning analysis, not legal verification
2. **Always Verify:** Independently verify job postings through:
   - Company website
   - Official contact information
   - Professional networks
   - Job board verification

3. **False Positives/Negatives:** The system may occasionally misclassify jobs
4. **Use as Tool:** Treat results as one factor in your decision-making process

---

## Troubleshooting

### Chrome Extension Issues

#### Extension Not Extracting Data

**Problem:** "No job posting detected on this page"

**Solutions:**
1. Ensure you're on a job posting page (not search results)
2. Wait for page to fully load
3. Click "Refresh Data" button
4. Try refreshing the page and re-opening extension

#### Analysis Fails

**Problem:** "Error: API error" or connection errors

**Solutions:**
1. Check if backend server is running
2. Verify internet connection
3. Check if API URL is correct in extension settings
4. Try again after a few moments

#### Extension Not Appearing

**Problem:** Extension icon not in toolbar

**Solutions:**
1. Go to `chrome://extensions/`
2. Ensure extension is enabled
3. Click "Details" → "Extension options" to pin to toolbar

### Web Dashboard Issues

#### Cannot Connect to Backend

**Problem:** "Error analyzing job posting"

**Solutions:**
1. Verify backend server is running
2. Check `NEXT_PUBLIC_API_URL` environment variable
3. Check browser console for detailed errors
4. Verify CORS is configured correctly

#### Results Not Showing

**Problem:** Analysis completes but no results displayed

**Solutions:**
1. Check browser console for JavaScript errors
2. Try refreshing the page
3. Clear browser cache
4. Try a different browser

#### Statistics Not Loading

**Problem:** Analytics tab shows "Loading statistics..."

**Solutions:**
1. Check backend connection
2. Verify MongoDB is accessible
3. Check backend logs for errors

---

## FAQ

### General Questions

**Q: Is this system 100% accurate?**
A: No. The system uses machine learning and may have false positives/negatives. Always verify independently.

**Q: Does the system store my personal information?**
A: No. The system only stores job posting data and analysis results. No personal user data is collected.

**Q: Can I use this for any job board?**
A: The Chrome extension works best with LinkedIn, Indeed, and Naukri. The web dashboard works with any job description.

**Q: How often is the model updated?**
A: Model updates depend on the deployment. Check with your system administrator.

**Q: What if I disagree with a prediction?**
A: The system is a tool to assist decision-making. Use your judgment and verify independently.

### Technical Questions

**Q: Why does analysis take time?**
A: The system processes text, extracts features, and runs ML inference. Typically 2-5 seconds.

**Q: Can I analyze multiple jobs at once?**
A: Currently, analyze one job at a time. Use the History tab to track multiple analyses.

**Q: How is data stored?**
A: Job data and predictions are stored in MongoDB. No personal information is stored.

**Q: Can I export my analysis history?**
A: Currently not available in the UI, but data is accessible via the API.

### Privacy and Security

**Q: Is my data secure?**
A: Data is transmitted over HTTPS and stored securely. However, always review the privacy policy.

**Q: Who can see my analyses?**
A: Analyses are stored in the database. Check with your system administrator about access controls.

**Q: Can I delete my analysis history?**
A: Contact your system administrator for data deletion requests.

---

## Best Practices

1. **Use Multiple Sources:** Don't rely solely on this tool - verify through multiple channels
2. **Check Company Website:** Always verify job postings on official company websites
3. **Be Skeptical:** If something seems too good to be true, it probably is
4. **Report Scams:** Report confirmed scams to job boards and authorities
5. **Stay Updated:** Keep the extension and system updated for best results

---

## Support

For technical support or questions:
- Check the troubleshooting section
- Review system logs
- Contact your system administrator
- Refer to the deployment guide for technical details

---

## Disclaimer

⚠️ **Important:** This system provides AI-based predictions and should not be considered legal or professional advice. Always verify job postings independently through official channels. The system developers are not responsible for any decisions made based on these predictions.
