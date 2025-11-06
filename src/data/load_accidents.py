"""
Module for loading US Accidents dataset and converting to GeoDataFrame.

This module handles reading the accidents CSV file, creating Point geometries from
lat/lon coordinates, and converting to a GeoDataFrame with proper CRS.
"""

import logging
from typing import Optional
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def load_accidents_data(
    filepath: Optional[str] = None,
    nrows: Optional[int] = None,
    states: Optional[list[str]] = None,
    severity_filter: Optional[list[int]] = None,
    date_range: Optional[tuple[str, str]] = None

) -> gpd.GeoDataFrame:
    """
    Load US Accidents dataset and convert to GeoDataFrame with geometries.
    
    Args:
        filepath: Path to the accidents CSV file. If None, uses Config.ACCIDENTS_CSV_PATH
        nrows: Number of rows to load (useful for testing). None loads all rows
        states: List of state codes to filter (e.g., ['CA', 'TX']). None loads all states
        severity_filter: List of severity levels to include (e.g., [3, 4]). None includes all
        date_range: Tuple of (start_date, end_date) as strings 'YYYY-MM-DD'. None includes all dates
    
    Returns:
        GeoDataFrame with Point geometries in WGS84 (EPSG:4326) projection
    
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If required columns are missing
    
    Example:
        >>> # Load all data
        >>> accidents_gdf = load_accidents_data()
        
        >>> # Load sample for testing
        >>> sample = load_accidents_data(nrows=10000)
        
        >>> # Load specific states
        >>> ca_tx = load_accidents_data(states=['CA', 'TX'])
    """
    # Use default path if not provided
    if filepath is None:
        filepath = Config.ACCIDENTS_CSV_PATH
    
    filepath = Path(filepath)
    
    # Check file exists
    if not filepath.exists():
        raise FileNotFoundError(
            f"Accidents CSV file not found: {filepath}\n"
            f"Please download the US Accidents dataset from Kaggle and place it at {filepath}"
        )
    
    logger.info(f"Loading accidents data from {filepath}")
    
    import os
    import kagglehub
    from dotenv import load_dotenv
    import os

    load_dotenv()

    username = os.getenv("KAGGLE_USERNAME")
    api_key = os.getenv("KAGGLE_KEY")
    # Set credentials directly in the script (be cautious with security)
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = api_key

    # Authenticate using kagglehub (no prompt)
    kagglehub.login()

    # Now, download the dataset
    dataset_path = kagglehub.dataset_download('sobhanmoosavi/us-accidents')
    print(f'Dataset downloaded to: {dataset_path}')


    # Load CSV
    try:
        df = pd.read_csv(
            filepath,
            nrows=nrows,
            low_memory=False
        )
        logger.info(f"Loaded {len(df):,} accident records")
    except Exception as e:
        logger.error(f"Failed to load CSV: {str(e)}")
        raise
    
    # Validate required columns
    required_columns = ['Start_Lat', 'Start_Lng', 'Severity']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Filter by states if specified
    if states is not None:
        if 'State' not in df.columns:
            logger.warning("State column not found. Cannot filter by states.")
        else:
            original_count = len(df)
            df = df[df['State'].isin(states)]
            logger.info(f"Filtered to states {states}: {len(df):,} records (from {original_count:,})")
    
    # Filter by severity if specified
    if severity_filter is not None:
        original_count = len(df)
        df = df[df['Severity'].isin(severity_filter)]
        logger.info(f"Filtered to severity {severity_filter}: {len(df):,} records (from {original_count:,})")
    
    # Filter by date range if specified
    if date_range is not None:
        if 'Start_Time' not in df.columns:
            logger.warning("Start_Time column not found. Cannot filter by date.")
        else:
            df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
            start_date, end_date = date_range
            original_count = len(df)
            df = df[(df['Start_Time'] >= start_date) & (df['Start_Time'] <= end_date)]
            logger.info(f"Filtered to date range {start_date} to {end_date}: {len(df):,} records")
    
    # Remove records with missing coordinates
    original_count = len(df)
    df = df.dropna(subset=['Start_Lat', 'Start_Lng'])
    if len(df) < original_count:
        logger.warning(f"Removed {original_count - len(df):,} records with missing coordinates")
    
    # Validate coordinate ranges (contiguous US)
    # Latitude: 24.5°N (Key West) to 49.4°N (Canadian border)
    # Longitude: -125°W (Pacific) to -66°W (Atlantic)
    lat_valid = (df['Start_Lat'] >= 24.5) & (df['Start_Lat'] <= 49.4)
    lon_valid = (df['Start_Lng'] >= -125.0) & (df['Start_Lng'] <= -66.0)
    
    invalid_coords = ~(lat_valid & lon_valid)
    if invalid_coords.sum() > 0:
        logger.warning(
            f"Removing {invalid_coords.sum():,} records with coordinates outside contiguous US"
        )
        df = df[~invalid_coords]
    
    # Create Point geometries
    logger.info("Creating Point geometries from coordinates")
    geometry = [Point(xy) for xy in zip(df['Start_Lng'], df['Start_Lat'])]
    
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=geometry,
        crs=f"EPSG:{Config.WGS84_EPSG}"
    )
    
    # Convert Start_Time to datetime if it exists and isn't already
    if 'Start_Time' in gdf.columns:
        gdf['Start_Time'] = pd.to_datetime(gdf['Start_Time'], errors='coerce')
    
    if 'End_Time' in gdf.columns:
        gdf['End_Time'] = pd.to_datetime(gdf['End_Time'], errors='coerce')
    
    # Convert boolean columns
    boolean_columns = [
        'Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 'No_Exit',
        'Railway', 'Roundabout', 'Station', 'Stop', 'Traffic_Calming',
        'Traffic_Signal', 'Turning_Loop'
    ]
    for col in boolean_columns:
        if col in gdf.columns:
            gdf[col] = gdf[col].fillna(False).astype(bool)
    
    # Optimize memory usage with categorical dtypes
    categorical_columns = ['State', 'City', 'County', 'Weather_Condition', 'Wind_Direction']
    for col in categorical_columns:
        if col in gdf.columns:
            gdf[col] = gdf[col].astype('category')
    
    logger.info(
        f"Successfully created GeoDataFrame with {len(gdf):,} records "
        f"in {gdf.crs} projection"
    )
    
    # Log basic statistics
    logger.info(f"Severity distribution:\n{gdf['Severity'].value_counts().sort_index()}")
    
    if 'State' in gdf.columns:
        logger.info(f"Top 5 states by accident count:\n{gdf['State'].value_counts().head()}")
    
    return gdf


def save_accidents_gdf(
    gdf: gpd.GeoDataFrame,
    output_path: Optional[Path] = None,
    format: str = "parquet"
) -> None:
    """
    Save accidents GeoDataFrame to file.
    
    Args:
        gdf: GeoDataFrame to save
        output_path: Path to save file. If None, uses default path in Config
        format: Output format ('parquet', 'geojson', 'shapefile')
    
    Example:
        >>> gdf = load_accidents_data(nrows=10000)
        >>> save_accidents_gdf(gdf, output_path=Path('data/processed/sample.parquet'))
    """
    if output_path is None:
        output_path = Config.ACCIDENTS_CLEANED_DIR / f"accidents_with_geometry.{format}"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving GeoDataFrame to {output_path}")
    
    if format == "parquet":
        gdf.to_parquet(output_path, compression='snappy')
    elif format == "geojson":
        gdf.to_file(output_path, driver='GeoJSON')
    elif format == "shapefile":
        gdf.to_file(output_path, driver='ESRI Shapefile')
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    logger.info(f"Successfully saved {len(gdf):,} records to {output_path}")


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Load US Accidents data")
    parser.add_argument("--nrows", type=int, default=None, help="Number of rows to load")
    parser.add_argument("--states", type=str, nargs="+", help="State codes to filter")
    parser.add_argument("--save", action="store_true", help="Save processed data")
    
    args = parser.parse_args()
    
    # Load data
    accidents_gdf = load_accidents_data(
        nrows=args.nrows,
        states=args.states
    )
    
    # Save if requested
    if args.save:
        save_accidents_gdf(accidents_gdf)
    
    print(f"\nLoaded {len(accidents_gdf):,} accidents")
    print(f"\nFirst few records:\n{accidents_gdf.head()}")
    print(f"\nColumn names:\n{accidents_gdf.columns.tolist()}")
