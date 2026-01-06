# Heart Disease Prediction - MLOps Project Structure

```
heart-disease-mlops/
│
├── data/
│   ├── raw/                          # Raw dataset
│   ├── processed/                    # Processed data
│   └── download_data.py              # Script to download dataset
│
├── notebooks/
│   ├── 01_eda.ipynb                  # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb  # Feature engineering experiments
│   └── 03_model_training.ipynb       # Model training experiments
│
├── src/
│   ├── __init__.py
│   ├── config.py                     # Configuration management
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_loader.py            # Data loading utilities
│   │   └── preprocessing.py          # Data preprocessing pipeline
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py    # Feature transformation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py                  # Model training
│   │   ├── predict.py                # Model prediction
│   │   └── evaluate.py               # Model evaluation
│   └── utils/
│       ├── __init__.py
│       └── logger.py                 # Logging utilities
│
├── api/
│   ├── __init__.py
│   ├── app.py                        # FastAPI application
│   └── schemas.py                    # Pydantic models for API
│
├── tests/
│   ├── __init__.py
│   ├── test_data_preprocessing.py    # Data processing tests
│   ├── test_model.py                 # Model tests
│   └── test_api.py                   # API tests
│
├── mlruns/                           # MLflow tracking directory
│
├── models/                           # Saved models
│   └── .gitkeep
│
├── deployment/
│   ├── kubernetes/
│   │   ├── deployment.yaml           # K8s deployment
│   │   ├── service.yaml              # K8s service
│   │   └── ingress.yaml              # K8s ingress
│   ├── helm/
│   │   └── heart-disease-chart/      # Helm chart
│   └── docker-compose.yml            # Local deployment
│
├── monitoring/
│   ├── prometheus.yml                # Prometheus config
│   └── grafana-dashboard.json        # Grafana dashboard
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # GitHub Actions pipeline
│
├── scripts/
│   ├── train_model.py                # Training script
│   ├── test_api.sh                   # API testing script
│   └── build_docker.sh               # Docker build script
│
├── screenshots/                      # Screenshots for report
│
├── Dockerfile                        # Docker configuration
├── docker-compose.yml                # Docker Compose setup
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package setup
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── .dockerignore                     # Docker ignore rules
├── pytest.ini                        # Pytest configuration
├── README.md                         # Project documentation
└── REPORT.md                         # Assignment report
```

## Quick Start Guide

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd heart-disease-mlops
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Data
```bash
python data/download_data.py
```

### 3. Run EDA
```bash
jupyter notebook notebooks/01_eda.ipynb
```

### 4. Train Model
```bash
python scripts/train_model.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

### 6. Build Docker Image
```bash
docker build -t heart-disease-api:latest .
```

### 7. Run API Locally
```bash
docker run -p 8000:8000 heart-disease-api:latest
```

### 8. Test API
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, ...}'
```

## Key Technologies
- **ML Framework**: scikit-learn
- **Experiment Tracking**: MLflow
- **API**: FastAPI
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Testing**: Pytest
```
