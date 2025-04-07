# ================================================================
# File: user_routes.py
# Version: v6.0
# Description: FastAPI routes for user authentication and session handling.
# ================================================================

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from modules.auth_manager import register_user, authenticate_user, sessions

router = APIRouter()

# ------------------------------
# GET: Registration Page
# ------------------------------
@router.get("/register", response_class=HTMLResponse)
async def register_form():
    return """
    <form method="post" action="/register">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Register">
    </form>
    """

# ------------------------------
# POST: Register User
# ------------------------------
@router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    success = register_user(username, password)
    if success:
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=400, detail="Username already exists")

# ------------------------------
# GET: Login Page
# ------------------------------
@router.get("/login", response_class=HTMLResponse)
async def login_form():
    return """
    <form method="post" action="/login">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    """

# ------------------------------
# POST: Login User
# ------------------------------
@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ------------------------------
# GET: Logout
# ------------------------------
@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

# ------------------------------
# GET: User Dashboard Redirect
# ------------------------------
@router.get("/dashboard")
async def user_dashboard_redirect(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
    return RedirectResponse(url="/user-dashboard", status_code=HTTP_303_SEE_OTHER)
