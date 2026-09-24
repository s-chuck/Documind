import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from app.core.config import DATABASE_URL



if not DATABASE_URL:
    raise ValueError("DB_URL not found")

engine = create_engine(DATABASE_URL)

# with engine.connect() as connection:
#     connection.execute(text("SELECT 1"))
# print("Database connected successfully")

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Base = declarative_base()



# from app.core.config import DATABASE_URL
# from sqlalchemy import create_engine
# if not DATABASE_URL:
#     raise ValueError("DB_URL not found")

# engine = create_engine(DATABASE_URL)