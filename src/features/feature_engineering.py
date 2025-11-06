"""
Feature engineering module.

Creates derived features from raw accident and road data.
"""

import logging
import pandas as pd
import geopandas as gpd
from typing import Tuple, List

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def engineer_features(gdf: gpd.GeoDataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Engineer features for machine learning models.
    
    Args:
        gdf: GeoDataFrame with integrated accident-road data
    
    Returns:
        Tuple of (features DataFrame, list of feature names)
    
    Example:
        >>> features_df, feature_names = engineer_features(clean_gdf)
        >>> print(f"Created {len(feature_names)} features")
    """
    logger.info("Starting feature engineering...")
    
    df = gdf.copy()
    
    # Create temporal features
    df = create_temporal_features(df)
    
    # Create categorical encodings
    df = encode_categorical_features(df)
    
    # Create interaction features
    df = create_interaction_features(df)
    
    # Extract feature columns (exclude target and metadata)
    exclude_cols = ['Severity', 'ID', 'geometry', 'index_right']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    logger.info(f"Feature engineering complete. Created {len(feature_cols)} features")
    
    return df[feature_cols], feature_cols


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features."""
    if 'Start_Time' in df.columns:
        df['hour'] = df['Start_Time'].dt.hour
        df['day_of_week'] = df['Start_Time'].dt.dayofweek
        df['month'] = df['Start_Time'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        # Rush hour indicator could be useful but perhaps not hardcoded
        df['rush_hour'] = df['hour'].isin([7, 8, 9, 16, 17, 18]).astype(int)
    
    return df


def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical variables."""
    # One-hot encoding for nominal categories
    for col in ['road_surface', 'Weather_Condition']:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df, dummies], axis=1)
    
    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create interaction features."""
    # Example: surface x weather interaction
    if 'road_surface' in df.columns and 'Weather_Condition' in df.columns:
        df['surface_weather'] = df['road_surface'] + '_' + df['Weather_Condition']
    
    return df


if __name__ == "__main__":
    logger.info("Feature engineering module loaded")
