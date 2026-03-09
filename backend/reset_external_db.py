#!/usr/bin/env python
"""
Database reset script for SQLite database.
Works with the local SQLite database file.

Usage:
    python reset_external_db.py          # Interactive mode
    python reset_external_db.py --auto   # Use DATABASE_URL from env
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.database import Base, engine
from app.models import User, Patient, PredictionLog, UlcerImage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_sqlite_db():
    """
    Reset the SQLite database by dropping and recreating all tables.
    """
    try:
        logger.info("Resetting SQLite database...")

        # Drop all tables
        logger.info("Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✓ All tables dropped")

        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created successfully")

        # Verify tables were created
        try:
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"✓ Tables created: {', '.join(tables)}")
        except Exception as e:
            logger.warning(f"Could not verify tables: {e}")

        logger.info("✓ SQLite database reset complete!")

    except Exception as e:
        logger.error(f"❌ Error resetting database: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Reset SQLite database")
    parser.add_argument("--auto", action="store_true", help="Use DATABASE_URL from environment")
    args = parser.parse_args()

    if args.auto:
        reset_sqlite_db()
    else:
        # Interactive mode
        print("This will reset the SQLite database (drop and recreate all tables).")
        confirm = input("Are you sure? (y/N): ").lower().strip()
        if confirm == 'y':
            reset_sqlite_db()
        else:
            print("Operation cancelled.")


if __name__ == "__main__":
    main()
