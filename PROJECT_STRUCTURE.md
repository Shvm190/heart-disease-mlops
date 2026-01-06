# Project Structure

```
heart-disease-mlops/
├── data/
│   ├── raw/                          # Raw dataset files
│   └── processed/                    # Processed data
├── notebooks/
│   ├── 01_eda.ipynb                  # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb  # Feature engineering
│   └── 03_model_training.ipynb       # Model training experiments
├── src/
│   ├── __init__.py
│   ├── config.py                     # Configuration
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── preprocessing.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── api/
│   ├── __init__.py
│   ├── app.py                        # FastAPI application
│   └── schemas.py                    # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── test_data_preprocessing.py
│   ├── test_model.py
│   └── test_api.py
├── models/                           # Saved models
├── mlruns/                          # MLflow tracking
├── deployment/
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── helm/
│       └── heart-disease-chart/
├── monitoring/
│   ├── prometheus.yml
│   └── grafana-dashboard.json
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── scripts/
│   ├── train_model.py
│   └── test_api.sh
├── screenshots/                      # Screenshots for report
├── logs/                            # Application logs
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── setup.py
├── pytest.ini
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```
