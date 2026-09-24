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


#our old config.py file is like a container to all the variables now the new one isn't 

# from functools import lru_cache

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     DATABASE_URL: str
#     JWT_SECRET_KEY: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore",
#     )


# @lru_cache
# def get_settings() -> Settings:
#     return Settings()