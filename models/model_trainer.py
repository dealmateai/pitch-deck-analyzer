"""
Model training module for company and founder fit prediction.
Trains XGBoost models for both scoring dimensions.
"""

import pickle
from typing import Tuple, Dict, List, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from utils.logger import log
from config import MODEL_CONFIG, MODEL_PATHS

class ModelTrainer:
    """
    Train ML models for company and founder fit prediction.
    """
    
    def __init__(self):
        """Initialize model trainer."""
        log.info("Initializing model trainer...")
        
        self.company_model = None
        self.founder_model = None
        self.scaler_company = StandardScaler()
        self.scaler_founder = StandardScaler()
        self.feature_names = None
        
        log.info("✓ ModelTrainer initialized")
    
    def prepare_data(
        self,
        X: pd.DataFrame,
        y_company: pd.Series,
        y_founder: pd.Series,
        test_size: float = None,
        random_state: int = None
    ) -> Tuple:
        """
        Split data into train and test sets.
        
        Args:
            X: Feature matrix
            y_company: Company fit labels
            y_founder: Founder fit labels
            test_size: Test size ratio
            random_state: Random state
        
        Returns:
            (X_train, X_test, y_company_train, y_company_test, y_founder_train, y_founder_test)
        """
        if test_size is None:
            test_size = MODEL_CONFIG["test_size"]
        if random_state is None:
            random_state = MODEL_CONFIG["random_state"]
        
        X_train, X_test, y_company_train, y_company_test = train_test_split(
            X, y_company, test_size=test_size, random_state=random_state
        )
        
        _, _, y_founder_train, y_founder_test = train_test_split(
            X, y_founder, test_size=test_size, random_state=random_state
        )
        
        log.info(f"✓ Data split completed")
        log.info(f"  Train size: {len(X_train)}, Test size: {len(X_test)}")
        
        return X_train, X_test, y_company_train, y_company_test, y_founder_train, y_founder_test
    
    def train_company_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_type: str = "xgboost"
    ):
        """
        Train company fit model.
        
        Args:
            X_train: Training features
            y_train: Training labels (company fit scores)
            model_type: "xgboost" or "random_forest"
        """
        log.info(f"Training company fit model ({model_type})...")
        
        # Scale features
        X_train_scaled = self.scaler_company.fit_transform(X_train)
        
        # Create and train model
        if model_type == "xgboost":
            self.company_model = XGBRegressor(**MODEL_CONFIG["xgboost_params"])
        else:
            self.company_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=MODEL_CONFIG["random_state"]
            )
        
        self.company_model.fit(X_train_scaled, y_train)
        
        log.info("✓ Company fit model training completed")
    
    def train_founder_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_type: str = "xgboost"
    ):
        """
        Train founder fit model.
        
        Args:
            X_train: Training features
            y_train: Training labels (founder fit scores)
            model_type: "xgboost" or "random_forest"
        """
        log.info(f"Training founder fit model ({model_type})...")
        
        # Scale features
        X_train_scaled = self.scaler_founder.fit_transform(X_train)
        
        # Create and train model
        if model_type == "xgboost":
            self.founder_model = XGBRegressor(**MODEL_CONFIG["xgboost_params"])
        else:
            self.founder_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=MODEL_CONFIG["random_state"]
            )
        
        self.founder_model.fit(X_train_scaled, y_train)
        
        log.info("✓ Founder fit model training completed")
    
    def evaluate_model(
        self,
        model,
        scaler,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        model_name: str = "Model"
    ) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            model: Trained model
            scaler: Feature scaler
            X_test: Test features
            y_test: Test labels
            model_name: Model name for logging
        
        Returns:
            Dictionary with metrics
        """
        X_test_scaled = scaler.transform(X_test)
        y_pred = model.predict(X_test_scaled)
        
        metrics = {
            "mse": mean_squared_error(y_test, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
            "mae": mean_absolute_error(y_test, y_pred),
            "r2": r2_score(y_test, y_pred),
        }
        
        log.info(f"{model_name} Evaluation Metrics:")
        for metric, value in metrics.items():
            log.info(f"  {metric.upper()}: {value:.4f}")
        
        return metrics
    
    def get_feature_importance(
        self,
        model,
        feature_names: List[str],
        top_n: int = 10
    ) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Args:
            model: Trained model
            feature_names: List of feature names
            top_n: Number of top features to return
        
        Returns:
            Dictionary of feature importances
        """
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_importance = dict(zip(feature_names, importances))
            
            # Sort and get top n
            sorted_importance = dict(sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_n])
            
            log.info(f"Top {top_n} important features:")
            for feature, importance in sorted_importance.items():
                log.info(f"  {feature}: {importance:.4f}")
            
            return sorted_importance
        
        return {}
    
    def save_models(self):
        """Save trained models and scalers to disk."""
        log.info("Saving models...")
        
        # Create models directory if not exists
        MODEL_PATHS["company_model"].parent.mkdir(parents=True, exist_ok=True)
        
        # Save models
        with open(MODEL_PATHS["company_model"], "wb") as f:
            pickle.dump(self.company_model, f)
        
        with open(MODEL_PATHS["founder_model"], "wb") as f:
            pickle.dump(self.founder_model, f)
        
        # Save scalers
        with open(MODEL_PATHS["scaler_company"], "wb") as f:
            pickle.dump(self.scaler_company, f)
        
        with open(MODEL_PATHS["scaler_founder"], "wb") as f:
            pickle.dump(self.scaler_founder, f)
        
        # Save feature names
        with open(MODEL_PATHS["feature_names"], "wb") as f:
            pickle.dump(self.feature_names, f)
        
        log.info("✓ Models saved successfully")
        log.info(f"  Company model: {MODEL_PATHS['company_model']}")
        log.info(f"  Founder model: {MODEL_PATHS['founder_model']}")
    
    def load_models(self):
        """Load trained models and scalers from disk."""
        log.info("Loading models...")
        
        try:
            with open(MODEL_PATHS["company_model"], "rb") as f:
                self.company_model = pickle.load(f)
            
            with open(MODEL_PATHS["founder_model"], "rb") as f:
                self.founder_model = pickle.load(f)
            
            with open(MODEL_PATHS["scaler_company"], "rb") as f:
                self.scaler_company = pickle.load(f)
            
            with open(MODEL_PATHS["scaler_founder"], "rb") as f:
                self.scaler_founder = pickle.load(f)
            
            with open(MODEL_PATHS["feature_names"], "rb") as f:
                self.feature_names = pickle.load(f)
            
            log.info("✓ Models loaded successfully")
            return True
        
        except FileNotFoundError:
            log.warning("Model files not found - need to train models first")
            return False
    
    def predict(
        self,
        X: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions with trained models.
        
        Args:
            X: Feature matrix
        
        Returns:
            (company_fit_scores, founder_fit_scores)
        """
        if self.company_model is None or self.founder_model is None:
            log.error("Models not trained or loaded")
            return None, None
        
        X_company_scaled = self.scaler_company.transform(X)
        X_founder_scaled = self.scaler_founder.transform(X)
        
        company_scores = self.company_model.predict(X_company_scaled)
        founder_scores = self.founder_model.predict(X_founder_scaled)
        
        return company_scores, founder_scores