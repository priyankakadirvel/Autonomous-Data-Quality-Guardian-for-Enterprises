# ------------------------------------------------------------
# Autonomous Data Quality Guardian - Main Orchestrator
# ------------------------------------------------------------
# 
#   End-to-end orchestrator for Autonomous Data Quality Guardian
#   Handles data ingestion (CSV, DB, API, Web),
#   performs data quality checks, drift & anomaly detection,
#   invokes LLM reasoning, triggers alerts, and runs
#   Great Expectations validation.
# ------------------------------------------------------------

from src.utils.logger import setup_logger
from src.utils.file_handler import archive_report
from src.utils.config_validator import validate_all_configs

from src.ingest.ingest_manager import load_all_sources, load_thresholds
from src.quality.data_quality_checker import calculate_quality_metrics
from src.quality.drift_detector import detect_drift
from src.quality.anomaly_detector import detect_anomalies
from src.agent.reasoning_agent import llm_reasoning
from src.agent.notifier import send_alert

# Great Expectations validation integration
from great_expectations_validation import (
    load_config,
    create_context,
    build_expectations,
    run_validation,
)

import json
import os


def run_great_expectations_validation():
    """Runs Great Expectations data validation on PostgreSQL source."""
    print("\nRunning Great Expectations Validation...")
    cfg = load_config()
    context = create_context(cfg)

    schema_path = os.path.join("data", "inferred_schema.json")
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = json.load(f)
    else:
        schema = {"columns": []}

    build_expectations(context, cfg, schema)
    results = run_validation(context, cfg)
    print("GE Validation Complete.\n")
    return results


def main():
    logger = setup_logger()

    logger.info("Starting Autonomous Data Quality Guardian Pipeline...")

    # Step 0: Validate Configurations
    if not validate_all_configs():
        logger.error("Configuration validation failed. Fix issues before running again.")
        return
    logger.info("Configuration Validation Passed.")

    # Step 1: Load Data Sources & Thresholds
    sources = load_all_sources()
    thresholds = load_thresholds()

    csv_df = sources.get("CSV_SOURCE")
    api_df = sources.get("API_SOURCE")

    # Step 2: Data Quality Check
    quality_report = calculate_quality_metrics(csv_df)
    logger.info(f"Data Quality Report: {quality_report}")

    # Step 3: Drift Detection
    drift_report = detect_drift(csv_df, api_df, ["Open", "Close", "Volume"])
    logger.info(f"Drift Report: {drift_report}")

    # Step 4: Anomaly Detection
    anomaly_report, _ = detect_anomalies(csv_df, ["Open", "Close", "Volume"])
    logger.info(f"Anomaly Report: {anomaly_report}")

    # Step 5: Agent Reasoning (LLM Summary)
    reasoning = llm_reasoning(quality_report, drift_report)
    logger.info(f"Agent Reasoning: {reasoning}")

    # Step 6: Conditional Alerting
    if quality_report["completeness"] < thresholds["data_quality"]["completeness"]:
        send_alert("Completeness below threshold!", "High")
        logger.warning("Completeness below acceptable threshold!")

    # Step 7: Archive Quality Reports
    combined_report = {
        "data_quality": quality_report,
        "drift": drift_report,
        "anomalies": anomaly_report,
        "agent_reasoning": reasoning,
    }
    report_path = archive_report(combined_report)
    logger.info(f"Reports archived at: {report_path}")

    # Step 8: Run Great Expectations Validation
    # ge_results = run_great_expectations_validation()
    # logger.info(f"Great Expectations Validation Summary: {ge_results}")

    logger.info("Autonomous Data Quality Guardian Execution Completed Successfully.")


if __name__ == "__main__":
    main()
