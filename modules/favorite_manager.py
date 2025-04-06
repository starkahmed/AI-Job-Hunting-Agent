# ================================================================
# File: modules/favorite_manager.py
# Version: v1.4+
# Description: Manage favorite job saving/loading from JSON
# ================================================================

import os
import json

FAV_FILE = "favorites.json"

def load_favorites():
    """Load saved jobs from the JSON file."""
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    """Save updated favorites list to JSON file."""
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, indent=2)
