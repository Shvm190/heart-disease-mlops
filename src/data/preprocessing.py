"""
Data Preprocessing Pipeline
Handles missing values, feature encoding, and scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

class HeartDiseasePreprocessor:
    """Preprocessor for Heart Disease dataset"""
    
    def __init__(self):
        self.numerical_features = [
            'age', 'trestbps', 'chol', 'thalach', 'oldpeak'
        ]
        
        self.categorical_features = [
            'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'
        ]
        
        self.pipeline = None
        self._create_pipeline()
    
    def _create_pipeline(self):
        """Create preprocessing pipeline"""
        
        # Numerical pipeline
        numerical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # Categorical pipeline (simple imputation, no encoding as they're already numeric)
        categorical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent'))
        ])
        
        # Combine pipelines
        self.pipeline = ColumnTransformer([
            ('numerical', numerical_pipeline, self.numerical_features),
            ('categorical', categorical_pipeline, self.categorical_features)
        ])
    
    def fit(self, X):
        """Fit the preprocessing pipeline"""
        self.pipeline.fit(X)
        return self
    
    def transform(self, X):
        """Transform the data"""
        X_transformed = self.pipeline.transform(X)
        
        # Create feature names
        feature_names = self.numerical_features + self.categorical_features
        
        return pd.DataFrame(
            X_transformed, 
            columns=feature_names,
            index=X.index
        )
    
    def fit_transform(self, X):
        """Fit and transform the data"""
        self.fit(X)
        return self.transform(X)
    
    def save(self, path: Path):
        """Save the preprocessor"""
        joblib.dump(self, path)
        print(f"✓ Preprocessor saved to {path}")
    
    @staticmethod
    def load(path: Path):
        """Load a saved preprocessor"""
        return joblib.load(path)

def load_data(file_path: Path):
    """Load the raw data"""
    df = pd.read_csv(file_path)
    print(f"✓ Data loaded: {df.shape}")
    return df

def clean_data(df: pd.DataFrame):
    """Clean the dataset"""
    print(f"Missing values before cleaning:\n{df.isnull().sum()}")
    
    # Remove rows with too many missing values (>50%)
    threshold = len(df.columns) * 0.5
    df_clean = df.dropna(thresh=threshold)
    
    print(f"✓ Data cleaned: {df_clean.shape}")
    print(f"Missing values after cleaning:\n{df_clean.isnull().sum()}")
    
    return df_clean

def split_features_target(df: pd.DataFrame, target_col: str = 'target'):
    """Split features and target"""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}")
    print(f"✓ Target distribution:\n{y.value_counts()}")
    
    return X, y

if __name__ == "__main__":
    # Test preprocessing
    from src.config import config
    
    df = load_data(config.data.raw_data_path)
    df_clean = clean_data(df)
    X, y = split_features_target(df_clean)
    
    preprocessor = HeartDiseasePreprocessor()
    X_transformed = preprocessor.fit_transform(X)
    
    print("\nTransformed data shape:", X_transformed.shape)
    print("\nTransformed data preview:")
    print(X_transformed.head())
