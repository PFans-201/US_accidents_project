# Project Specification: US Accidents and Road Quality Analysis

## 1. Project Overview

### 1.1 Research Context
This project addresses a critical gap in traffic safety research by combining large-scale accident data with infrastructure quality information. While numerous studies examine accident causation factors (weather, traffic density, driver behavior), fewer investigate the systematic relationship between road surface conditions and accident patterns.

### 1.2 Motivation
- **7.6 million** accidents recorded in the US (2016-2023)
- Road infrastructure conditions are often overlooked in accident analysis
- OpenStreetMap provides granular road surface data at scale
- Spatial data science enables precise accident-road matching
- Findings can inform infrastructure investment and maintenance priorities

## 2. Research Questions and Objectives

### 2.1 Primary Research Question
**How does road surface quality influence traffic accident frequency, severity, and outcomes across the United States?**

### 2.2 Secondary Research Questions
1. Which road surface types (asphalt, concrete, gravel, unpaved) are associated with higher accident rates?
2. Does road surface quality interact with environmental factors (weather, time of day)?
3. Can road quality features improve accident severity prediction models?
4. Are there geographic patterns in road quality-related accidents?

### 2.3 Project Objectives
- Integrate US Accidents data with OSM road network using spatial joins
- Quantify relationships between road surface types and accident characteristics
- Develop predictive models incorporating road quality features
- Compare interpretable vs. black-box model performance
- Provide actionable insights for infrastructure improvement

## 3. Datasets

### 3.1 Primary Dataset: US Accidents (Kaggle)

**Source**: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

**Description**: A countrywide traffic accident dataset covering 49 states of the USA (2016-2023).

**Size**: ~7.6 million records

**Key Attributes**:
- **Spatial**: `Start_Lat`, `Start_Lng`, `End_Lat`, `End_Lng`, `City`, `County`, `State`, `Zipcode`
- **Temporal**: `Start_Time`, `End_Time`
- **Severity**: `Severity` (1-4 scale, 1=minor, 4=severe)
- **Environmental**: `Temperature`, `Humidity`, `Pressure`, `Visibility`, `Wind_Speed`, `Precipitation`, `Weather_Condition`
- **Infrastructure**: `Amenity`, `Bump`, `Crossing`, `Give_Way`, `Junction`, `No_Exit`, `Railway`, `Roundabout`, `Station`, `Stop`, `Traffic_Calming`, `Traffic_Signal`, `Turning_Loop`
- **Descriptive**: `Description`, `Street`, `Side`

**Data Quality Considerations**:
- Missing values in weather attributes
- Coordinate precision varies
- Severity is subjectively reported
- Temporal coverage varies by state

### 3.2 Secondary Dataset: OpenStreetMap Road Network

**Source**: OpenStreetMap (via `osmnx` Python library)

**Description**: Crowd-sourced global map data including road networks with attributes.

**Key Attributes**:
- **Geometry**: LineString geometries for road segments
- **Surface Types**: 
  - `paved`, `asphalt`, `concrete`
  - `unpaved`, `gravel`, `dirt`, `compacted`
  - `ground`, `fine_gravel`, `cobblestone`
- **Road Classification**: `highway` tag (motorway, trunk, primary, secondary, residential, etc.)
- **Road Name**: `name` attribute
- **Additional**: `lanes`, `maxspeed`, `oneway`

**Data Quality Considerations**:
- Surface attribute coverage is incomplete (~30-60% depending on region)
- Data quality varies by contributor activity
- Urban areas have better coverage than rural
- Temporal alignment: OSM reflects current state, not historical

## 4. Analytical Goals

### 4.1 Problem Type
**Hybrid**: Classification (severity prediction) and Exploratory Analysis

### 4.2 Target Variables
1. **Primary**: `Severity` (multi-class: 1, 2, 3, 4)
2. **Alternative**: Binary classification (severe vs. non-severe)
3. **Exploratory**: Accident occurrence rate by surface type

### 4.3 Feature Groups
- **Road Quality**: Surface type, road classification
- **Environmental**: Weather conditions, visibility, temperature
- **Temporal**: Hour, day of week, month, season
- **Infrastructure**: Presence of signals, crossings, junctions
- **Spatial**: Urban/rural classification, state/region

## 5. Ethical and Regulatory Considerations

### 5.1 Data Privacy
- **Anonymization**: Dataset contains no personally identifiable information (PII)
- **Aggregation**: Individual accidents cannot be linked to specific drivers
- **Location Data**: GPS coordinates are rounded to protect exact locations

### 5.2 Potential Biases
- **Reporting Bias**: Not all accidents are reported uniformly across jurisdictions
- **Geographic Bias**: Data overrepresents states with higher digital reporting systems
- **Temporal Bias**: Recent years have more comprehensive data
- **Socioeconomic Factors**: Road quality may correlate with neighborhood income levels

### 5.3 Fairness Considerations
- **Infrastructure Investment**: Findings should not perpetuate existing inequities in road maintenance
- **Blame Attribution**: Analysis focuses on infrastructure, not individual driver fault
- **Policy Implications**: Results should inform equitable resource allocation

### 5.4 Regulatory Compliance
- **Data Usage**: Kaggle dataset is publicly available for research under CC0: Public Domain
- **OSM Licensing**: OpenStreetMap data is under Open Database License (ODbL)
- **Academic Use**: Project complies with university research ethics guidelines

## 6. Data Integration Strategy

### 6.1 Integration Model
**Spatial Join**: Match accident points to nearest road segments

### 6.2 Technical Approach
1. Convert accident CSV to GeoDataFrame with Point geometries
2. Download OSM road networks for relevant geographic areas
3. Project both datasets to common projected CRS (EPSG:3857)
4. Use spatial indexing (R-tree) for efficient nearest neighbor search
5. Apply distance threshold (100 meters) for matching
6. Merge road attributes onto accident records

### 6.3 Handling Mismatches
- **No nearby road found**: Flag and exclude or assign "unknown" surface type
- **Multiple roads within threshold**: Select nearest by Euclidean distance
- **Missing surface attribute in OSM**: Create "unspecified" category

### 6.4 Data Model Schema

```
integrated_accidents_roads
├── accident_id (unique identifier)
├── latitude (decimal degrees)
├── longitude (decimal degrees)
├── start_time (datetime)
├── severity (integer 1-4)
├── weather_condition (categorical)
├── temperature (float)
├── visibility (float)
├── road_surface (categorical: asphalt, concrete, gravel, unpaved, unknown)
├── road_type (categorical: motorway, primary, residential, etc.)
├── distance_to_road (float, meters)
├── junction (boolean)
├── traffic_signal (boolean)
└── ... (additional features)
```

## 7. Machine Learning Methodology

### 7.1 Interpretable Models
**Purpose**: Provide transparent, explainable insights

1. **Logistic Regression**
   - Multi-class classification (severity)
   - Coefficients directly interpretable
   - Assess contribution of road surface features

2. **Decision Trees**
   - Visual rule-based interpretation
   - Feature importance rankings
   - Identify key decision thresholds

3. **Linear Regression** (if predicting continuous outcome like duration)

### 7.2 Black-Box Models
**Purpose**: Maximize predictive performance

1. **Random Forest**
   - Ensemble of decision trees
   - Feature importance via impurity reduction
   - Handles non-linear relationships

2. **XGBoost (Gradient Boosting)**
   - State-of-the-art performance
   - Handles imbalanced classes
   - Customizable loss functions

3. **Neural Networks** (optional, if sufficient data)
   - Deep learning for complex patterns
   - Requires careful hyperparameter tuning

### 7.3 Model Explainability
Even for black-box models, we employ:

- **SHAP (SHapley Additive exPlanations)**
  - Compute feature contribution for each prediction
  - Generate summary plots showing feature importance
  - Local explanations for individual accidents

- **LIME (Local Interpretable Model-agnostic Explanations)**
  - Approximate black-box predictions locally with interpretable models
  - Validate SHAP findings

### 7.4 Evaluation Strategy
- **Train/Validation/Test Split**: 70% / 15% / 15%
- **Stratification**: By severity class and geographic region
- **Cross-Validation**: 5-fold stratified CV
- **Metrics**:
  - Accuracy, Precision, Recall, F1-Score (per class)
  - ROC-AUC (one-vs-rest for multi-class)
  - Confusion Matrix
  - Feature Importance Rankings

## 8. Implementation Steps (9-Step Pipeline)

### Step 1: Data Loading and Preparation
- Load US Accidents CSV
- Create Point geometries from lat/lon
- Convert to GeoDataFrame (WGS84)
- **Deliverable**: `src/data/load_accidents.py`, `notebooks/01_data_loading_accidents.ipynb`

### Step 2: OSM Data Acquisition
- Use `osmnx` to download road networks
- Handle large geographic areas via segmentation (by state/city)
- Extract surface and highway type attributes
- **Deliverable**: `src/data/load_osm_data.py`, `notebooks/02_osm_data_acquisition.ipynb`

### Step 3: Spatial Join Operation
- Reproject to EPSG:3857 for accurate distance
- Build spatial index for roads
- Find nearest road for each accident
- Apply distance threshold (100m)
- **Deliverable**: `src/data/spatial_join.py`, `notebooks/03_spatial_join.ipynb`

### Step 4: Data Cleaning
- Handle missing road surface values
- Detect and remove duplicates
- Validate coordinate integrity
- Impute missing weather data
- **Deliverable**: `src/data/data_cleaning.py`, `notebooks/04_data_cleaning.ipynb`

### Step 5: Feature Engineering
- Encode categorical variables (one-hot, label encoding)
- Create temporal features (hour, day of week, season)
- Aggregate infrastructure features
- Normalize/scale continuous variables
- **Deliverable**: `src/features/feature_engineering.py`, `notebooks/06_feature_engineering.ipynb`

### Step 6: Exploratory Data Analysis
- Surface type distribution
- Severity by surface type
- Temporal patterns
- Geographic visualizations (choropleth maps)
- Correlation analysis
- **Deliverable**: `notebooks/05_eda.ipynb`, figures for paper

### Step 7: Model Development
- Implement train/test split
- Train interpretable models (Logistic Regression, Decision Tree)
- Train black-box models (Random Forest, XGBoost)
- Hyperparameter tuning (GridSearchCV, RandomizedSearchCV)
- **Deliverable**: `src/models/train.py`, `notebooks/07_model_development.ipynb`

### Step 8: Model Evaluation and Interpretation
- Compute evaluation metrics
- Generate confusion matrices
- Apply SHAP for feature importance
- Apply LIME for local explanations
- Compare interpretable vs. black-box performance
- **Deliverable**: `src/models/evaluate.py`, `notebooks/08_model_evaluation.ipynb`

### Step 9: Final Analysis and Reporting
- Synthesize findings
- Create publication-quality visualizations
- Answer research questions
- Discuss limitations and future work
- **Deliverable**: `notebooks/09_final_analysis.ipynb`, research paper sections

## 9. Success Criteria

### 9.1 Technical Criteria
- [ ] Successfully join >90% of accidents to road segments
- [ ] Achieve >75% classification accuracy for severity prediction
- [ ] Demonstrate statistically significant relationship between road quality and accidents
- [ ] Generate interpretable SHAP/LIME explanations
- [ ] Maintain >80% test coverage

### 9.2 Research Criteria
- [ ] Answer all research questions with data-driven evidence
- [ ] Produce 8-page research paper in ACM format
- [ ] Create presentation with clear visualizations
- [ ] Document methodology reproducibly
- [ ] Discuss ethical implications and limitations

### 9.3 Collaboration Criteria
- [ ] All team members contribute code (tracked in git)
- [ ] Maintain organized Git repository with clear commit history
- [ ] Document contribution hours in paper appendix
- [ ] Code passes CI/CD pipeline checks

## 10. Deliverables Checklist

### Code and Notebooks
- [ ] Fully functional data pipeline (`src/`)
- [ ] 10 Jupyter notebooks (00-09) with complete analysis
- [ ] Comprehensive test suite (`tests/`)
- [ ] Documentation (`docs/`)

### Research Paper (ACM Format, 8 pages)
- [ ] Abstract
- [ ] Introduction
- [ ] Related Work
- [ ] Data Description
- [ ] Methodology
- [ ] Results and Discussion
- [ ] Conclusions and Future Work
- [ ] References
- [ ] Appendices (data samples, contribution hours)

### Presentation
- [ ] Slide deck (15-20 minutes)
- [ ] Key visualizations and results
- [ ] Demo (optional)

### Repository
- [ ] Clean, organized Git history
- [ ] README with setup instructions
- [ ] Requirements and dependencies documented
- [ ] MIT License

## 11. Timeline and Milestones

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 1 | Project Setup | Repository, structure, documentation |
| 2-3 | Steps 1-3 | Data loading, OSM acquisition, spatial join |
| 4 | Step 4 | Data cleaning and validation |
| 5 | Steps 5-6 | Feature engineering and EDA |
| 6-7 | Step 7 | Model development and tuning |
| 8 | Step 8 | Model evaluation and interpretation |
| 9 | Step 9 | Final analysis and synthesis |
| 10 | Paper Writing | Complete research paper |
| 11 | Presentation | Prepare and rehearse presentation |
| 12 | Submission | Final deliverables and repository cleanup |

## 12. Risk Management

### Technical Risks
- **Data volume**: 7.6M records may exceed memory → **Mitigation**: Process by state/region
- **OSM coverage gaps**: Surface data incomplete → **Mitigation**: Create "unknown" category, analyze completeness
- **Spatial join performance**: Slow for large datasets → **Mitigation**: Use spatial indexing, parallel processing

### Research Risks
- **Weak correlations**: Road quality may not strongly predict accidents → **Mitigation**: Frame as exploratory study, consider alternative hypotheses
- **Confounding factors**: Many variables influence accidents → **Mitigation**: Use multivariate models, control for confounders

### Collaboration Risks
- **Unequal contributions**: Team members contribute unevenly → **Mitigation**: Regular check-ins, clear task assignments
- **Merge conflicts**: Concurrent git work → **Mitigation**: Feature branches, pull request reviews

## 13. References

1. Moosavi, Sobhan, et al. "A Countrywide Traffic Accident Dataset." arXiv:1906.05409 (2019).
2. Boeing, G. "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks." Computers, Environment and Urban Systems 65 (2017): 126-139.
3. OpenStreetMap contributors. (2023). OpenStreetMap. Retrieved from https://www.openstreetmap.org
4. Lundberg, S., & Lee, S. "A Unified Approach to Interpreting Model Predictions." NIPS 2017.

---

**Document Version**: 1.0  
**Last Updated**: November 5, 2025  
**Authors**: Project Team
