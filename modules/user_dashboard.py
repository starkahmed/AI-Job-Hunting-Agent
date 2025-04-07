# ===============================================================
# File: user_dashboard.py
# Version: v6.0
# Description: Dashboard logic for authenticated users.
# ===============================================================

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from auth_manager import get_current_user
from favorite_manager import get_user_favorites
from application_tracker import get_user_applications
from resume_scorer import get_resume_summary

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Please log in to view your dashboard."})

    favorites = get_user_favorites(user["username"])
    applications = get_user_applications(user["username"])
    resume_summary = get_resume_summary(user["username"])

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "favorites": favorites,
        "applications": applications,
        "resume_summary": resume_summary
    })
