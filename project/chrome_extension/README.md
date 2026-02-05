# Chrome Extension - Fake Job Posting Detector

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select this `chrome_extension` folder
5. The extension icon should appear in your toolbar

## Usage

1. Navigate to a job posting on LinkedIn, Indeed, or Naukri
2. Click the extension icon in your toolbar
3. The extension will automatically extract job details and analyze them
4. View the prediction, trust score, and reasons in the popup

## Configuration

Update the `API_BASE_URL` in `popup.js` to point to your deployed backend URL.

## Note on Icons

The extension requires icon files (icon16.png, icon48.png, icon128.png). You can:
- Create simple icons using any image editor
- Use online icon generators
- Placeholder icons will work for development
