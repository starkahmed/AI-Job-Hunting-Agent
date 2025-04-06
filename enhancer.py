# =====================================================
# File: enhancer.py
# Description: AI-powered resume rewriter for specific roles and tones
# Version: v1.6
# =====================================================

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure this is set properly

def enhance_resume(resume_text, role, tone):
    prompt = f"Rewrite this resume for a '{role}' role with a '{tone}' tone:\n\n{resume_text[:3000]}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
