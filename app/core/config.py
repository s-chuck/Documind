import os
from pathlib import Path

from dotenv import load_dotenv


current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent

load_dotenv(root_dir / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found")