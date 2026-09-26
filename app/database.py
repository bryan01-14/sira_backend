from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

import os
import tempfile

def create_db_engine():
    db_url = settings.DATABASE_URL
    if db_url and db_url.startswith("postgresql"):
        try:
            # Test direct connection
            test_engine = create_engine(
                db_url,
                connect_args={"connect_timeout": 5},
                pool_pre_ping=True,
                echo=False
            )
            with test_engine.connect() as conn:
                pass
            print("[Database] Connecté avec succès à Supabase PostgreSQL Cloud.")
            return test_engine
        except Exception as e:
            print(f"[Database Notice] Supabase PostgreSQL non accessible ({e}). Utilisation du stockage temporaire /tmp.")
            tmp_db = os.path.join(tempfile.gettempdir(), "sira.db")
            return create_engine(f"sqlite:///{tmp_db}", connect_args={"check_same_thread": False}, echo=False)
    
    # Mode SQLite local / serverless
    tmp_db = os.path.join(tempfile.gettempdir(), "sira.db")
    return create_engine(f"sqlite:///{tmp_db}", connect_args={"check_same_thread": False}, echo=False)


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
