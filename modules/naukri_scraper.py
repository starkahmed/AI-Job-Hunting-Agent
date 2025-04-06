# ================================================================
# File: naukri_scraper.py
# Version: v1.1
# Description: Scraper to fetch job listings from Naukri
# ================================================================

def run_naukri_scraper(query, location):
    print(f"[Naukri] Running scraper for query='{query}' and location='{location}'")
    # Simulated scraping result
    return [
        {
            "title": f"{query} Analyst",
            "company": "Naukri Ltd",
            "location": location,
            "description": "Exciting role at Naukri.com",
            "url": "https://www.naukri.com/job-details/112233",
            "salary": "₹8 LPA",
            "source": "Naukri"
        }
    ]
