# This script will contain the logic for sending notifications.
import smtplib

def send_alert(summary, impact):
    print(" Sending Notification...")
    print(f"ALERT: {summary} | Impact: {impact}")
    # Mock alert system (future: integrate Slack or email)
