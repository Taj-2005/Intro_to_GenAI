# Fake Job Posting Detection System

An end-to-end AI-based system that detects fake job postings from platforms like LinkedIn, Indeed, and Naukri using a **self-trained Machine Learning model**. The system provides real-time analysis with explainable predictions and trust scores.

## 🎯 Features

- ✅ **Self-Trained ML Model** - No external AI APIs (OpenAI, Gemini, etc.)
- ✅ **Chrome Extension** - Automatic job extraction and analysis
- ✅ **Web Dashboard** - Manual analysis with analytics
- ✅ **Explainable AI** - Provides reasons for predictions
- ✅ **Trust Score** - 0-100% confidence indicator
- ✅ **MongoDB Integration** - Stores analysis history and statistics
- ✅ **Real-Time Analysis** - Fast inference (2-5 seconds)

## 📋 Project Structure

```
project/
├── ml_model/          # ML model training and inference
│   ├── train.py       # Model training script
│   ├── model.py       # Model inference class
│   └── preprocess.py  # Text preprocessing
├── backend/           # FastAPI server
│   ├── app.py         # API endpoints
│   └── database.py    # MongoDB operations
├── chrome_extension/  # Browser extension
│   ├── manifest.json  # Extension config
│   ├── content.js     # Data extraction
│   └── popup.*        # UI components
├── frontend/          # Next.js dashboard
│   └── app/           # Dashboard pages
└── docs/              # Documentation
```

## 🚀 Quick Start

See [QUICK_START.md](QUICK_START.md) for a 5-minute setup guide.

### 1. Train the ML Model
```bash
cd ml_model
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python train.py
```

### 2. Start the Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Set MONGO_URI environment variable (or use local MongoDB)
uvicorn app:app --reload
```

### 3. Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `chrome_extension` folder
4. (Optional) Run `python create_icons.py` in chrome_extension/ for icons

### 4. Start Frontend Dashboard
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## 🧩 Components

### ML Model
- **Algorithms**: Logistic Regression, Random Forest, XGBoost
- **Features**: TF-IDF + domain-specific risk indicators
- **Performance**: Targets 85%+ accuracy
- **Explainability**: Generates human-readable reasons

### FastAPI Backend
- **Endpoints**: `/analyze`, `/statistics`, `/recent`, `/health`
- **Database**: MongoDB for job history and analytics
- **CORS**: Configured for extension and dashboard

### Chrome Extension
- **Platforms**: LinkedIn, Indeed, Naukri
- **Features**: Auto-extraction, real-time analysis, popup UI
- **Manifest V3**: Modern Chrome extension architecture

### Next.js Dashboard
- **Tabs**: Analyze, History, Analytics
- **Styling**: Tailwind CSS
- **TypeScript**: Type-safe React components

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project organization
- **[docs/architecture.md](docs/architecture.md)** - System architecture
- **[docs/deployment.md](docs/deployment.md)** - Production deployment
- **[docs/user_manual.md](docs/user_manual.md)** - User guide
- **[docs/analysis.md](docs/analysis.md)** - Final analysis & evaluation

## 🔧 Technology Stack

- **ML**: Scikit-learn, XGBoost, NLTK, TF-IDF
- **Backend**: FastAPI, PyMongo, Uvicorn
- **Frontend**: Next.js 14, React, Tailwind CSS, TypeScript
- **Database**: MongoDB (Atlas or local)
- **Extension**: Chrome Extension Manifest V3

## 🎓 How It Works

1. **Data Extraction**: Chrome extension extracts job details from web pages
2. **Preprocessing**: Text cleaning, tokenization, feature extraction
3. **ML Inference**: Trained model predicts REAL/FAKE with confidence
4. **Reason Generation**: System explains why it made the prediction
5. **Storage**: Results saved to MongoDB for analytics
6. **Display**: Results shown in extension popup or dashboard

## ⚠️ Important Notes

- **AI-Based Predictions**: Results are machine learning predictions, not legal verdicts
- **Always Verify**: Independently verify job postings through official channels
- **False Positives/Negatives**: System may occasionally misclassify jobs
- **Privacy**: No personal user data is collected or stored

## 🚢 Deployment

See [docs/deployment.md](docs/deployment.md) for deployment on:
- **Backend**: AWS EC2, Render, Railway, DigitalOcean
- **Database**: MongoDB Atlas
- **Frontend**: Vercel, Netlify
- **Extension**: Chrome Web Store (optional)

## 📊 Model Performance

- **Target Accuracy**: 85%+
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Features**: Text analysis + risk indicators
- **Training**: Kaggle Fake Job Postings dataset

## 🤝 Contributing

This is a complete project with all components. To extend:
1. Improve model with more training data
2. Add support for more job boards
3. Enhance feature extraction
4. Add user feedback mechanism

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🙏 Acknowledgments

- Kaggle Fake Job Postings dataset
- Open-source ML libraries (Scikit-learn, XGBoost, NLTK)
- FastAPI, Next.js, and MongoDB communities
