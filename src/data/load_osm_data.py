"""
Module for downloading and processing OpenStreetMap road network data.

Uses the osmnx library to download road networks with surface attributes
from OpenStreetMap.
"""

import logging
from pathlib import Path
from typing import Optional, Union
import pickle

import geopandas as gpd
import osmnx as ox

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

# Configure osmnx
ox.settings.use_cache = Config.OSM_USE_CACHE
ox.settings.cache_folder = str(Config.OSM_CACHE_DIR)
ox.settings.log_console = False


def download_osm_roads(
    place_name: Optional[str] = None,
    polygon: Optional[gpd.GeoSeries] = None,
    network_type: str = "drive",
    custom_filter: Optional[str] = None,
    simplify: bool = True,
    retain_all: bool = False
) -> gpd.GeoDataFrame:
    """
    Download road network from OpenStreetMap.
    
    Args:
        place_name: Name of place to download (e.g., "Los Angeles, California, USA")
        polygon: Custom polygon boundary as GeoSeries. Overrides place_name if provided
        network_type: Type of network ('drive', 'walk', 'bike', 'all')
        custom_filter: Custom OSM filter string (e.g., '["highway"~"motorway|trunk"]')
        simplify: Whether to simplify the network topology
        retain_all: Retain all network components (not just largest)
    
    Returns:
        GeoDataFrame of road segments with attributes including surface type
    
    Raises:
        ValueError: If neither place_name nor polygon is provided
        Exception: If download fails
    
    Example:
        >>> # Download roads for a city
        >>> roads = download_osm_roads("Los Angeles, California, USA")
        
        >>> # Download roads within custom boundary
        >>> boundary = get_city_boundary()
        >>> roads = download_osm_roads(polygon=boundary)
    """
    if place_name is None and polygon is None:
        raise ValueError("Either place_name or polygon must be provided")
    
    logger.info(f"Downloading road network for: {place_name or 'custom polygon'}")
    
    try:
        # Download the network
        if polygon is not None:
            # Use polygon boundary
            G = ox.graph_from_polygon(
                polygon.unary_union,
                network_type=network_type,
                simplify=simplify,
                retain_all=retain_all,
                custom_filter=custom_filter
            )
        else:
            # Use place name
            G = ox.graph_from_place(
                place_name,
                network_type=network_type,
                simplify=simplify,
                retain_all=retain_all,
                custom_filter=custom_filter
            )
        
        logger.info(f"Downloaded network with {len(G.nodes)} nodes and {len(G.edges)} edges")
        
        # Convert to GeoDataFrame (edges only, we don't need nodes)
        roads_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
        
        logger.info(f"Converted to GeoDataFrame with {len(roads_gdf)} road segments")
        
        # Extract and clean surface information
        roads_gdf = extract_surface_attributes(roads_gdf)
        
        # Log surface type distribution
        if 'surface' in roads_gdf.columns:
            surface_counts = roads_gdf['surface'].value_counts()
            logger.info(f"Surface types found:\n{surface_counts.head(10)}")
        
        return roads_gdf
        
    except Exception as e:
        logger.error(f"Failed to download OSM data: {str(e)}")
        raise


def extract_surface_attributes(roads_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Extract and standardize road surface attributes from OSM data.
    
    Args:
        roads_gdf: GeoDataFrame with OSM road data
    
    Returns:
        GeoDataFrame with cleaned surface attribute
    """
    # OSM surface attribute may be in different forms
    if 'surface' not in roads_gdf.columns:
        logger.warning("No 'surface' attribute found in OSM data. Creating 'unknown' category.")
        roads_gdf['surface'] = 'unknown'
    else:
        # Fill missing values
        roads_gdf['surface'] = roads_gdf['surface'].fillna('unspecified')
        
        # Standardize surface types
        surface_mapping = {
            'asphalt': 'asphalt',
            'paved': 'paved',
            'concrete': 'concrete',
            'concrete:plates': 'concrete',
            'concrete:lanes': 'concrete',
            'unpaved': 'unpaved',
            'gravel': 'gravel',
            'fine_gravel': 'gravel',
            'compacted': 'unpaved',
            'dirt': 'dirt',
            'ground': 'unpaved',
            'grass': 'unpaved',
            'earth': 'dirt',
            'sand': 'unpaved',
            'cobblestone': 'cobblestone',
            'paving_stones': 'paved',
            'sett': 'cobblestone',
            'unspecified': 'unknown',
            'unknown': 'unknown'
        }
        
        # Apply mapping (case-insensitive)
        roads_gdf['surface'] = roads_gdf['surface'].str.lower().map(
            lambda x: surface_mapping.get(x, 'unknown')
        )
    
    # Create broader surface category
    roads_gdf['surface_category'] = roads_gdf['surface'].map({
        'asphalt': 'paved',
        'concrete': 'paved',
        'paved': 'paved',
        'gravel': 'unpaved',
        'dirt': 'unpaved',
        'unpaved': 'unpaved',
        'cobblestone': 'paved',
        'unknown': 'unknown'
    })
    
    # Extract highway type
    if 'highway' in roads_gdf.columns:
        # Simplify highway types
        highway_mapping = {
            'motorway': 'motorway',
            'motorway_link': 'motorway',
            'trunk': 'trunk',
            'trunk_link': 'trunk',
            'primary': 'primary',
            'primary_link': 'primary',
            'secondary': 'secondary',
            'secondary_link': 'secondary',
            'tertiary': 'tertiary',
            'tertiary_link': 'tertiary',
            'residential': 'residential',
            'living_street': 'residential',
            'unclassified': 'unclassified',
            'service': 'service',
            'road': 'unclassified'
        }
        
        if isinstance(roads_gdf['highway'].iloc[0], list):
            # Handle cases where highway is a list
            roads_gdf['highway'] = roads_gdf['highway'].apply(
                lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'unclassified'
            )
        
        roads_gdf['highway'] = roads_gdf['highway'].map(
            lambda x: highway_mapping.get(x, 'other')
        )
    
    return roads_gdf


def download_roads_by_state(
    state_name: str,
    network_type: str = "drive"
) -> gpd.GeoDataFrame:
    """
    Download roads for an entire US state.
    
    Args:
        state_name: Full state name (e.g., "California")
        network_type: Type of network to download
    
    Returns:
        GeoDataFrame of road segments for the state
    
    Example:
        >>> ca_roads = download_roads_by_state("California")
    """
    place_query = f"{state_name}, USA"
    return download_osm_roads(place_query, network_type=network_type)


def download_roads_by_city(
    city_name: str,
    state_name: str,
    network_type: str = "drive"
) -> gpd.GeoDataFrame:
    """
    Download roads for a specific city.
    
    Args:
        city_name: City name
        state_name: State name
        network_type: Type of network to download
    
    Returns:
        GeoDataFrame of road segments for the city
    
    Example:
        >>> la_roads = download_roads_by_city("Los Angeles", "California")
    """
    place_query = f"{city_name}, {state_name}, USA"
    return download_osm_roads(place_query, network_type=network_type)


def save_roads_gdf(
    roads_gdf: gpd.GeoDataFrame,
    output_path: Optional[Path] = None,
    format: str = "parquet"
) -> None:
    """
    Save roads GeoDataFrame to file.
    
    Args:
        roads_gdf: GeoDataFrame to save
        output_path: Path to save file
        format: Output format ('parquet', 'geojson', 'pickle')
    """
    if output_path is None:
        output_path = Config.OSM_PROCESSED_DIR / f"roads.{format}"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving roads GeoDataFrame to {output_path}")
    
    if format == "parquet":
        roads_gdf.to_parquet(output_path, compression='snappy')
    elif format == "geojson":
        roads_gdf.to_file(output_path, driver='GeoJSON')
    elif format == "pickle":
        with open(output_path, 'wb') as f:
            pickle.dump(roads_gdf, f)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    logger.info(f"Successfully saved {len(roads_gdf):,} road segments")


def load_roads_gdf(filepath: Union[str, Path]) -> gpd.GeoDataFrame:
    """
    Load previously saved roads GeoDataFrame.
    
    Args:
        filepath: Path to the saved file
    
    Returns:
        GeoDataFrame of roads
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Roads file not found: {filepath}")
    
    logger.info(f"Loading roads from {filepath}")
    
    if filepath.suffix == '.parquet':
        roads_gdf = gpd.read_parquet(filepath)
    elif filepath.suffix == '.geojson':
        roads_gdf = gpd.read_file(filepath)
    elif filepath.suffix == '.pkl':
        with open(filepath, 'rb') as f:
            roads_gdf = pickle.load(f)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    logger.info(f"Loaded {len(roads_gdf):,} road segments")
    
    return roads_gdf


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Download OSM road data")
    parser.add_argument("--city", type=str, help="City name")
    parser.add_argument("--state", type=str, help="State name")
    parser.add_argument("--place", type=str, help="Full place name")
    parser.add_argument("--save", action="store_true", help="Save downloaded data")
    
    args = parser.parse_args()
    
    # Download based on arguments
    if args.city and args.state:
        roads_gdf = download_roads_by_city(args.city, args.state)
    elif args.state:
        roads_gdf = download_roads_by_state(args.state)
    elif args.place:
        roads_gdf = download_osm_roads(args.place)
    else:
        print("Please provide --city and --state, --state, or --place")
        exit(1)
    
    print(f"\nDownloaded {len(roads_gdf):,} road segments")
    print(f"\nSurface type distribution:\n{roads_gdf['surface'].value_counts()}")
    print(f"\nHighway type distribution:\n{roads_gdf['highway'].value_counts()}")
    
    # Save if requested
    if args.save:
        save_roads_gdf(roads_gdf)
