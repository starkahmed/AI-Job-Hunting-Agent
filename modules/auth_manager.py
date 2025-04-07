# ================================================================
# File: auth_manager.py
# Version: v6.0
# Description: Manages user registration, authentication, and sessions
# ================================================================

import bcrypt
import sqlite3
import uuid
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional

# Simple in-memory session store (can replace with JWT or Redis later)
sessions = {}

DB_PATH = "users.db"

def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username: str, email: str, password: str):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (id, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, email, hashed_pw, created_at))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    finally:
        conn.close()

def authenticate_user(username: str, password: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        session_token = str(uuid.uuid4())
        sessions[session_token] = {
            "user_id": user[0],
            "username": username,
            "expires_at": datetime.utcnow() + timedelta(hours=1)
        }
        return session_token
    else:
        return None

def get_current_user(session_token: str) -> Optional[str]:
    session = sessions.get(session_token)
    if session and session['expires_at'] > datetime.utcnow():
        return session['username']
    return None

def logout_user(session_token: str):
    sessions.pop(session_token, None)

# Initialize user table when module is imported
create_user_table()