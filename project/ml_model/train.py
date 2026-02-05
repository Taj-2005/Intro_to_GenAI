"""
Train ML model for fake job posting detection.
Downloads dataset from Kaggle or uses local dataset.
"""
import pandas as pd
import numpy as np
import joblib
import os
import requests
import zipfile
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from xgboost import XGBClassifier
from preprocess import clean_text, extract_features

# Dataset URL (Kaggle Fake Job Postings dataset)
DATASET_URL = "https://raw.githubusercontent.com/shivamshinde123/fake-job-posting-prediction/main/fake_job_postings.csv"


def download_dataset():
    """Download the fake job postings dataset."""
    print("Downloading dataset...")
    try:
        df = pd.read_csv(DATASET_URL)
        print(f"Dataset downloaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Creating synthetic dataset for demonstration...")
        return create_synthetic_dataset()


def create_synthetic_dataset():
    """Create a synthetic dataset if download fails."""
    np.random.seed(42)
    n_samples = 1000
    
    fake_descriptions = [
        "URGENT! Work from home! Easy money! No experience needed! Apply now!",
        "Immediate opening! Guaranteed income! Send your resume to gmail.com",
        "High paying job! No qualifications required! Act now!",
        "Make $5000/week working from home! Limited time offer!",
        "Get rich quick! No interview needed! Wire transfer required.",
    ]
    
    real_descriptions = [
        "We are seeking a qualified candidate with 3+ years of experience in software development.",
        "Our company offers competitive salary and benefits package. Please apply through our official website.",
        "Position requires bachelor's degree and relevant work experience. Full-time position with benefits.",
        "Join our team! We offer professional development opportunities and a collaborative work environment.",
        "We are an equal opportunity employer. Competitive compensation based on experience.",
    ]
    
    data = []
    for i in range(n_samples):
        is_fake = np.random.choice([0, 1], p=[0.5, 0.5])
        if is_fake:
            desc = np.random.choice(fake_descriptions)
            company = "" if np.random.random() < 0.3 else "Company " + str(i)
            salary = "$100k+" if np.random.random() < 0.5 else ""
        else:
            desc = np.random.choice(real_descriptions)
            company = "Company " + str(i)
            salary = "$50k-$80k" if np.random.random() < 0.7 else ""
        
        data.append({
            'description': desc,
            'company_profile': company,
            'salary_range': salary,
            'fraudulent': is_fake
        })
    
    return pd.DataFrame(data)


def prepare_features(df):
    """Prepare features for training."""
    print("Preprocessing data...")
    
    # Clean text
    df['description_clean'] = df['description'].apply(clean_text)
    
    # Extract risk features
    feature_list = []
    for idx, row in df.iterrows():
        features = extract_features(
            row.get('description', ''),
            row.get('company_profile', ''),
            row.get('salary_range', '')
        )
        feature_list.append(features)
    
    feature_df = pd.DataFrame(feature_list)
    
    # Combine TF-IDF features with extracted features
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), min_df=2)
    tfidf_features = vectorizer.fit_transform(df['description_clean'])
    
    # Convert to dense array and combine
    tfidf_array = tfidf_features.toarray()
    feature_array = feature_df.values
    
    X = np.hstack([tfidf_array, feature_array])
    y = df['fraudulent'].values
    
    return X, y, vectorizer, feature_df.columns.tolist()


def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and select the best one."""
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss')
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
        print(f"{name} Results:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
    
    # Select best model based on F1 score
    best_model_name = max(results, key=lambda x: results[x]['f1'])
    print(f"\nBest model: {best_model_name} (F1: {results[best_model_name]['f1']:.4f})")
    
    return results[best_model_name]['model'], best_model_name, results


def main():
    """Main training function."""
    print("=" * 60)
    print("Fake Job Posting Detection - Model Training")
    print("=" * 60)
    
    # Download or create dataset
    df = download_dataset()
    
    # Prepare features
    X, y, vectorizer, feature_names = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train models
    best_model, model_name, all_results = train_models(X_train, X_test, y_train, y_test)
    
    # Save model and vectorizer
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, 'models/job_classifier.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    joblib.dump(feature_names, 'models/feature_names.pkl')
    
    print(f"\nModel saved to models/job_classifier.pkl")
    print(f"Vectorizer saved to models/tfidf_vectorizer.pkl")
    
    # Save training results
    results_df = pd.DataFrame({
        'Model': list(all_results.keys()),
        'Accuracy': [all_results[m]['accuracy'] for m in all_results.keys()],
        'Precision': [all_results[m]['precision'] for m in all_results.keys()],
        'Recall': [all_results[m]['recall'] for m in all_results.keys()],
        'F1-Score': [all_results[m]['f1'] for m in all_results.keys()]
    })
    results_df.to_csv('models/training_results.csv', index=False)
    
    print("\nTraining completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
