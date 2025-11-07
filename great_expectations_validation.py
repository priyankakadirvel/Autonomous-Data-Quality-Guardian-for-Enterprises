# ------------------------------------------------------------
# Great Expectations Validation Script
# ------------------------------------------------------------
# This script connects to a PostgreSQL database,
# builds and runs dynamic data validation using
# Great Expectations.
# ------------------------------------------------------------

import great_expectations as gx
from sqlalchemy import create_engine
import yaml
import os
import json

# ------------------------------------------------------------
# Load database config
# ------------------------------------------------------------

def load_config():
    """Load PostgreSQL configuration details from YAML."""
    with open(os.path.join("config", "db_config.yaml"), "r") as f:
        return yaml.safe_load(f)["postgres"]

# ------------------------------------------------------------
# Create Great Expectations context and datasource (v1.0+)
# ------------------------------------------------------------
def create_context(cfg):
    """Initialize Great Expectations context and add Postgres datasource (new API)."""
    print("Creating Great Expectations context (v1.0+)...")

    import great_expectations as gx
    from great_expectations.data_context import FileDataContext

    # Create or load the GE context
    context = gx.get_context()  # This returns a FileDataContext

    # Define a PostgreSQL datasource configuration
    datasource_config = {
        "name": "postgres_datasource",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "SqlAlchemyExecutionEngine",
            "connection_string": (
                f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@"
                f"{cfg['host']}:{cfg['port']}/{cfg['database']}"
            ),
        },
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"],
            }
        },
    }

    # Add or update the datasource in the context
    context.add_datasource(**datasource_config)
    print("PostgreSQL Datasource added successfully (v1.0+ API).")

    return context


# ------------------------------------------------------------
# Build Expectations dynamically from inferred schema
# ------------------------------------------------------------
def build_expectations(context, cfg, schema):
    """Build Great Expectations rules dynamically from schema."""
    print("Building Great Expectations expectation suite...")

    suite_name = "data_quality_suite"
    suite = context.create_expectation_suite(suite_name, overwrite_existing=True)

    validator = context.get_validator(
        datasource_name="postgres_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=f"{cfg['schema']}.{cfg['table']}",
        create_expectation_suite_with_name=suite_name,
    )

    # Expect table to have rows
    validator.expect_table_row_count_to_be_greater_than(0)

    # Expect all columns from schema
    expected_columns = [col["name"] for col in schema.get("columns", [])]
    if expected_columns:
        validator.expect_table_columns_to_match_ordered_list(expected_columns)

    # Basic column-level rules
    for col in schema.get("columns", []):
        name = col["name"]
        dtype = col["type"].lower()
        validator.expect_column_values_to_not_be_null(name)

        if "char" in dtype or "text" in dtype:
            validator.expect_column_value_lengths_to_be_between(name, 1, 200)
        elif "int" in dtype or "float" in dtype or "double" in dtype or "numeric" in dtype:
            validator.expect_column_min_to_be_between(name, min_value=0, strict_min=False)

    context.save_expectation_suite(suite, suite_name)
    print("Expectation suite built successfully.")


# ------------------------------------------------------------
# Run Great Expectations validation
# ------------------------------------------------------------
def run_validation(context, cfg):
    """Run Great Expectations Checkpoint and build Data Docs."""
    print("Running data validation...")

    # Handle GE version compatibility
    try:
        from great_expectations.checkpoint import SimpleCheckpoint
        checkpoint_class = SimpleCheckpoint
    except ImportError:
        from great_expectations.checkpoint import Checkpoint
        checkpoint_class = Checkpoint

    checkpoint = checkpoint_class(
        name="data_quality_checkpoint",
        data_context=context,
        validations=[
            {
                "batch_request": {
                    "runtime_parameters": {
                        "query": f"SELECT * FROM {cfg['schema']}.{cfg['table']};"
                    },
                    "datasource_name": "postgres_datasource",
                    "data_connector_name": "default_runtime_data_connector_name",
                    "data_asset_name": f"{cfg['schema']}.{cfg['table']}",
                    "batch_identifiers": {"default_identifier_name": "default_id"},
                },
                "expectation_suite_name": "data_quality_suite",
            }
        ],
    )

    results = checkpoint.run()
    context.build_data_docs()
    print("Validation complete! View Data Docs at:")
    print("   uncommitted/data_docs/local_site/index.html")
    return results


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    print("Starting Great Expectations Validation...")

    cfg = load_config()
    context = create_context(cfg)

    schema_path = os.path.join("data", "inferred_schema.json")
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = json.load(f)
    else:
        schema = {"columns": []}

    build_expectations(context, cfg, schema)
    run_validation(context, cfg)
