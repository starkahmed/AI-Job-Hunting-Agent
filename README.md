🤖 AI Job Hunting Agent — v6.0
AI-powered job search assistant to discover, analyze, and apply for jobs with personalized tools including resume scoring, cover letter generation, application tracking, and more — all in one smart platform.

🚀 Features
🔍 Unified Job Search
Aggregates job listings from LinkedIn, Indeed, Naukri, and Glassdoor

📄 Resume Scoring & Feedback
AI evaluates resumes with match scores + improvement suggestions

✉️ Cover Letter Generator
Personalized, job-specific letters generated using GPT

⭐ Favorites & Tracking
Save jobs, mark statuses (applied/interviewed/offered), and manage in dashboard

📊 Smart Analytics Dashboard
Visualize your job search progress, resume performance, and AI insights

👥 Multi-user Sessions
Supports user-specific preferences, resumes, and application history

⚙️ User Preferences
Location, roles, industries saved and used for tailored search & scoring

🧠 Modular Backend Architecture
Built with FastAPI, modular Python components, and Jinja2 templates

job_agent_v6.0/
├── main.py                  # FastAPI entry point
├── routes.py                # All route handlers and sessions
├── modules/
│   ├── resume_parser.py           # Text extraction and skill parsing
│   ├── job_search.py              # Unified job search (Indeed, LinkedIn, etc.)
│   ├── cover_letter_generator.py  # GPT-based letter generation
│   ├── feedback_generator.py      # AI feedback & resume suggestions
│   ├── resume_scorer.py           # Job match scoring
│   ├── favorite_manager.py        # Save/view job favorites
│   ├── dashboard_manager.py       # App tracking + user metrics
│   └── analytics_engine.py        # AI-powered visual analytics
├── templates/
│   ├── index.html                 # Main UI with upload/search
│   ├── dashboard.html             # Analytics and favorites
│   └── favorites.html             # Saved jobs page
├── static/                  # CSS, JS, assets
└── uploads/                 # Uploaded resumes (PDF/DOCX)

