# ================================================================
# File: analytics_engine.py
# Version: v5.5
# Description: Provides analytics on job market trends, resume stats,
#              user engagement, and application tracking.
# ================================================================

from datetime import datetime
from typing import List, Dict
import statistics

class AnalyticsEngine:
    def __init__(self):
        self.applications = []
        self.job_views = []
        self.resume_scores = []
        self.job_sources = []

    def log_application(self, job_id: str, source: str, timestamp: str = None):
        timestamp = timestamp or datetime.now().isoformat()
        self.applications.append({"job_id": job_id, "source": source, "timestamp": timestamp})

    def log_job_view(self, job_id: str, source: str, timestamp: str = None):
        timestamp = timestamp or datetime.now().isoformat()
        self.job_views.append({"job_id": job_id, "source": source, "timestamp": timestamp})

    def log_resume_score(self, score: float):
        self.resume_scores.append(score)

    def log_source(self, source: str):
        self.job_sources.append(source)

    def get_resume_score_stats(self) -> Dict:
        if not self.resume_scores:
            return {"average": 0, "max": 0, "min": 0, "count": 0}
        return {
            "average": round(statistics.mean(self.resume_scores), 2),
            "max": max(self.resume_scores),
            "min": min(self.resume_scores),
            "count": len(self.resume_scores)
        }

    def get_job_source_distribution(self) -> Dict[str, int]:
        distribution = {}
        for source in self.job_sources:
            distribution[source] = distribution.get(source, 0) + 1
        return distribution

    def get_application_count_by_day(self) -> Dict[str, int]:
        daily_counts = {}
        for app in self.applications:
            date = app["timestamp"].split("T")[0]
            daily_counts[date] = daily_counts.get(date, 0) + 1
        return daily_counts

    def get_most_viewed_jobs(self, top_n: int = 5) -> List[str]:
        view_count = {}
        for view in self.job_views:
            job_id = view["job_id"]
            view_count[job_id] = view_count.get(job_id, 0) + 1
        return sorted(view_count, key=view_count.get, reverse=True)[:top_n]

    def summary(self) -> Dict:
        return {
            "resume_stats": self.get_resume_score_stats(),
            "application_trends": self.get_application_count_by_day(),
            "popular_jobs": self.get_most_viewed_jobs(),
            "job_source_distribution": self.get_job_source_distribution()
        }