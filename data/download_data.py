"""
Data Download Script for Heart Disease Dataset
Downloads the UCI Heart Disease dataset from UCI ML Repository
"""

import os
import pandas as pd
import requests
from pathlib import Path

# Create directories
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Dataset URL
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

# Column names for the dataset
COLUMN_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 
    'ca', 'thal', 'target'
]

def download_data():
    """Download the Heart Disease dataset"""
    print("Downloading Heart Disease dataset...")
    
    try:
        response = requests.get(DATASET_URL)
        response.raise_for_status()
        
        # Save raw data
        raw_file = RAW_DIR / "heart_disease.csv"
        with open(raw_file, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Data downloaded successfully to {raw_file}")
        
        # Load and add column names
        df = pd.read_csv(raw_file, names=COLUMN_NAMES, na_values='?')
        
        # Binary classification: 0 = no disease, 1+ = disease
        df['target'] = (df['target'] > 0).astype(int)
        
        # Save with headers
        processed_file = RAW_DIR / "heart_disease_with_headers.csv"
        df.to_csv(processed_file, index=False)
        
        print(f"✓ Data saved with headers to {processed_file}")
        print(f"✓ Dataset shape: {df.shape}")
        print(f"✓ Missing values: {df.isnull().sum().sum()}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error downloading data: {e}")
        raise

if __name__ == "__main__":
    df = download_data()
    print("\nDataset Preview:")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
