# ================================================================
# File: favorite_manager.py
# Version: v5.5
# Description: Manages user's favorite (saved) job listings.
# ================================================================

import json
import os

FAVORITES_FILE = "data/favorites.json"

def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=4)

def add_to_favorites(job):
    favorites = load_favorites()
    if job not in favorites:
        favorites.append(job)
        save_favorites(favorites)
        return True
    return False

def remove_from_favorites(job_id):
    favorites = load_favorites()
    updated = [job for job in favorites if job.get("id") != job_id]
    save_favorites(updated)
    return len(favorites) != len(updated)

def get_favorites():
    return load_favorites()

def is_favorited(job_id):
    favorites = load_favorites()
    return any(job.get("id") == job_id for job in favorites)
