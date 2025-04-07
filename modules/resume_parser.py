# ================================================================
# File: modules/resume_parser.py
# Version: v5.5
# Description: Parses uploaded resumes or LinkedIn/Naukri/Indeed profiles.
#              Extracts skills, education, experience, contact info, and more
#              for downstream scoring, analytics, and enhancement.
# ================================================================

import pdfplumber
import docx
import re
import os
import spacy
import nltk
from langdetect import detect
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stopwords.words('english'))

# Keywords database (simplified)
SKILLS_DB = ["python", "java", "excel", "sql", "react", "aws", "data analysis", "machine learning"]
EDUCATION_KEYWORDS = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.sc", "m.sc"]
EXPERIENCE_KEYWORDS = ["experience", "worked", "employment", "role", "responsibilities"]
LOCATION_REGEX = r'\b(?:[A-Z][a-z]+\s?){1,3},?\s?(?:India)?\b'


def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + ' '
    return text.strip()


def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return ' '.join([para.text for para in doc.paragraphs])


def detect_file_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else ""


def extract_phone(text):
    match = re.search(r'\+?\d[\d -]{8,}\d', text)
    return match.group(0) if match else ""


def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS_DB if skill in text]


def extract_education(text):
    edu = []
    for keyword in EDUCATION_KEYWORDS:
        if keyword in text.lower():
            edu.append(keyword)
    return edu


def extract_experience(text):
    exp_sentences = []
    for line in text.split('\n'):
        if any(keyword in line.lower() for keyword in EXPERIENCE_KEYWORDS):
            exp_sentences.append(line.strip())
    return exp_sentences


def extract_locations(text):
    return re.findall(LOCATION_REGEX, text)


def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    language = detect_file_language(text)

    resume_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "locations": extract_locations(text),
        "language": language,
        "raw_text": text
    }
    return resume_data
