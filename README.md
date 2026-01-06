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
