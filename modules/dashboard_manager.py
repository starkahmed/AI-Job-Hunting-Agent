# ================================================================
# File: dashboard_manager.py
# Version: v5.5
# Description: Manages user dashboard data including job applications,
#              saved jobs, resume analytics, and job search insights.
# ================================================================

from typing import List, Dict
from datetime import datetime
import json
import os

DASHBOARD_DIR = "user_data/dashboard/"

os.makedirs(DASHBOARD_DIR, exist_ok=True)

def _get_dashboard_path(user_id: str) -> str:
    return os.path.join(DASHBOARD_DIR, f"{user_id}_dashboard.json")

def initialize_dashboard(user_id: str) -> None:
    path = _get_dashboard_path(user_id)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({
                "saved_jobs": [],
                "applications": [],
                "resume_scores": [],
                "cover_letters": [],
                "job_insights": [],
                "last_updated": str(datetime.utcnow())
            }, f)

def save_dashboard_data(user_id: str, data: dict) -> None:
    path = _get_dashboard_path(user_id)
    data["last_updated"] = str(datetime.utcnow())
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_dashboard_data(user_id: str) -> dict:
    path = _get_dashboard_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        initialize_dashboard(user_id)
        return get_dashboard_data(user_id)

def add_application(user_id: str, job_data: dict) -> None:
    dashboard = get_dashboard_data(user_id)
    dashboard["applications"].append(job_data)
    save_dashboard_data(user_id, dashboard)

def add_saved_job(user_id: str, job_data: dict) -> None:
    dashboard = get_dashboard_data(user_id)
    if job_data not in dashboard["saved_jobs"]:
        dashboard["saved_jobs"].append(job_data)
    save_dashboard_data(user_id, dashboard)

def add_resume_score(user_id: str, score_data: dict) -> None:
    dashboard = get_dashboard_data(user_id)
    dashboard["resume_scores"].append(score_data)
    save_dashboard_data(user_id, dashboard)

def add_cover_letter(user_id: str, letter_data: dict) -> None:
    dashboard = get_dashboard_data(user_id)
    dashboard["cover_letters"].append(letter_data)
    save_dashboard_data(user_id, dashboard)

def add_job_insight(user_id: str, insight_data: dict) -> None:
    dashboard = get_dashboard_data(user_id)
    dashboard["job_insights"].append(insight_data)
    save_dashboard_data(user_id, dashboard)
