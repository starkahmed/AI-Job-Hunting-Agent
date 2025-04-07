# ================================================================
# File: main.py
# Version: v3.6
# Description: FastAPI app with resume upload, parsing, scraping,
#              dynamic filtering, scoring, favorites, cover letters,
#              and analytics dashboard
# ================================================================

from fastapi import FastAPI, File, UploadFile, Form, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from modules.job_search import run_all_scrapers, create_jobs_table
from modules.resume_parser import parse_resume
from modules.resume_scorer import score_resume_against_job  # NEW
import sqlite3
import uuid
import os
import shutil
from collections import Counter

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "favorites.db")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize DB
create_jobs_table()

def init_fav_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            url TEXT,
            status TEXT DEFAULT 'Applied',
            match_score REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_fav_db()

# =================== Resume Upload =====================
@app.post("/upload_resume", response_class=HTMLResponse)
async def upload_resume(request: Request, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    parsed_resume = parse_resume(path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume": parsed_resume,
        "message": "✅ Resume uploaded successfully!"
    })

# =================== Trigger Scraping =====================
@app.post("/scrape_jobs")
def scrape_jobs(query: str = Form(...), location: str = Form("")):
    run_all_scrapers(query, location)
    return {"message": "Scraping complete"}

# =================== Get Filtered Job Listings =====================
@app.get("/jobs", response_class=HTMLResponse)
async def list_jobs(request: Request,
                    query: str = "",
                    location: str = "",
                    experience: str = "",
                    min_salary: int = 0,
                    max_salary: int = 999999):

    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("""
        SELECT id, title, company, location, description, url, salary, source
        FROM jobs
    """)
    rows = c.fetchall()
    conn.close()

    jobs = []
    for row in rows:
        job = {
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "description": row[4],
            "url": row[5],
            "salary": row[6] or "",
            "source": row[7]
        }

        if location.lower() not in job["location"].lower():
            continue
        if query.lower() not in job["title"].lower() and query.lower() not in job["description"].lower():
            continue

        try:
            sal = int("".join(filter(str.isdigit, job["salary"])))
            if not (min_salary <= sal <= max_salary):
                continue
        except:
            pass

        try:
            resume_text = request.query_params.get("resume") or ""
            if resume_text:
                job["match_score"] = score_resume_against_job(resume_text, job["description"])
        except:
            job["match_score"] = None

        jobs.append(job)

    return templates.TemplateResponse("job_list.html", {"request": request, "jobs": jobs})

# =================== Save Job to Favorites =====================
@app.post("/save")
async def save_job(title: str = Form(...), company: str = Form(...), location: str = Form(...), description: str = Form(...), url: str = Form(...), match_score: float = Form(0.0)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO favorites (title, company, location, description, url, match_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, company, location, description, url, match_score))
    conn.commit()
    conn.close()
    return {"message": "Job saved successfully"}

# =================== Show Favorite Jobs =====================
@app.get("/favorites", response_class=HTMLResponse)
async def show_favorites(request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, company, location, description, url, status, match_score FROM favorites ORDER BY id DESC")
    favorites = c.fetchall()
    conn.close()
    return templates.TemplateResponse("favorites.html", {"request": request, "favorites": favorites})

# =================== Remove Favorite Job =====================
@app.post("/remove_favorite")
async def remove_favorite(job_id: int = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return {"message": "Job removed from favorites"}

# =================== Update Job Status =====================
@app.post("/update_status")
async def update_status(job_id: int = Form(...), status: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE favorites SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()
    return {"message": "Status updated"}

# =================== Analytics Dashboard =====================
@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status, match_score FROM favorites")
    data = c.fetchall()
    conn.close()

    status_counts = Counter([row[0] for row in data])

    match_score_bins = {
        "0–50%": 0,
        "50–70%": 0,
        "70–90%": 0,
        "90–100%": 0
    }

    for _, score in data:
        score = score or 0
        score *= 100
        if score < 50:
            match_score_bins["0–50%"] += 1
        elif score < 70:
            match_score_bins["50–70%"] += 1
        elif score < 90:
            match_score_bins["70–90%"] += 1
        else:
            match_score_bins["90–100%"] += 1

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "status_data": dict(status_counts),
        "score_data": match_score_bins
    })

# =================== Home Page =====================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})