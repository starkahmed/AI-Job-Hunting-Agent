# ================================================================
# File: feedback_generator.py
# Version: v5.5
# Description: Generates AI feedback for resume improvement and job suitability.
# ================================================================

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_resume_feedback(resume_text: str, job_title: str = "") -> str:
    """
    Uses OpenAI to provide feedback on the resume. Tailors advice to job title if given.
    """
    if not resume_text:
        return "No resume text provided."

    prompt = f"""
    You are an expert career advisor. Analyze the following resume and provide:
    1. Strengths of the resume.
    2. Weak areas that need improvement.
    3. Suggestions to improve clarity, formatting, and keyword optimization.
    {f"4. Tailored suggestions for the job title: {job_title}." if job_title else ""}

    Resume:
    {resume_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI resume advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating feedback: {str(e)}"

def generate_resume_summary(resume_text: str) -> str:
    """
    Returns a short professional summary of the resume using GPT.
    """
    prompt = f"""
    Summarize the following resume into a short 3-5 sentence professional summary:

    Resume:
    {resume_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"