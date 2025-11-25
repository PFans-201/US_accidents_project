"""
Configuration management for the US Accidents and Road Quality Analysis project.

This module centralizes all configuration parameters including paths, model hyperparameters,
and processing settings. Configuration can be overridden via environment variables.
"""
from pathlib import Path

class Config:
    """Central configuration class for the project."""
    
    # ==================== Project Metadata ====================
    PROJECT_NAME = "fars-fatal-accidents"
    VERSION = "0.1.0"
    
    # ==================== Paths ====================
    # Base directories
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    
    # Raw data
    RAW_DATA_DIR = DATA_DIR / "raw"
    FARS_RAW_DIR = RAW_DATA_DIR / "fars"
    
    # Processed data
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    FARS_CLEANED_DIR = PROCESSED_DATA_DIR / "fars"
    
    # US Accidents dataset path
    FARS_ACCIDENTS_CSV_PATH = f"{FARS_RAW_DIR}/accidents.csv"
    FARS_PERSON_CSV_PATH = f"{FARS_RAW_DIR}/person.csv"
    FARS_DRUGS_CSV_PATH = f"{FARS_RAW_DIR}/drugs.csv"
    
    # ==================== Model Training ====================
    # Random seed for reproducibility
    RANDOM_SEED = 42
    
    # ==================== Visualization ====================
    FIGURE_DPI = 300
    FIGURE_FORMAT = "png"
    FIGURE_SIZE_DEFAULT = 8
    
    # Matplotlib style
    PLOT_STYLE = "seaborn-v0_8-darkgrid"

