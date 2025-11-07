# This script will contain the logic for checking data quality.

import pandas as pd

def calculate_quality_metrics(df):
    print("Calculating Data Quality Metrics...")
    total_cells = df.shape[0] * df.shape[1]
    metrics = {
        "completeness": round(1 - df.isnull().sum().sum() / total_cells, 3),
        "uniqueness": round(1 - (df.duplicated().sum() / len(df)), 3),
        "numeric_validity": round((df.select_dtypes("number") >= 0).mean().mean(), 3)
    }
    return metrics
