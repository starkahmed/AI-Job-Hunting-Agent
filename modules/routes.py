# ===============================================================
# File: routes.py
# Version: v6.0
# Description: FastAPI route definitions for AI Job Hunting Agent.
# ===============================================================

from fastapi import APIRouter, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

# ====== Import internal modules ======
from modules import (
    resume_parser, job_search, favorite_manager,
    feedback_generator, cover_letter_generator,
    resume_scorer, dashboard_manager, analytics_engine
)

# Initialize the FastAPI router
router = APIRouter()

# Initialize Jinja2 templates for rendering HTML pages
templates = Jinja2Templates(directory="templates")

# ====== Global cache for resume & extracted data ======
# These variables store the user's uploaded resume text and parsed skills
user_resume_text = ""
user_parsed_skills = []

# ====== Routes ======

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the home page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload_resume")
async def upload_resume(request: Request, file: UploadFile):
    """
    Handle resume upload, extract text and skills, and render the updated home page.
    """
    global user_resume_text, user_parsed_skills
    # Extract text from the uploaded resume
    user_resume_text = await resume_parser.extract_text(file)
    # Extract skills from the resume text
    user_parsed_skills = resume_parser.extract_skills(user_resume_text)
    # Render the home page with the extracted resume text and skills
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume_text": user_resume_text,
        "skills": user_parsed_skills,
    })


@router.get("/search_jobs")
async def search_jobs(request: Request, query: str = Form(...), location: str = Form("remote")):
    """
    Search for jobs based on the query and location, and render the results.
    """
    # Perform a unified job search
    results = job_search.unified_job_search(query=query, location=location)
    # Render the home page with the job search results
    return templates.TemplateResponse("index.html", {
        "request": request,
        "jobs": results,
        "resume_text": user_resume_text
    })


@router.post("/match_score")
async def match_score(job_description: str):
    """
    Calculate the match score between the user's resume and a job description.
    """
    # Score the resume against the job description
    score = resume_scorer.score_resume(user_resume_text, job_description)
    # Generate suggestions for improving the resume
    suggestions = resume_scorer.suggest_improvements(user_resume_text)
    return {"score": score, "suggestions": suggestions}


@router.post("/generate_cover_letter")
async def generate_cover_letter(job_description: str, job_title: Optional[str] = ""):
    """
    Generate a cover letter based on the user's resume and job description.
    """
    # Generate a cover letter using the resume text and job description
    letter = cover_letter_generator.generate_cover_letter(
        resume_text=user_resume_text,
        job_description=job_description,
        job_title=job_title
    )
    return {"cover_letter": letter}


@router.post("/feedback")
async def get_feedback():
    """
    Generate feedback for the user's resume.
    """
    # Generate feedback for the uploaded resume
    feedback = feedback_generator.generate_feedback(user_resume_text)
    return {"feedback": feedback}


@router.post("/add_favorite")
async def add_favorite(job_id: str, job_data: dict):
    """
    Add a job to the user's list of favorites.
    """
    # Add the job to the favorites list
    favorite_manager.add_to_favorites(job_id, job_data)
    return {"status": "Job added to favorites."}


@router.get("/favorites")
async def view_favorites(request: Request):
    """
    View the user's list of favorite jobs.
    """
    # Retrieve the list of favorite jobs
    favorites = favorite_manager.get_favorites()
    # Render the favorites page with the list of favorite jobs
    return templates.TemplateResponse("favorites.html", {"request": request, "favorites": favorites})


@router.get("/dashboard")
async def dashboard(request: Request):
    """
    View the user's dashboard with metrics and analytics.
    """
    # Generate dashboard metrics based on the user's resume
    metrics = dashboard_manager.generate_dashboard(user_resume_text)
    # Generate analytics based on the user's resume
    analytics = analytics_engine.generate_analytics(user_resume_text)
    # Render the dashboard page with metrics and analytics
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "metrics": metrics,
        "analytics": analytics
    })