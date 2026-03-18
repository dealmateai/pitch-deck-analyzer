"""
Configuration - UPDATED for Kaggle datasets
Pitch Deck Analyzer - Extract Company & Founder Details
"""

import os
from pathlib import Path

# ==================== PROJECT DIRECTORIES ====================
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATASETS_DIR = DATA_DIR / "datasets"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, DATASETS_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ==================== KAGGLE CONFIG ====================
KAGGLE_CONFIG = {
    "yc_dataset": "https://www.kaggle.com/datasets/amirhosseinmirzaie/y-combinator-companies-data",
    "crunchbase_dataset": "https://www.kaggle.com/datasets/gauthamp10/crunchbase-startups-dataset",
    "local_yc_path": DATASETS_DIR / "companies.csv",
    "local_crunchbase_path": DATASETS_DIR / "startups.csv",
}

# ==================== NLP CONFIG ====================
NLP_CONFIG = {
    "spacy_model": "en_core_web_sm",
    "sentence_transformer_model": "all-MiniLM-L6-v2",
    "embedding_dim": 384,
    "max_tokens": 512,
}

# ==================== MODEL CONFIG ====================
MODEL_CONFIG = {
    "test_size": 0.2,
    "random_state": 42,
    "xgboost_params": {
        "n_estimators": 100,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "random_state": 42,
    },
}

# ==================== API CONFIG ====================
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "max_file_size": 50 * 1024 * 1024,  # 50 MB
}

# ==================== LOGGING CONFIG ====================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    "log_file": LOGS_DIR / "app.log",
}

# ==================== DATASET CONFIG ====================
DATASET_CONFIG = {
    "training_dataset": DATASETS_DIR / "training_dataset.csv",
    "min_samples": 50,
}

# ==================== PDF CONFIG (PDFPLUMBER ONLY) ====================
PDF_CONFIG = {
    "max_pages": 100,
    "timeout": 30,
    "use_pdfplumber": True,
}

# ==================== MODEL PATHS ====================
MODEL_PATHS = {
    "company_model": MODELS_DIR / "company_fit_model.pkl",
    "founder_model": MODELS_DIR / "founder_fit_model.pkl",
    "scaler_company": MODELS_DIR / "scaler_company.pkl",
    "scaler_founder": MODELS_DIR / "scaler_founder.pkl",
    "feature_names": MODELS_DIR / "feature_names.pkl",
}

# ==================== EXTRACTION CONFIG ====================
EXTRACTION_CONFIG = {
    "company_keywords": [
        "problem", "solution", "market", "size", "industry", 
        "business model", "revenue", "traction", "users", "growth"
    ],
    "founder_keywords": [
        "founder", "team", "ceo", "experience", "education", 
        "background", "expertise", "serial entrepreneur", "startup"
    ],
    "industry_mapping": {
        "ai": ["ai", "machine learning", "deep learning", "neural", "nlp"],
        "fintech": ["finance", "payment", "crypto", "trading", "banking"],
        "saas": ["saas", "cloud", "software", "subscription"],
        "ecommerce": ["ecommerce", "marketplace", "shopping"],
        "healthtech": ["health", "medical", "healthcare"],
        "edtech": ["education", "learning", "course"],
        "logistics": ["logistics", "supply chain", "shipping"],
    }
}