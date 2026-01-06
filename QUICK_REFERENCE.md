# Quick Reference Guide

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Data & Training
```bash
# Download data
python data/download_data.py

# Train model
python scripts/train_model.py

# View MLflow UI
mlflow ui
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov=api --cov-report=html

# Run specific test
pytest tests/test_preprocessing.py -v
```

### API
```bash
# Start API
uvicorn api.app:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

### Docker
```bash
# Build image
docker build -t heart-disease-api:latest .

# Run container
docker run -p 8000:8000 heart-disease-api:latest

# Run with docker-compose
docker-compose up -d

# Stop containers
docker-compose down
```

### Kubernetes
```bash
# Apply deployment
kubectl apply -f deployment/kubernetes/

# Get pods
kubectl get pods

# Get services
kubectl get services

# View logs
kubectl logs <pod-name>

# Port forward
kubectl port-forward service/heart-disease-api-service 8000:80
```

### Git
```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Add remote and push
git remote add origin <your-repo-url>
git push -u origin main
```
