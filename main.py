from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import spacy
import openai

# Load spaCy NLP model for skill extraction
nlp = spacy.load("en_core_web_sm")

# Dummy job dataset (replace with API later)
jobs = [
    {"id": 1, "title": "Embedded Software Engineer", "skills": ["C++", "AUTOSAR", "Embedded Systems"]},
    {"id": 2, "title": "Cloud Engineer", "skills": ["GCP", "Docker", "Kubernetes"]},
    {"id": 3, "title": "Full Stack Developer", "skills": ["Python", "FastAPI", "React"]}
]

# OpenAI API Key (replace with your actual key)
openai.api_key = "your-openai-api-key"

app = FastAPI()

class ResumeFile(BaseModel):
    filename: str

# Extract skills from resume text
def extract_skills(text):
    doc = nlp(text)
    return list(set([token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]))

# AI Resume Refinement
def refine_resume(resume_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Improve this resume for better job matching."},
                  {"role": "user", "content": resume_text}]
    )
    return response["choices"][0]["message"]["content"]

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume_text = content.decode("utf-8")
    skills = extract_skills(resume_text)
    return {"extracted_skills": skills}

@app.post("/match-jobs/")
async def match_jobs(resume: ResumeFile):
    resume_skills = extract_skills(resume.filename)
    matched_jobs = [job for job in jobs if any(skill in job["skills"] for skill in resume_skills)]
    return {"matched_jobs": matched_jobs}

@app.post("/refine-resume/")
async def refine_resume_api(resume: ResumeFile):
    refined_text = refine_resume(resume.filename)
    return {"refined_resume": refined_text}
