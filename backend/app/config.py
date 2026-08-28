"""
Central place for reading environment variables so the rest of the app
never has to touch os.environ directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
database_url = os.getenv("DATABASE_URL")

if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

if not database_url:
    raise RuntimeError("DATABASE_URL is missing. Add it to your .env file.")
