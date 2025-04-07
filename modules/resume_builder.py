# ===============================================================
# File: resume_builder.py
# Version: v6.0
# Description: AI-enhanced resume builder from parsed data + GPT.
# ===============================================================

import os
import openai
from resume_parser import parse_resume
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

RESUME_OUTPUT_DIR = "data/generated_resumes"
os.makedirs(RESUME_OUTPUT_DIR, exist_ok=True)

def generate_enhanced_resume(username: str, resume_path: str) -> str:
    """
    Parse resume and enhance content using GPT for improved formatting, clarity,
    and impact. Save to file and return path.
    """
    parsed = parse_resume(resume_path)

    prompt = f"""
    You're a resume optimization assistant. Based on the user's parsed resume data below,
    generate an ATS-friendly, well-structured, and professional resume in markdown format.
    
    Resume data:
    Name: {parsed.get('name')}
    Email: {parsed.get('email')}
    Skills: {parsed.get('skills')}
    Education: {parsed.get('education')}
    Experience: {parsed.get('experience')}
    Summary: {parsed.get('summary', 'N/A')}

    Highlight strengths, tailor language for tech/remote roles, and organize content cleanly.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    enhanced_md = response.choices[0].message.content.strip()
    output_path = os.path.join(RESUME_OUTPUT_DIR, f"{username}_enhanced.md")

    with open(output_path, "w") as f:
        f.write(enhanced_md)

    return output_path

def load_enhanced_resume(username: str) -> str:
    """Retrieve previously generated enhanced resume."""
    filepath = os.path.join(RESUME_OUTPUT_DIR, f"{username}_enhanced.md")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    return "Resume not generated yet. Please upload your resume."

def delete_enhanced_resume(username: str):
    """Remove user's generated resume."""
    filepath = os.path.join(RESUME_OUTPUT_DIR, f"{username}_enhanced.md")
    if os.path.exists(filepath):
        os.remove(filepath)
