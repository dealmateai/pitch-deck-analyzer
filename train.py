import sys
import ast
import pandas as pd
import numpy as np
from typing import Tuple
from utils.logger import log, setup_logger
from scraper.dataset_builder import DatasetBuilder
from nlp.feature_extractor import FeatureExtractor
from models.model_trainer import ModelTrainer
from config import MODEL_PATHS

setup_logger()


def _safe_founder_count(founders_value) -> int:
    """Parse founder list and return founder count."""
    if isinstance(founders_value, list):
        return len(founders_value)

    if pd.isna(founders_value):
        return 1

    if isinstance(founders_value, str):
        try:
            parsed = ast.literal_eval(founders_value)
            if isinstance(parsed, list):
                return len(parsed)
        except (ValueError, SyntaxError):
            pass

        if founders_value.strip():
            return max(1, founders_value.count(",") + 1)

    return 1


def _build_training_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create numeric feature matrix for model training.
    Includes both company and founder features.
    """
    log.info("Building training features...")
    
    features = pd.DataFrame(index=df.index)

    # Basic text features
    features["name_length"] = df["name"].fillna("").astype(str).str.len()
    features["description_length"] = df["description"].fillna("").astype(str).str.len()
    features["description_word_count"] = df["description"].fillna("").astype(str).str.split().str.len()
    
    # Company features
    features["founded_year"] = pd.to_numeric(df["founded_year"], errors="coerce").fillna(2018)
    features["team_size"] = pd.to_numeric(df["team_size"], errors="coerce").fillna(5)
    
    # Founder features - from new dataset
    features["founder_count"] = df["founder_count"].fillna(1)
    features["founder_names_count"] = df["founder_names_count"].fillna(1)
    features["has_previous_companies"] = df["has_previous_companies"].fillna(False).astype(int)
    features["founder_technical_background"] = df["founder_technical_background"].fillna(False).astype(int)
    
    # Categorical encoding
    categorical_columns = ["industry", "status", "source", "location", "batch"]
    available_columns = [column for column in categorical_columns if column in df.columns]

    if available_columns:
        encoded = pd.get_dummies(
            df[available_columns].fillna("unknown"), 
            prefix=available_columns,
            drop_first=True
        )
        features = pd.concat([features, encoded], axis=1)

    log.info(f"✓ Built {features.shape[1]} features")
    
    return features.astype(float)


def _build_targets(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Generate supervised targets (0-100) from dataset.
    Incorporates founder experience into scoring.
    """
    log.info("Building target labels...")
    
    label = pd.to_numeric(df["label"], errors="coerce").fillna(0)
    founder_count = df["founder_count"].fillna(1)
    team_size = pd.to_numeric(df["team_size"], errors="coerce").fillna(5)
    description_length = df["description"].fillna("").astype(str).str.len()
    has_previous_companies = df["has_previous_companies"].fillna(False).astype(int)
    technical_background = df["founder_technical_background"].fillna(False).astype(int)

    # Company Fit Score (0-100)
    company_fit = (
        20  # Base score
        + (label * 60)  # YC label: 60 points
        + np.clip(description_length / 25, 0, 12)  # Description quality: 0-12 points
        + np.clip(team_size / 500, 0, 8)  # Team size: 0-8 points
    ).clip(0, 100)

    # Founder Fit Score (0-100) - ENHANCED WITH EXPERIENCE
    founder_fit = (
        15  # Base score
        + (label * 55)  # YC label: 55 points
        + np.clip(founder_count * 8, 0, 24)  # Multiple founders: 0-24 points
        + np.clip(np.log1p(team_size) * 3, 0, 12)  # Team size: 0-12 points
        + (has_previous_companies * 15)  # Previous companies: 15 points
        + (technical_background * 10)  # Technical skills: 10 points
    ).clip(0, 100)

    log.info(f"✓ Created targets")
    log.info(f"  Company Fit range: {company_fit.min():.1f} - {company_fit.max():.1f}")
    log.info(f"  Founder Fit range: {founder_fit.min():.1f} - {founder_fit.max():.1f}")
    
    return company_fit, founder_fit


def main():
    """Main training workflow."""
    try:
        log.info("=" * 80)
        log.info("PITCH DECK ANALYZER - COMPLETE TRAINING PIPELINE")
        log.info("=" * 80)
        
        # ===== STEP 1: BUILD DATASET =====
        log.info("\n[STEP 1] Building Dataset with Founder Experience...")
        builder = DatasetBuilder()
        df = builder.build_complete_dataset()
        
        if len(df) == 0:
            log.error("❌ Failed to build dataset")
            return 1
        
        log.info(f"✓ Dataset ready: {len(df)} companies")
        log.info(f"  Columns: {', '.join(df.columns[:5])}...")

        # ===== STEP 2: BUILD FEATURES =====
        log.info("\n[STEP 2] Building Training Features...")
        X = _build_training_features(df)
        
        if X.shape[0] == 0:
            log.error("❌ Failed to build features")
            return 1
        
        log.info(f"✓ Features built: {X.shape}")

        # ===== STEP 3: BUILD TARGETS =====
        log.info("\n[STEP 3] Building Target Labels...")
        y_company, y_founder = _build_targets(df)
        
        log.info(f"✓ Targets built")
        log.info(f"  Company fit - mean: {y_company.mean():.1f}, std: {y_company.std():.1f}")
        log.info(f"  Founder fit - mean: {y_founder.mean():.1f}, std: {y_founder.std():.1f}")

        # ===== STEP 4: TRAIN MODELS =====
        log.info("\n[STEP 4] Training Models...")
        trainer = ModelTrainer()
        trainer.feature_names = X.columns.tolist()
        
        company_metrics, founder_metrics = trainer.train(
            X, y_company, y_founder,
            X.columns.tolist()
        )
        
        log.info("✓ Models trained and saved")

        # ===== RESULTS =====
        log.info("\n" + "=" * 80)
        log.info("✅ TRAINING PIPELINE COMPLETE")
        log.info("=" * 80)
        
        log.info("\n📊 DATASET SUMMARY:")
        log.info(f"  Total companies: {len(df)}")
        log.info(f"  YC Companies: {(df['label'] == 1).sum()}")
        log.info(f"  Non-YC Companies: {(df['label'] == 0).sum()}")
        log.info(f"  Features: {X.shape[1]}")
        
        log.info("\n📈 MODEL METRICS:")
        log.info(f"  Company Fit R²: {company_metrics['r2']:.4f}")
        log.info(f"  Founder Fit R²: {founder_metrics['r2']:.4f}")
        
        log.info("\n💾 SAVED FILES:")
        log.info(f"  Company model: {MODEL_PATHS['company_model']}")
        log.info(f"  Founder model: {MODEL_PATHS['founder_model']}")
        log.info(f"  Scalers: {MODEL_PATHS['scaler_company']}")
        log.info(f"  Features: {MODEL_PATHS['feature_names']}")
        
        log.info("\n🚀 NEXT STEPS:")
        log.info("  1. Start API: python api_server.py")
        log.info("  2. Test API: python test_api.py")
        log.info("  3. Use Postman: POST http://localhost:8000/analyze")
        log.info("")
        
        return 0
    
    except Exception as e:
        log.error(f"❌ Error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())