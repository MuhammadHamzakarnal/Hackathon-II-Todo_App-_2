#!/usr/bin/env python3
"""
Test script to verify database connection and table creation
"""

import sys
from sqlmodel import Session, select
from src.database import get_session, init_db
from src.models.user import User
from src.models.task import Task

def test_database():
    print("Testing database connection...")

    try:
        # Initialize database tables
        print("Initializing database tables...")
        init_db()
        print("[SUCCESS] Database tables initialized successfully")

        # Test getting a session
        print("Getting database session...")
        session_gen = get_session()
        session = next(session_gen)
        print("[SUCCESS] Database session acquired successfully")

        # Test querying users (should not error even if table is empty)
        users = session.exec(select(User)).all()
        print(f"[SUCCESS] Successfully queried users table, found {len(users)} users")

        # Test querying tasks (should not error even if table is empty)
        tasks = session.exec(select(Task)).all()
        print(f"[SUCCESS] Successfully queried tasks table, found {len(tasks)} tasks")

        print("\n[SUCCESS] All database tests passed!")
        print("The database connection and tables appear to be working correctly.")

    except Exception as e:
        print(f"\n[ERROR] Database test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        try:
            session.close()
        except:
            pass

    return True

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)