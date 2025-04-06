import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(resume_text):
    """
    This function generates feedback for a resume using OpenAI's GPT-3.5 model.
    It provides feedback on formatting, clarity, keyword usage, and job relevance.
    
    Args:
    resume_text (str): The text content of the resume to analyze.

    Returns:
    str: Feedback on the resume from the AI.
    """
    prompt = f"""You are an expert career coach. Please analyze the following resume and provide constructive feedback.
    
    Resume:
    {resume_text}

    Give feedback on formatting, clarity, keyword usage, and job relevance. Include suggestions for improvement.
    """

    try:
        # Make a request to OpenAI API for generating feedback
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Return the generated feedback from the model
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # In case of an error, return the error message
        return f"Error generating feedback: {e}"
