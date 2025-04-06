# ================================================================
# File: modules/save_favorites_sqlite.py
# Description: Save and load favorite jobs using SQLite database
# ================================================================

import sqlite3

DB_FILE = "favorites.db"

# Initialize table
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    description TEXT,
    url TEXT UNIQUE,
    salary TEXT,
    source TEXT
)
""")
conn.commit()
conn.close()

def save_favorite_sqlite(job):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO favorites (title, company, location, description, url, salary, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job["title"],
            job["company"],
            job["location"],
            job["description"],
            job["url"],
            job["salary"],
            job["source"]
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Job already saved.")
    finally:
        conn.close()

def get_saved_favorites():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, location, description, url, salary, source FROM favorites")
    jobs = cursor.fetchall()
    conn.close()
    return jobs
