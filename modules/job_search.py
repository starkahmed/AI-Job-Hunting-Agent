# ====================================================================
# File: job_search.py
# Version: v5.5
# Description: Unified job search across LinkedIn, Indeed, Naukri, Glassdoor
# ====================================================================

from modules.linkedin_scraper import run_linkedin_scraper
from modules.indeed_scraper import run_indeed_scraper
from modules.naukri_scraper import run_naukri_scraper
from modules.glassdoor_scraper import run_glassdoor_scraper
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../jobs.db')

# =================== Create Jobs Table =====================
def create_jobs_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            url TEXT,
            salary TEXT,
            source TEXT
        )
    ''')
    conn.commit()
    conn.close()

# =================== Insert Jobs =====================
def insert_jobs_to_db(jobs, source):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for job in jobs:
        c.execute('''
            INSERT INTO jobs (title, company, location, description, url, salary, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("description", ""),
            job.get("url", ""),
            job.get("salary", ""),
            source
        ))
    conn.commit()
    conn.close()

# =================== Run All Scrapers =====================
def run_all_scrapers(query: str, location: str):
    all_jobs = []

    print("Scraping LinkedIn...")
    linkedin_jobs = run_linkedin_scraper(query, location)
    insert_jobs_to_db(linkedin_jobs, "LinkedIn")
    all_jobs.extend(linkedin_jobs)

    print("Scraping Indeed...")
    indeed_jobs = run_indeed_scraper(query, location)
    insert_jobs_to_db(indeed_jobs, "Indeed")
    all_jobs.extend(indeed_jobs)

    print("Scraping Naukri...")
    naukri_jobs = run_naukri_scraper(query, location)
    insert_jobs_to_db(naukri_jobs, "Naukri")
    all_jobs.extend(naukri_jobs)

    print("Scraping Glassdoor...")
    glassdoor_jobs = run_glassdoor_scraper(query, location)
    insert_jobs_to_db(glassdoor_jobs, "Glassdoor")
    all_jobs.extend(glassdoor_jobs)

    print(f"Total jobs scraped: {len(all_jobs)}")
    return all_jobs