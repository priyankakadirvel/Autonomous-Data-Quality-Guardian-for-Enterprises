# This script will contain the logic for detecting anomalies in data.

import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, numerical_cols, contamination=0.05):
    """
    Detect anomalies in numerical columns using Isolation Forest.
    Args:
        df (pd.DataFrame): Input dataframe
        numerical_cols (list): List of numerical column names
        contamination (float): Percentage of data expected to be anomalous (0.01 - 0.1)
    Returns:
        dict: Column-wise anomaly summary and anomaly-tagged dataframe
    """
    print("Running Anomaly Detection...")
    anomalies_report = {}
    df_anomaly = df.copy()

    try:
        for col in numerical_cols:
            if col not in df.columns:
                continue

            # Convert to numeric and drop NaNs
            series = pd.to_numeric(df[col], errors="coerce").dropna().values.reshape(-1, 1)

            # Initialize Isolation Forest
            iso = IsolationForest(contamination=contamination, random_state=42)
            preds = iso.fit_predict(series)

            # Create anomaly flag
            mask = pd.Series(preds, index=df.index[:len(preds)])
            df_anomaly[f"{col}_Anomaly"] = mask.map({1: 0, -1: 1})  # 1 → anomaly detected

            anomalies_report[col] = {
                "anomalies_detected": int(df_anomaly[f"{col}_Anomaly"].sum()),
                "percentage": round(df_anomaly[f"{col}_Anomaly"].mean() * 100, 2)
            }

        print("Anomaly Detection Complete.")
        return anomalies_report, df_anomaly

    except Exception as e:
        print(f"Error in anomaly detection: {e}")
        return {}, df

