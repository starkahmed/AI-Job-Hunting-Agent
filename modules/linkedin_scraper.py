# ================================================================
# File: linkedin_scraper.py
# Version: v5.5
# Description: Scrapes job listings from LinkedIn based on query and location.
# Integrates into the unified job search system with match scoring support.
# ================================================================

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def run_linkedin_scraper(query: str, location: str = "India", max_results: int = 10) -> List[Dict]:
    """
    Scrapes LinkedIn jobs based on query and location.
    Returns a list of job dicts with keys: title, company, location, description, link, source.
    """
    jobs = []
    try:
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&trk=public_jobs_jobs-search-bar_search-submit"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("li", class_="result-card job-result-card result-card--with-hover-state")

        for idx, card in enumerate(job_cards[:max_results]):
            title_tag = card.find("h3", class_="result-card__title")
            company_tag = card.find("h4", class_="result-card__subtitle")
            location_tag = card.find("span", class_="job-result-card__location")
            link_tag = card.find("a", class_="result-card__full-card-link")

            job = {
                "title": title_tag.text.strip() if title_tag else "N/A",
                "company": company_tag.text.strip() if company_tag else "N/A",
                "location": location_tag.text.strip() if location_tag else location,
                "description": "Details not available. Click to view on LinkedIn.",
                "link": link_tag['href'] if link_tag else "",
                "source": "LinkedIn"
            }
            jobs.append(job)

    except Exception as e:
        print(f"[LinkedIn Scraper] Error: {str(e)}")

    return jobs
