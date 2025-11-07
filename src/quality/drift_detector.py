# This script will contain the logic for detecting data drift.

from scipy.stats import ks_2samp

def detect_drift(df1, df2, numerical_cols):
    print("Running Drift Detection...")
    drift_report = {}
    for col in numerical_cols:
        try:
            stat, p = ks_2samp(df1[col].dropna().astype(float),
                               df2[col].dropna().astype(float))
            drift_report[col] = " Drift Detected" if p < 0.05 else "✅ Stable"
        except Exception:
            drift_report[col] = "N/A"
    return drift_report
