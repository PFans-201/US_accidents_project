"""
Script to download US Accidents dataset from Kaggle using kagglehub.

This script downloads the US Accidents dataset and places it in the data/raw/accidents_raw directory.
It also generates metadata documentation for the dataset.

Requirements:
    pip install kagglehub python-dotenv pandas
    
Setup:
    1. Get Kaggle API credentials from https://www.kaggle.com/settings/account
    2. Click "Create New API Token" to download kaggle.json
    3. Add credentials to .env file:
       KAGGLE_USERNAME=your_username
       KAGGLE_KEY=your_api_key
    
Usage:
    python scripts/download_accidents_data.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import Config
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def download_us_accidents_dataset():
    """
    Download US Accidents dataset from Kaggle using kagglehub.
    
    Returns:
        str: Path where data was downloaded
    """
    try:
        import kagglehub
        from dotenv import load_dotenv
    except ImportError as e:
        logger.error("Required packages not found. Please install: pip install kagglehub python-dotenv")
        raise e
    
    logger.info("=" * 80)
    logger.info("Downloading US Accidents Dataset from Kaggle")
    logger.info("=" * 80)
    
    # Load credentials from .env file
    load_dotenv()
    username = os.getenv("KAGGLE_USERNAME")
    api_key = os.getenv("KAGGLE_KEY")
    
    if not username or not api_key:
        logger.error("Kaggle credentials not found in .env file!")
        logger.error("Please add the following to your .env file:")
        logger.error("  KAGGLE_USERNAME=your_username")
        logger.error("  KAGGLE_KEY=your_api_key")
        logger.error("\nTo get your credentials:")
        logger.error("  1. Go to https://www.kaggle.com/settings/account")
        logger.error("  2. Click 'Create New API Token'")
        logger.error("  3. Extract username and key from downloaded kaggle.json")
        raise ValueError("Missing Kaggle credentials")
    
    # Set environment variables for kagglehub
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = api_key
    
    # Kaggle dataset identifier
    dataset_name = "sobhanmoosavi/us-accidents"
    
    logger.info(f"Dataset: {dataset_name}")
    logger.info("Downloading to kagglehub cache directory...")
    logger.info("This may take several minutes for the first download (~2-3 GB)")
    
    try:
        # Download the dataset
        # kagglehub caches downloads, so subsequent runs will be faster
        dataset_path = kagglehub.dataset_download(dataset_name)
        
        logger.info("✓ Dataset downloaded successfully!")
        logger.info(f"Dataset cached at: {dataset_path}")
        
        # Find the CSV file in the downloaded directory
        csv_files = list(Path(dataset_path).glob("*.csv"))
        
        if csv_files:
            source_file = csv_files[0]  # Use the first (should be only one main file)
            logger.info(f"Source file: {source_file.name}")
            logger.info(f"File size: {source_file.stat().st_size / 1024**3:.2f} GB")
            
            # Copy to project data directory
            target_dir = Config.ACCIDENTS_RAW_DIR
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / source_file.name
            
            # Copy the file if it doesn't exist in project directory
            if not target_file.exists():
                import shutil
                logger.info("\nCopying dataset to project directory...")
                logger.info(f"Source: {source_file}")
                logger.info(f"Target: {target_file}")
                logger.info("This may take a minute for large files...")
                
                shutil.copy2(source_file, target_file)
                logger.info("✓ Dataset copied to project directory!")
            else:
                logger.info("\n✓ Dataset already exists in project directory: {target_file}")
            
            # Create metadata info file
            info_file = target_dir / "DATA_INFO.txt"
            with open(info_file, 'w') as f:
                full_memory = target_file.stat().st_size 
                f.write("US Accidents Dataset Information\n")
                f.write("==================================\n\n")
                f.write(f"Dataset file: {target_file.name}\n")
                f.write(f"Full path: {target_file}\n")
                f.write(f"File size: {full_memory/ 1024**3:.2f} GB\n")
                f.write(f"Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("To use in your code:\n")
                f.write("import pandas as pd\n")
                f.write(f"df = pd.read_csv('{target_file}')\n\n")
                f.write("Or using project config:\n")
                f.write("from src.data.load_accidents import load_accidents_data\n")
                f.write("accidents_gdf = load_accidents_data()\n")
            
            logger.info(f"✓ Dataset info saved to: {info_file}")
            
            # Update config to point to the project file
            logger.info("\nUpdate your .env file with:")
            logger.info(f"ACCIDENTS_CSV_PATH={target_file}")
            
            return str(target_file)
        else:
            logger.warning("No CSV files found in cache directory")
            return dataset_path
        
    except Exception as e:
        logger.error(f"Failed to download dataset: {str(e)}")
        logger.error("Make sure you have:")
        logger.error("1. Installed kagglehub: pip install kagglehub")
        logger.error("2. Added Kaggle credentials to .env file")
        raise


def generate_metadata(full_memory, file_path):
    """
    Generate metadata documentation for the dataset.
    
    Args:
        file_path: Path where the data is stored
        full_memory: Full size of the dataset file in bytes
    """
    import pandas as pd
    
    logger.info("\nGenerating metadata documentation...")
    logger.info("Loading dataset to analyze...")
    
    # Load dataset for analysis
    df = pd.read_csv(file_path, nrows=100000)  # Sample for metadata generation
    
    metadata_path = Config.ACCIDENTS_RAW_DIR / "DATASET_METADATA.md"
    
    # Collect metadata
    n_rows = len(df)
    n_cols = len(df.columns)
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    
    # Get column info
    dtypes_summary = df.dtypes.value_counts()
    missing_summary = df.isnull().sum()
    missing_pct = (missing_summary / len(df) * 100).round(2)
    
    metadata_content = f"""# US Accidents Dataset Metadata

## Dataset Information

**Source**: [Kaggle - US Accidents (2016-2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

**Downloaded**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Location**: `{file_path}`

**Citation**:
```
Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. 
"A Countrywide Traffic Accident Dataset.", 2019.
Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. 
"Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights." 
In proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, 
ACM, 2019.
```

## Sampled Dataset Dimensions

- **Total Records**: {n_rows:,}
- **Total Columns**: {n_cols}
- **Memory Usage**: {memory_mb:,.2f} MB
- **Memory Coverage**: {memory_mb/full_memory:.2f}%
- **Time Range**: 2016-2023 (49 US states)

## Data Types Summary

"""
    
    for dtype, count in dtypes_summary.items():
        metadata_content += f"- **{dtype}**: {count} columns\n"
    
    metadata_content += """

## Column Information

### Key Columns

| Column | Type | Non-Null Count | Missing % | Description |
|--------|------|----------------|-----------|-------------|
"""
    
    # Add key columns first
    key_columns = [
        'ID', 'Severity', 'Start_Time', 'End_Time', 
        'Start_Lat', 'Start_Lng', 'Distance(mi)',
        'City', 'County', 'State', 'Zipcode',
        'Temperature(F)', 'Humidity(%)', 'Pressure(in)', 
        'Visibility(mi)', 'Wind_Speed(mph)', 'Weather_Condition'
    ]
    
    for col in key_columns:
        if col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].count()
            missing_pct_val = missing_pct[col]
            
            # Add description
            descriptions = {
                'ID': 'Unique identifier for the accident',
                'Severity': 'Severity level (1-4, 1=minor, 4=severe)',
                'Start_Time': 'Start time of accident impact',
                'End_Time': 'End time of accident impact',
                'Start_Lat': 'Latitude (WGS84)',
                'Start_Lng': 'Longitude (WGS84)',
                'Distance(mi)': 'Length of road affected',
                'City': 'City name',
                'County': 'County name',
                'State': 'State code (2 letters)',
                'Zipcode': 'Postal code',
                'Temperature(F)': 'Temperature in Fahrenheit',
                'Humidity(%)': 'Relative humidity',
                'Pressure(in)': 'Atmospheric pressure',
                'Visibility(mi)': 'Visibility in miles',
                'Wind_Speed(mph)': 'Wind speed in mph',
                'Weather_Condition': 'Weather description'
            }
            
            desc = descriptions.get(col, '')
            metadata_content += f"| `{col}` | {dtype} | {non_null:,} | {missing_pct_val:.1f}% | {desc} |\n"
    
    metadata_content += f"""

### All Columns ({n_cols} total)

<details>
<summary>Click to expand full column list</summary>

| # | Column Name | Data Type | Non-Null | Missing % |
|---|-------------|-----------|----------|-----------|
"""
    
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].count()
        missing_pct_val = missing_pct[col]
        metadata_content += f"| {i} | `{col}` | {dtype} | {non_null:,} | {missing_pct_val:.1f}% |\n"
    
    metadata_content += """
</details>

## Data Quality

"""
    
    # Calculate quality metrics
    total_missing = missing_summary.sum()
    total_cells = n_rows * n_cols
    overall_completeness = (1 - total_missing / total_cells) * 100
    
    metadata_content += f"""
- **Overall Completeness**: {overall_completeness:.2f}%
- **Total Missing Values**: {total_missing:,} out of {total_cells:,} cells
- **Columns with >50% Missing**: {(missing_pct > 50).sum()}
- **Columns with No Missing**: {(missing_pct == 0).sum()}

### Columns with High Missing Rates (>25%)

"""
    
    high_missing = missing_pct[missing_pct > 25].sort_values(ascending=False)
    if len(high_missing) > 0:
        for col, pct in high_missing.head(10).items():
            metadata_content += f"- `{col}`: {pct:.1f}% missing\n"
    else:
        metadata_content += "*No columns with >25% missing values*\n"
    
    # Add data ranges for key numeric columns
    metadata_content += """

## Data Ranges

### Severity Distribution

"""
    
    if 'Severity' in df.columns:
        sev_counts = df['Severity'].value_counts().sort_index()
        for sev, count in sev_counts.items():
            pct = (count / n_rows) * 100
            metadata_content += f"- **Severity {sev}**: {count:,} ({pct:.1f}%)\n"
    
    metadata_content += """

### Geographic Coverage

"""
    
    if 'State' in df.columns:
        top_states = df['State'].value_counts().head(10)
        metadata_content += "**Top 10 States by Accident Count:**\n\n"
        for state, count in top_states.items():
            pct = (count / n_rows) * 100
            metadata_content += f"- **{state}**: {count:,} ({pct:.1f}%)\n"
    
    # Add temporal info
    if 'Start_Time' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Start_Time']):
        min_date = df['Start_Time'].min()
        max_date = df['Start_Time'].max()
        metadata_content += f"""

### Temporal Coverage

- **Earliest Accident**: {min_date}
- **Latest Accident**: {max_date}
- **Time Span**: {(max_date - min_date).days} days
"""
    
    metadata_content += """

## Usage Notes

### Loading the Dataset

```python
import pandas as pd
from pathlib import Path

# Load full dataset
df = pd.read_csv('""" + str(file_path) + """')

# Or load with specific columns
columns = ['Start_Lat', 'Start_Lng', 'Severity', 'Start_Time', 'Weather_Condition']
df = pd.read_csv('""" + str(file_path) + """', usecols=columns)

# Or load in chunks for large dataset
for chunk in pd.read_csv('""" + str(file_path) + """', chunksize=100000):
    # Process chunk
    pass
```

### Using with Project Code

```python
from src.data.load_accidents import load_accidents_data

# Load with project utilities (handles geometry creation, filtering, etc.)
accidents_gdf = load_accidents_data(nrows=10000, states=['CA', 'TX'])
```

## Data Preprocessing Recommendations

1. **Missing Values**: 
   - Weather attributes have ~5-10% missing - consider median imputation
   - Some infrastructure boolean features may need False as default

2. **Outliers**:
   - Check `Temperature(F)` for extreme values
   - Validate `Visibility(mi)` ranges
   - Review `Distance(mi)` outliers

3. **Coordinate Validation**:
   - Ensure lat/lon are within contiguous US bounds
   - Remove any (0, 0) coordinates

4. **Date/Time Processing**:
   - Convert `Start_Time` and `End_Time` to datetime
   - Extract hour, day_of_week, month for temporal analysis

5. **Categorical Encoding**:
   - `Weather_Condition` needs grouping (too many categories)
   - `State`, `City` for geographic analysis

## Updates

- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Generated By**: `scripts/download_accidents_data.py`

## References

- Dataset Homepage: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
- Original Research: https://arxiv.org/abs/1906.05409
- Documentation: https://smoosavi.org/datasets/us_accidents

---

*This metadata file is automatically generated. Do not edit manually.*
"""
    
    # Write metadata file
    with open(metadata_path, 'w') as f:
        f.write(metadata_content)
    
    logger.info(f"✓ Metadata saved to: {metadata_path}")
    
    return metadata_path


def main():
    """Main execution function."""
    import pandas as pd
    
    try:
        # Download dataset
        full_memory, file_path = download_us_accidents_dataset()
        
        # Generate metadata
        metadata_path = generate_metadata(full_memory, file_path)
        
        # Load a sample to show summary
        logger.info("\nLoading sample for summary...")
        df_sample = pd.read_csv(file_path, nrows=5)
        
        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("DOWNLOAD COMPLETE")
        logger.info("=" * 80)
        logger.info("\n✓ Dataset downloaded and cached by kagglehub")
        logger.info(f"✓ Metadata generated: {metadata_path}")
        logger.info("\n📊 Dataset Summary:")
        logger.info(f"   - Location: {file_path}")
        logger.info(f"   - Columns: {len(df_sample.columns)}")
        
        logger.info("\n🔍 First 5 records:")
        print(df_sample.head())
        
        logger.info("\n📋 Next Steps:")
        logger.info(f"   1. Review metadata: {metadata_path}")
        logger.info(f"   2. Update .env with: ACCIDENTS_CSV_PATH={file_path}")
        logger.info("   3. Start data exploration in notebooks/01_data_loading_accidents.ipynb")
        
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
