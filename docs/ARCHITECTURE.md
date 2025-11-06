# System Architecture: US Accidents and Road Quality Analysis

## 1. Overview

This document describes the technical architecture, data flow, and system components of the US Accidents and Road Quality Analysis project.

## 2. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                             │
├──────────────────────────┬──────────────────────────────────────┤
│  US Accidents (Kaggle)   │   OpenStreetMap (OSM via osmnx)      │
│  - CSV Format            │   - Graph/GeoDataFrame               │
│  - 7.6M records          │   - Road network + attributes        │
└──────────────────────────┴──────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LOADING LAYER                          │
│  (src/data/)                                                     │
├─────────────────────────────────────────────────────────────────┤
│  • load_accidents.py  - Load CSV, create geometries             │
│  • load_osm_data.py   - Download OSM roads with osmnx           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SPATIAL INTEGRATION LAYER                     │
│  (src/data/)                                                     │
├─────────────────────────────────────────────────────────────────┤
│  • spatial_join.py    - Join accidents to nearest roads          │
│                       - Distance threshold (100m)                │
│                       - Spatial indexing (R-tree)                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     DATA PROCESSING LAYER                        │
│  (src/data/)                                                     │
├─────────────────────────────────────────────────────────────────┤
│  • data_cleaning.py   - Handle missing values                    │
│                       - Remove duplicates                        │
│                       - Validate data integrity                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                   FEATURE ENGINEERING LAYER                      │
│  (src/features/)                                                 │
├─────────────────────────────────────────────────────────────────┤
│  • feature_engineering.py - Temporal features                    │
│                           - Categorical encoding                 │
│                           - Feature scaling                      │
│                           - Interaction features                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      MODELING LAYER                              │
│  (src/models/)                                                   │
├─────────────────────────────────────────────────────────────────┤
│  • model_selection.py - Define model architectures               │
│  • train.py           - Training pipeline                        │
│  • evaluate.py        - Evaluation metrics, SHAP/LIME            │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VISUALIZATION LAYER                           │
│  (src/visualization/)                                            │
├─────────────────────────────────────────────────────────────────┤
│  • plots.py           - EDA plots, maps, confusion matrices      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUTS                                  │
├──────────────────────────┬──────────────────────────────────────┤
│  Jupyter Notebooks       │   Research Paper (LaTeX)             │
│  - Exploratory analysis  │   - 8-page ACM format                │
│  - Model results         │   - Figures and tables               │
│                          │                                      │
│  Trained Models          │   Presentation                       │
│  - Pickle/joblib files   │   - Slides (PPTX)                    │
└──────────────────────────┴──────────────────────────────────────┘
```

## 3. Module Architecture

### 3.1 Source Code Structure (`src/`)

```
src/
├── __init__.py
├── config.py                    # Configuration management
├── main.py                      # Main pipeline orchestration
│
├── data/
│   ├── __init__.py
│   ├── load_accidents.py        # Accidents data loader
│   ├── load_osm_data.py         # OSM data acquisition
│   ├── spatial_join.py          # Spatial joining logic
│   └── data_cleaning.py         # Data cleaning utilities
│
├── features/
│   ├── __init__.py
│   └── feature_engineering.py   # Feature creation and transformation
│
├── models/
│   ├── __init__.py
│   ├── model_selection.py       # Model definitions
│   ├── train.py                 # Training pipeline
│   └── evaluate.py              # Evaluation and interpretation
│
├── visualization/
│   ├── __init__.py
│   └── plots.py                 # Plotting utilities
│
└── utils/
    ├── __init__.py
    ├── logging.py               # Logging configuration
    └── helpers.py               # Helper functions
```

### 3.2 Module Dependencies

```
config.py
    ↓
utils/ (logging, helpers)
    ↓
data/ (load_accidents, load_osm_data)
    ↓
data/ (spatial_join)
    ↓
data/ (data_cleaning)
    ↓
features/ (feature_engineering)
    ↓
visualization/ (plots) ← → models/ (train, evaluate)
    ↓
main.py (orchestration)
```

## 4. Data Flow

### 4.1 Pipeline Stages

```python
# Stage 1: Data Loading
accidents_df = load_accidents_data("data/raw/accidents_raw/US_Accidents_March23.csv")
roads_gdf = download_osm_roads("Los Angeles, CA, USA")

# Stage 2: Spatial Join
joined_gdf = spatial_join_accidents_roads(accidents_df, roads_gdf, max_distance=100)

# Stage 3: Data Cleaning
clean_df = clean_data(joined_gdf)

# Stage 4: Feature Engineering
features_df, feature_names = engineer_features(clean_df)

# Stage 5: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(features_df, clean_df['Severity'])

# Stage 6: Model Training
models = {
    'lr': train_logistic_regression(X_train, y_train),
    'rf': train_random_forest(X_train, y_train),
    'xgb': train_xgboost(X_train, y_train)
}

# Stage 7: Evaluation
for name, model in models.items():
    metrics = evaluate_model(model, X_test, y_test)
    shap_values = compute_shap(model, X_test)
    
# Stage 8: Visualization
plot_feature_importance(models['xgb'], feature_names)
plot_shap_summary(shap_values, X_test)
```

### 4.2 Data Storage Schema

```
data/
├── raw/
│   ├── accidents_raw/
│   │   └── US_Accidents_March23.csv          # Original Kaggle dataset
│   └── osm_raw/
│       ├── los_angeles_roads.pkl              # Cached OSM downloads
│       └── texas_roads.pkl
│
├── processed/
│   ├── accidents_cleaned/
│   │   └── accidents_with_geometry.parquet    # GeoDataFrame format
│   └── osm_processed/
│       └── roads_with_surface.parquet
│
└── integrated/
    └── accidents_with_road_quality/
        ├── full_dataset.parquet               # Complete integrated data
        ├── train.parquet                      # Training split
        ├── validation.parquet                 # Validation split
        └── test.parquet                       # Test split
```

## 5. Key Design Decisions

### 5.1 Coordinate Reference Systems

**Decision**: Use WGS84 (EPSG:4326) for input/output, Web Mercator (EPSG:3857) for processing

**Rationale**:
- WGS84: Standard for GPS coordinates, human-readable
- Web Mercator: Meters-based for accurate distance calculations
- Avoids distortion in distance measurements

### 5.2 Spatial Indexing

**Decision**: Use R-tree spatial indexing via `geopandas.sindex`

**Rationale**:
- O(log n) query time vs. O(n) for brute force
- Critical for 7.6M accident records
- Enables efficient nearest neighbor search

**Implementation**:
```python
# Build spatial index on roads
spatial_index = roads_gdf.sindex

# Query nearest road for each accident
for idx, accident in accidents_gdf.iterrows():
    nearest_idx = list(spatial_index.nearest(accident.geometry.bounds, 1))
    nearest_road = roads_gdf.iloc[nearest_idx[0]]
```

### 5.3 Memory Management

**Challenge**: 7.6M records may exceed available RAM

**Strategies**:
1. **Chunking**: Process data in batches
   ```python
   for chunk in pd.read_csv('accidents.csv', chunksize=100000):
       process_chunk(chunk)
   ```

2. **Geographic Segmentation**: Process by state/region
   ```python
   for state in ['CA', 'TX', 'FL']:
       state_accidents = accidents_df[accidents_df['State'] == state]
       state_roads = download_osm_roads(state)
       process_state(state_accidents, state_roads)
   ```

3. **Efficient Data Types**: Use categorical dtype for strings
   ```python
   accidents_df['State'] = accidents_df['State'].astype('category')
   ```

4. **Parquet Format**: Store processed data in columnar format
   ```python
   df.to_parquet('data/processed/data.parquet', compression='snappy')
   ```

### 5.4 Configuration Management

**Decision**: Centralized configuration in `src/config.py` with environment variables

**Structure**:
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Paths
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    
    # Spatial Join
    MAX_DISTANCE = float(os.getenv('MAX_DISTANCE_METERS', 100))
    
    # Model Training
    RANDOM_SEED = int(os.getenv('RANDOM_SEED', 42))
    TEST_SIZE = float(os.getenv('TEST_SIZE', 0.2))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### 5.5 Error Handling Strategy

**Approach**: Graceful degradation with logging

```python
import logging

logger = logging.getLogger(__name__)

def spatial_join_accidents_roads(accidents_gdf, roads_gdf, max_distance=100):
    try:
        # Validate inputs
        if accidents_gdf.crs != roads_gdf.crs:
            logger.warning("CRS mismatch detected. Reprojecting roads to match accidents.")
            roads_gdf = roads_gdf.to_crs(accidents_gdf.crs)
        
        # Perform spatial join
        joined = gpd.sjoin_nearest(accidents_gdf, roads_gdf, max_distance=max_distance)
        
        # Log statistics
        match_rate = (joined['index_right'].notna().sum() / len(accidents_gdf)) * 100
        logger.info(f"Spatial join completed. Match rate: {match_rate:.2f}%")
        
        return joined
        
    except Exception as e:
        logger.error(f"Spatial join failed: {str(e)}", exc_info=True)
        raise
```

## 6. Testing Strategy

### 6.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Pytest fixtures
├── test_data_loading.py        # Test data loaders
├── test_spatial_join.py        # Test spatial operations
├── test_data_cleaning.py       # Test cleaning functions
└── test_models.py              # Test model training/evaluation
```

### 6.2 Test Fixtures

```python
# conftest.py
import pytest
import pandas as pd
import geopandas as gpd

@pytest.fixture
def sample_accidents():
    """Create sample accident data for testing."""
    return gpd.GeoDataFrame({
        'ID': ['A-1', 'A-2', 'A-3'],
        'Start_Lat': [34.05, 34.06, 34.07],
        'Start_Lng': [-118.25, -118.26, -118.27],
        'Severity': [2, 3, 1],
        'geometry': [Point(-118.25, 34.05), Point(-118.26, 34.06), Point(-118.27, 34.07)]
    }, crs='EPSG:4326')

@pytest.fixture
def sample_roads():
    """Create sample road network for testing."""
    # Implementation...
```

### 6.3 Test Coverage Goals

- Unit tests: >80% code coverage
- Integration tests: Critical data pipeline paths
- End-to-end tests: Full pipeline execution on small dataset

## 7. Performance Considerations

### 7.1 Bottlenecks

1. **Spatial Join**: Most computationally expensive operation
   - **Optimization**: Spatial indexing, parallel processing
   
2. **OSM Data Download**: Network I/O bound
   - **Optimization**: Caching, batch downloads

3. **Model Training**: CPU/GPU intensive
   - **Optimization**: Hyperparameter tuning on sample, parallel CV

### 7.2 Scalability

**Current Scale**: 7.6M accidents, ~1M road segments per state

**Scaling Strategy**:
- Horizontal: Process states in parallel
- Vertical: Use high-memory instances for in-memory processing
- Storage: Parquet with compression for 10x size reduction

### 7.3 Performance Benchmarks (Target)

| Operation | Target Time | Notes |
|-----------|-------------|-------|
| Load 1M accidents | <30 seconds | CSV to GeoDataFrame |
| Download OSM (1 city) | 1-5 minutes | Depends on network |
| Spatial join (100k records) | <2 minutes | With spatial index |
| Feature engineering | <1 minute | Per 100k records |
| Model training (XGBoost) | 5-15 minutes | On full dataset |

## 8. Deployment and Reproducibility

### 8.1 Environment Setup

**Requirements**:
- Python 3.8+
- 16GB RAM minimum (32GB recommended)
- ~50GB disk space
- Internet connection for OSM downloads

**Setup Steps**:
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install project package
pip install -e .

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Run tests
make test

# 6. Execute pipeline
make run-pipeline
```

### 8.2 Docker Support (Optional)

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY setup.py .
RUN pip install -e .

# Run pipeline
CMD ["python", "-m", "src.main"]
```

### 8.3 CI/CD Pipeline

**GitHub Actions Workflow** (`.github/workflows/ci.yml`):
1. **Lint**: Check code style (black, flake8, pylint)
2. **Type Check**: Run mypy
3. **Test**: Execute test suite with coverage
4. **Security**: Check dependencies for vulnerabilities

## 9. Future Extensions

### 9.1 Potential Enhancements

1. **Real-time Analysis**: Stream accident data for live predictions
2. **Interactive Dashboard**: Web app for exploring results
3. **Temporal Analysis**: Analyze how road degradation over time affects accidents
4. **Deep Learning**: CNN on aerial imagery for automatic road quality assessment
5. **API Development**: REST API for model predictions

### 9.2 Research Extensions

1. **Causal Inference**: Propensity score matching to estimate causal effects
2. **Survival Analysis**: Time-to-accident based on road conditions
3. **Spatial Regression**: Account for spatial autocorrelation
4. **Multi-city Comparison**: Cross-region road quality impact analysis

---

**Document Version**: 1.0  
**Last Updated**: November 5, 2025  
**Architecture Review**: Pending team approval
