"""
FastAPI Application for Heart Disease Prediction
"""

import logging
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Gauge, Histogram,
                               generate_latest)
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Prometheus Metrics
PREDICTION_COUNT = Counter(
    "prediction_count_total", "Total number of heart disease predictions"
)
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds", "Time spent processing prediction"
)

# metrics for Model Outputs
PREDICTION_RESULTS = Counter(
    "model_prediction_results_total",
    "Count of predictions by risk level",
    ["risk_level", "prediction_class"],
)

# metrics for Feature Distributions (Gauges are best for current values)
FEATURE_AGE = Gauge("feature_age_years", "Age of the latest applicant")
FEATURE_CHOL = Gauge(
    "feature_cholesterol_mgdl", "Cholesterol level of the latest applicant"
)

# Create FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease risk",
    version="1.0.0",
)

# Load model and preprocessor at startup
MODEL_PATH = Path("models/best_model.pkl")
PREPROCESSOR_PATH = Path("models/preprocessor.pkl")

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    logger.info("✓ Model and preprocessor loaded successfully")
except Exception as e:
    logger.error(f"✗ Error loading model: {e}")
    model = None
    preprocessor = None


# Request schema
class HeartDiseaseInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (1=male, 0=female)")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type")
    trestbps: int = Field(..., ge=50, le=250, description="Resting blood pressure")
    chol: int = Field(..., ge=100, le=600, description="Serum cholesterol in mg/dl")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: int = Field(..., ge=0, le=2, description="Resting ECG results")
    thalach: int = Field(..., ge=50, le=250, description="Maximum heart rate")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(..., ge=0, le=10, description="ST depression")
    slope: int = Field(..., ge=0, le=2, description="Slope of peak exercise ST")
    ca: int = Field(..., ge=0, le=4, description="Number of major vessels")
    thal: int = Field(..., ge=0, le=3, description="Thalassemia")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1,
            }
        }
    }


# Response schema
class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str
    message: str
    timestamp: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {"health": "/health", "predict": "/predict", "docs": "/docs"},
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    preprocessor_status = "loaded" if preprocessor is not None else "not loaded"

    return {
        "status": "healthy" if (model and preprocessor) else "unhealthy",
        "model_status": model_status,
        "preprocessor_status": preprocessor_status,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: HeartDiseaseInput):
    """Prediction endpoint"""
    with PREDICTION_LATENCY.time():
        try:
            # 1. Track Input Features (Data Drift Monitoring)
            FEATURE_AGE.set(input_data.age)
            FEATURE_CHOL.set(input_data.chol)
            # Check if model is loaded
            if model is None or preprocessor is None:
                logger.error("Model or preprocessor not loaded")
                raise HTTPException(status_code=503, detail="Model not available")

            # Log request
            logger.info(f"Prediction request received: {input_data.model_dump()}")

            # Convert input to DataFrame
            input_df = pd.DataFrame([input_data.model_dump()])

            # Preprocess
            input_processed = preprocessor.transform(input_df)

            # Increment the counter
            PREDICTION_COUNT.inc()

            # Make prediction
            prediction = model.predict(input_processed)[0]
            probability = model.predict_proba(input_processed)[0][1]

            # Determine risk level
            if probability < 0.3:
                risk_level = "Low"
            elif probability < 0.7:
                risk_level = "Medium"
            else:
                risk_level = "High"

            # Create response
            response = PredictionResponse(
                prediction=int(prediction),
                probability=float(probability),
                risk_level=risk_level,
                message=f"Heart disease {'detected' if prediction == 1 else 'not detected'}",
                timestamp=datetime.now().isoformat(),
            )

            # Log response
            logger.info(f"Prediction: {prediction}, Probability: {probability:.4f}")
            PREDICTION_RESULTS.labels(
                risk_level=risk_level, prediction_class=str(prediction)
            ).inc()

            return response

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# @app.get("/metrics")
# async def get_metrics():
#     """Get API metrics (placeholder for Prometheus)"""
#     # This would integrate with Prometheus in production
#     return {
#         "total_predictions": 0,
#         "average_response_time": 0,
#         "error_rate": 0
#     }
@app.get("/metrics")
async def get_metrics():
    """Exposes Prometheus metrics in the correct text format"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
