# ================================================================
# File: modules/resume_parser.py
# Version: v1.2
# Description: Parse resumes from uploaded files or external sources like LinkedIn, Naukri, Indeed.
# ================================================================

import re
import docx2txt
import pdfplumber
from typing import Dict, Optional


# =================== Extract Text from Resume =====================

def extract_text_from_pdf(file_path: str) -> str:
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    return text

def extract_text_from_docx(file_path: str) -> str:
    return docx2txt.process(file_path)

def extract_text(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

# =================== Parse Common Fields =====================

def parse_resume_text(text: str) -> Dict[str, Optional[str]]:
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    summary = extract_summary(text)
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "summary": summary
    }

# =================== Extract Individual Fields =====================

def extract_name(text: str) -> Optional[str]:
    lines = text.strip().splitlines()
    return lines[0] if lines else None

def extract_email(text: str) -> Optional[str]:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    match = re.search(r'\+?\d[\d\s\-()]{7,}\d', text)
    return match.group(0) if match else None

def extract_skills(text: str) -> str:
    skills_section = re.findall(r"(skills|technical skills|technologies)\s*[:\-]?\s*(.*)", text, re.IGNORECASE)
    if skills_section:
        return skills_section[0][1].strip()
    return ""

def extract_summary(text: str) -> str:
    summary_section = re.findall(r"(summary|professional summary)\s*[:\-]?\s*(.*)", text, re.IGNORECASE)
    if summary_section:
        return summary_section[0][1].strip()
    return ""

# =================== Unified Resume Parser Interface =====================

def parse_resume(file_path: Optional[str] = None, source_data: Optional[dict] = None) -> Dict[str, str]:
    """
    Supports:
    - file_path: uploaded PDF/DOCX resume
    - source_data: dict from LinkedIn, Naukri, or Indeed import
    """
    if file_path:
        text = extract_text(file_path)
        return parse_resume_text(text)
    elif source_data:
        return {
            "name": source_data.get("name", ""),
            "email": source_data.get("email", ""),
            "phone": source_data.get("phone", ""),
            "skills": ", ".join(source_data.get("skills", [])),
            "summary": source_data.get("summary", ""),
        }
    else:
        raise ValueError("Either file_path or source_data must be provided")
