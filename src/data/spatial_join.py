"""
Module for performing spatial join between accidents and road segments.

Matches each accident point to the nearest road segment using spatial indexing
for performance.
"""

import logging
from typing import Optional

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def spatial_join_accidents_roads(
    accidents_gdf: gpd.GeoDataFrame,
    roads_gdf: gpd.GeoDataFrame,
    max_distance: float = 100.0,
    distance_col: str = "distance_to_road"
) -> gpd.GeoDataFrame:
    """
    Perform spatial join between accident points and road segments.
    
    Finds the nearest road segment for each accident within a maximum distance threshold.
    Uses spatial indexing for performance.
    
    Args:
        accidents_gdf: GeoDataFrame of accident points
        roads_gdf: GeoDataFrame of road segments
        max_distance: Maximum distance in meters for matching (default: 100.0)
        distance_col: Name of column to store distance values
    
    Returns:
        GeoDataFrame with accidents joined to nearest road attributes
    
    Raises:
        ValueError: If input GeoDataFrames have incompatible CRS
    
    Example:
        >>> accidents = load_accidents_data(nrows=1000)
        >>> roads = download_osm_roads("Los Angeles, CA")
        >>> joined = spatial_join_accidents_roads(accidents, roads, max_distance=100)
        >>> print(f"Matched {joined['matched'].sum()} out of {len(joined)} accidents")
    """
    logger.info(f"Starting spatial join: {len(accidents_gdf):,} accidents × {len(roads_gdf):,} roads")
    logger.info(f"Maximum distance threshold: {max_distance} meters")
    
    # Validate inputs
    if accidents_gdf.empty:
        raise ValueError("Accidents GeoDataFrame is empty")
    
    if roads_gdf.empty:
        raise ValueError("Roads GeoDataFrame is empty")
    
    # Check and align CRS
    if accidents_gdf.crs is None:
        logger.warning("Accidents GeoDataFrame has no CRS. Assuming WGS84 (EPSG:4326)")
        accidents_gdf = accidents_gdf.set_crs(f"EPSG:{Config.WGS84_EPSG}")
    
    if roads_gdf.crs is None:
        logger.warning("Roads GeoDataFrame has no CRS. Assuming WGS84 (EPSG:4326)")
        roads_gdf = roads_gdf.set_crs(f"EPSG:{Config.WGS84_EPSG}")
    
    # Reproject to Web Mercator for accurate distance calculations
    logger.info("Reprojecting to Web Mercator (EPSG:3857) for distance calculations")
    accidents_proj = accidents_gdf.to_crs(f"EPSG:{Config.WEB_MERCATOR_EPSG}")
    roads_proj = roads_gdf.to_crs(f"EPSG:{Config.WEB_MERCATOR_EPSG}")
    
    # Perform spatial join using sjoin_nearest (GeoPandas 0.10+)
    try:
        logger.info("Performing nearest neighbor spatial join...")
        joined = gpd.sjoin_nearest(
            accidents_proj,
            roads_proj,
            how="left",
            max_distance=max_distance,
            distance_col=distance_col
        )
        
        # Add matched flag
        joined['matched'] = joined['index_right'].notna()
        
        # Log matching statistics
        match_count = joined['matched'].sum()
        match_rate = (match_count / len(accidents_proj)) * 100
        
        logger.info(f"Spatial join completed:")
        logger.info(f"  Total accidents: {len(accidents_proj):,}")
        logger.info(f"  Matched to roads: {match_count:,} ({match_rate:.2f}%)")
        logger.info(f"  Unmatched: {len(accidents_proj) - match_count:,}")
        
        if match_count < len(accidents_proj):
            logger.warning(
                f"{len(accidents_proj) - match_count:,} accidents could not be matched "
                f"to roads within {max_distance}m threshold"
            )
        
        # Log distance statistics for matched records
        if match_count > 0:
            matched_distances = joined[joined['matched']][distance_col]
            logger.info(f"Distance statistics (matched records):")
            logger.info(f"  Mean: {matched_distances.mean():.2f}m")
            logger.info(f"  Median: {matched_distances.median():.2f}m")
            logger.info(f"  Max: {matched_distances.max():.2f}m")
        
        # Reproject back to WGS84
        joined = joined.to_crs(f"EPSG:{Config.WGS84_EPSG}")
        
        return joined
        
    except Exception as e:
        logger.error(f"Spatial join failed: {str(e)}", exc_info=True)
        raise


def batch_spatial_join(
    accidents_gdf: gpd.GeoDataFrame,
    roads_gdf: gpd.GeoDataFrame,
    batch_size: int = 10000,
    max_distance: float = 100.0
) -> gpd.GeoDataFrame:
    """
    Perform spatial join in batches for large datasets.
    
    Useful when the full dataset exceeds memory limits.
    
    Args:
        accidents_gdf: GeoDataFrame of accidents
        roads_gdf: GeoDataFrame of roads
        batch_size: Number of accidents to process per batch
        max_distance: Maximum matching distance in meters
    
    Returns:
        Combined GeoDataFrame of all batches
    
    Example:
        >>> # Process 1M accidents in batches of 10k
        >>> joined = batch_spatial_join(accidents, roads, batch_size=10000)
    """
    logger.info(f"Starting batch spatial join with batch size: {batch_size:,}")
    
    n_batches = int(np.ceil(len(accidents_gdf) / batch_size))
    results = []
    
    for i in range(n_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(accidents_gdf))
        
        logger.info(f"Processing batch {i+1}/{n_batches} (records {start_idx:,} to {end_idx:,})")
        
        batch = accidents_gdf.iloc[start_idx:end_idx]
        joined_batch = spatial_join_accidents_roads(batch, roads_gdf, max_distance=max_distance)
        results.append(joined_batch)
    
    # Combine all batches
    logger.info("Combining batches...")
    combined = gpd.GeoDataFrame(pd.concat(results, ignore_index=True))
    
    logger.info(f"Batch processing complete. Total records: {len(combined):,}")
    
    return combined


def validate_spatial_join(joined_gdf: gpd.GeoDataFrame) -> dict:
    """
    Validate the results of a spatial join.
    
    Args:
        joined_gdf: GeoDataFrame from spatial_join_accidents_roads
    
    Returns:
        Dictionary with validation statistics
    
    Example:
        >>> joined = spatial_join_accidents_roads(accidents, roads)
        >>> stats = validate_spatial_join(joined)
        >>> print(stats)
    """
    stats = {
        'total_records': len(joined_gdf),
        'matched_records': joined_gdf['matched'].sum() if 'matched' in joined_gdf.columns else None,
        'match_rate': None,
        'has_surface_data': None,
        'surface_coverage': None,
        'has_highway_data': None,
        'highway_coverage': None
    }
    
    if stats['matched_records'] is not None:
        stats['match_rate'] = (stats['matched_records'] / stats['total_records']) * 100
    
    # Check for surface attribute
    if 'surface' in joined_gdf.columns:
        stats['has_surface_data'] = True
        non_unknown = joined_gdf['surface'] != 'unknown'
        stats['surface_coverage'] = (non_unknown.sum() / len(joined_gdf)) * 100
    else:
        stats['has_surface_data'] = False
    
    # Check for highway attribute
    if 'highway' in joined_gdf.columns:
        stats['has_highway_data'] = True
        non_null = joined_gdf['highway'].notna()
        stats['highway_coverage'] = (non_null.sum() / len(joined_gdf)) * 100
    else:
        stats['has_highway_data'] = False
    
    return stats


if __name__ == "__main__":
    # Example usage and testing
    from src.data.load_accidents import load_accidents_data
    from src.data.load_osm_data import download_osm_roads
    
    # Load sample data
    logger.info("Loading sample accident data...")
    accidents = load_accidents_data(nrows=1000, states=['CA'])
    
    logger.info("Downloading OSM roads for Los Angeles...")
    roads = download_osm_roads("Los Angeles, California, USA")
    
    # Perform spatial join
    logger.info("Performing spatial join...")
    joined = spatial_join_accidents_roads(accidents, roads, max_distance=100)
    
    # Validate results
    stats = validate_spatial_join(joined)
    
    print("\nSpatial Join Statistics:")
    print(f"  Total accidents: {stats['total_records']:,}")
    print(f"  Matched: {stats['matched_records']:,} ({stats['match_rate']:.2f}%)")
    print(f"  Surface data coverage: {stats['surface_coverage']:.2f}%")
    print(f"  Highway data coverage: {stats['highway_coverage']:.2f}%")
    
    print(f"\nFirst few joined records:\n{joined.head()}")
    
    if 'surface' in joined.columns:
        print(f"\nSurface type distribution:\n{joined['surface'].value_counts()}")
