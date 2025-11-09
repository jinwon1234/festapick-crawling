from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

DATASOURCE_URL = os.getenv("DATASOURCE_URL")
DATASOURCE_USERNAME = os.getenv("DATASOURCE_USERNAME")
DATASOURCE_PASSWORD = os.getenv("DATASOURCE_PASSWORD")


DATABASE_INFO = (
    f"mysql+mysqlconnector://{DATASOURCE_USERNAME}:{DATASOURCE_PASSWORD}@{DATASOURCE_URL}/festapick"
)

engine = create_engine(
    DATABASE_INFO,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()