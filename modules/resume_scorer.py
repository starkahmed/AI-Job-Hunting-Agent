# ================================================================
# File: modules/resume_scorer.py
# Version: v1.1
# Description: Score resume content and generate AI-based feedback
# ================================================================

import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# =================== Resume Scoring =====================

def score_resume(resume_text: str) -> dict:
    """
    Scores the resume based on relevance, clarity, format, and skills.
    Returns a dictionary with individual scores and total score.
    """
    prompt = f"""
You are an expert resume evaluator. Analyze the following resume and score it in the following categories (each out of 10):
- Relevance to tech industry jobs
- Clarity & structure
- Skills & technologies
- Formatting & layout
Then calculate a total score (out of 40). Give brief explanation for each score.

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond in JSON format like this:
{{
  "relevance": 8,
  "clarity": 7,
  "skills": 6,
  "formatting": 9,
  "total_score": 30,
  "feedback": {{
    "relevance": "Relevant experience but missing recent tools.",
    "clarity": "Well-structured with a few long paragraphs.",
    "skills": "Good coverage of web dev, but no mention of cloud tech.",
    "formatting": "Clean and ATS-friendly."
  }}
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        result = response.choices[0].message.content
        return eval(result)  # Assumes OpenAI returns clean JSON-like dict
    except Exception as e:
        return {
            "error": str(e),
            "relevance": 0,
            "clarity": 0,
            "skills": 0,
            "formatting": 0,
            "total_score": 0,
            "feedback": {
                "relevance": "Error scoring resume.",
                "clarity": "",
                "skills": "",
                "formatting": ""
            }
        }

# =================== Resume vs Job Match Scoring (v1.1+) =====================

def score_resume_against_job(resume_text: str, job_description: str) -> int:
    """
    Returns a simple match score (0-100) based on keyword overlap between resume and job description.
    """
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    if not job_words:
        return 0
    overlap = resume_words & job_words
    return int(len(overlap) / len(job_words) * 100)

# =================== Feedback Only (optional) =====================

def generate_resume_feedback(resume_text: str) -> str:
    """
    Generates general improvement suggestions for the resume.
    """
    prompt = f"""
You are a professional career coach. Read the resume below and provide improvement suggestions in 5 bullet points.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career coach and resume expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating feedback: {str(e)}"
