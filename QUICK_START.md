# Quick Start Guide: US Accidents and Road Quality Analysis

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies (2 min)
```bash
cd /home/pfanyka/Desktop/MASTERS/FCDados/DScience_project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Download Data (Manual Step)
- Go to: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
- Download **US_Accidents_March23.csv** (~2.5 GB)
- Place in: `data/raw/accidents_raw/US_Accidents_March23.csv`

### 3. Test the Setup (1 min)
```bash
# Test Python imports
python -c "from src.config import Config; print('✓ Config loaded')"
python -c "from src.data.load_accidents import load_accidents_data; print('✓ Modules working')"
```

### 4. Load Sample Data (2 min)
```bash
# Open Python interactive shell
python
```

```python
# Load 1000 sample accidents from California
from src.data.load_accidents import load_accidents_data

accidents = load_accidents_data(nrows=1000, states=['CA'])
print(f"Loaded {len(accidents)} accidents")
print(accidents.head())
```

## 🎯 Your First Analysis

### Option A: Interactive Python
```python
# 1. Load accidents
from src.data.load_accidents import load_accidents_data
accidents = load_accidents_data(nrows=5000, states=['CA'])

# 2. Download roads
from src.data.load_osm_data import download_osm_roads
roads = download_osm_roads("Los Angeles, California, USA")

# 3. Spatial join
from src.data.spatial_join import spatial_join_accidents_roads
joined = spatial_join_accidents_roads(accidents, roads, max_distance=100)

# 4. Check results
print(f"Matched {joined['matched'].sum()} out of {len(joined)} accidents")
print(joined['surface'].value_counts())
```

### Option B: Command Line Pipeline
```bash
# Run pipeline with sample data
python -m src.main --nrows 1000 --states CA
```

### Option C: Jupyter Notebook
```bash
# Start Jupyter
jupyter notebook notebooks/

# Create a new notebook and run:
```

```python
import sys
sys.path.append('..')

from src.data.load_accidents import load_accidents_data
from src.data.load_osm_data import download_osm_roads
from src.data.spatial_join import spatial_join_accidents_roads

# Your analysis code here...
```

## 📊 Next Steps by Priority

### HIGH PRIORITY (Do First)
1. **Create notebook 01**: Data loading exploration
   - File: `notebooks/01_data_loading_accidents.ipynb`
   - Load accidents, explore distributions, visualize

2. **Create notebook 02**: OSM data acquisition
   - File: `notebooks/02_osm_data_acquisition.ipynb`
   - Download roads, check surface coverage

3. **Create notebook 03**: Spatial join analysis
   - File: `notebooks/03_spatial_join.ipynb`
   - Join accidents to roads, validate matches

4. **Implement data cleaning**: Complete `src/data/data_cleaning.py`
   - Handle missing values
   - Remove outliers
   - Create notebook 04

5. **Implement feature engineering**: Complete `src/features/feature_engineering.py`
   - Temporal features
   - Categorical encoding
   - Create notebook 06

### MEDIUM PRIORITY (Do Second)
6. **Exploratory Data Analysis**: Create `notebooks/05_eda.ipynb`
   - Visualizations
   - Statistical tests
   - Correlations

7. **Model Development**: Implement `src/models/train.py`
   - Logistic Regression
   - Decision Trees
   - Random Forest
   - XGBoost

8. **Model Evaluation**: Implement `src/models/evaluate.py`
   - Metrics
   - SHAP explanations
   - Model comparison

### LOWER PRIORITY (Do Last)
9. **Test Suite**: Create tests in `tests/`
10. **Research Paper**: Write LaTeX in `paper/`
11. **Presentation**: Create slides in `presentation/`

## 🛠️ Useful Commands

```bash
# Code quality
make format          # Format code with Black
make lint           # Check code style
make test           # Run tests (when created)

# Development
make notebooks      # Start Jupyter
make clean          # Clean build artifacts
make clean-data     # Remove processed data (keeps raw)

# Pipeline
python -m src.main --help  # See all options
python -m src.main --nrows 1000 --states CA  # Small test run
```

## 📖 Documentation Quick Links

- **Getting Started**: `README.md`
- **Implementation Plan**: `docs/PROJECT_SPECIFICATION.md` (9-step plan)
- **What's Been Created**: `PROJECT_SETUP_SUMMARY.md`
- **Data Variables**: `docs/DATA_DICTIONARY.md`
- **Methods**: `docs/METHODOLOGY.md`
- **Architecture**: `docs/ARCHITECTURE.md`

## 🔍 Troubleshooting

### Import errors?
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Reinstall package
pip install -e .
```

### OSM download fails?
- Check internet connection
- Try a smaller area first (city instead of state)
- OSM may rate-limit - use caching

### Memory issues?
- Use `nrows` parameter to limit data
- Process by state instead of all at once
- Use batch processing functions

### Module not found?
```bash
# Verify installation
pip list | grep geopandas
pip list | grep osmnx

# If missing, reinstall
pip install -r requirements.txt
```

## 💡 Pro Tips

1. **Start Small**: Use `nrows=1000` for testing before processing full dataset
2. **Save Intermediate Results**: Use `.to_parquet()` to save processed data
3. **Use Logging**: All modules have logging - check `logs/pipeline.log`
4. **Git Branches**: Create feature branches for each step
5. **Document as You Go**: Add notes to notebooks as you analyze

## 🎓 Learning Resources

- **GeoPandas**: https://geopandas.org/
- **OSMnx**: https://osmnx.readthedocs.io/
- **Spatial Analysis**: https://geographicdata.science/book/
- **SHAP**: https://shap.readthedocs.io/

## ✅ Checklist for First Week

- [ ] Install dependencies and test setup
- [ ] Download US Accidents dataset
- [ ] Load sample data (1000-10000 records)
- [ ] Download OSM roads for one city
- [ ] Perform spatial join on sample
- [ ] Create notebook 01: Data loading
- [ ] Create notebook 02: OSM acquisition
- [ ] Create notebook 03: Spatial join
- [ ] Commit and push initial work to Git

## 📞 Need Help?

1. Check documentation in `docs/`
2. Review `PROJECT_SETUP_SUMMARY.md`
3. Check code comments and docstrings
4. Create GitHub issue
5. Ask team members

---

**Ready to start?** Run:
```bash
source venv/bin/activate
python -c "from src.data.load_accidents import load_accidents_data; print('✓ Ready!')"
```

Good luck with your project! 🎉
