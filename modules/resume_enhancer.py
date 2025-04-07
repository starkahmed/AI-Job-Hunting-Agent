# ================================================
# File: resume_enhancer.py
# Version: v3.7
# Description: AI-powered enhancement suggestions
# ================================================

import openai

openai.api_key = "your-openai-api-key"  # Replace with your key or load via env

def generate_resume_suggestions(resume_text: str) -> list:
    prompt = f"""
You are a resume coach AI. Analyze the following resume and suggest specific improvements.
Point out vague descriptions, missing metrics, or lack of skills. Give clear, actionable tips.

Resume:
\"\"\"
{resume_text}
\"\"\"

Respond with a bullet list of suggestions.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        suggestions = response.choices[0].message['content'].strip()
        return suggestions.split("\n") if suggestions else []
    except Exception as e:
        return [f"⚠️ Error generating suggestions: {str(e)}"]
