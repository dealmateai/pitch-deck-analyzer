"""
Dataset Builder - USE SYNTHETIC DATA
"""

import pandas as pd
from pathlib import Path
from utils.logger import log
from config import DATASET_CONFIG
from scraper.synthetic_data_generator import SyntheticDataGenerator

class DatasetBuilder:
    """Build training dataset from synthetic data."""
    
    def __init__(self):
        """Initialize dataset builder."""
        self.generator = SyntheticDataGenerator()
        log.info("�� DatasetBuilder initialized")
    
    def build_complete_dataset(self) -> pd.DataFrame:
        """
        Build complete synthetic dataset.
        
        Returns:
            DataFrame with 100 companies
        """
        log.info("=" * 80)
        log.info("Building synthetic dataset (100 companies)...")
        log.info("=" * 80)
        
        # Generate dataset
        df = self.generator.generate_dataset()
        
        # Save dataset
        self.save_dataset(df)
        
        return df
    
    def save_dataset(self, df: pd.DataFrame):
        """Save dataset to CSV."""
        output_path = DATASET_CONFIG["training_dataset"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False)
        
        log.info(f"✓ Dataset saved to {output_path}")
        log.info(f"  Total records: {len(df)}")
        log.info(f"  Positive (YC): {(df['label'] == 1).sum()}")
        log.info(f"  Negative (Non-YC): {(df['label'] == 0).sum()}")