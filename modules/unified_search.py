# ================================================================
# File: unified_search.py
# Version: v5.5
# Description: Aggregates job data from multiple sources (LinkedIn,
#              Indeed, Naukri, Glassdoor) for a unified job listing.
# ================================================================

from modules.linkedin_scraper import run_linkedin_scraper
from modules.indeed_scraper import run_indeed_scraper
from modules.naukri_scraper import run_naukri_scraper
from modules.glassdoor_scraper import run_glassdoor_scraper


def unified_job_search(query: str, location: str = "Remote") -> list:
    """
    Searches for jobs from LinkedIn, Indeed, Naukri, and Glassdoor.

    Args:
        query (str): Job title, keywords, or role.
        location (str): Preferred job location (city/state/country or Remote).

    Returns:
        List[Dict]: A unified list of jobs with source, title, company, and URL.
    """
    results = []

    try:
        linkedin_jobs = run_linkedin_scraper(query, location)
        indeed_jobs = run_indeed_scraper(query, location)
        naukri_jobs = run_naukri_scraper(query, location)
        glassdoor_jobs = run_glassdoor_scraper(query, location)

        for job in linkedin_jobs + indeed_jobs + naukri_jobs + glassdoor_jobs:
            results.append(job)

    except Exception as e:
        print(f"[ERROR] Unified Search failed: {str(e)}")

    return results
