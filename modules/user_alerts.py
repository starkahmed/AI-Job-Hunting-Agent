# ===============================================================
# File: user_alerts.py
# Version: v6.0
# Description: Handles daily job alerts based on user preferences.
# ===============================================================

import os
import json
from datetime import datetime
from job_search import unified_job_search
from user_preferences import get_preferences

ALERTS_DIR = "data/user_alerts"
os.makedirs(ALERTS_DIR, exist_ok=True)

def generate_daily_alerts(username: str):
    """Generate job alerts based on user preferences and save them."""
    preferences = get_preferences(username)
    query = " ".join(preferences.get("keywords", []))
    location = preferences.get("location", "Remote")
    job_types = preferences.get("job_types", ["Full-time"])
    salary_min = preferences.get("salary_min", 0)
    salary_max = preferences.get("salary_max", 1000000)

    jobs = unified_job_search(query=query, location=location, job_type=job_types)

    # Filter based on salary
    filtered = [job for job in jobs if job.get("salary", 0) >= salary_min and job.get("salary", 0) <= salary_max]

    alert_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "jobs": filtered[:10]  # limit to 10 jobs
    }

    with open(os.path.join(ALERTS_DIR, f"{username}.json"), "w") as f:
        json.dump(alert_data, f, indent=2)

def get_daily_alerts(username: str) -> dict:
    """Retrieve saved job alerts for the user."""
    filepath = os.path.join(ALERTS_DIR, f"{username}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {"date": None, "jobs": []}

def delete_alerts(username: str):
    """Remove user's job alert file."""
    filepath = os.path.join(ALERTS_DIR, f"{username}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
