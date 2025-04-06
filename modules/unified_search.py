from modules.job_search import get_adzuna_jobs
from modules.glassdoor_scraper import search_jobs as glassdoor_jobs
from modules.indeed_scraper import search_jobs as indeed_jobs
from modules.naukri_scraper import search_jobs as naukri_jobs
from modules.linkedin_scraper import search_jobs as linkedin_jobs

def get_all_jobs(query, location="", min_salary=None, max_salary=None, experience=None):
    jobs = []
    jobs += get_adzuna_jobs(query, location, min_salary, max_salary, experience=experience)
    jobs += glassdoor_jobs(query, location, min_salary, max_salary, experience)
    jobs += indeed_jobs(query, location, min_salary, max_salary, experience)
    jobs += naukri_jobs(query, location, min_salary, max_salary, experience)
    jobs += linkedin_jobs(query, location, min_salary, max_salary, experience)
    return jobs
