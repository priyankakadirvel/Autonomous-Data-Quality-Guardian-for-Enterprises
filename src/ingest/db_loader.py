# ------------------------------------------------------------
# Database Loader Module
# ------------------------------------------------------------
# This script handles data ingestion from a database source.
# In this setup, we simulate database extraction using a CSV
# file (all_stocks_5yr.csv). Later, this can be upgraded to
# connect to a live database using SQLAlchemy.
# ------------------------------------------------------------

import pandas as pd
import os

def load_db_data(path="data/db_source/all_stocks_5yr.csv"):
    """
    Loads data from the database source (simulated as a CSV file).
    If the CSV file is not found, falls back to a small simulated dataset.
    """
    print("Attempting to load Database Source...")

    try:
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"Database Source Loaded Successfully: {path}")
            print(f"Shape: {df.shape}")
        else:
            print("Database file not found. Loading simulated sample data...")
            data = {
                "Date": ["2025-11-01", "2025-11-02", "2025-11-03"],
                "Ticker": ["AAPL", "AAPL", "AAPL"],
                "Open": [180.5, 182.2, 183.1],
                "High": [182.0, 184.1, 185.0],
                "Low": [179.8, 181.0, 182.5],
                "Close": [181.7, 183.5, 184.4],
                "Volume": [5000000, 5200000, 4800000]
            }
            df = pd.DataFrame(data)
            print(f"Simulated DB Data Loaded. Shape: {df.shape}")

        # Convert date column if exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        return df

    except Exception as e:
        print(f"Error loading DB data: {e}")
        return pd.DataFrame()
