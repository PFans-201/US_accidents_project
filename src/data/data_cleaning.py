"""
Data cleaning and validation module.

Handles missing values, duplicates, outliers, and data validation.
"""

import logging
from typing import Optional, Dict
import pandas as pd
import geopandas as gpd

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def clean_data(
    gdf: gpd.GeoDataFrame,
    missing_strategies: Optional[Dict[str, str]] = None,
    remove_outliers: bool = True,
    outlier_columns: Optional[list] = None
) -> gpd.GeoDataFrame:
    """
    Clean and validate the integrated accident-road dataset.
    
    Args:
        gdf: GeoDataFrame to clean
        missing_strategies: Dictionary mapping column names to strategies
        remove_outliers: Whether to remove outliers
        outlier_columns: Columns to check for outliers
    
    Returns:
        Cleaned GeoDataFrame
    
    Example:
        >>> joined = spatial_join_accidents_roads(accidents, roads)
        >>> clean_gdf = clean_data(joined)
    """
    logger.info(f"Starting data cleaning. Input: {len(gdf):,} records")
    
    original_count = len(gdf)
    gdf = gdf.copy()
    
    # Handle missing values
    if missing_strategies is None:
        missing_strategies = Config.MISSING_VALUE_STRATEGIES
    
    gdf = handle_missing_values(gdf, missing_strategies)
    
    # Remove duplicates
    gdf = remove_duplicates(gdf)
    
    # Remove outliers
    if remove_outliers and outlier_columns is not None:
        gdf = remove_outliers_iqr(gdf, outlier_columns)
    
    logger.info(
        f"Data cleaning complete. Output: {len(gdf):,} records "
        f"({original_count - len(gdf):,} removed)"
    )
    
    return gdf


def handle_missing_values(
    gdf: gpd.GeoDataFrame,
    strategies: Dict[str, str]
) -> gpd.GeoDataFrame:
    """
    Handle missing values according to specified strategies.
    
    Args:
        gdf: GeoDataFrame
        strategies: Dictionary mapping column names to strategies
                   ('median', 'mode', 'unknown', 'keep_missing', 'drop')
    
    Returns:
        GeoDataFrame with missing values handled
    """
    for column, strategy in strategies.items():
        if column not in gdf.columns:
            continue
        
        missing_count = gdf[column].isna().sum()
        if missing_count == 0:
            continue
        
        logger.info(f"Handling {missing_count:,} missing values in '{column}' using '{strategy}'")
        
        if strategy == 'median':
            gdf[column] = gdf[column].fillna(gdf[column].median())
        elif strategy == 'mode':
            gdf[column] = gdf[column].fillna(gdf[column].mode()[0])
        elif strategy == 'unknown':
            gdf[column] = gdf[column].fillna('unknown')
        elif strategy == 'drop':
            gdf = gdf.dropna(subset=[column])
        # 'keep_missing' means do nothing
    
    return gdf


def remove_duplicates(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Remove duplicate records based on key columns.
    
    Args:
        gdf: GeoDataFrame
    
    Returns:
        GeoDataFrame without duplicates
    """
    original_count = len(gdf)
    
    # Define duplicate criteria
    subset_cols = []
    for col in ['Start_Lat', 'Start_Lng', 'Start_Time', 'Severity']:
        if col in gdf.columns:
            subset_cols.append(col)
    
    if not subset_cols:
        logger.warning("Cannot check for duplicates: key columns not found")
        return gdf
    
    gdf = gdf.drop_duplicates(subset=subset_cols, keep='first')
    
    removed = original_count - len(gdf)
    if removed > 0:
        logger.info(f"Removed {removed:,} duplicate records")
    
    return gdf


def remove_outliers_iqr(
    gdf: gpd.GeoDataFrame,
    columns: list,
    factor: float = 3.0
) -> gpd.GeoDataFrame:
    """
    Remove outliers using IQR method.
    
    Args:
        gdf: GeoDataFrame
        columns: List of columns to check
        factor: IQR multiplier for bounds
    
    Returns:
        GeoDataFrame with outliers removed
    """
    original_count = len(gdf)
    
    for column in columns:
        if column not in gdf.columns:
            continue
        
        Q1 = gdf[column].quantile(0.25)
        Q3 = gdf[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        mask = (gdf[column] >= lower_bound) & (gdf[column] <= upper_bound)
        removed = (~mask).sum()
        
        if removed > 0:
            logger.info(
                f"Removing {removed:,} outliers from '{column}' "
                f"(bounds: {lower_bound:.2f} to {upper_bound:.2f})"
            )
            gdf = gdf[mask]
    
    total_removed = original_count - len(gdf)
    if total_removed > 0:
        logger.info(f"Total outliers removed: {total_removed:,}")
    
    return gdf


if __name__ == "__main__":
    # Test with sample data
    logger.info("Testing data cleaning module...")
