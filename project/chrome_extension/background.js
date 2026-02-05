/**
 * Background service worker for Chrome extension.
 */
chrome.runtime.onInstalled.addListener(() => {
    console.log('Fake Job Posting Detector extension installed');
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    // The popup will handle the UI
    console.log('Extension icon clicked on tab:', tab.url);
});
