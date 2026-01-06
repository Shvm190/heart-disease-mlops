#!/bin/bash

# Heart Disease MLOps - Project Setup Script
# This script creates the complete folder structure for the MLOps project

set -e  # Exit on error

echo "=========================================="
echo "Heart Disease MLOps - Project Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project name
PROJECT_NAME="heart-disease-mlops"

# Check if directory already exists
if [ -d "$PROJECT_NAME" ]; then
    echo "⚠️  Directory '$PROJECT_NAME' already exists!"
    read -p "Do you want to remove it and create a fresh setup? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing directory..."
        rm -rf "$PROJECT_NAME"
    else
        echo "❌ Setup cancelled."
        exit 1
    fi
fi

# Create project root
echo "📁 Creating project directory: $PROJECT_NAME"
mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

echo "📁 Creating folder structure..."

# Create main directories
mkdir -p data/{raw,processed}
mkdir -p notebooks
mkdir -p src/{data,models,features,utils}
mkdir -p api
mkdir -p tests
mkdir -p models
mkdir -p logs
mkdir -p mlruns
mkdir -p deployment/{kubernetes,helm/heart-disease-chart}
mkdir -p monitoring
mkdir -p scripts
mkdir -p screenshots
mkdir -p .github/workflows

echo -e "${GREEN}✓${NC} Main directories created"

# Create __init__.py files for Python packages
echo "🐍 Creating Python package files..."
touch src/__init__.py
touch src/data/__init__.py
touch src/models/__init__.py
touch src/features/__init__.py
touch src/utils/__init__.py
touch api/__init__.py
touch tests/__init__.py

echo -e "${GREEN}✓${NC} Python package files created"

# Create .gitkeep files for empty directories
echo "📝 Creating .gitkeep files..."
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch models/.gitkeep
touch logs/.gitkeep
touch screenshots/.gitkeep
touch mlruns/.gitkeep

echo -e "${GREEN}✓${NC} .gitkeep files created"

# Create placeholder files
echo "📄 Creating placeholder files..."

# Create README.md stub
cat > README.md << 'EOF'
# Heart Disease Prediction - MLOps Project

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download data:
```bash
python data/download_data.py
```

3. Train model:
```bash
python scripts/train_model.py
```

4. Run API:
```bash
uvicorn api.app:app --reload
```

More documentation coming soon...
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Environment Variables Template
# Copy this file to .env and fill in your values

# MLflow
MLFLOW_TRACKING_URI=file:./mlruns

# API
API_HOST=0.0.0.0
API_PORT=8000

# Docker Hub (for CI/CD)
DOCKER_USERNAME=your_username
DOCKER_PASSWORD=your_password

# Kubernetes (optional)
KUBE_CONFIG=your_kube_config
EOF

# Create pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=src
    --cov=api
    --cov-report=term-missing
    --cov-report=html
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
EOF

# Create .dockerignore
cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build

# Virtual Environment
venv/
env/
ENV/

# IDEs
.vscode
.idea
*.swp
*.swo

# Testing
.pytest_cache
.coverage
htmlcov/
*.cover

# Data (don't include in image)
data/raw/*.csv
mlruns/

# Docs
*.md
docs/

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
EOF

# Create a simple project structure documentation
cat > PROJECT_STRUCTURE.md << 'EOF'
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
EOF

echo -e "${GREEN}✓${NC} Placeholder files created"

# Create a setup checklist
cat > SETUP_CHECKLIST.md << 'EOF'
# Setup Checklist

## Initial Setup
- [ ] Run setup_project.sh
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy .env.example to .env and configure

## Development
- [ ] Download data: `python data/download_data.py`
- [ ] Run EDA notebook: `notebooks/01_eda.ipynb`
- [ ] Train model: `python scripts/train_model.py`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Start API: `uvicorn api.app:app --reload`

## Docker
- [ ] Build image: `docker build -t heart-disease-api:latest .`
- [ ] Run container: `docker run -p 8000:8000 heart-disease-api:latest`
- [ ] Test API: `curl http://localhost:8000/health`

## Deployment
- [ ] Push to GitHub
- [ ] Configure GitHub Secrets
- [ ] Deploy to Kubernetes
- [ ] Verify deployment

## Documentation
- [ ] Take screenshots
- [ ] Update README.md
- [ ] Write final report
- [ ] Record demo video
EOF

# Create a quick reference guide
cat > QUICK_REFERENCE.md << 'EOF'
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
EOF

# Initialize git repository
echo "🔧 Initializing git repository..."
git init
git branch -M main

echo -e "${GREEN}✓${NC} Git repository initialized"

# Create initial .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Jupyter Notebook
.ipynb_checkpoints

# Data
data/raw/*.csv
data/processed/*.csv
!data/raw/.gitkeep
!data/processed/.gitkeep

# Models
models/*.pkl
models/*.h5
models/*.onnx
!models/.gitkeep

# Logs
logs/
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/
coverage.xml

# Environment variables
.env
.env.local

# MLflow
mlruns/
mlartifacts/

# Screenshots
screenshots/*.png
!screenshots/.gitkeep

# Temporary files
*.tmp
*.bak
EOF

echo -e "${GREEN}✓${NC} .gitignore created"

# Print summary
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Project setup completed successfully!${NC}"
echo "=========================================="
echo ""
echo "📊 Project Statistics:"
echo "   • Directories created: $(find . -type d | wc -l)"
echo "   • Files created: $(find . -type f | wc -l)"
echo ""
echo "📁 Project location: $(pwd)"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. Navigate to project directory:"
echo -e "   ${BLUE}cd $PROJECT_NAME${NC}"
echo ""
echo "2. Create virtual environment:"
echo -e "   ${BLUE}python -m venv venv${NC}"
echo ""
echo "3. Activate virtual environment:"
echo -e "   ${BLUE}source venv/bin/activate${NC}  # Linux/Mac"
echo -e "   ${BLUE}venv\\Scripts\\activate${NC}      # Windows"
echo ""
echo "4. Copy your code files into the appropriate directories"
echo ""
echo "5. Install dependencies:"
echo -e "   ${BLUE}pip install -r requirements.txt${NC}"
echo ""
echo "6. Follow the SETUP_CHECKLIST.md for complete setup"
echo ""
echo "📚 Reference Files Created:"
echo "   • PROJECT_STRUCTURE.md - Project layout overview"
echo "   • SETUP_CHECKLIST.md - Step-by-step setup guide"
echo "   • QUICK_REFERENCE.md - Common commands"
echo "   • .env.example - Environment variables template"
echo ""
echo "=========================================="
echo "Happy coding! 🎉"
echo "=========================================="
