"""
Main Training Script
Orchestrates the entire training pipeline
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.data.preprocessing import (
    load_data,
    clean_data,
    split_features_target,
    HeartDiseasePreprocessor,
)
from src.models.train import ModelTrainer
from sklearn.model_selection import train_test_split
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main training pipeline"""
    try:
        logger.info("=" * 60)
        logger.info("Starting Heart Disease Prediction Model Training")
        logger.info("=" * 60)

        # 1. Load data
        logger.info("\n[1/6] Loading data...")
        df = load_data(config.data.raw_data_path)

        # 2. Clean data
        logger.info("\n[2/6] Cleaning data...")
        df_clean = clean_data(df)

        # 3. Split features and target
        logger.info("\n[3/6] Splitting features and target...")
        X, y = split_features_target(df_clean)

        # 4. Preprocess features
        logger.info("\n[4/6] Preprocessing features...")
        preprocessor = HeartDiseasePreprocessor()
        X_transformed = preprocessor.fit_transform(X)

        # Save preprocessor
        preprocessor.save(config.api.preprocessor_path)

        # 5. Split data
        logger.info("\n[5/6] Splitting train/test sets...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_transformed,
            y,
            test_size=config.data.test_size,
            random_state=config.data.random_state,
            stratify=y,
        )

        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")

        # 6. Train models
        logger.info("\n[6/6] Training models...")
        trainer = ModelTrainer(config)

        # Train Logistic Regression
        trainer.train_logistic_regression(X_train, y_train, X_test, y_test)

        # Train Random Forest
        trainer.train_random_forest(X_train, y_train, X_test, y_test)

        # Select best model
        best_model, best_model_name = trainer.select_best_model(metric="roc_auc")

        # Save best model
        trainer.save_model(best_model, config.api.model_path)

        logger.info("\n" + "=" * 60)
        logger.info("✓ Training completed successfully!")
        logger.info(f"✓ Best model: {best_model_name}")
        logger.info(f"✓ Model saved to: {config.api.model_path}")
        logger.info(f"✓ Preprocessor saved to: {config.api.preprocessor_path}")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error(f"\n✗ Training failed: {str(e)}")
        raise


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
