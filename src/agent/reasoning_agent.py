# This script will contain the logic for the reasoning agent.

def llm_reasoning(data_quality_report, drift_report):
    print("Agent Reasoning about Data Quality...")
    # Mock reasoning output (you can later connect to GPT)
    issues = [col for col, val in drift_report.items() if "Drift" in val]
    summary = f"Detected drifts in {issues}. Recommend checking API refresh timing."
    reasoning_output = {
        "summary": summary,
        "impact": "Medium" if issues else "Low",
        "action": "Trigger API update and notify data team." if issues else "All stable."
    }
    return reasoning_output
