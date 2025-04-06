# ================================================================
# File: create_jobs_table.py
# Version: v1.0
# Description: Script to initialize the jobs table in jobs.db
# Usage: Run once using `python create_jobs_table.py`
# ================================================================

import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create the 'jobs' table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    description TEXT,
    url TEXT,
    salary TEXT,
    source TEXT
);
""")

# Save and close the connection
conn.commit()
conn.close()

print("✅ 'jobs' table created successfully in jobs.db.")
