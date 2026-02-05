# Testing Guide

Comprehensive testing guide for the Fake Job Posting Detection System.

## Prerequisites

- All components installed and running
- Backend server running on http://localhost:8000
- Frontend running on http://localhost:3000
- Chrome extension loaded
- MongoDB accessible

## 1. ML Model Testing

### Test Model Training

```bash
cd ml_model
python train.py
```

**Expected Output:**
- Dataset downloaded/created
- Models trained (Logistic Regression, Random Forest, XGBoost)
- Best model selected
- Model files saved to `models/` directory
- Training results CSV generated

**Verify:**
- `models/job_classifier.pkl` exists
- `models/tfidf_vectorizer.pkl` exists
- `models/feature_names.pkl` exists
- `models/training_results.csv` shows accuracy metrics

### Test Model Inference

```python
from ml_model.model import JobPostingClassifier

classifier = JobPostingClassifier()
result = classifier.predict(
    description="URGENT! Work from home! Easy money!",
    company_name="",
    salary="$100k"
)
print(result)
```

**Expected Output:**
```json
{
  "prediction": "FAKE",
  "confidence": 85,
  "reasons": [
    "Use of urgency-based language detected",
    "Emotional manipulation tactics identified"
  ]
}
```

## 2. Backend API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Test Analysis Endpoint

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "We are seeking a qualified software engineer with 3+ years of experience. Competitive salary and benefits package.",
    "job_title": "Software Engineer",
    "company_name": "Tech Corp",
    "salary": "$80k-$100k"
  }'
```

**Expected Response:**
```json
{
  "prediction": "REAL",
  "confidence": 75,
  "reasons": [
    "Company information provided",
    "Detailed job description provided"
  ]
}
```

### Test Fake Job

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "URGENT! Work from home! Easy money! No experience needed! Apply now! Send resume to gmail.com",
    "job_title": "Easy Job",
    "company_name": "",
    "salary": "$5000/week"
  }'
```

**Expected Response:**
```json
{
  "prediction": "FAKE",
  "confidence": 90,
  "reasons": [
    "Use of urgency-based language detected",
    "Personal email domain detected instead of company email",
    "Missing or suspicious company information"
  ]
}
```

### Test Statistics Endpoint

```bash
curl http://localhost:8000/statistics
```

**Expected Response:**
```json
{
  "total_analyzed": 10,
  "fake_count": 5,
  "real_count": 5,
  "fake_percentage": 50.0,
  "real_percentage": 50.0,
  "common_patterns": [...]
}
```

### Test Recent Jobs Endpoint

```bash
curl http://localhost:8000/recent
```

**Expected Response:**
```json
{
  "jobs": [
    {
      "id": "...",
      "job_title": "...",
      "company_name": "...",
      "prediction": "FAKE",
      "confidence": 85,
      "analyzed_at": "2024-..."
    }
  ]
}
```

## 3. Frontend Testing

### Manual Testing Checklist

1. **Analyze Tab**
   - [ ] Page loads correctly
   - [ ] Form fields are visible
   - [ ] Can enter job description
   - [ ] "Analyze" button works
   - [ ] Results display correctly
   - [ ] Prediction badge shows correct color
   - [ ] Trust score displays
   - [ ] Reasons list shows

2. **History Tab**
   - [ ] Tab switches correctly
   - [ ] Recent jobs list displays
   - [ ] Job information shows correctly
   - [ ] Prediction badges display
   - [ ] Timestamps show

3. **Analytics Tab**
   - [ ] Tab switches correctly
   - [ ] Statistics cards display
   - [ ] Percentages calculate correctly
   - [ ] Common patterns list shows
   - [ ] Pattern counts display

### Test Cases

#### Test Case 1: Real Job Posting
1. Go to Analyze tab
2. Enter:
   - Title: "Software Engineer"
   - Company: "Microsoft"
   - Description: "We are looking for an experienced software engineer with 5+ years in Python and cloud technologies. Competitive salary and comprehensive benefits."
3. Click "Analyze"
4. **Expected**: Prediction = REAL, Trust score > 70%

#### Test Case 2: Fake Job Posting
1. Go to Analyze tab
2. Enter:
   - Title: "Easy Work"
   - Company: ""
   - Description: "URGENT! Work from home! Make $5000/week! No experience needed! Apply now to gmail.com"
3. Click "Analyze"
4. **Expected**: Prediction = FAKE, Trust score < 30%

#### Test Case 3: Edge Cases
- Empty description → Error message
- Very long description → Should still work
- Special characters → Should be handled
- Missing fields → Should work with defaults

## 4. Chrome Extension Testing

### Installation Test
- [ ] Extension loads without errors
- [ ] Icon appears in toolbar
- [ ] No console errors

### Data Extraction Test

1. **LinkedIn**
   - [ ] Navigate to a LinkedIn job posting
   - [ ] Open extension
   - [ ] Verify job title extracted
   - [ ] Verify company name extracted
   - [ ] Verify description extracted

2. **Indeed**
   - [ ] Navigate to an Indeed job posting
   - [ ] Open extension
   - [ ] Verify data extraction

3. **Naukri**
   - [ ] Navigate to a Naukri job posting
   - [ ] Open extension
   - [ ] Verify data extraction

### Analysis Test

1. Navigate to a job posting
2. Open extension
3. Click "Analyze Job Posting"
4. **Expected**:
   - Loading spinner shows
   - Results display
   - Prediction shows
   - Trust score shows
   - Reasons list shows

### Error Handling Test

1. **Backend Not Running**
   - [ ] Open extension
   - [ ] Click analyze
   - [ ] Error message displays

2. **No Job Data**
   - [ ] Navigate to non-job page
   - [ ] Open extension
   - [ ] "No job posting detected" message shows

## 5. Integration Testing

### End-to-End Test Flow

1. **Train Model** → Model files created
2. **Start Backend** → API accessible
3. **Start Frontend** → Dashboard loads
4. **Load Extension** → Extension works
5. **Analyze via Extension** → Results show
6. **Analyze via Dashboard** → Results show
7. **Check History** → Jobs appear
8. **Check Analytics** → Statistics update

### Database Integration Test

1. Analyze a job via extension
2. Analyze a job via dashboard
3. Check MongoDB:
   ```javascript
   db.analyzed_jobs.find().pretty()
   ```
4. Verify:
   - [ ] Jobs are stored
   - [ ] Predictions are saved
   - [ ] Timestamps are correct
   - [ ] Source field is set

## 6. Performance Testing

### Response Time
- [ ] Analysis completes in < 5 seconds
- [ ] Statistics load in < 2 seconds
- [ ] Recent jobs load in < 2 seconds

### Load Testing
- [ ] Handle 10 concurrent requests
- [ ] Handle 100 requests sequentially
- [ ] Database queries are fast

## 7. Security Testing

### CORS
- [ ] Extension can call API
- [ ] Dashboard can call API
- [ ] Unauthorized origins blocked (in production)

### Input Validation
- [ ] XSS attempts are sanitized
- [ ] SQL injection attempts fail (MongoDB injection)
- [ ] Large inputs are handled

### Error Messages
- [ ] No sensitive data in error messages
- [ ] Errors are user-friendly

## 8. Browser Compatibility

### Chrome Extension
- [ ] Works in Chrome (latest)
- [ ] Works in Chromium-based browsers

### Web Dashboard
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge

## 9. Common Issues and Solutions

### Issue: Model Not Loading
**Solution**: Ensure model files exist in `ml_model/models/`

### Issue: MongoDB Connection Failed
**Solution**: Check MONGO_URI environment variable

### Issue: CORS Errors
**Solution**: Update `allow_origins` in `backend/app.py`

### Issue: Extension Not Extracting Data
**Solution**: Check if page matches content script patterns

### Issue: Frontend Can't Connect
**Solution**: Verify `NEXT_PUBLIC_API_URL` environment variable

## 10. Automated Testing (Future Enhancement)

Consider adding:
- Unit tests for ML model
- API endpoint tests
- Frontend component tests
- E2E tests with Playwright/Cypress

## Test Report Template

```
Test Date: __________
Tester: __________

Component          Status    Notes
─────────────────────────────────────
ML Model Training  [ ] Pass [ ] Fail
Backend API        [ ] Pass [ ] Fail
Frontend           [ ] Pass [ ] Fail
Chrome Extension   [ ] Pass [ ] Fail
Integration        [ ] Pass [ ] Fail
Performance        [ ] Pass [ ] Fail
Security           [ ] Pass [ ] Fail

Overall Status: [ ] Pass [ ] Fail

Issues Found:
1. __________
2. __________
```

---

**Note**: This testing guide covers manual testing. For production deployment, consider implementing automated testing suites.
