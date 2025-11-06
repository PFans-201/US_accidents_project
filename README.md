# US Accidents and Road Quality Analysis

[![CI Pipeline](https://github.com/yourusername/us-accidents-road-quality/workflows/CI%20Pipeline/badge.svg)](https://github.com/yourusername/us-accidents-road-quality/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> End-to-end data science project analyzing the relationship between road surface conditions and US traffic accident patterns using Kaggle accident data and OpenStreetMap road quality information.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Research Question](#research-question)
- [Datasets](#datasets)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

This project combines two major data sources to investigate how road surface quality influences traffic accident patterns, severity, and outcomes across the United States:

1. **US Accidents Dataset (2016-2023)** - 7.6M accident records with GPS coordinates
2. **OpenStreetMap Road Network** - Road segments with surface quality attributes

### Key Objectives
- Spatially join accident locations with corresponding road surface data
- Analyze correlations between road conditions and accident severity
- Build predictive models for accident risk based on road quality
- Compare interpretable and black-box machine learning approaches
- Provide actionable insights for transportation safety improvements

## 🔬 Research Question (TODO REVISE)

**How does road surface quality (asphalt, concrete, gravel, etc.) influence traffic accident frequency, severity, and outcomes in the United States?**

### Hypotheses
- H1: Poor road surface conditions correlate with higher accident severity
- H2: Specific surface types (e.g., gravel, unpaved) show elevated accident rates
- H3: Road quality impacts vary by weather conditions and time of day

## 📊 Datasets

### Primary Dataset: US Accidents (Kaggle)
- **Source**: [US Accidents (2016-2023) on Kaggle](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
- **Size**: ~7.6 million records
- **Key Features**:
  - GPS Coordinates: `Start_Lat`, `Start_Lng`
  - Temporal: `Start_Time`, `End_Time`
  - Environmental: Weather conditions, visibility, temperature
  - Infrastructure: Traffic signals, crossings, junctions
  - Severity: 1-4 scale

### Secondary Dataset: OpenStreetMap
- **Source**: OSM via `osmnx` library
- **Coverage**: US road network
- **Key Attributes**:
  - Road surface types: `paved`, `asphalt`, `concrete`, `gravel`, `unpaved`, `dirt`
  - Road classification: highway types
  - Geometry: LineString road segments

## 📁 Project Structure

```
us-accidents-road-quality/
├── .github/                    # GitHub configuration
│   ├── workflows/
│   │   └── ci.yml             # CI/CD pipeline
│   └── CONTRIBUTING.md        # Contribution guidelines
├── data/                       # Data directory (gitignored)
│   ├── raw/                   # Original datasets
│   ├── processed/             # Cleaned data
│   └── integrated/            # Joined data with road quality
├── docs/                       # Documentation
│   ├── PROJECT_SPECIFICATION.md
│   ├── DATA_DICTIONARY.md
│   ├── METHODOLOGY.md
│   └── ARCHITECTURE.md
├── notebooks/                  # Jupyter notebooks
│   ├── 00_data_exploration.ipynb
│   ├── 01_data_loading_accidents.ipynb
│   ├── 02_osm_data_acquisition.ipynb
│   ├── 03_spatial_join.ipynb
│   ├── 04_data_cleaning.ipynb
│   ├── 05_eda.ipynb
│   ├── 06_feature_engineering.ipynb
│   ├── 07_model_development.ipynb
│   ├── 08_model_evaluation.ipynb
│   └── 09_final_analysis.ipynb
├── src/                        # Source code
│   ├── data/                  # Data loading and processing
│   ├── features/              # Feature engineering
│   ├── models/                # ML models
│   ├── visualization/         # Plotting utilities
│   └── utils/                 # Helper functions
├── tests/                      # Unit tests
├── paper/                      # Research paper (LaTeX)
├── presentation/              # Presentation materials
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── Makefile                   # Build automation
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git
- (Recommended) Virtual environment tool


### Python Environment Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/us-accidents-road-quality.git
cd us-accidents-road-quality
```

2. **Create virtual environment**:
```bash
python -m venv DS_venv
source DS_venv/bin/activate  # On Windows: DS_venv\Scripts\activate
```

3. **Install dependencies**:
```bash
make install
# Or manually:
pip install -r requirements.txt
pip install -e .
```

4. **Set up Kaggle API credentials** (required for dataset download):

📖 **See detailed guide**: [`docs/KAGGLE_SETUP_GUIDE.md`](docs/KAGGLE_SETUP_GUIDE.md)

**Quick setup**:
- Get credentials from https://www.kaggle.com/settings/account
- Create `.env` file from template:
  ```bash
  cp .env.example .env
  ```
- Add your credentials to `.env`:
  ```bash
  KAGGLE_USERNAME=your_kaggle_username
  KAGGLE_KEY=your_kaggle_api_key
  ```

5. **Download the US Accidents dataset**:
```bash
python scripts/download_accidents_data.py
```

This will:
- Download ~2-3 GB dataset from Kaggle (first time only)
- Cache it locally (subsequent runs are instant)
- Generate comprehensive metadata documentation
- Create reference files in `data/raw/accidents_raw/`

4. **Install development tools** (optional):
```bash
make install-dev
```

5. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## ⚡ Quick Start

### 1. Download the Data
Download the US Accidents dataset from [Kaggle](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) and place it in:
```
data/raw/accidents_raw/US_Accidents_March23.csv
```

### 2. Run Jupyter Notebooks
```bash
make notebooks
# Navigate to: http://localhost:8888
```

Start with `00_data_exploration.ipynb` and proceed sequentially.

### 3. Run Full Pipeline
```bash
make run-pipeline
```

### 4. Run Tests
```bash
make test
```

## 💻 Usage

### Load Accident Data
```python
from src.data.load_accidents import load_accidents_data

# Load accidents with geometry
accidents_gdf = load_accidents_data(
    filepath="data/raw/accidents_raw/US_Accidents_March23.csv",
    nrows=10000  # Optional: limit for testing
)
```

### Acquire OSM Road Data
```python
from src.data.load_osm_data import download_osm_roads

# Download roads for a specific area
roads_gdf = download_osm_roads(
    place_name="Los Angeles, California, USA",
    network_type="drive"
)
```

### Spatial Join
```python
from src.data.spatial_join import spatial_join_accidents_roads

# Join accidents with nearest roads
joined_data = spatial_join_accidents_roads(
    accidents_gdf=accidents_gdf,
    roads_gdf=roads_gdf,
    max_distance=100.0  # meters
)
```

### Train Models
```python
from src.models.train import train_model
from src.models.evaluate import evaluate_model

# Train a model
model = train_model(
    X_train, y_train,
    model_type='xgboost'
)

# Evaluate
metrics = evaluate_model(model, X_test, y_test)
```

## 🔬 Methodology

### Data Pipeline
1. **Data Loading**: Load US Accidents CSV and convert to GeoDataFrame
2. **OSM Acquisition**: Download road networks with surface attributes via `osmnx`
3. **Spatial Join**: Match accidents to nearest road segments (max distance: 100m)
4. **Data Cleaning**: Handle missing values, validate coordinates
5. **Feature Engineering**: Create derived features (time-based, categorical encoding)
6. **Exploratory Analysis**: Statistical analysis and visualization
7. **Model Development**: Train interpretable and black-box models
8. **Model Interpretation**: Apply SHAP/LIME for explainability
9. **Evaluation**: Cross-validation, performance metrics, critical analysis

### Machine Learning Models

#### Interpretable Models
- Logistic Regression
- Decision Trees
- Linear Regression (for continuous targets)

#### Black-Box Models
- Random Forest
- XGBoost
- Neural Networks (if applicable)

### Evaluation Metrics
- Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Regression: RMSE, MAE, R²
- Cross-validation: 5-fold stratified

## 📈 Results

> Results will be populated as the analysis progresses. See notebooks for detailed findings.

### Key Findings
- TBD: Road surface impact on accident severity
- TBD: Temporal patterns by surface type
- TBD: Geographic distribution of high-risk road conditions

### Model Performance
| Model | Accuracy | F1-Score | ROC-AUC |
|-------|----------|----------|---------|
| Logistic Regression | TBD | TBD | TBD |
| Decision Tree | TBD | TBD | TBD |
| Random Forest | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD |

## 🧪 Testing

Run the test suite:
```bash
# All tests
make test

# With coverage report
make test-cov

# Specific test file
pytest tests/test_spatial_join.py -v
```

## 🎨 Code Quality

Format and lint code:
```bash
# Auto-format with Black
make format

# Run linters
make lint

# Type checking
make type-check
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:
- [Project Specification](docs/PROJECT_SPECIFICATION.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Methodology](docs/METHODOLOGY.md)
- [System Architecture](docs/ARCHITECTURE.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](.github/CONTRIBUTING.md) for details.

### Development Process
1. Fork the repository
2. Create a feature branch: `feature/03-your-feature`
3. Commit changes: `[STEP-3] Your commit message`
4. Push to your fork
5. Submit a pull request

### Coding Standards
- Follow PEP 8
- Add type hints
- Write docstrings
- Maintain >80% test coverage
- Use descriptive variable names

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **US Accidents Dataset**: Moosavi, Sobhan, et al. "A Countrywide Traffic Accident Dataset." arXiv preprint arXiv:1906.05409 (2019).
- **OpenStreetMap**: © OpenStreetMap contributors
- **OSMnx Library**: Boeing, G. 2017. "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks." Computers, Environment and Urban Systems 65, 126-139.

## 📧 Contact

For questions or collaboration inquiries, please open an issue or contact the project maintainers.

## 🗺️ Roadmap

- [x] Project structure setup
- [ ] Step 1: Data loading implementation
- [ ] Step 2: OSM data acquisition
- [ ] Step 3: Spatial join operation
- [ ] Step 4: Data cleaning
- [ ] Step 5: Feature engineering
- [ ] Step 6: Exploratory data analysis
- [ ] Step 7: Model development
- [ ] Step 8: Model interpretation
- [ ] Step 9: Research paper completion
- [ ] Final presentation

---

**Note**: This is an academic research project for educational purposes. Results and insights are exploratory and should not be used as the sole basis for policy or infrastructure decisions.
