# ===============================================================
# File: user_preferences.py
# Version: v6.0
# Description: Manages user job preferences for alerts, filters.
# ===============================================================

import json
import os

PREFERENCES_DIR = "data/user_preferences"
os.makedirs(PREFERENCES_DIR, exist_ok=True)

def get_preferences(username: str) -> dict:
    """Load user preferences from file."""
    filepath = os.path.join(PREFERENCES_DIR, f"{username}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {
        "location": "Remote",
        "keywords": [],
        "job_types": ["Full-time"],
        "salary_min": 0,
        "salary_max": 1000000
    }

def save_preferences(username: str, preferences: dict):
    """Save updated preferences for the user."""
    filepath = os.path.join(PREFERENCES_DIR, f"{username}.json")
    with open(filepath, "w") as f:
        json.dump(preferences, f, indent=2)

def update_preferences(username: str, field: str, value):
    """Update specific field in preferences."""
    preferences = get_preferences(username)
    preferences[field] = value
    save_preferences(username, preferences)

def delete_preferences(username: str):
    """Delete a user's preferences file."""
    filepath = os.path.join(PREFERENCES_DIR, f"{username}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
