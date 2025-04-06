# ================================================================
# File: glassdoor_scraper.py
# Version: v1.1
# Description: Scraper to fetch job listings and/or company insights from Glassdoor
# ================================================================

def run_glassdoor_scraper(query, location):
    print(f"[Glassdoor] Running scraper for query='{query}' and location='{location}'")
    # Simulate Glassdoor job scraping or API results
    return [
        {
            "title": f"{query} Specialist",
            "company": "Glassdoor Inc.",
            "location": location,
            "description": "Join our team at Glassdoor with competitive benefits.",
            "url": "https://www.glassdoor.com/job-listing/445566",
            "salary": "$95,000",
            "source": "Glassdoor"
        }
    ]
