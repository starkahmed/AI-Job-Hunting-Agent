# ===============================================================
# File: daily_alerts.py
# Version: v6.0
# Description: Module to send daily job alerts to users via email.
# ===============================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import get_registered_users, get_user_preferences
from job_search import run_unified_search

EMAIL_ADDRESS = "your_email@example.com"  # Replace with alert sender email
EMAIL_PASSWORD = "your_password"           # Replace with secure password or use env vars
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def generate_alert_content(username, preferences):
    # Generate job matches based on user preferences
    jobs = run_unified_search(preferences.get("role", ""), preferences.get("location", ""))
    message = f"Hi {username},\n\nHere are your latest job matches for today:\n\n"
    for job in jobs[:5]:
        message += f"- {job['title']} at {job['company']} ({job['location']})\n  {job['url']}\n\n"
    message += "\nGood luck with your job search!\n"
    return message

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"[✔] Alert sent to {to_email}")
    except Exception as e:
        print(f"[✖] Failed to send alert to {to_email}: {e}")

def send_daily_job_alerts():
    users = get_registered_users()
    for user in users:
        preferences = get_user_preferences(user["username"])
        if preferences:
            email_content = generate_alert_content(user["username"], preferences)
            send_email(user["email"], "Your Daily Job Matches", email_content)

# Optionally, this could be triggered via cron or background task in FastAPI
if __name__ == "__main__":
    send_daily_job_alerts()
