"""
Main pipeline orchestrator for the US Accidents and Road Quality Analysis project.

This module provides the main entry point for running the full data pipeline.
"""

import logging
import argparse
from pathlib import Path

from src.config import Config
from src.utils.logging import setup_logger
from src.utils.helpers import print_section_header

logger = setup_logger(__name__)


def run_pipeline(
    nrows: int = None,
    states: list = None,
    cities: list = None,
    skip_download: bool = False,
    skip_spatial_join: bool = False
):
    """
    Run the complete data processing pipeline.
    
    Args:
        nrows: Number of accident records to process (None = all)
        states: List of state codes to process
        cities: List of cities to process
        skip_download: Skip OSM download if data exists
        skip_spatial_join: Skip spatial join if integrated data exists
    """
    print_section_header("US Accidents and Road Quality Analysis Pipeline")
    
    logger.info("Pipeline configuration:")
    logger.info(f"  Accident records: {nrows or 'all'}")
    logger.info(f"  States filter: {states or 'all'}")
    logger.info(f"  Cities filter: {cities or 'none'}")
    logger.info(f"  Skip OSM download: {skip_download}")
    logger.info(f"  Skip spatial join: {skip_spatial_join}")
    
    try:
        # Step 1: Load Accidents Data
        print_section_header("Step 1: Loading Accidents Data")
        from src.data.load_accidents import load_accidents_data, save_accidents_gdf
        
        accidents_gdf = load_accidents_data(
            nrows=nrows,
            states=states
        )
        logger.info(f"Loaded {len(accidents_gdf):,} accident records")
        
        # Save processed accidents
        accidents_path = Config.ACCIDENTS_CLEANED_DIR / "accidents_with_geometry.parquet"
        if not accidents_path.exists():
            save_accidents_gdf(accidents_gdf, accidents_path)
        
        # Step 2: Download OSM Roads
        print_section_header("Step 2: Downloading OSM Road Data")
        from src.data.load_osm_data import download_osm_roads, save_roads_gdf
        
        if not skip_download:
            if cities:
                # Download by city
                for city in cities:
                    state = "USA"  # Simplified - improve with city-state mapping
                    logger.info(f"Downloading roads for {city}, {state}")
                    roads_gdf = download_osm_roads(f"{city}, {state}")
                    save_roads_gdf(
                        roads_gdf,
                        Config.OSM_PROCESSED_DIR / f"{city.replace(' ', '_')}_roads.parquet"
                    )
            elif states:
                # Download by state
                for state in states:
                    logger.info(f"Downloading roads for {state}")
                    roads_gdf = download_osm_roads(f"{state}, USA")
                    save_roads_gdf(
                        roads_gdf,
                        Config.OSM_PROCESSED_DIR / f"{state}_roads.parquet"
                    )
            else:
                logger.warning("No cities or states specified. Skipping OSM download.")
                logger.info("Specify --cities or --states to download OSM data")
        
        # Step 3: Spatial Join
        if not skip_spatial_join:
            print_section_header("Step 3: Spatial Join")
            from src.data.spatial_join import spatial_join_accidents_roads
            
            # For demo purposes, load first available roads file
            roads_files = list(Config.OSM_PROCESSED_DIR.glob("*.parquet"))
            if roads_files:
                from src.data.load_osm_data import load_roads_gdf
                roads_gdf = load_roads_gdf(roads_files[0])
                
                logger.info("Performing spatial join...")
                joined_gdf = spatial_join_accidents_roads(
                    accidents_gdf,
                    roads_gdf,
                    max_distance=Config.MAX_DISTANCE_METERS
                )
                
                # Save integrated data
                output_path = Config.ACCIDENTS_WITH_ROAD_QUALITY_DIR / "integrated_data.parquet"
                joined_gdf.to_parquet(output_path, compression='snappy')
                logger.info(f"Saved integrated data to {output_path}")
            else:
                logger.warning("No OSM roads data found. Skipping spatial join.")
        
        # Step 4: Data Cleaning
        print_section_header("Step 4: Data Cleaning")
        logger.info("Data cleaning - to be implemented")
        
        # Step 5: Feature Engineering
        print_section_header("Step 5: Feature Engineering")
        logger.info("Feature engineering - to be implemented")
        
        # Step 6-9: Analysis, Modeling, Evaluation
        print_section_header("Pipeline Status")
        logger.info("✓ Steps 1-3 completed")
        logger.info("⏳ Steps 4-9 to be implemented")
        
        print_section_header("Pipeline Complete")
        logger.info("Pipeline execution finished successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description="US Accidents and Road Quality Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process sample data (10k records) for California
  python -m src.main --nrows 10000 --states CA

  # Process all data for multiple states
  python -m src.main --states CA TX FL

  # Process specific cities
  python -m src.main --cities "Los Angeles" "Houston"

  # Skip downloads if data exists
  python -m src.main --nrows 10000 --states CA --skip-download
        """
    )
    
    parser.add_argument(
        "--nrows",
        type=int,
        default=None,
        help="Number of accident records to process (default: all)"
    )
    
    parser.add_argument(
        "--states",
        type=str,
        nargs="+",
        default=None,
        help="State codes to process (e.g., CA TX FL)"
    )
    
    parser.add_argument(
        "--cities",
        type=str,
        nargs="+",
        default=None,
        help="Cities to process (e.g., 'Los Angeles' 'Houston')"
    )
    
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip OSM download if data exists"
    )
    
    parser.add_argument(
        "--skip-spatial-join",
        action="store_true",
        help="Skip spatial join if integrated data exists"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Run pipeline
    run_pipeline(
        nrows=args.nrows,
        states=args.states,
        cities=args.cities,
        skip_download=args.skip_download,
        skip_spatial_join=args.skip_spatial_join
    )


if __name__ == "__main__":
    main()
