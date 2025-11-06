# Scripts Directory

This directory contains utility scripts for data downloading, preprocessing, and other project automation tasks.

## Available Scripts

### `download_accidents_data.py`

Downloads the US Accidents dataset from Kaggle using kagglehub and generates comprehensive metadata documentation.

**Requirements:**
```bash
pip install kagglehub python-dotenv pandas
```

**Setup:**

Before running, you need Kaggle API credentials. See detailed guide: [`../docs/KAGGLE_SETUP_GUIDE.md`](../docs/KAGGLE_SETUP_GUIDE.md)

**Quick setup:**
1. Get credentials from https://www.kaggle.com/settings/account
2. Add to `.env` file:
   ```bash
   KAGGLE_USERNAME=your_kaggle_username
   KAGGLE_KEY=your_kaggle_api_key
   ```

**Usage:**
```bash
python scripts/download_accidents_data.py
```

**What it does:**
1. Downloads the US Accidents dataset from Kaggle (sobhanmoosavi/us-accidents)
2. Caches the dataset using kagglehub (~2-3 GB, first time only)
3. Generates `data/raw/accidents_raw/DATASET_METADATA.md` with:
   - Dataset dimensions and statistics
   - Column information and data types
   - Missing value analysis
   - Data quality metrics
   - Geographic and temporal coverage
   - Usage examples and preprocessing recommendations
4. Creates `data/raw/accidents_raw/DATA_LOCATION.txt` pointing to the cached dataset

**Output:**
- Dataset cached by kagglehub (typically in `~/.cache/kagglehub/`)
- Metadata: `data/raw/accidents_raw/DATASET_METADATA.md`
- Location reference: `data/raw/accidents_raw/DATA_LOCATION.txt`

**After Running:**
The script will show you the dataset location. Update your `.env` file:
```bash
ACCIDENTS_CSV_PATH=/path/to/cached/US_Accidents_March23.csv
```

## Future Scripts

Additional scripts will be added for:
- Downloading OSM data for specific regions
- Batch processing spatial joins
- Model training and evaluation
- Report generation
