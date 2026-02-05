"""
MongoDB database connection and operations.
"""
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "job_analysis_db")

client = None
db = None


def get_database():
    """Get MongoDB database connection."""
    global client, db
    if client is None:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
    return db


def save_job_analysis(job_data, prediction_result):
    """Save job analysis to MongoDB."""
    db = get_database()
    collection = db['analyzed_jobs']
    
    document = {
        'job_title': job_data.get('job_title', ''),
        'company_name': job_data.get('company_name', ''),
        'salary': job_data.get('salary', ''),
        'description': job_data.get('description', ''),
        'prediction': prediction_result.get('prediction', ''),
        'confidence': prediction_result.get('confidence', 0),
        'reasons': prediction_result.get('reasons', []),
        'analyzed_at': datetime.utcnow(),
        'source': job_data.get('source', 'unknown')
    }
    
    result = collection.insert_one(document)
    return result.inserted_id


def get_job_statistics():
    """Get statistics about analyzed jobs."""
    db = get_database()
    collection = db['analyzed_jobs']
    
    total = collection.count_documents({})
    fake_count = collection.count_documents({'prediction': 'FAKE'})
    real_count = collection.count_documents({'prediction': 'REAL'})
    
    # Get common scam patterns
    fake_jobs = collection.find({'prediction': 'FAKE'})
    all_reasons = []
    for job in fake_jobs:
        all_reasons.extend(job.get('reasons', []))
    
    # Count reason frequency
    reason_counts = {}
    for reason in all_reasons:
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    
    common_patterns = sorted(reason_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_analyzed': total,
        'fake_count': fake_count,
        'real_count': real_count,
        'fake_percentage': round((fake_count / total * 100) if total > 0 else 0, 2),
        'real_percentage': round((real_count / total * 100) if total > 0 else 0, 2),
        'common_patterns': [{'pattern': pattern, 'count': count} for pattern, count in common_patterns]
    }


def get_recent_jobs(limit=50):
    """Get recent analyzed jobs."""
    db = get_database()
    collection = db['analyzed_jobs']
    
    jobs = collection.find().sort('analyzed_at', -1).limit(limit)
    
    return [{
        'id': str(job['_id']),
        'job_title': job.get('job_title', ''),
        'company_name': job.get('company_name', ''),
        'prediction': job.get('prediction', ''),
        'confidence': job.get('confidence', 0),
        'analyzed_at': job.get('analyzed_at').isoformat() if job.get('analyzed_at') else None
    } for job in jobs]
