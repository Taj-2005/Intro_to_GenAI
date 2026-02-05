# Project Structure

```
project/
├── README.md                 # Main project README
├── SETUP.md                  # Setup instructions
├── .gitignore               # Git ignore file
│
├── ml_model/                # Machine Learning Model
│   ├── train.py             # Model training script
│   ├── model.py             # Model inference class
│   ├── preprocess.py        # Text preprocessing utilities
│   ├── requirements.txt     # Python dependencies
│   └── models/              # Trained model files (generated)
│       ├── job_classifier.pkl
│       ├── tfidf_vectorizer.pkl
│       └── feature_names.pkl
│
├── backend/                 # FastAPI Backend
│   ├── app.py               # Main FastAPI application
│   ├── database.py          # MongoDB operations
│   ├── requirements.txt     # Python dependencies
│   └── env_example.txt     # Environment variables example
│
├── chrome_extension/        # Chrome Browser Extension
│   ├── manifest.json        # Extension configuration
│   ├── popup.html           # Popup UI
│   ├── popup.css            # Popup styles
│   ├── popup.js             # Popup logic
│   ├── content.js           # Content script for data extraction
│   ├── background.js        # Background service worker
│   ├── README.md            # Extension setup guide
│   └── ICONS.md             # Icon creation guide
│
├── frontend/                # Next.js Web Dashboard
│   ├── app/
│   │   ├── page.tsx         # Main dashboard page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── package.json         # Node.js dependencies
│   ├── next.config.js       # Next.js configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── postcss.config.js    # PostCSS configuration
│
└── docs/                    # Documentation
    ├── architecture.md      # System architecture
    ├── deployment.md        # Deployment guide
    ├── user_manual.md       # User manual
    └── analysis.md          # Final analysis and evaluation
```

## Key Files Explained

### ML Model
- **train.py**: Downloads dataset, preprocesses data, trains multiple models, selects best one
- **model.py**: Loads trained model and makes predictions with explanations
- **preprocess.py**: Text cleaning, tokenization, feature extraction

### Backend
- **app.py**: FastAPI server with REST endpoints for analysis, statistics, and recent jobs
- **database.py**: MongoDB connection and CRUD operations

### Chrome Extension
- **manifest.json**: Extension configuration and permissions
- **content.js**: Extracts job data from web pages
- **popup.html/js/css**: User interface for displaying results

### Frontend
- **app/page.tsx**: Main dashboard with three tabs (Analyze, History, Analytics)
- Uses Tailwind CSS for styling
- TypeScript for type safety

### Documentation
- **architecture.md**: System design and component interactions
- **deployment.md**: Step-by-step deployment instructions
- **user_manual.md**: End-user guide
- **analysis.md**: Strengths, limitations, challenges, and future improvements

## Data Flow

1. **User visits job posting** → Chrome extension extracts data
2. **Extension sends data** → FastAPI backend via POST /analyze
3. **Backend preprocesses** → Text cleaning and feature extraction
4. **ML model predicts** → Classification with confidence and reasons
5. **Results saved** → MongoDB database
6. **Response sent** → Extension or dashboard displays results

## Development Workflow

1. **Train Model**: `cd ml_model && python train.py`
2. **Start Backend**: `cd backend && uvicorn app:app --reload`
3. **Start Frontend**: `cd frontend && npm run dev`
4. **Load Extension**: Chrome → Extensions → Load unpacked

## Production Deployment

See `docs/deployment.md` for:
- Backend deployment (AWS, Render, Railway)
- Database setup (MongoDB Atlas)
- Frontend deployment (Vercel, Netlify)
- Extension packaging
