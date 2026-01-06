"""
Model Training with MLflow Tracking
"""

import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, classification_report, confusion_matrix
)
import joblib
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class ModelTrainer:
    """Model training and evaluation"""
    
    def __init__(self, config):
        self.config = config
        self.models = {}
        self.results = {}
        mlflow.set_tracking_uri(config.mlflow.tracking_uri)
        mlflow.set_experiment(config.mlflow.experiment_name)
    
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train Logistic Regression model"""
        print("\n" + "="*50)
        print("Training Logistic Regression")
        print("="*50)
        
        with mlflow.start_run(run_name="logistic_regression"):
            # Log parameters
            params = self.config.model.logistic_regression_params
            mlflow.log_params(params)
            
            # Train model
            model = LogisticRegression(**params)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred, y_pred_proba)
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X_train, y_train, 
                cv=self.config.model.cv_folds, 
                scoring='roc_auc'
            )
            metrics['cv_roc_auc_mean'] = cv_scores.mean()
            metrics['cv_roc_auc_std'] = cv_scores.std()
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Save confusion matrix
            self._plot_confusion_matrix(y_test, y_pred, "lr_confusion_matrix.png")
            mlflow.log_artifact("lr_confusion_matrix.png")
            
            self.models['logistic_regression'] = model
            self.results['logistic_regression'] = metrics
            
            print(f"✓ Logistic Regression trained")
            self._print_metrics(metrics)
            
            return model, metrics
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model"""
        print("\n" + "="*50)
        print("Training Random Forest")
        print("="*50)
        
        with mlflow.start_run(run_name="random_forest"):
            # Log parameters
            params = self.config.model.random_forest_params
            mlflow.log_params(params)
            
            # Train model
            model = RandomForestClassifier(**params)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred, y_pred_proba)
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X_train, y_train, 
                cv=self.config.model.cv_folds, 
                scoring='roc_auc'
            )
            metrics['cv_roc_auc_mean'] = cv_scores.mean()
            metrics['cv_roc_auc_std'] = cv_scores.std()
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log feature importance
            feature_importance = pd.DataFrame({
                'feature': range(X_train.shape[1]),
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            mlflow.log_dict(
                feature_importance.to_dict(), 
                "feature_importance.json"
            )
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Save confusion matrix
            self._plot_confusion_matrix(y_test, y_pred, "rf_confusion_matrix.png")
            mlflow.log_artifact("rf_confusion_matrix.png")
            
            self.models['random_forest'] = model
            self.results['random_forest'] = metrics
            
            print(f"✓ Random Forest trained")
            self._print_metrics(metrics)
            
            return model, metrics
    
    def _calculate_metrics(self, y_true, y_pred, y_pred_proba):
        """Calculate evaluation metrics"""
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_true, y_pred_proba)
        }
    
    def _print_metrics(self, metrics):
        """Print metrics in a formatted way"""
        print("\nMetrics:")
        for metric, value in metrics.items():
            print(f"  {metric:20s}: {value:.4f}")
    
    def _plot_confusion_matrix(self, y_true, y_pred, filename):
        """Plot and save confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
    
    def select_best_model(self, metric='roc_auc'):
        """Select the best model based on a metric"""
        best_model_name = max(
            self.results.items(), 
            key=lambda x: x[1][metric]
        )[0]
        
        print(f"\n✓ Best model: {best_model_name} "
              f"({metric}={self.results[best_model_name][metric]:.4f})")
        
        return self.models[best_model_name], best_model_name
    
    def save_model(self, model, model_path: Path):
        """Save model to disk"""
        joblib.dump(model, model_path)
        print(f"✓ Model saved to {model_path}")

import pandas as pd

if __name__ == "__main__":
    from src.config import config
    from src.data.preprocessing import (
        load_data, clean_data, split_features_target, 
        HeartDiseasePreprocessor
    )
    
    # Load and preprocess data
    df = load_data(config.data.raw_data_path)
    df_clean = clean_data(df)
    X, y = split_features_target(df_clean)
    
    # Preprocess features
    preprocessor = HeartDiseasePreprocessor()
    X_transformed = preprocessor.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_transformed, y,
        test_size=config.data.test_size,
        random_state=config.data.random_state,
        stratify=y
    )
    
    # Train models
    trainer = ModelTrainer(config)
    trainer.train_logistic_regression(X_train, y_train, X_test, y_test)
    trainer.train_random_forest(X_train, y_train, X_test, y_test)
    
    # Select and save best model
    best_model, best_model_name = trainer.select_best_model()
    trainer.save_model(best_model, config.api.model_path)
    preprocessor.save(config.api.preprocessor_path)
