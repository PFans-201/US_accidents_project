"""
Configuration management for the US Accidents and Road Quality Analysis project.

This module centralizes all configuration parameters including paths, model hyperparameters,
and processing settings. Configuration can be overridden via environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration class for the project."""
    
    # ==================== Project Metadata ====================
    PROJECT_NAME = "us-accidents-road-quality"
    VERSION = "0.1.0"
    
    # ==================== Paths ====================
    # Base directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Raw data
    RAW_DATA_DIR = DATA_DIR / "raw"
    ACCIDENTS_RAW_DIR = RAW_DATA_DIR / "accidents_raw"
    OSM_RAW_DIR = RAW_DATA_DIR / "osm_raw"
    
    # Processed data
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    ACCIDENTS_CLEANED_DIR = PROCESSED_DATA_DIR / "accidents_cleaned"
    OSM_PROCESSED_DIR = PROCESSED_DATA_DIR / "osm_processed"
    
    # Integrated data
    INTEGRATED_DATA_DIR = DATA_DIR / "integrated"
    ACCIDENTS_WITH_ROAD_QUALITY_DIR = INTEGRATED_DATA_DIR / "accidents_with_road_quality"
    
    # Output directories
    MODELS_DIR = BASE_DIR / "models"
    FIGURES_DIR = BASE_DIR / "figures"
    LOGS_DIR = BASE_DIR / "logs"
    
    # US Accidents dataset path
    ACCIDENTS_CSV_PATH = os.getenv(
        "ACCIDENTS_CSV_PATH",
        str(ACCIDENTS_RAW_DIR / "US_Accidents_March23.csv")
    )
    
    # ==================== Coordinate Reference Systems ====================
    WGS84_EPSG = 4326          # Standard lat/lon
    WEB_MERCATOR_EPSG = 3857   # Meters-based for distance calculations
    
    # ==================== Spatial Join Configuration ====================
    SPATIAL_JOIN_METHOD = os.getenv("SPATIAL_JOIN_METHOD", "nearest")
    MAX_DISTANCE_METERS = float(os.getenv("MAX_DISTANCE_METERS", 100.0))
    
    # ==================== OpenStreetMap Configuration ====================
    OSM_CACHE_DIR = OSM_RAW_DIR
    OSM_USE_CACHE = os.getenv("OSM_USE_CACHE", "True").lower() == "true"
    OSM_NETWORK_TYPE = "drive"  # Options: 'all', 'drive', 'bike', 'walk'
    
    # States to process (if segmenting by state)
    STATES = os.getenv("STATES", "").split(",") if os.getenv("STATES") else None
    CITIES = os.getenv("CITIES", "").split(",") if os.getenv("CITIES") else None
    
    # ==================== Data Processing ====================
    # Chunk size for processing large datasets
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 100000))
    
    # Missing value strategies
    MISSING_VALUE_STRATEGIES = {
        "Temperature(F)": "median",
        "Visibility(mi)": "median",
        "Humidity(%)": "median",
        "Weather_Condition": "mode",
        "road_surface": "unknown",
        "Zipcode": "keep_missing"
    }
    
    # Outlier detection
    OUTLIER_IQR_FACTOR = 3.0
    
    # ==================== Feature Engineering ====================
    # Categorical encoding methods
    ONEHOT_ENCODING_FEATURES = ["Weather_Condition", "road_surface", "highway"]
    LABEL_ENCODING_FEATURES = ["State", "County"]
    
    # Feature scaling
    FEATURES_TO_SCALE = ["Temperature(F)", "Visibility(mi)", "Humidity(%)", 
                         "Pressure(in)", "Wind_Speed(mph)", "distance_to_road"]
    
    # ==================== Model Training ====================
    # Random seed for reproducibility
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))
    
    # Train/validation/test split
    TEST_SIZE = float(os.getenv("TEST_SIZE", 0.15))
    VALIDATION_SIZE = float(os.getenv("VALIDATION_SIZE", 0.15))
    
    # Cross-validation
    N_FOLDS = int(os.getenv("N_FOLDS", 5))
    
    # Target variable
    TARGET_VARIABLE = "Severity"
    BINARY_SEVERITY_THRESHOLD = 2  # Severity > 2 is considered severe
    
    # ==================== Model Hyperparameters ====================
    # Logistic Regression
    LR_MAX_ITER = 1000
    LR_CLASS_WEIGHT = "balanced"
    
    # Decision Tree
    DT_MAX_DEPTH = 10
    DT_MIN_SAMPLES_SPLIT = 100
    DT_MIN_SAMPLES_LEAF = 50
    DT_CLASS_WEIGHT = "balanced"
    
    # Random Forest
    RF_N_ESTIMATORS = int(os.getenv("RF_N_ESTIMATORS", 100))
    RF_MAX_DEPTH = 15
    RF_MIN_SAMPLES_SPLIT = 50
    RF_MIN_SAMPLES_LEAF = 20
    RF_CLASS_WEIGHT = "balanced"
    RF_N_JOBS = int(os.getenv("N_JOBS", -1))  # -1 uses all cores
    
    # XGBoost
    XGBOOST_N_ESTIMATORS = int(os.getenv("XGBOOST_N_ESTIMATORS", 100))
    XGBOOST_MAX_DEPTH = int(os.getenv("XGBOOST_MAX_DEPTH", 6))
    XGBOOST_LEARNING_RATE = float(os.getenv("XGBOOST_LEARNING_RATE", 0.1))
    XGBOOST_SUBSAMPLE = 0.8
    XGBOOST_COLSAMPLE_BYTREE = 0.8
    
    # ==================== Model Interpretation ====================
    # SHAP configuration
    SHAP_N_SAMPLES = 1000  # Number of samples for SHAP explanation
    SHAP_CHECK_ADDITIVITY = False  # Speed up computation
    
    # LIME configuration
    LIME_N_FEATURES = 10
    LIME_N_SAMPLES = 5000
    
    # ==================== Logging ====================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / "pipeline.log"
    
    # ==================== Visualization ====================
    FIGURE_DPI = int(os.getenv("FIGURE_DPI", 300))
    FIGURE_FORMAT = os.getenv("FIGURE_FORMAT", "png")
    FIGURE_SIZE_DEFAULT = (12, 8)
    
    # Matplotlib style
    PLOT_STYLE = "seaborn-v0_8-darkgrid"
    
    # ==================== API Keys (if needed) ====================
    MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", None)
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", None)
    
    # ==================== Performance ====================
    N_JOBS = int(os.getenv("N_JOBS", -1))  # Number of parallel jobs
    MEMORY_LIMIT_GB = int(os.getenv("MEMORY_LIMIT_GB", 16))
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories if they don't exist."""
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.ACCIDENTS_RAW_DIR,
            cls.OSM_RAW_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.ACCIDENTS_CLEANED_DIR,
            cls.OSM_PROCESSED_DIR,
            cls.INTEGRATED_DATA_DIR,
            cls.ACCIDENTS_WITH_ROAD_QUALITY_DIR,
            cls.MODELS_DIR,
            cls.FIGURES_DIR,
            cls.LOGS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """
        Get a summary of key configuration parameters.
        
        Returns:
            dict: Dictionary of configuration parameters
        """
        return {
            "project_name": cls.PROJECT_NAME,
            "version": cls.VERSION,
            "accidents_csv_path": cls.ACCIDENTS_CSV_PATH,
            "max_distance_meters": cls.MAX_DISTANCE_METERS,
            "random_seed": cls.RANDOM_SEED,
            "test_size": cls.TEST_SIZE,
            "validation_size": cls.VALIDATION_SIZE,
            "n_folds": cls.N_FOLDS,
            "xgboost_n_estimators": cls.XGBOOST_N_ESTIMATORS,
            "xgboost_max_depth": cls.XGBOOST_MAX_DEPTH,
            "xgboost_learning_rate": cls.XGBOOST_LEARNING_RATE,
            "log_level": cls.LOG_LEVEL
        }


# Create directories on module import
Config.create_directories()
