# This script will contain the logic for loading data from an API.

import requests
import pandas as pd

def fetch_api_data(symbol="AAPL", api_key="1NQJYRYFBF7SRUOS"):
    print(f"Fetching API Data for {symbol}...")
    url = "https://www.alphavantage.co/query"
    params = {"function": "TIME_SERIES_DAILY", "symbol": symbol, "apikey": api_key}
    
    try:
        response = requests.get(url, params=params)
        data = response.json().get("Time Series (Daily)", {})
        if not data:
            print("API limit reached or invalid response.")
            return pd.DataFrame()

        df = pd.DataFrame(data).T
        df.reset_index(inplace=True)
        df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        df["Date"] = pd.to_datetime(df["Date"])
        print(f"API Data Loaded for {symbol}. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error fetching API data: {e}")
        return pd.DataFrame()
