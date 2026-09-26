from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

def create_db_engine():
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql"):
        try:
            # Test direct connection
            test_engine = create_engine(db_url, connect_args={"connect_timeout": 3}, echo=False)
            with test_engine.connect() as conn:
                pass
            print("[Database] Connecté avec succès à Supabase PostgreSQL Cloud.")
            return test_engine
        except Exception as e:
            print(f"[Database Notice] Impossible de joindre Supabase PostgreSQL ({e}). Utilisation automatique du mode local SQLite.")
            return create_engine("sqlite:///./sira.db", connect_args={"check_same_thread": False}, echo=False)
    
    return create_engine(db_url, connect_args={"check_same_thread": False}, echo=False)

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
