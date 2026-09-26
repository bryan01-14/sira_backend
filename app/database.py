from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

import os
import tempfile

def create_db_engine():
    db_url = settings.DATABASE_URL
    if db_url and db_url.startswith("postgresql"):
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,
            max_overflow=0,
            connect_args={"connect_timeout": 5}
        )
    
    # Mode SQLite local / serverless fallback
    tmp_db = os.path.join(tempfile.gettempdir(), "sira.db")
    return create_engine(f"sqlite:///{tmp_db}", connect_args={"check_same_thread": False})



engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
