"""
Configuration Management for MLOps Project
"""

import os
from pathlib import Path
from dataclasses import dataclass

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

@dataclass
class DataConfig:
    """Data related configuration"""
    raw_data_path: Path = RAW_DATA_DIR / "heart_disease_with_headers.csv"
    processed_data_path: Path = PROCESSED_DATA_DIR / "processed_data.csv"
    test_size: float = 0.2
    random_state: int = 42
    
@dataclass
class ModelConfig:
    """Model training configuration"""
    model_dir: Path = MODELS_DIR
    random_state: int = 42
    cv_folds: int = 5
    
    # Model hyperparameters
    logistic_regression_params: dict = None
    random_forest_params: dict = None
    
    def __post_init__(self):
        if self.logistic_regression_params is None:
            self.logistic_regression_params = {
                'max_iter': 1000,
                'random_state': self.random_state,
                'solver': 'liblinear'
            }
        
        if self.random_forest_params is None:
            self.random_forest_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'random_state': self.random_state,
                'n_jobs': -1
            }

@dataclass
class MLflowConfig:
    """MLflow tracking configuration"""
    tracking_uri: str = "file:./mlruns"
    experiment_name: str = "heart-disease-prediction"
    
@dataclass
class APIConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    model_path: Path = MODELS_DIR / "best_model.pkl"
    preprocessor_path: Path = MODELS_DIR / "preprocessor.pkl"
    
@dataclass
class Config:
    """Main configuration class"""
    data: DataConfig = DataConfig()
    model: ModelConfig = ModelConfig()
    mlflow: MLflowConfig = MLflowConfig()
    api: APIConfig = APIConfig()
    
# Global config instance
config = Config()
