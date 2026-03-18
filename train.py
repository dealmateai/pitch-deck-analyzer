"""
Training Script - UPDATED for Kaggle Datasets
Builds training dataset from YC and Crunchbase
"""

import sys
import ast
import pandas as pd
import numpy as np
from typing import Tuple
from utils.logger import log, setup_logger
from scraper.dataset_builder import DatasetBuilder
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
    """Create numeric feature matrix for model training."""
    features = pd.DataFrame(index=df.index)

    features["name_length"] = df["name"].fillna("").astype(str).str.len()
    features["description_length"] = df["description"].fillna("").astype(str).str.len()
    features["founded_year"] = pd.to_numeric(df["founded_year"], errors="coerce").fillna(2018)
    features["team_size"] = pd.to_numeric(df["team_size"], errors="coerce").fillna(5)
    features["founder_count"] = df["founders"].apply(_safe_founder_count)

    categorical_columns = ["industry", "status", "source", "location", "batch"]
    available_columns = [column for column in categorical_columns if column in df.columns]

    if available_columns:
        encoded = pd.get_dummies(df[available_columns].fillna("unknown"), prefix=available_columns)
        features = pd.concat([features, encoded], axis=1)

    return features.astype(float)


def _build_targets(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """Generate supervised targets (0-100) from dataset columns."""
    label = pd.to_numeric(df["label"], errors="coerce").fillna(0)
    founder_count = df["founders"].apply(_safe_founder_count)
    team_size = pd.to_numeric(df["team_size"], errors="coerce").fillna(5)
    description_length = df["description"].fillna("").astype(str).str.len()

    company_fit = (
        20
        + (label * 60)
        + np.clip(description_length / 25, 0, 12)
        + np.clip(team_size / 500, 0, 8)
    ).clip(0, 100)

    founder_fit = (
        15
        + (label * 55)
        + np.clip(founder_count * 8, 0, 24)
        + np.clip(np.log1p(team_size) * 3, 0, 12)
    ).clip(0, 100)

    return company_fit, founder_fit

def main():
    """Main training workflow."""
    try:
        log.info("=" * 80)
        log.info("PITCH DECK ANALYZER - DATASET BUILDER")
        log.info("=" * 80)
        
        # Build dataset
        builder = DatasetBuilder()
        df = builder.build_complete_dataset()
        
        if len(df) == 0:
            log.error("Failed to build dataset")
            return 1

        log.info("\n" + "=" * 80)
        log.info("TRAINING MODELS")
        log.info("=" * 80)

        X = _build_training_features(df)
        y_company, y_founder = _build_targets(df)

        trainer = ModelTrainer()
        trainer.feature_names = X.columns.tolist()

        (
            X_train,
            X_test,
            y_company_train,
            y_company_test,
            y_founder_train,
            y_founder_test,
        ) = trainer.prepare_data(X, y_company, y_founder)

        trainer.train_company_model(X_train, y_company_train, model_type="xgboost")
        trainer.train_founder_model(X_train, y_founder_train, model_type="xgboost")

        trainer.evaluate_model(
            trainer.company_model,
            trainer.scaler_company,
            X_test,
            y_company_test,
            model_name="Company Fit Model",
        )
        trainer.evaluate_model(
            trainer.founder_model,
            trainer.scaler_founder,
            X_test,
            y_founder_test,
            model_name="Founder Fit Model",
        )

        trainer.save_models()
        
        log.info("\n" + "=" * 80)
        log.info("✓ DATASET + MODELS READY")
        log.info("=" * 80)
        log.info(f"Total records: {len(df)}")
        log.info(f"YC Companies: {(df['label'] == 1).sum()}")
        log.info(f"Other Companies: {(df['label'] == 0).sum()}")
        log.info(f"Company model: {MODEL_PATHS['company_model']}")
        log.info(f"Founder model: {MODEL_PATHS['founder_model']}")
        log.info(f"Company scaler: {MODEL_PATHS['scaler_company']}")
        log.info(f"Founder scaler: {MODEL_PATHS['scaler_founder']}")
        log.info(f"Feature names: {MODEL_PATHS['feature_names']}")
        
        log.info("\nNext: python api_server.py")
        
        return 0
    
    except Exception as e:
        log.error(f"Error: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())