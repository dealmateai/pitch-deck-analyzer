"""
Dataset Builder
Builds complete training dataset from synthetic data
Handles data validation and preprocessing
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from utils.logger import log
from scraper.synthetic_data_generator import SyntheticDataGenerator

class DatasetBuilder:
    """Build complete training dataset."""
    
    def __init__(self, output_dir: str = "data/datasets"):
        """
        Initialize dataset builder.
        
        Args:
            output_dir: Directory to save datasets
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"✓ DatasetBuilder initialized - Output: {self.output_dir}")
    
    def build_complete_dataset(self) -> pd.DataFrame:
        """
        Build complete training dataset.
        
        Returns:
            DataFrame with 100 companies
        """
        log.info("\n" + "="*80)
        log.info("BUILDING COMPLETE DATASET")
        log.info("="*80)
        
        # Step 1: Generate synthetic data
        log.info("\n[STEP 1] Generating synthetic data...")
        generator = SyntheticDataGenerator()
        df = generator.generate_dataset()
        
        log.info(f"✓ Generated {len(df)} companies")
        
        # Step 2: Validate data
        log.info("\n[STEP 2] Validating data...")
        df = self._validate_data(df)
        log.info(f"✓ Data validated - {len(df)} companies remain")
        
        # Step 3: Clean data
        log.info("\n[STEP 3] Cleaning data...")
        df = self._clean_data(df)
        log.info(f"✓ Data cleaned")
        
        # Step 4: Add features
        log.info("\n[STEP 4] Adding features...")
        df = self._add_features(df)
        log.info(f"✓ Features added")
        
        # Step 5: Save dataset
        log.info("\n[STEP 5] Saving dataset...")
        self._save_dataset(df)
        log.info(f"✓ Dataset saved to {self.output_dir}")
        
        log.info("\n" + "="*80)
        log.info("✅ DATASET BUILDING COMPLETE")
        log.info("="*80 + "\n")
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate dataset.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Validated DataFrame
        """
        # Check required columns
        required_cols = [
            'name', 'description', 'industry', 'founded_year', 
            'team_size', 'source', 'label', 'founder_names',
            'founder_previous_companies', 'founder_education'
        ]
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            log.warning(f"⚠ Missing columns: {missing_cols}")
            # Add missing columns with default values
            for col in missing_cols:
                if 'founder' in col:
                    df[col] = "Unknown"
                elif col == 'label':
                    df[col] = 0
                else:
                    df[col] = ""
        
        # Check for empty descriptions
        empty_desc = df[df['description'].isna() | (df['description'] == '')].shape[0]
        if empty_desc > 0:
            log.warning(f"⚠ Found {empty_desc} empty descriptions")
            # Fill with generic description
            df.loc[df['description'].isna() | (df['description'] == ''), 'description'] = \
                "Technology company providing innovative solutions"
        
        # Check label distribution
        label_dist = df['label'].value_counts()
        log.info(f"  Label distribution:")
        for label, count in label_dist.items():
            log.info(f"    Label {label}: {count} companies ({count/len(df)*100:.1f}%)")
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean dataset.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['name'])
        removed = initial_count - len(df)
        if removed > 0:
            log.info(f"  Removed {removed} duplicate companies")
        
        # Fill missing values
        df['founded_year'] = df['founded_year'].fillna(2020).astype(int)
        df['team_size'] = df['team_size'].fillna(0).astype(int)
        df['batch'] = df['batch'].fillna('N/A')
        df['status'] = df['status'].fillna('Private')
        df['location'] = df['location'].fillna('Unknown')
        
        # Clean founder fields
        df['founder_count'] = df['founder_count'].fillna(0).astype(int)
        df['founder_names'] = df['founder_names'].fillna('Unknown')
        df['founder_previous_companies'] = df['founder_previous_companies'].fillna('None')
        df['founder_education'] = df['founder_education'].fillna('Unknown')
        df['founder_technical_background'] = df['founder_technical_background'].fillna(False).astype(bool)
        
        log.info(f"  Filled all missing values")
        
        return df
    
    def _add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived features.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with new features
        """
        # Add text length features
        df['description_length'] = df['description'].fillna('').str.len()
        df['description_word_count'] = df['description'].fillna('').str.split().str.len()
        
        # Add founder features
        df['founder_names_count'] = df['founder_names'].fillna('').str.split('|').str.len()
        df['has_previous_companies'] = df['founder_previous_companies'] != 'None'
        df['has_education'] = df['founder_education'] != 'Unknown'
        
        # Add company age (as of 2026)
        current_year = 2026
        df['company_age'] = current_year - df['founded_year']
        df['company_age'] = df['company_age'].clip(lower=0)
        
        # Add company size categories
        def categorize_team_size(size):
            if size == 0:
                return 'Unknown'
            elif size < 10:
                return 'Micro (0-9)'
            elif size < 50:
                return 'Small (10-49)'
            elif size < 200:
                return 'Medium (50-199)'
            elif size < 1000:
                return 'Large (200-999)'
            else:
                return 'Enterprise (1000+)'
        
        df['team_size_category'] = df['team_size'].apply(categorize_team_size)
        
        # Add batch year (extract from batch string)
        def extract_batch_year(batch):
            if batch == 'N/A':
                return 2020
            # Extract year from strings like "Winter 2009", "Summer 2010", etc.
            try:
                year = int(batch.split()[-1])
                return year
            except:
                return 2020
        
        df['batch_year'] = df['batch'].apply(extract_batch_year)
        
        log.info(f"  Added features:")
        log.info(f"    - Text length features")
        log.info(f"    - Founder features")
        log.info(f"    - Company age")
        log.info(f"    - Team size categories")
        log.info(f"    - Batch year")
        
        return df
    
    def _save_dataset(self, df: pd.DataFrame) -> None:
        """
        Save dataset to CSV.
        
        Args:
            df: DataFrame to save
        """
        # Save main dataset
        csv_path = self.output_dir / "training_dataset.csv"
        df.to_csv(csv_path, index=False)
        log.info(f"  Saved main dataset: {csv_path}")
        
        # Save by label
        yc_df = df[df['label'] == 1]
        yc_path = self.output_dir / "yc_companies.csv"
        yc_df.to_csv(yc_path, index=False)
        log.info(f"  Saved YC companies ({len(yc_df)}): {yc_path}")
        
        non_yc_df = df[df['label'] == 0]
        non_yc_path = self.output_dir / "non_yc_companies.csv"
        non_yc_df.to_csv(non_yc_path, index=False)
        log.info(f"  Saved non-YC companies ({len(non_yc_df)}): {non_yc_path}")
        
        # Save summary
        summary = {
            "total_companies": len(df),
            "yc_companies": len(yc_df),
            "non_yc_companies": len(non_yc_df),
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
        }
        
        log.info(f"\n📊 Dataset Summary:")
        log.info(f"  Total companies: {summary['total_companies']}")
        log.info(f"  YC companies: {summary['yc_companies']}")
        log.info(f"  Non-YC companies: {summary['non_yc_companies']}")
        log.info(f"  Total columns: {len(summary['columns'])}")
        
        return summary