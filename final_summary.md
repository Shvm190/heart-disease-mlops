# 🎯 START HERE - Complete Setup Guide

Welcome! This guide will help you set up your Heart Disease MLOps project from scratch.

## 📦 What You Have

I've provided you with:

1. **Setup Scripts**
   - `setup_project.sh` (for Linux/Mac)
   - `setup_project.bat` (for Windows)

2. **All Code Files** (14 code artifacts)
   - Configuration files
   - Data processing scripts
   - Model training code
   - FastAPI application
   - Tests
   - Docker & Kubernetes configs
   - CI/CD pipeline

3. **Documentation**
   - Implementation guide
   - Quick reference
   - Copy files guide

---

## 🚀 Step-by-Step Setup (15 minutes)

### Step 1: Run Setup Script (2 minutes)

**For Linux/Mac:**
```bash
# Make script executable
chmod +x setup_project.sh

# Run script
./setup_project.sh
```

**For Windows:**
```cmd
# Run script
setup_project.bat
```

This creates the complete folder structure:
```
heart-disease-mlops/
├── data/
├── notebooks/
├── src/
├── api/
├── tests/
├── models/
├── deployment/
├── monitoring/
└── ... (all directories)
```

### Step 2: Copy Code Files (10 minutes)

Now you need to copy the code I provided into the correct locations. Here's the mapping:

| File Name | Copy To Location |
|-----------|------------------|
| `requirements.txt` | → `heart-disease-mlops/requirements.txt` |
| `Dockerfile` | → `heart-disease-mlops/Dockerfile` |
| `docker-compose.yml` | → `heart-disease-mlops/docker-compose.yml` |
| `setup.py` | → `heart-disease-mlops/setup.py` |
| `config.py` | → `heart-disease-mlops/src/config.py` |
| `download_data.py` | → `heart-disease-mlops/data/download_data.py` |
| `preprocessing.py` | → `heart-disease-mlops/src/data/preprocessing.py` |
| `train.py` | → `heart-disease-mlops/src/models/train.py` |
| `app.py` (API) | → `heart-disease-mlops/api/app.py` |
| `train_model.py` (script) | → `heart-disease-mlops/scripts/train_model.py` |
| `test_preprocessing.py` | → `heart-disease-mlops/tests/test_preprocessing.py` |
| `test_api.py` | → `heart-disease-mlops/tests/test_api.py` |
| `ci-cd.yml` | → `heart-disease-mlops/.github/workflows/ci-cd.yml` |
| `deployment.yaml` | → `heart-disease-mlops/deployment/kubernetes/deployment.yaml` |
| `prometheus.yml` | → `heart-disease-mlops/monitoring/prometheus.yml` |

💡 **Tip:** See `COPY_FILES_GUIDE.md` for detailed instructions.

### Step 3: Setup Environment (3 minutes)

```bash
# Navigate to project
cd heart-disease-mlops

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ✅ Verification (5 minutes)

Test that everything is set up correctly:

```bash
# 1. Download data
python data/download_data.py
# Expected: ✓ Data downloaded successfully

# 2. Test imports
python -c "from src.config import config; print('✓ Config OK')"
python -c "from src.data.preprocessing import HeartDiseasePreprocessor; print('✓ Preprocessing OK')"
python -c "from api.app import app; print('✓ API OK')"

# 3. Run tests
pytest tests/ -v
# Expected: All tests pass

# 4. Train model (quick test)
python scripts/train_model.py
# Expected: Model trains successfully
```

If all commands succeed, you're ready to go! 🎉

---

## 📚 What to Do Next

### For Assignment Completion:

Follow the tasks in order using `IMPLEMENTATION_GUIDE.md`:

1. **Task 1: EDA** (1-2 hours)
   - Open `notebooks/01_eda.ipynb`
   - Run the provided EDA code
   - Generate visualizations
   - Save screenshots

2. **Task 2-3: Model Training** (1 hour)
   - Already done! Just run: `python scripts/train_model.py`
   - View MLflow: `mlflow ui`
   - Take screenshots

3. **Task 4-5: Testing & CI/CD** (1 hour)
   - Tests already written
   - GitHub Actions already configured
   - Just push to GitHub

4. **Task 6: Docker** (30 min)
   - Build: `docker build -t heart-disease-api:latest .`
   - Run: `docker run -p 8000:8000 heart-disease-api:latest`
   - Test API
   - Take screenshots

5. **Task 7: Kubernetes** (1 hour)
   - Deploy: `kubectl apply -f deployment/kubernetes/`
   - Verify deployment
   - Take screenshots

6. **Task 8: Monitoring** (30 min)
   - Start: `docker-compose up -d`
   - Access Grafana: `http://localhost:3000`
   - Take screenshots

7. **Task 9: Documentation** (2-3 hours)
   - Write 10-page report
   - Organize screenshots
   - Record video demo

---

## 📖 Reference Documents

| Document | Purpose |
|----------|---------|
| `IMPLEMENTATION_GUIDE.md` | Complete step-by-step guide for all 50 marks |
| `QUICK_REFERENCE.md` | Common commands cheat sheet |
| `COPY_FILES_GUIDE.md` | Detailed file copying instructions |
| `SETUP_CHECKLIST.md` | Task checklist |
| `PROJECT_STRUCTURE.md` | Directory structure overview |
| `README.md` | Project documentation |

---

## 🎯 Assignment Task Mapping

Each task is covered by specific files:

| Task | Files Involved | Status |
|------|----------------|--------|
| 1. Data & EDA | `download_data.py`, `01_eda.ipynb` | ✅ Provided |
| 2. Feature Engineering | `preprocessing.py` | ✅ Provided |
| 3. Experiment Tracking | `train.py` (MLflow integrated) | ✅ Provided |
| 4. Model Packaging | `train.py`, `config.py` | ✅ Provided |
| 5. CI/CD | `ci-cd.yml`, tests | ✅ Provided |
| 6. Containerization | `Dockerfile`, `docker-compose.yml` | ✅ Provided |
| 7. Deployment | `deployment.yaml` | ✅ Provided |
| 8. Monitoring | `prometheus.yml`, `app.py` | ✅ Provided |
| 9. Documentation | Templates provided | 📝 You write |

---

## 💡 Pro Tips

1. **Work Incrementally**
   - Complete one task at a time
   - Test after each step
   - Take screenshots immediately

2. **Use Version Control**
   ```bash
   git add .
   git commit -m "Completed Task X"
   git push
   ```

3. **Document as You Go**
   - Keep notes of any issues
   - Screenshot everything
   - Record your screen when doing tasks

4. **Time Management**
   - Total estimated time: 15-20 hours
   - Spread over 3-4 days
   - Don't rush the documentation

---

## 🆘 Getting Help

### Common Issues:

**"Module not found"**
```bash
# Make sure you're in the right directory
cd heart-disease-mlops
# And virtual environment is activated
source venv/bin/activate
```

**"Docker command not found"**
```bash
# Install Docker first
# Visit: https://docs.docker.com/get-docker/
```

**"Tests failing"**
```bash
# Check if data is downloaded
python data/download_data.py
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Still Stuck?

1. Check the `IMPLEMENTATION_GUIDE.md` for detailed steps
2. Review the `QUICK_REFERENCE.md` for commands
3. Look at error messages carefully
4. Google the specific error
5. Ask on course forums

---

## ✨ Success Criteria

You'll know you're done when:

- [x] All code files are in place
- [x] Virtual environment set up
- [x] Data downloaded
- [x] Model trains successfully
- [x] Tests pass
- [x] API runs
- [x] Docker container works
- [x] Kubernetes deploys
- [x] Screenshots collected
- [x] Report written
- [x] Video recorded
- [x] Repository pushed to GitHub

---

## 🎓 Submission Checklist

Before submitting, verify:

- [ ] GitHub repository is public/accessible
- [ ] All code is pushed
- [ ] README.md is complete
- [ ] Screenshots are organized
- [ ] 10-page report is ready (PDF/DOCX)
- [ ] Video demo is recorded (15-20 min)
- [ ] API is deployed (or instructions provided)
- [ ] All deliverables are mentioned in submission

---

## 🎉 You're Ready!

Everything is set up and ready to go. Follow these steps:

1. ✅ Run setup script
2. ✅ Copy code files
3. ✅ Setup environment
4. ✅ Verify installation
5. 📖 Open `IMPLEMENTATION_GUIDE.md`
6. 🚀 Start with Task 1

**Good luck with your assignment!** 💪

Remember: The code is production-ready and modular. You just need to:
- Set it up correctly
- Understand what each part does
- Document your work
- Present it well

You've got this! 🌟

---

## 📞 Quick Links

- Assignment Requirements: `MLOPS_ASSIGNMENT.md`
- Implementation Guide: `IMPLEMENTATION_GUIDE.md`
- Quick Reference: `QUICK_REFERENCE.md`
- Copy Files Guide: `COPY_FILES_GUIDE.md`
- Project Structure: `PROJECT_STRUCTURE.md`

---

**Last Updated:** January 2026
**Version:** 1.0.0
**Status:** Ready for Use ✅
