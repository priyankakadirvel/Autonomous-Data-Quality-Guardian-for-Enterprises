# This script will contain the logic for validating data schemas.
def validate_schema(current_df, baseline_columns):
    missing_cols = [col for col in baseline_columns if col not in current_df.columns]
    extra_cols = [col for col in current_df.columns if col not in baseline_columns]
    return {"missing_columns": missing_cols, "extra_columns": extra_cols}
