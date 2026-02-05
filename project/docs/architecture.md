# System Architecture

## Overview

The Fake Job Posting Detection System is an end-to-end AI-powered solution that automatically analyzes job postings and classifies them as REAL or FAKE. The system consists of four main components:

1. **Chrome Browser Extension** (User Interface Layer)
2. **FastAPI Backend** (AI & API Layer)
3. **Machine Learning Model** (Self-Trained AI)
4. **Next.js Web Dashboard** (Analytics & Manual Analysis)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Chrome Browser Extension                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Content.js  │  │   Popup.js   │  │ Background.js│         │
│  │ (Extract Job)│  │  (UI Logic)  │  │  (Service)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP REST API
                             │ (POST /analyze)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Server                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                           │  │
│  │  - POST /analyze    (Analyze job posting)                │  │
│  │  - GET /statistics  (Get analytics)                      │  │
│  │  - GET /recent      (Get recent jobs)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Preprocessing   │────────▶│  ML Model        │            │
│  │  - Text Cleaning │         │  Inference       │            │
│  │  - Feature Ext.  │         │  - Classification│            │
│  └──────────────────┘         │  - Confidence    │            │
│                                │  - Reasons       │            │
│                                └──────────────────┘            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  MongoDB Database                                         │  │
│  │  Collections:                                             │  │
│  │  - analyzed_jobs (Job data + predictions)                │  │
│  │  - user_feedback (Optional)                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP REST API
                             │ (GET /statistics, /recent)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js Web Dashboard                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Analyze    │  │   History    │  │  Analytics   │         │
│  │   Tab        │  │   Tab        │  │   Tab        │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Chrome Browser Extension

**Technology Stack:**
- Manifest V3
- Vanilla JavaScript
- HTML/CSS

**Key Files:**
- `manifest.json`: Extension configuration
- `content.js`: Extracts job data from web pages
- `popup.html/css/js`: User interface for displaying results
- `background.js`: Service worker for extension lifecycle

**Functionality:**
- Automatically detects job posting pages (LinkedIn, Indeed, Naukri)
- Extracts job title, company name, salary, and description
- Sends data to FastAPI backend via REST API
- Displays prediction, confidence score, and reasons in popup

### 2. FastAPI Backend

**Technology Stack:**
- FastAPI (Python web framework)
- PyMongo (MongoDB driver)
- Joblib (Model loading)
- Scikit-learn (ML utilities)

**Key Files:**
- `app.py`: Main FastAPI application with endpoints
- `database.py`: MongoDB connection and operations
- `models.py`: Pydantic models for request/response

**Endpoints:**
- `POST /analyze`: Analyze a job posting
- `GET /statistics`: Get analytics and statistics
- `GET /recent`: Get recently analyzed jobs
- `GET /health`: Health check

**Data Flow:**
1. Receive job posting data from extension or web dashboard
2. Preprocess text (cleaning, tokenization)
3. Extract risk features
4. Load trained ML model
5. Make prediction
6. Generate reasons
7. Save to MongoDB
8. Return JSON response

### 3. Machine Learning Model

**Technology Stack:**
- Scikit-learn (Logistic Regression, Random Forest)
- XGBoost
- NLTK (Natural Language Processing)
- TF-IDF Vectorization

**Key Files:**
- `train.py`: Model training script
- `model.py`: Model inference class
- `preprocess.py`: Text preprocessing utilities

**Model Architecture:**
1. **Text Preprocessing:**
   - Lowercase conversion
   - URL/email removal
   - Special character removal
   - Tokenization and lemmatization

2. **Feature Engineering:**
   - TF-IDF features (500 features, 1-2 grams)
   - Risk-based features:
     - Urgency indicators
     - Emotional manipulation words
     - Personal email detection
     - Missing company info
     - Suspicious keywords
     - Text length metrics

3. **Model Training:**
   - Multiple models tested (Logistic Regression, Random Forest, XGBoost)
   - Best model selected based on F1-score
   - Model saved as pickle file

4. **Prediction:**
   - Combine TF-IDF and risk features
   - Predict class (REAL/FAKE)
   - Calculate confidence score
   - Generate human-readable reasons

### 4. Next.js Web Dashboard

**Technology Stack:**
- Next.js 14 (React framework)
- Tailwind CSS (Styling)
- Axios (HTTP client)
- TypeScript

**Key Features:**
- **Analyze Tab:** Manual job posting analysis
- **History Tab:** View previously analyzed jobs
- **Analytics Tab:** Statistics and common scam patterns

**Pages:**
- `app/page.tsx`: Main dashboard with tabs
- `app/layout.tsx`: Root layout
- `app/globals.css`: Global styles

## Data Flow

### Analysis Flow

1. **User Action:**
   - User visits job posting page OR pastes job description in dashboard

2. **Data Extraction:**
   - Chrome extension extracts job data from page
   - OR user manually enters data in dashboard

3. **API Request:**
   - Data sent to FastAPI backend via POST /analyze

4. **Processing:**
   - Backend preprocesses text
   - Extracts features
   - Loads ML model
   - Makes prediction

5. **Storage:**
   - Results saved to MongoDB

6. **Response:**
   - JSON response with prediction, confidence, reasons

7. **Display:**
   - Results shown in extension popup or dashboard

### Analytics Flow

1. **Dashboard Request:**
   - User navigates to Analytics tab

2. **API Request:**
   - Dashboard requests statistics from GET /statistics

3. **Database Query:**
   - Backend queries MongoDB for aggregated data

4. **Response:**
   - Statistics returned (total analyzed, fake/real counts, common patterns)

5. **Display:**
   - Analytics displayed in dashboard

## Database Schema

### analyzed_jobs Collection

```json
{
  "_id": "ObjectId",
  "job_title": "string",
  "company_name": "string",
  "salary": "string",
  "description": "string",
  "prediction": "FAKE" | "REAL",
  "confidence": "number (0-100)",
  "reasons": ["string"],
  "analyzed_at": "ISODate",
  "source": "string (chrome_extension | web_dashboard)"
}
```

## Security Considerations

1. **CORS:** Configured to allow requests from extension and dashboard
2. **Input Validation:** Pydantic models validate all inputs
3. **Error Handling:** Comprehensive error handling at all layers
4. **Environment Variables:** Sensitive data stored in .env files
5. **No Personal Data:** System does not store personal user information

## Scalability

1. **Backend:** Can be horizontally scaled using load balancers
2. **Database:** MongoDB Atlas supports automatic scaling
3. **Model:** Lightweight models allow fast inference
4. **Caching:** Can add Redis for caching frequent queries

## Deployment Architecture

```
┌─────────────┐
│   Chrome    │
│  Extension  │
│  (Client)   │
└──────┬──────┘
       │
       │ HTTPS
       ▼
┌─────────────────────────────────┐
│      Cloud Load Balancer        │
└──────────────┬──────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌──────────┐    ┌──────────┐
│ FastAPI  │    │ FastAPI  │
│ Server 1 │    │ Server 2 │
└────┬─────┘    └────┬─────┘
     │               │
     └───────┬───────┘
             │
             ▼
     ┌──────────────┐
     │ MongoDB Atlas│
     │   (Cloud)    │
     └──────────────┘

┌─────────────────────────────────┐
│   Next.js Dashboard (Vercel)    │
└─────────────────────────────────┘
```

## Technology Choices Rationale

1. **FastAPI:** Fast, modern Python framework with automatic API documentation
2. **MongoDB:** Flexible schema for storing varied job posting data
3. **Next.js:** Server-side rendering, excellent developer experience
4. **Chrome Extension:** Direct integration with job posting sites
5. **Scikit-learn/XGBoost:** Proven ML libraries, no external API dependencies
6. **TF-IDF:** Lightweight text representation, interpretable features
