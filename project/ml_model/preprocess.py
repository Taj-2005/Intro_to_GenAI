"""
Text preprocessing utilities for fake job posting detection.
"""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def clean_text(text):
    """
    Clean and preprocess text for analysis.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def tokenize_and_lemmatize(text):
    """
    Tokenize and lemmatize text.
    
    Args:
        text: Cleaned text string
        
    Returns:
        List of lemmatized tokens
    """
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and len(token) > 2]
    return tokens


def extract_features(text, company_name="", salary=""):
    """
    Extract risk features from job posting.
    
    Args:
        text: Job description text
        company_name: Company name
        salary: Salary information
        
    Returns:
        Dictionary of extracted features
    """
    features = {}
    
    if not text:
        text = ""
    if not company_name:
        company_name = ""
    if not salary:
        salary = ""
    
    text_lower = text.lower()
    company_lower = company_name.lower()
    
    # Urgency indicators
    urgency_words = ['urgent', 'immediate', 'asap', 'hurry', 'limited time', 'act now', 'apply now']
    features['urgency_count'] = sum(1 for word in urgency_words if word in text_lower)
    
    # Emotional manipulation
    emotional_words = ['guaranteed', 'easy money', 'work from home', 'no experience needed', 'get rich']
    features['emotional_count'] = sum(1 for word in emotional_words if word in text_lower)
    
    # Suspicious email patterns
    personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
    features['personal_email'] = 1 if any(domain in text_lower for domain in personal_domains) else 0
    
    # Missing company info
    features['has_company_name'] = 1 if len(company_name.strip()) > 0 else 0
    
    # Unrealistic salary indicators
    if salary:
        # Check for very high salary mentions
        salary_numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:k|K)?)', salary)
        features['has_salary'] = 1 if salary_numbers else 0
    else:
        features['has_salary'] = 0
    
    # Text length (very short descriptions are suspicious)
    features['text_length'] = len(text)
    features['word_count'] = len(text.split())
    
    # Suspicious keywords
    suspicious_keywords = ['wire transfer', 'western union', 'moneygram', 'cashier check', 
                          'processing fee', 'upfront payment', 'training fee']
    features['suspicious_keywords'] = sum(1 for keyword in suspicious_keywords if keyword in text_lower)
    
    # Grammar quality (simple heuristic: count capitalization errors)
    features['caps_ratio'] = sum(1 for c in text[:100] if c.isupper()) / max(len(text[:100]), 1)
    
    return features
