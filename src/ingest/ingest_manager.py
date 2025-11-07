import yaml
from pathlib import Path

from src.ingest.csv_loader import load_csv_data
from src.ingest.db_loader import load_db_data
from src.ingest.api_loader import fetch_api_data
from src.ingest.web_loader import load_web_data


def load_config(file_path):
    """Helper function to load YAML configuration files."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file {file_path}: {e}")
        return {}


def load_all_sources():
    """Load all data sources dynamically based on config/data_sources.yaml"""
    print("\nLoading Data Sources from Configuration...\n")

    # Load source configuration
    config_path = Path("config/data_sources.yaml")
    sources_cfg = load_config(config_path).get("sources", {})

    loaded_sources = {}

    for source_name, params in sources_cfg.items():
        if not params.get("enabled", False):
            print(f"Skipping disabled source: {source_name}")
            continue

        print(f"Loading Source: {params['name']}")

        if source_name == "csv_source":
            df = load_csv_data(params["path"])

        elif source_name == "db_source":
            df = load_db_data()  # Simulated for now, could use db_config.yaml

        elif source_name == "api_source":
            df = fetch_api_data(
                symbol=params["symbol"],
                api_key=params["api_key"]
            )

        elif source_name == "web_source":
            df = load_web_data(params["path"])

        else:
            print(f" Unknown source type: {source_name}")
            continue

        loaded_sources[source_name.upper()] = df

    print("\nAll Enabled Data Sources Loaded Successfully!\n")
    return loaded_sources


def load_thresholds():
    """Load thresholds from config/thresholds.yaml"""
    thresholds_path = Path("config/thresholds.yaml")
    thresholds_cfg = load_config(thresholds_path)
    print("Loaded Threshold Settings:", thresholds_cfg)
    return thresholds_cfg


if __name__ == "__main__":
    sources = load_all_sources()
    thresholds = load_thresholds()

    print("\nLoaded Sources:", list(sources.keys()))
    print("Threshold Settings:", thresholds["data_quality"])
