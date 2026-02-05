"""
Model inference utilities for fake job posting detection.
"""
import joblib
import numpy as np
import os
import sys

# Handle imports - try absolute import first (when used as package), then relative/current dir
try:
    from ml_model.preprocess import clean_text, extract_features
except ImportError:
    try:
        from .preprocess import clean_text, extract_features
    except ImportError:
        # If both fail, add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        from preprocess import clean_text, extract_features


class JobPostingClassifier:
    """Classifier for fake job posting detection."""
    
    def __init__(self, model_path='models/job_classifier.pkl', 
                 vectorizer_path='models/tfidf_vectorizer.pkl',
                 feature_names_path='models/feature_names.pkl'):
        """Initialize the classifier."""
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.feature_names = joblib.load(feature_names_path)
    
    def predict(self, description, company_name="", salary=""):
        """
        Predict if a job posting is fake.
        
        Args:
            description: Job description text
            company_name: Company name
            salary: Salary information
            
        Returns:
            Dictionary with prediction, confidence, and reasons
        """
        # Clean and preprocess
        cleaned_text = clean_text(description)
        
        # Extract risk features
        risk_features = extract_features(description, company_name, salary)
        
        # Transform text with TF-IDF
        tfidf_features = self.vectorizer.transform([cleaned_text]).toarray()
        
        # Combine features
        feature_array = np.array([[risk_features.get(name, 0) for name in self.feature_names]])
        combined_features = np.hstack([tfidf_features, feature_array])
        
        # Predict
        prediction = self.model.predict(combined_features)[0]
        probabilities = self.model.predict_proba(combined_features)[0]
        
        # Calculate confidence (probability of predicted class)
        confidence = int(probabilities[prediction] * 100)
        
        # Generate reasons
        reasons = self._generate_reasons(risk_features, description, company_name, salary, prediction)
        
        return {
            'prediction': 'FAKE' if prediction == 1 else 'REAL',
            'confidence': confidence,
            'reasons': reasons
        }
    
    def _generate_reasons(self, risk_features, description, company_name, salary, prediction):
        """Generate human-readable reasons for the prediction."""
        reasons = []
        description_lower = description.lower() if description else ""
        
        if prediction == 1:  # FAKE
            if risk_features.get('urgency_count', 0) > 0:
                reasons.append("Use of urgency-based language detected")
            
            if risk_features.get('emotional_count', 0) > 0:
                reasons.append("Emotional manipulation tactics identified")
            
            if risk_features.get('personal_email', 0) == 1:
                reasons.append("Personal email domain detected instead of company email")
            
            if risk_features.get('has_company_name', 0) == 0:
                reasons.append("Missing or suspicious company information")
            
            if risk_features.get('suspicious_keywords', 0) > 0:
                reasons.append("Suspicious keywords related to financial scams detected")
            
            if risk_features.get('text_length', 0) < 200:
                reasons.append("Unusually short job description")
            
            if risk_features.get('word_count', 0) < 50:
                reasons.append("Insufficient detail in job description")
            
            if salary and any(word in description_lower for word in ['guaranteed', 'easy', 'no experience']):
                reasons.append("Unrealistic salary claims with low requirements")
        else:  # REAL
            if risk_features.get('has_company_name', 0) == 1:
                reasons.append("Company information provided")
            
            if risk_features.get('text_length', 0) > 500:
                reasons.append("Detailed job description provided")
            
            if risk_features.get('urgency_count', 0) == 0:
                reasons.append("No urgency-based language detected")
            
            if risk_features.get('suspicious_keywords', 0) == 0:
                reasons.append("No suspicious keywords detected")
        
        # If no specific reasons, add generic ones
        if not reasons:
            if prediction == 1:
                reasons.append("Multiple risk factors detected in job posting")
            else:
                reasons.append("Job posting appears legitimate based on analysis")
        
        return reasons[:5]  # Return top 5 reasons
