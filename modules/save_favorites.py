# File: modules/save_favorites.py
# Description: Save selected job listings to local JSON file

import json
import os

FAVORITE_FILE = "saved_jobs.json"

def save_favorite_json(job):
    if not os.path.exists(FAVORITE_FILE):
        with open(FAVORITE_FILE, "w") as f:
            json.dump([job], f, indent=2)
    else:
        with open(FAVORITE_FILE, "r+") as f:
            data = json.load(f)
            data.append(job)
            f.seek(0)
            json.dump(data, f, indent=2)
