import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings

logger = logging.getLogger(__name__)

# Create engine with proper error handling
try:
    connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
    engine = create_engine(settings.database_url, connect_args=connect_args)
    logger.info(f"✓ Database engine created: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'SQLite'}")
except Exception as e:
    logger.error(f"❌ Error creating database engine: {e}")
    # Fallback to SQLite
    engine = create_engine("sqlite:///./medvision.db", connect_args={"check_same_thread": False})
    logger.warning("Using fallback SQLite database")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
