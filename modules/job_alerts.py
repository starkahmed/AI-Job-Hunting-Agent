# ===============================================================
# File: job_alerts.py
# Version: v6.0
# Description: Module to generate and manage daily job alerts for users.
# ===============================================================

import json
import os
from datetime import datetime
from unified_job_search import search_jobs
from user_preferences import get_preferences_for_user

ALERTS_DIR = "data/job_alerts"
os.makedirs(ALERTS_DIR, exist_ok=True)

# Utility to save alerts to a file for each user
def save_alerts_for_user(username, alerts):
    path = os.path.join(ALERTS_DIR, f"{username}_alerts.json")
    with open(path, "w") as f:
        json.dump({"alerts": alerts, "timestamp": datetime.utcnow().isoformat()}, f, indent=4)

# Utility to load saved alerts for display on dashboard or notifications
def get_alerts_for_user(username):
    path = os.path.join(ALERTS_DIR, f"{username}_alerts.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"alerts": [], "timestamp": None}

# Core function to generate job alerts using preferences and unified search
def generate_daily_alerts(username):
    preferences = get_preferences_for_user(username)
    query = preferences.get("keywords", "")
    location = preferences.get("location", "Remote")

    results = search_jobs(query=query, location=location)
    top_alerts = results[:10]  # Limit alerts to top 10 matches

    save_alerts_for_user(username, top_alerts)
    return top_alerts
