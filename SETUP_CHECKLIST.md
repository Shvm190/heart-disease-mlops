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
