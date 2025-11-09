# This script will contain the logic for handling files.
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def ensure_dir_exists(directory):
    """Create a directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def save_json(data, file_path):
    """Save any dictionary as a JSON file."""
    ensure_dir_exists(os.path.dirname(file_path))
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"JSON file saved -> {file_path}")


def load_json(file_path):
    """Load a JSON file if it exists."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}")
        return {}


def save_dataframe(df, file_path):
    """Save a pandas DataFrame to CSV."""
    ensure_dir_exists(os.path.dirname(file_path))
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved -> {file_path}")


def timestamped_filename(prefix, extension=".json"):
    """Generate a timestamped file name."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}{extension}"


def archive_report(data, folder="data/reports", prefix="data_quality_report"):
    """Save a timestamped report to /data/reports/"""
    ensure_dir_exists(folder)
    file_name = timestamped_filename(prefix)
    file_path = os.path.join(folder, file_name)
    save_json(data, file_path)
    return file_path
