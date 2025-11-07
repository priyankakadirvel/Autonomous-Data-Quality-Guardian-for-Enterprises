import os
import yaml
import requests
from pathlib import Path

def load_yaml(file_path):
    """Utility to safely load YAML files."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None


def validate_data_sources(config_path="config/data_sources.yaml"):
    """Validate data source configuration."""
    print("\n Validating Data Source Configurations...")
    cfg = load_yaml(config_path)
    if not cfg or "sources" not in cfg:
        print("Missing or invalid data_sources.yaml structure.")
        return False

    sources = cfg["sources"]
    all_valid = True

    for name, src in sources.items():
        if not src.get("enabled", False):
            print(f"{name} is disabled. Skipping validation.")
            continue

        print(f"Checking {name} ({src.get('name')})...")

        # Check file paths
        if "path" in src:
            path = Path(src["path"])
            if not path.exists():
                print(f"Missing file: {path}")
                all_valid = False
            else:
                print(f"Found data file: {path}")

        # Check API connectivity
        if "base_url" in src:
            try:
                test_params = {
                    "function": src.get("function", "TIME_SERIES_DAILY"),
                    "symbol": src.get("symbol", "AAPL"),
                    "apikey": src.get("api_key", "")
                }
                res = requests.get(src["base_url"], params=test_params, timeout=5)
                if res.status_code == 200:
                    print("API connection successful.")
                else:
                    print(f"API response error (status {res.status_code})")
            except Exception as e:
                print(f"API connection failed: {e}")
                all_valid = False

    return all_valid


def validate_db_config(config_path="config/db_config.yaml"):
    """Validate DB config structure."""
    print("\n Validating Database Configurations...")
    cfg = load_yaml(config_path)
    if not cfg:
        print("Missing db_config.yaml.")
        return False

    for db_type, params in cfg.items():
        if not all(k in params for k in ["host", "user", "password", "database"]):
            print(f"Incomplete credentials for {db_type}.")
            return False
        print(f"{db_type.capitalize()} configuration looks valid.")
    return True


def validate_thresholds(config_path="config/thresholds.yaml"):
    """Validate thresholds.yaml file."""
    print("\n Validating Threshold Settings...")
    cfg = load_yaml(config_path)
    if not cfg:
        print("thresholds.yaml not found or invalid.")
        return False

    try:
        dq = cfg.get("data_quality", {})
        if not (0 < dq.get("completeness", 0) <= 1 and 0 < dq.get("uniqueness", 0) <= 1):
            print("Data quality thresholds must be between 0 and 1.")
            return False
        print("Threshold values appear valid.")
        return True
    except Exception as e:
        print(f"Threshold validation error: {e}")
        return False


def validate_all_configs():
    """Run all config validation checks together."""
    print("\nStarting Configuration Validation...\n")
    ds_ok = validate_data_sources()
    db_ok = validate_db_config()
    th_ok = validate_thresholds()

    all_ok = ds_ok and db_ok and th_ok
    print("\n Configuration Validation Status:",
          "ALL GOOD " if all_ok else "FAILED")

    return all_ok


# Entry point when run directly
if __name__ == "__main__":
    validate_all_configs()
