"""
FastAPI backend for fake job posting detection.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Add parent directory to path to import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.model import JobPostingClassifier
from database import save_job_analysis, get_job_statistics, get_recent_jobs

app = FastAPI(title="Fake Job Posting Detection API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize classifier
try:
    # Try to load from ml_model directory
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'models', 'job_classifier.pkl')
    vectorizer_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'models', 'tfidf_vectorizer.pkl')
    feature_names_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_model', 'models', 'feature_names.pkl')
    
    classifier = JobPostingClassifier(model_path, vectorizer_path, feature_names_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    print("Please train the model first using: cd ml_model && python train.py")
    classifier = None


class JobPostingRequest(BaseModel):
    job_title: Optional[str] = ""
    company_name: Optional[str] = ""
    salary: Optional[str] = ""
    description: str
    source: Optional[str] = "unknown"


class AnalysisResponse(BaseModel):
    prediction: str
    confidence: int
    reasons: List[str]


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Fake Job Posting Detection API",
        "status": "running",
        "model_loaded": classifier is not None
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_job_posting(job_data: JobPostingRequest):
    """
    Analyze a job posting and return prediction.
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    if not job_data.description:
        raise HTTPException(status_code=400, detail="Job description is required")
    
    try:
        # Make prediction
        result = classifier.predict(
            description=job_data.description,
            company_name=job_data.company_name or "",
            salary=job_data.salary or ""
        )
        
        # Save to database
        try:
            save_job_analysis(
                {
                    'job_title': job_data.job_title or "",
                    'company_name': job_data.company_name or "",
                    'salary': job_data.salary or "",
                    'description': job_data.description,
                    'source': job_data.source or "unknown"
                },
                result
            )
        except Exception as e:
            print(f"Warning: Could not save to database: {e}")
        
        return AnalysisResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing job posting: {str(e)}")


@app.get("/statistics")
async def get_statistics():
    """Get statistics about analyzed jobs."""
    try:
        stats = get_job_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")


@app.get("/recent")
async def get_recent():
    """Get recently analyzed jobs."""
    try:
        jobs = get_recent_jobs()
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent jobs: {str(e)}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": classifier is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
