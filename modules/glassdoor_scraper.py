# ==================================================================
# File: glassdoor_scraper.py
# Version: v5.5
# Description: Scrapes job listings from Glassdoor using search queries.
# Note: This module assumes Glassdoor public pages are being scraped
#       and not the authenticated API. For production, consider
#       using Puppeteer/Selenium or a Glassdoor API partner.
# ==================================================================

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://www.glassdoor.co.in/Job"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def run_glassdoor_scraper(query: str, location: str = "India") -> List[Dict]:
    """
    Scrapes Glassdoor for jobs matching the query and location.
    """
    jobs = []
    try:
        search_url = f"{BASE_URL}/{location.replace(' ', '-')}-{query.replace(' ', '-')}-jobs-SRCH_IL.0,5_IC2851180_KO6,20.htm"
        response = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        job_cards = soup.select('article.jobCard')

        for card in job_cards:
            title_elem = card.select_one('a.jobLink')
            company_elem = card.select_one('div.jobInfoItem.jobEmpolyerName')
            location_elem = card.select_one('div.jobInfoItem.empLoc')
            summary_elem = card.select_one('div.job-snippet')

            jobs.append({
                "title": title_elem.text.strip() if title_elem else "",
                "company": company_elem.text.strip() if company_elem else "",
                "location": location_elem.text.strip() if location_elem else location,
                "summary": summary_elem.text.strip() if summary_elem else "",
                "source": "Glassdoor"
            })

    except Exception as e:
        print(f"[Glassdoor Scraper Error] {e}")

    return jobs
