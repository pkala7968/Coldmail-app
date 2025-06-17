from google import generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from keys.env file
load_dotenv(dotenv_path="keys.env")
api_key = os.getenv("API_KEY")

# Configure Gemini client
genai.configure(api_key=api_key)

# Create Gemini model instance
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_emailbody(cv_text, job_title="Software Engineer", company="ABC Corp"):
    prompt = f"""
    You are an AI assistant helping write professional job application emails.

    Based on the following resume content:
    ---
    {cv_text}
    ---

    Write a personalized job application email (only email body) for the position of "{job_title}" at "{company}".
    Make it formal, confident, and not a copy of the resume — just a strong, concise email.
    There should be missing values in the email body(like "Dear [Name],[mention a specific area of ABC Corp's work that interests you] etc."),
    also just give me the email body, no other text (like "Here is the email body:,Subject: Application for Data Scientist Position at ABC Corp etc.")
    """

    response = model.generate_content(prompt)
    return response.text.strip()
