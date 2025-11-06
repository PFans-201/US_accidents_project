# Methodology: US Accidents and Road Quality Analysis

## Table of Contents
1. [Research Design](#1-research-design)
2. [Data Collection](#2-data-collection)
3. [Data Integration](#3-data-integration)
4. [Data Preprocessing](#4-data-preprocessing)
5. [Exploratory Data Analysis](#5-exploratory-data-analysis)
6. [Feature Engineering](#6-feature-engineering)
7. [Machine Learning Methodology](#7-machine-learning-methodology)
8. [Model Interpretation](#8-model-interpretation)
9. [Evaluation Framework](#9-evaluation-framework)
10. [Reproducibility](#10-reproducibility)

---

## 1. Research Design

### 1.1 Study Type
**Cross-sectional observational study** analyzing the relationship between road surface quality and traffic accident patterns.

### 1.2 Research Framework
```
Research Question
    ↓
Data Acquisition (US Accidents + OSM)
    ↓
Spatial Integration
    ↓
Exploratory Analysis
    ↓
Hypothesis Testing
    ↓
Predictive Modeling
    ↓
Model Interpretation
    ↓
Conclusions & Recommendations
```

### 1.3 Hypotheses

**H1**: Road surface quality significantly influences accident severity
- Null: No relationship between surface type and severity
- Alternative: Poor surfaces (unpaved, gravel) associated with higher severity

**H2**: Surface type interacts with environmental factors
- Test interaction effects between surface and weather conditions

**H3**: Road quality features improve predictive model performance
- Compare models with/without road quality features

---

## 2. Data Collection

### 2.1 Primary Data Source: US Accidents

**Collection Method**: 
- Downloaded from Kaggle: `US_Accidents_March23.csv`
- Original data collected via traffic APIs (MapQuest, Bing) and law enforcement feeds

**Sample Selection**:
- Population: All reported traffic accidents in contiguous US (2016-2023)
- Sampling: Complete dataset (census, not sample)
- Geographic coverage: 49 states (excludes Hawaii)

**Data Limitations**:
- Reporting bias: Varies by jurisdiction
- Temporal completeness: Better in recent years
- No personal identifiers or driver characteristics

### 2.2 Secondary Data Source: OpenStreetMap

**Collection Method**:
```python
import osmnx as ox

# Download road network for a city
G = ox.graph_from_place(
    "Los Angeles, California, USA",
    network_type="drive",
    simplify=True
)

# Convert to GeoDataFrame with attributes
roads_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
```

**Attributes Extracted**:
- `surface`: Road surface material
- `highway`: Road classification
- `geometry`: Road segment geometries

**Handling Large Regions**:
- Process by state or county to manage data volume
- Use caching to avoid repeated API calls
- Respect OSM usage policies

---

## 3. Data Integration

### 3.1 Spatial Join Strategy

**Problem**: Match point-based accidents to linear road segments

**Solution**: Nearest neighbor spatial join with distance threshold

**Implementation**:
```python
# 1. Create geometries
accidents_gdf = gpd.GeoDataFrame(
    accidents_df,
    geometry=gpd.points_from_xy(accidents_df.Start_Lng, accidents_df.Start_Lat),
    crs="EPSG:4326"  # WGS84
)

# 2. Reproject to meters-based CRS for accurate distance
accidents_proj = accidents_gdf.to_crs("EPSG:3857")
roads_proj = roads_gdf.to_crs("EPSG:3857")

# 3. Spatial join with distance threshold
from shapely.ops import nearest_points
# Find nearest road within 100m
joined = gpd.sjoin_nearest(
    accidents_proj,
    roads_proj,
    max_distance=100,
    how="left"
)
```

**Coordinate Reference Systems**:
- Input: WGS84 (EPSG:4326) - decimal degrees
- Processing: Web Mercator (EPSG:3857) - meters
- Output: WGS84 for visualization

### 3.2 Distance Threshold Justification

**Threshold**: 100 meters

**Rationale**:
- GPS accuracy: ±10-50 meters typical
- Road width: Major roads 10-30 meters
- Positional uncertainty in accident reporting
- Balance: Too small → many unmatched; Too large → wrong road matches

**Sensitivity Analysis**:
Test thresholds: 50m, 75m, 100m, 150m, 200m

### 3.3 Handling Edge Cases

| Scenario | Handling Strategy |
|----------|-------------------|
| No road within threshold | Assign `road_surface = 'unknown'`, flag for exclusion |
| Multiple roads within threshold | Select nearest by Euclidean distance |
| Missing surface attribute in OSM | Assign `'unspecified'` category |
| Accident on highway ramp | Match to ramp if closer than mainline |

---

## 4. Data Preprocessing

### 4.1 Data Cleaning Steps

**1. Remove Invalid Coordinates**:
```python
# Remove records outside contiguous US
accidents = accidents[
    (accidents['Start_Lat'].between(24.5, 49.4)) &
    (accidents['Start_Lng'].between(-125, -66))
]
```

**2. Handle Missing Values**:
```python
# Strategy by variable type
missing_strategies = {
    'Temperature(F)': 'median',
    'Visibility(mi)': 'median',
    'Weather_Condition': 'mode',
    'road_surface': 'keep_as_unknown',
    'Zipcode': 'keep_missing'
}
```

**3. Remove Duplicates**:
```python
# Duplicates defined as same location, time, severity
duplicates = accidents.duplicated(subset=['Start_Lat', 'Start_Lng', 'Start_Time', 'Severity'])
accidents = accidents[~duplicates]
```

**4. Validate Data Types**:
```python
# Ensure correct types
accidents['Start_Time'] = pd.to_datetime(accidents['Start_Time'])
accidents['Severity'] = accidents['Severity'].astype(int)
accidents['Junction'] = accidents['Junction'].astype(bool)
```

### 4.2 Outlier Detection

**Method**: Interquartile Range (IQR) for continuous variables

```python
def remove_outliers(df, column, factor=3.0):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]
```

**Applied to**:
- `Temperature(F)`: Remove extreme values outside plausible range
- `Visibility(mi)`: Cap at reasonable maximum
- `Distance(mi)`: Remove accidents spanning unrealistic distances

### 4.3 Data Quality Report

Generate automated report:
```python
# Missing value summary
missing_summary = accidents.isnull().sum() / len(accidents) * 100

# Data type validation
type_check = accidents.dtypes

# Summary statistics
stats_summary = accidents.describe(include='all')
```

---

## 5. Exploratory Data Analysis

### 5.1 Univariate Analysis

**Continuous Variables**:
- Histograms and density plots
- Summary statistics (mean, median, std, quantiles)
- Identify skewness and kurtosis

**Categorical Variables**:
- Frequency tables
- Bar charts
- Chi-square goodness-of-fit tests

**Key Variables**:
- Severity distribution
- Road surface type distribution
- Weather condition distribution
- Temporal patterns (hour, day, month)

### 5.2 Bivariate Analysis

**Severity vs. Road Surface**:
```python
# Crosstab with chi-square test
ct = pd.crosstab(data['road_surface'], data['Severity'])
chi2, p_value, dof, expected = chi2_contingency(ct)

# Visualize
sns.heatmap(ct, annot=True, fmt='d', cmap='YlOrRd')
```

**Severity vs. Weather**:
```python
# Boxplot
sns.boxplot(x='Weather_Condition', y='Temperature', hue='Severity', data=data)
```

### 5.3 Multivariate Analysis

**Correlation Matrix**:
```python
# Select numeric features
numeric_features = data.select_dtypes(include=[np.number])
corr_matrix = numeric_features.corr()

# Visualize
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
```

**Principal Component Analysis** (optional):
- Dimensionality reduction for visualization
- Identify dominant variance patterns

### 5.4 Geographic Analysis

**Choropleth Maps**:
```python
import folium

# Accident frequency by state
state_counts = data.groupby('State').size().reset_index(name='count')

# Create map
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
folium.Choropleth(
    geo_data=us_states_geojson,
    data=state_counts,
    columns=['State', 'count'],
    key_on='feature.properties.state_code',
    fill_color='YlOrRd',
    legend_name='Accident Count'
).add_to(m)
```

**Hotspot Analysis**:
- Kernel density estimation of accident locations
- Identify high-risk corridors

---

## 6. Feature Engineering

### 6.1 Temporal Features

```python
# Extract time components
data['hour'] = data['Start_Time'].dt.hour
data['day_of_week'] = data['Start_Time'].dt.dayofweek
data['month'] = data['Start_Time'].dt.month
data['year'] = data['Start_Time'].dt.year

# Derived features
data['is_weekend'] = data['day_of_week'].isin([5, 6])
data['season'] = data['month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Fall', 10: 'Fall', 11: 'Fall'
})
data['rush_hour'] = data['hour'].isin([7, 8, 9, 16, 17, 18, 19])
```

### 6.2 Categorical Encoding

**One-Hot Encoding** (for non-ordinal):
```python
# Weather condition
weather_dummies = pd.get_dummies(data['Weather_Condition'], prefix='weather')

# Road surface
surface_dummies = pd.get_dummies(data['road_surface'], prefix='surface')
```

**Ordinal Encoding** (for ordered categories):
```python
# Highway type (ordered by traffic volume)
highway_order = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'residential']
data['highway_encoded'] = data['highway'].map({v: i for i, v in enumerate(highway_order)})
```

**Label Encoding** (for tree-based models):
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['state_encoded'] = le.fit_transform(data['State'])
```

### 6.3 Feature Scaling

**Standardization** (for linear models):
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[['Temperature(F)', 'Visibility(mi)', 'Humidity(%)']])
```

**Normalization** (if needed):
```python
from sklearn.preprocessing import MinMaxScaler

normalizer = MinMaxScaler()
normalized = normalizer.fit_transform(data[numeric_columns])
```

### 6.4 Interaction Features

```python
# Surface-weather interactions
data['surface_weather'] = data['road_surface'] + '_' + data['weather_category']

# Surface-time interactions
data['surface_night'] = data['road_surface'] + '_' + data['Sunrise_Sunset']
```

---

## 7. Machine Learning Methodology

### 7.1 Problem Formulation

**Task**: Multi-class classification

**Input**: Feature vector $X = [x_1, x_2, ..., x_n]$

**Output**: Severity class $y \in \{1, 2, 3, 4\}$

**Alternative**: Binary classification (severe vs. non-severe)

### 7.2 Train/Validation/Test Split

**Strategy**: Stratified split to maintain class balance

```python
from sklearn.model_selection import train_test_split

# Initial split: 70% train, 30% temp
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# Split temp into validation (15%) and test (15%)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)
```

**Rationale**:
- Train: Model learning
- Validation: Hyperparameter tuning
- Test: Final unbiased evaluation

### 7.3 Handling Class Imbalance

**Check Imbalance**:
```python
print(y_train.value_counts(normalize=True))
```

**Strategies**:
1. **Class Weights**: Assign higher weights to minority classes
   ```python
   from sklearn.utils.class_weight import compute_class_weight
   class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
   ```

2. **SMOTE** (Synthetic Minority Over-sampling):
   ```python
   from imblearn.over_sampling import SMOTE
   smote = SMOTE(random_state=42)
   X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
   ```

3. **Stratified Sampling**: Already applied in split

### 7.4 Model Selection

#### Interpretable Models

**1. Logistic Regression**
```python
from sklearn.linear_model import LogisticRegression

lr_model = LogisticRegression(
    multi_class='multinomial',
    class_weight='balanced',
    max_iter=1000,
    random_state=42
)
lr_model.fit(X_train, y_train)
```

**Advantages**: Coefficients directly interpretable, fast training

**2. Decision Tree**
```python
from sklearn.tree import DecisionTreeClassifier

dt_model = DecisionTreeClassifier(
    max_depth=10,
    min_samples_split=100,
    min_samples_leaf=50,
    class_weight='balanced',
    random_state=42
)
dt_model.fit(X_train, y_train)
```

**Advantages**: Visual interpretation, handles non-linearity

#### Black-Box Models

**1. Random Forest**
```python
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=50,
    class_weight='balanced',
    n_jobs=-1,
    random_state=42
)
rf_model.fit(X_train, y_train)
```

**Advantages**: High performance, robust to overfitting

**2. XGBoost**
```python
import xgboost as xgb

xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='mlogloss'
)
xgb_model.fit(X_train, y_train)
```

**Advantages**: Best-in-class performance, handles missing data

### 7.5 Hyperparameter Tuning

**Grid Search** (exhaustive):
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.01, 0.1, 0.3]
}

grid_search = GridSearchCV(
    xgb.XGBClassifier(),
    param_grid,
    cv=5,
    scoring='f1_macro',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

**Randomized Search** (faster):
```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'n_estimators': [50, 100, 150, 200],
    'max_depth': [3, 5, 7, 10, 15],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3]
}

random_search = RandomizedSearchCV(
    xgb.XGBClassifier(),
    param_dist,
    n_iter=20,
    cv=5,
    scoring='f1_macro',
    random_state=42,
    n_jobs=-1
)
random_search.fit(X_train, y_train)
```

### 7.6 Cross-Validation

**K-Fold Cross-Validation** (k=5):
```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=5,
    scoring='f1_macro'
)
print(f"CV F1-Score: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

---

## 8. Model Interpretation

### 8.1 Feature Importance (Tree-Based Models)

```python
# Get feature importances
importances = rf_model.feature_importances_
feature_names = X_train.columns

# Sort and visualize
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10, 6))
plt.bar(range(20), importances[indices][:20])
plt.xticks(range(20), feature_names[indices][:20], rotation=90)
plt.title("Top 20 Feature Importances")
plt.show()
```

### 8.2 SHAP (SHapley Additive exPlanations)

```python
import shap

# Create explainer
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test)

# Summary plot (global)
shap.summary_plot(shap_values, X_test, plot_type="bar")

# Detailed summary plot
shap.summary_plot(shap_values, X_test)

# Individual prediction explanation
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

**Interpretation**:
- Positive SHAP: Feature increases prediction towards higher severity
- Negative SHAP: Feature decreases severity prediction
- Magnitude: Importance of feature for that prediction

### 8.3 LIME (Local Interpretable Model-agnostic Explanations)

```python
from lime.lime_tabular import LimeTabularExplainer

# Create explainer
lime_explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=X_train.columns,
    class_names=['Severity_1', 'Severity_2', 'Severity_3', 'Severity_4'],
    mode='classification'
)

# Explain a prediction
i = 0  # Index of instance to explain
lime_exp = lime_explainer.explain_instance(
    X_test.iloc[i].values,
    xgb_model.predict_proba,
    num_features=10
)
lime_exp.show_in_notebook()
```

---

## 9. Evaluation Framework

### 9.1 Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

# Predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')
recall = recall_score(y_test, y_pred, average='macro')
f1 = f1_score(y_test, y_pred, average='macro')

# Multi-class ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='macro')

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-Score: {f1:.3f}")
print(f"ROC-AUC: {roc_auc:.3f}")
```

### 9.2 Confusion Matrix

```python
cm = confusion_matrix(y_test, y_pred)

# Visualize
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Sev 1', 'Sev 2', 'Sev 3', 'Sev 4'],
            yticklabels=['Sev 1', 'Sev 2', 'Sev 3', 'Sev 4'])
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.title('Confusion Matrix')
```

### 9.3 Model Comparison

```python
models = {
    'Logistic Regression': lr_model,
    'Decision Tree': dt_model,
    'Random Forest': rf_model,
    'XGBoost': xgb_model
}

results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    results.append({
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'F1-Score': f1_score(y_test, y_pred, average='macro'),
        'Precision': precision_score(y_test, y_pred, average='macro'),
        'Recall': recall_score(y_test, y_pred, average='macro')
    })

results_df = pd.DataFrame(results)
print(results_df)
```

---

## 10. Reproducibility

### 10.1 Random Seeds

Set seeds for all stochastic processes:
```python
import random
import numpy as np
import tensorflow as tf

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
```

### 10.2 Environment Management

Document all dependencies:
```bash
pip freeze > requirements.txt
```

### 10.3 Version Control

Commit all code changes with descriptive messages:
```bash
git add .
git commit -m "[STEP-3] Implement spatial join with 100m threshold"
git push origin feature/03-spatial-join
```

### 10.4 Documentation

- Docstrings for all functions
- README with setup instructions
- Methodology document (this file)
- Data dictionary

---

**Document Version**: 1.0  
**Last Updated**: November 5, 2025
