# Kaggle API Setup Guide

This guide will help you set up Kaggle API credentials to download the US Accidents dataset.

## Quick Setup (3 minutes)

### Step 1: Get Your Kaggle API Credentials

1. **Log in to Kaggle**: Go to [https://www.kaggle.com](https://www.kaggle.com) and sign in
   - If you don't have an account, create one for free

2. **Navigate to Account Settings**: Go to [https://www.kaggle.com/settings/account](https://www.kaggle.com/settings/account)

3. **Create API Token**:
   - Scroll down to the "API" section
   - Click **"Create New API Token"**
   - A file named `kaggle.json` will automatically download to your computer

4. **Open the downloaded file**: The `kaggle.json` file contains your credentials in this format:
   ```json
   {
     "username": "your_kaggle_username",
     "key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
   }
   ```

### Step 2: Add Credentials to Your Project

1. **Create `.env` file** (if it doesn't exist):
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** and add your credentials:
   ```bash
   # Open with your favorite editor
   nano .env
   # OR
   code .env
   ```

3. **Paste your credentials** from `kaggle.json`:
   ```bash
   KAGGLE_USERNAME=your_kaggle_username
   KAGGLE_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

4. **Save the file** (Ctrl+O in nano, Ctrl+S in VS Code)

### Step 3: Verify Setup

Run the download script to test:
```bash
python scripts/download_accidents_data.py
```

If credentials are correct, you'll see:
```
================================================================================
Downloading US Accidents Dataset from Kaggle
================================================================================
Dataset: sobhanmoosavi/us-accidents
Downloading to kagglehub cache directory...
```

## Security Best Practices

### ✅ DO:
- Keep `.env` file in project root (already in `.gitignore`)
- Use different API tokens for different projects
- Rotate tokens periodically
- Delete old tokens from Kaggle settings

### ❌ DON'T:
- Commit `.env` to Git (it's already ignored)
- Share your API key in chat, screenshots, or documentation
- Use the same token across multiple collaborators
- Store credentials in code files

## Troubleshooting

### Problem: "Kaggle credentials not found"
**Solution**: Make sure your `.env` file exists and contains:
```bash
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
```

### Problem: "401 Unauthorized"
**Solution**: 
- Verify credentials are correct (no extra spaces)
- Token might be expired - create a new one
- Accept Kaggle dataset terms: Visit [dataset page](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) and click "Download"

### Problem: Import error for kagglehub
**Solution**: Install required packages:
```bash
pip install -r requirements.txt
```

### Problem: "Dataset not found"
**Solution**: Make sure you've accepted the dataset's terms of use on Kaggle

## Alternative: Using kaggle.json (Traditional Method)

If you prefer the traditional Kaggle CLI method:

1. **Place kaggle.json in the standard location**:
   ```bash
   # Linux/Mac
   mkdir -p ~/.kaggle
   cp kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   
   # Windows
   mkdir %USERPROFILE%\.kaggle
   copy kaggle.json %USERPROFILE%\.kaggle\
   ```

2. **Our script will still work** - it checks both locations

## Collaborative Projects

If working with a team:

1. **Each person needs their own credentials**
   - Don't share API tokens
   - Each team member creates their own

2. **Share `.env.example`** (not `.env`)
   - Commit: `.env.example` ✅
   - Never commit: `.env` ❌

3. **Document the setup process**
   - Link to this guide in your README
   - Add to onboarding documentation

## Dataset Information

**Dataset**: US Accidents (2016-2023)
- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
- **Size**: ~2-3 GB
- **Records**: 7.6+ million accidents
- **Coverage**: 49 US states

**First download takes time** (~5-15 minutes depending on connection)
**Subsequent runs are instant** (cached by kagglehub)

## Next Steps

After successful setup:

1. ✅ Download dataset: `python scripts/download_accidents_data.py`
2. ✅ Review metadata: `data/raw/accidents_raw/DATASET_METADATA.md`
3. ✅ Update .env with dataset path
4. ✅ Start exploring: `notebooks/01_data_loading_accidents.ipynb`

## Need Help?

- **Kaggle API Docs**: https://www.kaggle.com/docs/api
- **kagglehub Docs**: https://github.com/Kaggle/kagglehub
- **Project Issues**: Check `docs/` folder for more guides

---

**Last Updated**: 2025-11-05  
**Version**: 1.0
