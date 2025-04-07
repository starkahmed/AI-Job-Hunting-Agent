# ================================================================
# File: resume_scorer.py
# Version: v5.5
# Description: Scores resume against job description and identifies
#              missing keywords and skills.
# ================================================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

def score_resume_against_job(resume_text: str, job_description: str) -> float:
    """
    Computes a cosine similarity score between resume text and job description.
    Returns a float between 0 and 1.
    """
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score, 2)

def find_missing_keywords(resume_text: str, job_description: str) -> list:
    """
    Identifies key terms in the job description that are missing from the resume.
    """
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    resume_tokens = set(resume_text.split())
    job_tokens = set(job_description.split())

    missing = job_tokens - resume_tokens
    # Optional: Filter to remove common/stop words (or use NLP libraries)
    return list(missing)

def analyze_resume_vs_job(resume_text: str, job_description: str) -> dict:
    """
    Returns both score and list of missing keywords.
    """
    score = score_resume_against_job(resume_text, job_description)
    missing_keywords = find_missing_keywords(resume_text, job_description)
    
    return {
        "match_score": score,
        "missing_keywords": missing_keywords
    }
