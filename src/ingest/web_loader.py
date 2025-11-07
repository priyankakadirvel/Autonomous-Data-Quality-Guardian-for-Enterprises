# This script will contain the logic for loading data from a web source.

import pandas as pd

def load_web_data(path="data/webscraped/raw_finance_dataset.csv"):
    print("Loading Webscraped Data...")
    try:
        df = pd.read_csv(path, skiprows=2)  # skip metadata rows
        df.columns = df.iloc[0]  # fix headers
        df = df[1:]
        print(f"Webscraped Data Loaded. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading web data: {e}")
        return pd.DataFrame()
