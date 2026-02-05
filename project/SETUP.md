# Setup Guide

Quick start guide for setting up the Fake Job Posting Detection System.

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- MongoDB (local or Atlas account)
- Chrome browser (for extension)

## Step 1: Train the ML Model

```bash
# Navigate to ML model directory
cd ml_model

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python train.py

# This will create model files in ml_model/models/
# - job_classifier.pkl
# - tfidf_vectorizer.pkl
# - feature_names.pkl
```

**Note:** The training script will download the dataset automatically. If download fails, it will create a synthetic dataset for demonstration.

## Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd ../backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file (copy from .env.example if available)
# Or set environment variables:
export MONGO_URI="mongodb://localhost:27017/"  # Or your MongoDB Atlas URI
export DATABASE_NAME="job_analysis_db"

# Start the backend server
uvicorn app:app --reload
```

The backend will be available at `http://localhost:8000`

**Verify:** Visit `http://localhost:8000/health` to check if the model loaded successfully.

## Step 3: Set Up Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Step 4: Install Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Navigate to and select the `chrome_extension` folder
5. The extension icon should appear in your toolbar

**Note:** You may need to create placeholder icon files (icon16.png, icon48.png, icon128.png) or the extension will show a default icon.

## Step 5: Test the System

### Test Backend
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "URGENT! Work from home! Easy money! No experience needed!",
    "job_title": "Test Job",
    "company_name": "Test Company"
  }'
```

### Test Frontend
1. Open `http://localhost:3000`
2. Go to "Analyze" tab
3. Paste a job description
4. Click "Analyze Job Posting"
5. View results

### Test Chrome Extension
1. Visit a job posting on LinkedIn, Indeed, or Naukri
2. Click the extension icon
3. Click "Analyze Job Posting"
4. View results in popup

## Troubleshooting

### Model Not Loading
- Ensure you've run `python train.py` in the `ml_model` directory
- Check that model files exist in `ml_model/models/`
- Verify file paths in backend code

### MongoDB Connection Issues
- Ensure MongoDB is running (if using local)
- Check MongoDB Atlas connection string (if using cloud)
- Verify network access settings in MongoDB Atlas

### CORS Errors
- Update `allow_origins` in `backend/app.py` with your frontend URL
- For development, `["*"]` should work

### Extension Not Working
- Check browser console for errors
- Verify backend is running and accessible
- Update `API_BASE_URL` in `chrome_extension/popup.js`

## Next Steps

- Read the [Deployment Guide](docs/deployment.md) for production deployment
- Review the [User Manual](docs/user_manual.md) for usage instructions
- Check the [Architecture Documentation](docs/architecture.md) for system design

## Production Deployment

See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions for:
- Backend (AWS EC2, Render, Railway)
- Database (MongoDB Atlas)
- Frontend (Vercel, Netlify)
- Chrome Extension packaging
