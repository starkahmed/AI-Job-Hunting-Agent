# ================================================================
# File: job_search.py
# Version: v1.3
# Description: Unified job scraper that runs all integrated sources and saves jobs to DB
# ================================================================

import sqlite3
from modules.linkedin_scraper import run_linkedin_scraper
from modules.indeed_scraper import run_indeed_scraper
from modules.naukri_scraper import run_naukri_scraper
from modules.glassdoor_scraper import run_glassdoor_scraper
from time import sleep

# Path to SQLite DB
DB_PATH = "jobs.db"

# =================== Create Jobs Table =====================

def create_jobs_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
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

# =================== Save Job to DB =====================

def save_job_to_db(job):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO jobs (title, company, location, description, url, salary, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            job["title"],
            job["company"],
            job["location"],
            job["description"],
            job["url"],
            job.get("salary", ""),
            job["source"]
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to save job to DB: {e}")

# =================== Run All Scrapers =====================

def run_all_scrapers(query, location):
    print("[JobSearch] Starting unified scraping for all sources...")
    all_sources = [
        ("LinkedIn", run_linkedin_scraper),
        ("Indeed", run_indeed_scraper),
        ("Naukri", run_naukri_scraper),
        ("Glassdoor", run_glassdoor_scraper),
    ]

    for source_name, scraper_fn in all_sources:
        try:
            print(f"[{source_name}] Running scraper...")
            jobs = scraper_fn(query, location)
            print(f"[{source_name}] Retrieved {len(jobs)} jobs")

            for job in jobs:
                save_job_to_db(job)

        except Exception as e:
            print(f"[{source_name} ERROR] Scraper failed: {e}")

        sleep(1)  # Be nice to servers or APIs

    print("[JobSearch] All sources scraped and saved successfully.")
