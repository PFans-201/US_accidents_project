# Predicting the likelihood of substance-based impairment in people involved in (fatal) car accidents in the USA

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> This project analyzes the **Fatal Accident Reporting System (FARS)** dataset to **model and predict** the factors contributing to **fatal traffic accidents involving alcohol and/or drug impairment**. The pipeline employs a sophisticated feature engineering strategy, including Gaussian Mixture Models (GMM) for age grouping, WOE encoding for categorical data, and a multi-stage feature selection process (Lasso regression and Bayesian Structure Learning) to identify the minimal set of highly predictive variables for impairment risk. The ultimate goal is to build the following predictive models to estimate the > This project analyzes the **Fatal Accident Reporting System (FARS)** dataset to **model and predict** the factors contributing to **fatal traffic accidents involving alcohol and/or drug impairment**. The pipeline employs a sophisticated feature engineering strategy, including Gaussian Mixture Models (GMM) for age grouping, WOE encoding for categorical data, and a multi-stage feature selection process (Lasso regression and Bayesian Structure Learning) to identify the minimal set of highly predictive variables for impairment risk. The ultimate goal is to build the following predictive models to estimate the probability of this susbtance involvment in said fatalities: Logistic Regression model as our explainable and interpretable model; and a Randmom Forest model as our black-box, possibly more accurate model.
## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Datasets](#datasets)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

This project combines multiple datasets from the Fatality Analysis Reporting System. The datasets contain information about fatal traffic accidents, the individuals involved, and any illicit/controlled substances or lack thereof detected in the aforementioned individuals.

1. **FARS accident dataset** - Fatal traffic accidents recorded in the FARS
2. **FARS person dataset** - All the individuals involved in the above dataset
3. **FARS accident dataset** - All the results for illicit/controlled substance tests or lack thereof in the above individuals

### Key Objectives
- Combine the desired information from the above datasets into one dataset
- Analyze the dataset to determine the most important uncorrelated variables
- Train a predictive model to predict when it is likely that a driver/other individual involved in an accident is likely to be under the influence of illicit/controlled substances

## 📊 Datasets

### Primary source: FARS (2023)
- **Source**: [FARS 2023](https://static.nhtsa.gov/nhtsa/downloads/FARS/2023/National/FARS2023NationalCSV.zip)

**Dataset sizes**:
- **Accidents**: ~37500 records 
- **Persons**: ~92500 records 
- **Drug test data**: ~130000 records 

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git
- (Recommended) Virtual environment tool

### Python Environment Setup
1. **Clone the repository**:
```bash
git clone https://github.com/PFans-201/US_accidents_project.git
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# to use pygraphviz, you might need to install graphviz system package
# On Ubuntu/Debian:
sudo apt-get install graphviz graphviz-dev
# On arch-based Linux:
sudo pacman -S graphviz
# On macOS using Homebrew:
brew install graphviz

# be sure to use a python envrironment that can access the system packages correctely!
```
**Note:** pyhraphviz installation can be tricky on some systems, and this package is only required for the Bayesian Network visualization, so if you face issues, you can skip it.

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```
1. **Download the FARS datasets**:
Download the FARS datasets zip file from the above source, unzip it, and place **accident.csv**, **drugs.csv**, and **person.csv** in **data/raw/fars**

## ⚡ Quick Start

1. Download the Data and place it in the correct directories
2. Run Jupyter Notebooks

## 🤝 Contributing

### Development Process
1. Clone the repository
2. Create a  branch: `student_name/feature_description`
3. Commit changes with a descriptive commit message, and push
4. Submit a pull request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or collaboration inquiries, please open an issue or contact the project maintainers.

---

**Note**: This is an academic research project for educational purposes. Results and insights are exploratory and should not be used as the sole basis for policy or infrastructure decisions.
