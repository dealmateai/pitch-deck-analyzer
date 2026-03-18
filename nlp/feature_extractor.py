"""
Feature Extraction
Extracts features from company data for ML models
Handles both company and founder features
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List
from utils.logger import log

class FeatureExtractor:
    """Extract features from startup data for training."""
    
    def __init__(self):
        """Initialize feature extractor."""
        log.info("✓ FeatureExtractor initialized")
        
        # Define feature names
        self.company_features = [
            'description_length',
            'description_word_count',
            'team_size',
            'company_age',
            'has_marketplace_words',
            'has_revenue_words',
            'has_growth_words',
            'has_ai_ml_words',
            'has_saas_words',
            'location_is_sf',
            'location_is_ny',
            'location_is_top_tech_hub',
            'is_public',
            'batch_year_recent',
            'team_size_large',
        ]
        
        self.founder_features = [
            'founder_count',
            'founder_names_count',
            'has_previous_companies',
            'founder_has_experience_years',
            'founder_attended_top_school',
            'founder_has_phd',
            'founder_technical_background',
            'founder_startup_background',
            'founder_faang_background',
            'founder_education_quality',
            'founder_multiple_founders',
            'founder_diverse_roles',
        ]
    
    def extract_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[str]]:
        """
        Extract features from dataset.
        
        Args:
            df: Input DataFrame with company data
        
        Returns:
            Tuple of (X, y_company, y_founder, feature_names)
        """
        log.info("Extracting features from dataset...")
        
        # Extract company features
        log.info(f"  Extracting {len(self.company_features)} company features...")
        company_features_df = self._extract_company_features(df)
        
        # Extract founder features
        log.info(f"  Extracting {len(self.founder_features)} founder features...")
        founder_features_df = self._extract_founder_features(df)
        
        # Combine features
        X = np.hstack([
            company_features_df.values,
            founder_features_df.values
        ])
        
        # Get labels
        y_company = df['label'].values
        # For founder fit, use label * founder quality score
        y_founder = (df['label'].values * 0.6 + 
                    self._calculate_founder_quality(founder_features_df).values * 0.4)
        
        feature_names = self.company_features + self.founder_features
        
        log.info(f"✓ Features extracted: {X.shape}")
        log.info(f"  Total features: {len(feature_names)}")
        log.info(f"  Company features: {len(self.company_features)}")
        log.info(f"  Founder features: {len(self.founder_features)}")
        
        return X, y_company, y_founder, feature_names
    
    def _extract_company_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract company-specific features."""
        features = pd.DataFrame()
        
        # Text-based features
        features['description_length'] = df['description'].fillna('').str.len()
        features['description_word_count'] = df['description'].fillna('').str.split().str.len()
        
        # Team and scale features
        features['team_size'] = df['team_size'].fillna(0)
        features['company_age'] = df['company_age'].fillna(0)
        
        # Description content features
        desc_lower = df['description'].fillna('').str.lower()
        
        marketplace_words = ['marketplace', 'platform', 'connect', 'network', 'community']
        features['has_marketplace_words'] = desc_lower.str.contains('|'.join(marketplace_words)).astype(int)
        
        revenue_words = ['revenue', 'profitable', 'monetize', 'pricing', 'subscription']
        features['has_revenue_words'] = desc_lower.str.contains('|'.join(revenue_words)).astype(int)
        
        growth_words = ['growth', 'scale', 'expand', 'market', 'disrupt']
        features['has_growth_words'] = desc_lower.str.contains('|'.join(growth_words)).astype(int)
        
        ai_ml_words = ['ai', 'machine learning', 'ml', 'neural', 'deep learning', 'nlp']
        features['has_ai_ml_words'] = desc_lower.str.contains('|'.join(ai_ml_words)).astype(int)
        
        saas_words = ['saas', 'cloud', 'api', 'software', 'platform']
        features['has_saas_words'] = desc_lower.str.contains('|'.join(saas_words)).astype(int)
        
        # Location features
        location_lower = df['location'].fillna('').str.lower()
        features['location_is_sf'] = location_lower.str.contains('san francisco|sf').astype(int)
        features['location_is_ny'] = location_lower.str.contains('new york|ny').astype(int)
        
        top_hubs = ['san francisco', 'new york', 'boston', 'silicon valley', 'palo alto', 
                   'mountain view', 'los angeles', 'seattle', 'austin', 'denver']
        features['location_is_top_tech_hub'] = location_lower.str.contains('|'.join(top_hubs)).astype(int)
        
        # Status features
        features['is_public'] = (df['status'].fillna('').str.lower() == 'public').astype(int)
        
        # Batch features
        features['batch_year_recent'] = (df['batch_year'].fillna(2020) >= 2018).astype(int)
        
        # Team size categories
        features['team_size_large'] = (df['team_size'].fillna(0) > 100).astype(int)
        
        return features[self.company_features]
    
    def _extract_founder_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract founder-specific features."""
        features = pd.DataFrame()
        
        # Basic founder info
        features['founder_count'] = df['founder_count'].fillna(1)
        features['founder_names_count'] = df['founder_names_count'].fillna(1)
        
        # Experience features
        features['has_previous_companies'] = df['has_previous_companies'].fillna(False).astype(int)
        
        # Calculate years of experience from previous companies
        def count_experience_years(prev_companies_str):
            if pd.isna(prev_companies_str) or prev_companies_str == 'None':
                return 0
            # Count how many previous companies
            companies = str(prev_companies_str).split('|')
            return min(len(companies) * 2, 20)  # Estimate 2 years per company, max 20
        
        features['founder_has_experience_years'] = df['founder_previous_companies'].apply(count_experience_years)
        
        # Education features
        education_lower = df['founder_education'].fillna('').str.lower()
        
        top_schools = ['stanford', 'mit', 'harvard', 'berkeley', 'carnegie mellon', 
                      'yale', 'princeton', 'penn', 'cornell', 'caltech']
        features['founder_attended_top_school'] = education_lower.str.contains('|'.join(top_schools)).astype(int)
        
        features['founder_has_phd'] = education_lower.str.contains('phd|doctoral').astype(int)
        
        # Technical background
        features['founder_technical_background'] = df['founder_technical_background'].fillna(False).astype(int)
        
        # Previous startup background
        prev_comp_lower = df['founder_previous_companies'].fillna('').str.lower()
        startup_keywords = ['founder', 'ceo', 'cto', 'co-founder', 'startup']
        features['founder_startup_background'] = prev_comp_lower.str.contains('|'.join(startup_keywords)).astype(int)
        
        # FAANG background
        faang = ['google', 'amazon', 'facebook', 'apple', 'microsoft', 'meta']
        features['founder_faang_background'] = prev_comp_lower.str.contains('|'.join(faang)).astype(int)
        
        # Education quality score
        def score_education(edu_str):
            if pd.isna(edu_str) or edu_str == 'Unknown':
                return 0
            score = 0
            edu_lower = str(edu_str).lower()
            if any(school in edu_lower for school in top_schools):
                score += 2
            if 'phd' in edu_lower or 'doctoral' in edu_lower:
                score += 1
            if 'master' in edu_lower or 'ms' in edu_lower or 'mba' in edu_lower:
                score += 1
            if 'cs' in edu_lower or 'computer science' in edu_lower or 'engineering' in edu_lower:
                score += 1
            return min(score, 5)  # Cap at 5
        
        features['founder_education_quality'] = df['founder_education'].apply(score_education)
        
        # Multiple founders (diversity)
        features['founder_multiple_founders'] = (df['founder_count'].fillna(1) > 1).astype(int)
        
        # Diverse roles
        def has_diverse_roles(names_str):
            if pd.isna(names_str):
                return 0
            # If has Founder/CEO, Founder/CTO, etc., it's diverse
            roles = str(names_str).split('|')
            return int(len(roles) > 1)  # Multiple roles = diverse
        
        features['founder_diverse_roles'] = df['founder_names'].apply(has_diverse_roles)
        
        return features[self.founder_features]
    
    def _calculate_founder_quality(self, founder_features_df: pd.DataFrame) -> pd.Series:
        """Calculate founder quality score (0-1)."""
        # Weighted combination of founder features
        founder_quality = (
            founder_features_df['has_previous_companies'] * 0.15 +
            founder_features_df['founder_has_experience_years'] / 20 * 0.15 +
            founder_features_df['founder_attended_top_school'] * 0.15 +
            founder_features_df['founder_technical_background'] * 0.2 +
            founder_features_df['founder_faang_background'] * 0.15 +
            founder_features_df['founder_multiple_founders'] * 0.1 +
            founder_features_df['founder_education_quality'] / 5 * 0.1
        )
        
        return founder_quality.clip(0, 1)