# This script will contain the logic for loading data from CSV files.

import pandas as pd

def load_csv_data(path="data/csv_source/sp500_stocks.csv"):
    print("Loading CSV Data...")
    try:
        df = pd.read_csv(path)
        print(f"CSV Loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()
