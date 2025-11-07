# This script will contain the logic for handling actions.

def adaptive_update(feedback, drift_thresholds):
    if feedback == "false_alarm":
        drift_thresholds["p_value"] += 0.01
    elif feedback == "missed_drift":
        drift_thresholds["p_value"] -= 0.01
    return drift_thresholds
