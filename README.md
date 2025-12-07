# Predicting Substance-Based Impairment in Fatal US Traffic Accidents

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A data science pipeline analyzing the **Fatal Accident Reporting System (FARS)** to model and predict the likelihood of alcohol and drug impairment in fatal crashes.

## 🎯 Project Overview

This project analyzes fatal traffic accident data (2018–2023) to identify the causal factors and predictors associated with driver impairment. Unlike standard classification tasks, this pipeline employs a sophisticated feature engineering and selection strategy to handle high-cardinality categorical data and uncover structural dependencies between variables.

**Key Objectives:**
1.  **Harmonize** multi-year FARS datasets (Accident, Person, Drugs).
2.  **Engineer** robust features using probabilistic methods (Gaussian Mixture Models for age, Harmonic encoding for time).
3.  **Select** the most predictive features using a hybrid approach of **Lasso Regularization** and **Bayesian Structure Learning (Markov Blankets)**.
4.  **Predict** impairment (Alcohol, Drugs, or Both) using interpretable (Logistic Regression) and high-performance (XGBoost/Random Forest) models.

## 🔬 Methodology & Pipeline

The project is structured into a sequential data science pipeline:

### 1. Data Ingestion & Cleaning
- **Source:** NHTSA FARS Data (2018, 2019, 2022, 2023).
- **Harmonization:** Standardizing column definitions across years (e.g., `DRUGRES` codes).
- **Imputation:** 
  - **Smart Imputation:** Random Forest classifier to impute `LGT_COND` based on time/location.
  - **Probabilistic Imputation:** GMM for missing `AGE` values.

### 2. Advanced Feature Engineering
- **Harmonic Time Features:** Sine/Cosine transformations for `HOUR`, `MONTH`, and `DAY` to preserve cyclical nature.
- **Age Clustering:** Using **Gaussian Mixture Models (GMM)** with BIC scoring to automatically identify and group demographic clusters.
- **Harm Indices:** Custom metrics for crash severity (e.g., Vulnerability Index for non-occupants).

### 3. Feature Selection Strategy
- **Encoding:** Hybrid strategy using **One-Hot Encoding** for low-cardinality and **Weight of Evidence (WOE)** for high-cardinality features (e.g., `STATENAME`).
- **Dimensionality Reduction:** **L1-Regularized Logistic Regression (Lasso)** to shrink irrelevant coefficients.
- **Causal Discovery:** **Bayesian Structure Learning** (Hill Climb Search) to identify the **Markov Blanket** of the target variable, isolating the minimal set of statistically relevant features.

### 4. Modeling
- **Targets:** `ALC_USE`, `DRUG_USE`, `ALC_&_DRUG_USE` (Co-occurrence).
- **Models:** 
  - **Logistic Regression:** For interpretability and baseline performance.
  - **XGBoost / Random Forest:** For capturing non-linear relationships.
- **Evaluation:** ROC-AUC, Precision-Recall, and Confusion Matrices.

## 📂 Project Structure

```text
.
├── data/
│   ├── raw/                 # Original FARS CSV files
│   ├── interim/             # Merged and harmonized datasets
│   └── processed/           # Final Parquet files for modeling
├── docs/                    # Documentation and references
├── EDA_reports/             # Generated HTML profiles and plots
│   ├── Structure_learning/  # Bayesian Network visualizations
│   └── Time_series_analysis/# Plots and insights on temporal trends
├── FDS_G5_PROJECT.ipynb     # Main pipeline notebook
├── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Graphviz (Required for Bayesian Network visualization)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PFans-201/US_accidents_project.git
   cd US_accidents_project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install System Dependencies (Graphviz)**:
   *Required for `pygraphviz` to visualize Bayesian Networks.*
   *   **Ubuntu/Debian:** `sudo apt-get install graphviz graphviz-dev`
   *   **MacOS:** `brew install graphviz`
   *   **Windows:** Download installer from Graphviz website.

4. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Quick Start

1.  **Data Setup:** Download FARS data (Accident, Person, Drugs) for desired years and place them in `data/raw/`.
2.  **Run Pipeline:** Open `FDS_G5_PROJECT.ipynb` to execute the full end-to-end pipeline.
3.  **View Reports:** Check `EDA_reports/` for automated data profiling and time-series analysis.

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Note**: This is an academic research project for educational purposes. Results and insights are exploratory and should not be used as the sole basis for policy or infrastructure decisions.