import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(resume_text, job_description):
    prompt = f"""You are a helpful assistant that writes personalized cover letters. 
Resume:
{resume_text}

Job Description:
{job_description}

Write a concise and professional cover letter for this job, based on the resume.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating cover letter: {e}"
