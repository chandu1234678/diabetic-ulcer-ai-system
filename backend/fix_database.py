#!/usr/bin/env python
"""
Database Diagnostic and Reset Script
Helps identify and fix database issues for auth problems.

Usage:
    python fix_database.py --check      # Check database status
    python fix_database.py --list-users # List all users in database
    python fix_database.py --reset      # DANGER: Drop all tables and recreate
    python fix_database.py --clean-users # Remove duplicate/test users
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, Base, engine
from app.models import User
from app.auth.password_utils import hash_password
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_database():
    """Check database connection and schema status."""
    logger.info("=" * 60)
    logger.info("DATABASE DIAGNOSTIC CHECK")
    logger.info("=" * 60)
    
    try:
        # Test connection
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("✓ Database connection: OK")
        db.close()
    except Exception as e:
        logger.error(f"✗ Database connection FAILED: {e}")
        return False
    
    # Check tables
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            logger.info(f"✓ Tables found: {', '.join(tables)}")
        else:
            logger.warning("⚠ No tables found in database")
            
    except Exception as e:
        logger.error(f"✗ Error checking tables: {e}")
        return False
    
    return True


def list_users():
    """List all users in database."""
    logger.info("=" * 60)
    logger.info("USERS IN DATABASE")
    logger.info("=" * 60)
    
    try:
        db = SessionLocal()
        users = db.query(User).all()
        
        if not users:
            logger.info("No users found in database")
            db.close()
            return
        
        logger.info(f"Total users: {len(users)}\n")
        for user in users:
            logger.info(f"ID: {user.id}")
            logger.info(f"  Email: {user.email}")
            logger.info(f"  Active: {user.is_active}")
            logger.info(f"  Created: {user.created_at}")
            logger.info(f"  Hash: {user.hashed_password[:30]}...")
            logger.info("")
        
        db.close()
    except Exception as e:
        logger.error(f"✗ Error listing users: {e}")


def clean_users():
    """Remove duplicate and test users."""
    logger.info("=" * 60)
    logger.info("CLEANING TEST USERS")
    logger.info("=" * 60)
    
    test_emails = [
        "test@example.com",
        "test@test.com",
        "admin@test.com",
        "demo@example.com"
    ]
    
    try:
        db = SessionLocal()
        
        for email in test_emails:
            user = db.query(User).filter(User.email == email).first()
            if user:
                db.delete(user)
                logger.info(f"✓ Deleted test user: {email}")
        
        db.commit()
        logger.info("✓ Cleanup complete")
        db.close()
    except Exception as e:
        logger.error(f"✗ Error during cleanup: {e}")


def reset_database():
    """DANGEROUS: Drop all tables and recreate schema."""
    logger.info("=" * 60)
    logger.warning("WARNING: THIS WILL DELETE ALL DATA!")
    logger.info("=" * 60)
    
    confirm = input("Type 'RESET' to confirm database reset: ").strip()
    if confirm != "RESET":
        logger.info("❌ Reset cancelled")
        return
    
    try:
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✓ Tables dropped")
        
        logger.info("Creating fresh schema...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tables created")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"✓ New tables: {', '.join(tables)}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ DATABASE RESET COMPLETE")
        logger.info("=" * 60)
        logger.info("\nYou can now create a new account:")
        logger.info("  Email: your-email@example.com")
        logger.info("  Password: at least 8 characters")
        
    except Exception as e:
        logger.error(f"✗ Error during reset: {e}")


def main():
    parser = argparse.ArgumentParser(description="Database diagnostic and reset tool")
    parser.add_argument("--check", action="store_true", help="Check database status")
    parser.add_argument("--list-users", action="store_true", help="List all users")
    parser.add_argument("--clean-users", action="store_true", help="Remove test users")
    parser.add_argument("--reset", action="store_true", help="Reset database (DANGER!)")
    
    args = parser.parse_args()
    
    if not any([args.check, args.list_users, args.clean_users, args.reset]):
        # Default to check
        args.check = True
    
    if args.check:
        check_database()
    
    if args.list_users:
        list_users()
    
    if args.clean_users:
        clean_users()
    
    if args.reset:
        reset_database()


if __name__ == "__main__":
    main()
