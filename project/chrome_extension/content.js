/**
 * Content script to extract job posting data from various job sites.
 */
(function() {
    'use strict';

    // Extract job data based on current website
    function extractJobData() {
        const hostname = window.location.hostname;
        const data = {
            job_title: '',
            company_name: '',
            salary: '',
            description: '',
            source: hostname
        };

        // LinkedIn
        if (hostname.includes('linkedin.com')) {
            data.job_title = document.querySelector('.jobs-details-top-card__job-title')?.textContent?.trim() || 
                           document.querySelector('h1.job-title')?.textContent?.trim() || '';
            
            data.company_name = document.querySelector('.jobs-details-top-card__company-name')?.textContent?.trim() || 
                              document.querySelector('.jobs-company__box a')?.textContent?.trim() || '';
            
            data.salary = document.querySelector('.jobs-details-top-card__salary-info')?.textContent?.trim() || '';
            
            const descElement = document.querySelector('.jobs-description__text') || 
                              document.querySelector('.jobs-box__html-content') ||
                              document.querySelector('[data-test-id="job-description"]');
            data.description = descElement?.textContent?.trim() || '';
        }
        
        // Indeed
        else if (hostname.includes('indeed.com')) {
            data.job_title = document.querySelector('h1.jobsearch-JobInfoHeader-title')?.textContent?.trim() || 
                           document.querySelector('.jobsearch-JobInfoHeader-title')?.textContent?.trim() || '';
            
            data.company_name = document.querySelector('[data-testid="inlineHeader-companyName"]')?.textContent?.trim() || 
                              document.querySelector('.jobsearch-InlineCompanyRating')?.textContent?.trim() || '';
            
            data.salary = document.querySelector('[data-testid="attribute_snippet_testid"]')?.textContent?.trim() || '';
            
            const descElement = document.querySelector('#jobDescriptionText') || 
                              document.querySelector('.jobsearch-jobDescriptionText');
            data.description = descElement?.textContent?.trim() || '';
        }
        
        // Naukri
        else if (hostname.includes('naukri.com')) {
            data.job_title = document.querySelector('.jd-header-title')?.textContent?.trim() || 
                           document.querySelector('h1')?.textContent?.trim() || '';
            
            data.company_name = document.querySelector('.jd-header-comp-name')?.textContent?.trim() || 
                              document.querySelector('.comp-name')?.textContent?.trim() || '';
            
            data.salary = document.querySelector('.salary')?.textContent?.trim() || '';
            
            const descElement = document.querySelector('.jd-desc') || 
                              document.querySelector('.job-desc');
            data.description = descElement?.textContent?.trim() || '';
        }
        
        // Generic fallback - try common selectors
        else {
            data.job_title = document.querySelector('h1')?.textContent?.trim() || '';
            data.company_name = document.querySelector('[class*="company"]')?.textContent?.trim() || '';
            data.salary = document.querySelector('[class*="salary"]')?.textContent?.trim() || '';
            
            // Try to find description in common containers
            const descSelectors = [
                '[class*="description"]',
                '[class*="job-desc"]',
                '[id*="description"]',
                'article',
                '.content'
            ];
            
            for (const selector of descSelectors) {
                const element = document.querySelector(selector);
                if (element && element.textContent.length > 100) {
                    data.description = element.textContent.trim();
                    break;
                }
            }
        }

        return data;
    }

    // Listen for messages from popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'extractJobData') {
            const jobData = extractJobData();
            sendResponse({ success: true, data: jobData });
        }
        return true; // Keep channel open for async response
    });

    // Store extracted data in storage for popup access
    function updateStoredData() {
        const jobData = extractJobData();
        chrome.storage.local.set({ 'extractedJobData': jobData });
    }

    // Update data when page changes (for SPAs)
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            setTimeout(updateStoredData, 1000);
        }
    }).observe(document, { subtree: true, childList: true });

    // Initial extraction
    setTimeout(updateStoredData, 2000);
})();
