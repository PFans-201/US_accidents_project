# Predicting the likelihood of substance-based impairment in people involved in (fatal) car accidents in the USA

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Project for analyzing and predicting the likelihood that an individual involved in a fatal car accident was impaired in any way by substances that alter driving ability

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
- Analyze the dataset to determine the most important variables
- Train a predictive model to predict when it is likely that a driver/other individual involved in an accident is under the influence of drugs and/or alcohol

## 📊 Datasets

### Primary source: FARS (eg.: 2023)
- **Source**: [FARS 2023](https://static.nhtsa.gov/nhtsa/downloads/FARS/2023/National/FARS2023NationalCSV.zip)

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
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
pip install -e .
```
4. **Download the FARS datasets**:
Download the FARS datasets zip file from the above source, unzip it, and place **accident.csv**, **drugs.csv**, and **person.csv** in **data/raw/**

## ⚡ Quick Start

1. Download the Data and place it in the correct directories
2. Run Jupyter Notebooks

## 🤝 Contributing

### Development Process
1. Clone the repository
2. Create a feature branch: `feature/03-your-feature`
3. Commit changes with a descriptive commit message, and push
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
