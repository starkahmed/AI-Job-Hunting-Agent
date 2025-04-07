# ================================================================
# File: naukri_scraper.py
# Version: v5.5
# Description: Scrapes job listings from Naukri.com using search query and location.
# Integrates into the unified job search system.
# ================================================================

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def run_naukri_scraper(query: str, location: str = "India", max_results: int = 10) -> List[Dict]:
    """
    Scrapes jobs from Naukri.com based on the search query and location.
    Returns a list of job dictionaries.
    """
    jobs = []
    try:
        formatted_query = query.replace(" ", "-")
        formatted_location = location.replace(" ", "-")
        search_url = f"https://www.naukri.com/{formatted_query}-jobs-in-{formatted_location}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("article", class_="jobTuple")

        for idx, card in enumerate(job_cards[:max_results]):
            title_tag = card.find("a", class_="title")
            company_tag = card.find("a", class_="subTitle")
            location_tag = card.find("li", class_="location")
            link_tag = title_tag

            job = {
                "title": title_tag.text.strip() if title_tag else "N/A",
                "company": company_tag.text.strip() if company_tag else "N/A",
                "location": location_tag.text.strip() if location_tag else location,
                "description": "Click the link for job details on Naukri.",
                "link": link_tag['href'] if link_tag else "",
                "source": "Naukri"
            }
            jobs.append(job)

    except Exception as e:
        print(f"[Naukri Scraper] Error: {str(e)}")

    return jobs