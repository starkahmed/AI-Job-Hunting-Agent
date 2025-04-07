# ================================================================
# File: main.py
# Version: v5.5
# Description: FastAPI backend integrating resume parsing, unified job search,
#              scoring, enhancement, analytics, favorite management, and dashboard.
# ================================================================

from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import uvicorn
import os

# ====== Importing internal modules ======
from modules import (
    resume_parser, job_search, favorite_manager,
    feedback_generator, cover_letter_generator,
    resume_scorer, dashboard_manager, analytics_engine
)

# ====== FastAPI Setup ======
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ====== Global cache for resume & extracted data ======
user_resume_text = ""
user_parsed_skills = []

# ====== Routes ======

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_resume")
async def upload_resume(request: Request, file: UploadFile):
    global user_resume_text, user_parsed_skills
    user_resume_text = await resume_parser.extract_text(file)
    user_parsed_skills = resume_parser.extract_skills(user_resume_text)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume_text": user_resume_text,
        "skills": user_parsed_skills,
    })

@app.get("/search_jobs")
async def search_jobs(request: Request, query: str = Form(...), location: str = Form("remote")):
    results = job_search.unified_job_search(query=query, location=location)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "jobs": results,
        "resume_text": user_resume_text
    })

@app.post("/match_score")
async def match_score(job_description: str):
    score = resume_scorer.score_resume(user_resume_text, job_description)
    suggestions = resume_scorer.suggest_improvements(user_resume_text)
    return {"score": score, "suggestions": suggestions}

@app.post("/generate_cover_letter")
async def generate_cover_letter(job_description: str, job_title: Optional[str] = ""):
    letter = cover_letter_generator.generate_cover_letter(
        resume_text=user_resume_text,
        job_description=job_description,
        job_title=job_title
    )
    return {"cover_letter": letter}

@app.post("/feedback")
async def get_feedback():
    feedback = feedback_generator.generate_feedback(user_resume_text)
    return {"feedback": feedback}

@app.post("/add_favorite")
async def add_favorite(job_id: str, job_data: dict):
    favorite_manager.add_to_favorites(job_id, job_data)
    return {"status": "Job added to favorites."}

@app.get("/favorites")
async def view_favorites(request: Request):
    favorites = favorite_manager.get_favorites()
    return templates.TemplateResponse("favorites.html", {"request": request, "favorites": favorites})

@app.get("/dashboard")
async def dashboard(request: Request):
    metrics = dashboard_manager.generate_dashboard(user_resume_text)
    analytics = analytics_engine.generate_analytics(user_resume_text)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "metrics": metrics,
        "analytics": analytics
    })

# ====== Run App ======
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)