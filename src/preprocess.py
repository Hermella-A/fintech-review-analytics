"""
Preprocessing module for Google Play Store reviews.
Handles cleaning, deduplication, date normalisation, and saving.
"""
import os
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw CSV file with error handling."""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows from {filepath}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading file: {e}")
        raise

def remove_duplicates(df: pd.DataFrame, subset: str = 'review') -> pd.DataFrame:
    """Remove duplicate reviews based on text."""
    initial = len(df)
    df = df.drop_duplicates(subset=subset)
    logger.info(f"Removed {initial - len(df)} duplicate reviews")
    return df

def drop_missing(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """Drop rows with missing values in specified columns."""
    if columns is None:
        columns = ['review', 'rating']
    initial = len(df)
    df = df.dropna(subset=columns)
    logger.info(f"Dropped {initial - len(df)} rows with missing values")
    return df

def normalise_dates(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
    """Convert date column to YYYY-MM-DD format."""
    try:
        df[date_col] = pd.to_datetime(df[date_col]).dt.date
        logger.info("Date normalisation successful")
    except Exception as e:
        logger.error(f"Date conversion error: {e}")
        raise
    return df

def ensure_rating_type(df: pd.DataFrame, rating_col: str = 'rating') -> pd.DataFrame:
    """Ensure rating column is integer type."""
    df[rating_col] = df[rating_col].astype(int)
    logger.info("Rating column converted to integer")
    return df

def select_columns(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """Select only required columns."""
    if columns is None:
        columns = ['review', 'rating', 'date', 'bank', 'source']
    return df[columns]

def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned DataFrame to CSV, creating directory if needed."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Cleaned data saved to {output_path}")

def preprocess_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    """Run full preprocessing pipeline."""
    logger.info("Starting preprocessing pipeline")
    df = load_raw_data(input_path)
    df = remove_duplicates(df)
    df = drop_missing(df)
    df = normalise_dates(df)
    df = ensure_rating_type(df)
    df = select_columns(df)
    save_cleaned_data(df, output_path)
    logger.info("Preprocessing completed successfully")
    return df

if __name__ == "__main__":
    # Example usage when run as script
    preprocess_pipeline('data/raw/raw_reviews.csv', 'data/raw/cleaned_reviews.csv')