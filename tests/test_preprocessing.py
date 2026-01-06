"""
Unit tests for data preprocessing
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.preprocessing import (
    HeartDiseasePreprocessor,
    load_data,
    clean_data,
    split_features_target
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'age': [63, 37, 41, 56, 57],
        'sex': [1, 1, 0, 1, 0],
        'cp': [3, 2, 1, 1, 0],
        'trestbps': [145, 130, 130, 120, 120],
        'chol': [233, 250, 204, 236, 354],
        'fbs': [1, 0, 0, 0, 0],
        'restecg': [0, 1, 0, 1, 1],
        'thalach': [150, 187, 172, 178, 163],
        'exang': [0, 0, 0, 0, 1],
        'oldpeak': [2.3, 3.5, 1.4, 0.8, 0.6],
        'slope': [0, 0, 2, 2, 2],
        'ca': [0, 0, 0, 0, 0],
        'thal': [1, 2, 2, 2, 2],
        'target': [1, 1, 0, 0, 0]
    })

@pytest.fixture
def sample_data_with_missing():
    """Create sample data with missing values"""
    data = pd.DataFrame({
        'age': [63, np.nan, 41, 56, 57],
        'sex': [1, 1, 0, 1, np.nan],
        'cp': [3, 2, np.nan, 1, 0],
        'trestbps': [145, 130, 130, np.nan, 120],
        'chol': [233, 250, 204, 236, 354],
        'fbs': [1, 0, 0, 0, 0],
        'restecg': [0, 1, 0, 1, 1],
        'thalach': [150, 187, 172, 178, 163],
        'exang': [0, 0, 0, 0, 1],
        'oldpeak': [2.3, 3.5, 1.4, 0.8, 0.6],
        'slope': [0, 0, 2, 2, 2],
        'ca': [0, 0, 0, 0, 0],
        'thal': [1, 2, 2, 2, 2],
        'target': [1, 1, 0, 0, 0]
    })
    return data

class TestPreprocessor:
    """Test HeartDiseasePreprocessor class"""
    
    def test_preprocessor_initialization(self):
        """Test preprocessor initialization"""
        preprocessor = HeartDiseasePreprocessor()
        assert preprocessor.pipeline is not None
        assert len(preprocessor.numerical_features) > 0
        assert len(preprocessor.categorical_features) > 0
    
    def test_fit_transform(self, sample_data):
        """Test fit_transform method"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop(columns=['target'])
        
        X_transformed = preprocessor.fit_transform(X)
        
        assert X_transformed.shape[0] == X.shape[0]
        assert X_transformed.shape[1] == len(
            preprocessor.numerical_features + preprocessor.categorical_features
        )
        assert not X_transformed.isnull().any().any()
    
    def test_transform_handles_missing_values(self, sample_data_with_missing):
        """Test that transform handles missing values"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data_with_missing.drop(columns=['target'])
        
        X_transformed = preprocessor.fit_transform(X)
        
        # Check no missing values in output
        assert not X_transformed.isnull().any().any()
    
    def test_numerical_scaling(self, sample_data):
        """Test that numerical features are scaled"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop(columns=['target'])
        
        X_transformed = preprocessor.fit_transform(X)
        
        # Check that numerical features have mean ≈ 0 and std ≈ 1
        numerical_cols = preprocessor.numerical_features
        for col in numerical_cols:
            if col in X_transformed.columns:
                mean = X_transformed[col].mean()
                std = X_transformed[col].std()
                assert abs(mean) < 1e-10  # Close to 0
                assert abs(std - 1) < 0.2  # Close to 1 (relaxed for small samples)

class TestDataFunctions:
    """Test data utility functions"""
    
    def test_clean_data(self, sample_data_with_missing):
        """Test clean_data function"""
        df_clean = clean_data(sample_data_with_missing)
        
        # Should not drop rows with few missing values
        assert len(df_clean) > 0
    
    def test_split_features_target(self, sample_data):
        """Test split_features_target function"""
        X, y = split_features_target(sample_data, target_col='target')
        
        assert 'target' not in X.columns
        assert len(X) == len(y)
        assert y.name == 'target'
    
    def test_split_features_target_invalid_column(self, sample_data):
        """Test split with invalid target column"""
        with pytest.raises(KeyError):
            split_features_target(sample_data, target_col='invalid_col')

class TestPreprocessorSaveLoad:
    """Test preprocessor save and load"""
    
    def test_save_and_load(self, sample_data, tmp_path):
        """Test saving and loading preprocessor"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop(columns=['target'])
        
        # Fit preprocessor
        preprocessor.fit(X)
        
        # Save
        save_path = tmp_path / "test_preprocessor.pkl"
        preprocessor.save(save_path)
        
        # Load
        loaded_preprocessor = HeartDiseasePreprocessor.load(save_path)
        
        # Test that loaded preprocessor works
        X_transformed_original = preprocessor.transform(X)
        X_transformed_loaded = loaded_preprocessor.transform(X)
        
        # Results should be identical
        pd.testing.assert_frame_equal(
            X_transformed_original, 
            X_transformed_loaded
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v"])