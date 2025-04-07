# ================================================================
# File: cover_letter_generator.py
# Version: v5.5
# Description: Uses OpenAI to generate a personalized cover letter
#              based on resume and job description.
# ================================================================

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(resume_text: str, job_description: str, job_title: str = "") -> str:
    """
    Generates a personalized cover letter using OpenAI's GPT model.
    """
    if not resume_text or not job_description:
        return "Insufficient information to generate a cover letter."

    prompt = f"""
You are a professional career assistant. Write a personalized and compelling cover letter for the following job:

Job Title: {job_title if job_title else "Unknown"}
Job Description:
{job_description}

Candidate's Resume:
{resume_text}

Make sure the tone is confident, concise, and tailored to the job description. Highlight the most relevant skills and achievements from the resume.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career assistant who writes excellent, ATS-friendly cover letters."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

