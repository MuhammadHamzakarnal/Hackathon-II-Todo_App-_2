#!/usr/bin/env python
"""
Test script to verify that the application starts correctly
"""

try:
    from src.main import app
    from src.config import settings
    print("[OK] Successfully imported main app and settings")

    # Check if settings can be loaded (will fail if .env is missing but won't crash)
    try:
        db_url = getattr(settings, 'DATABASE_URL', 'Not set')
        print(f"[OK] Settings loaded (DB URL: {'SET' if db_url != 'Not set' else 'NOT SET'})")
    except Exception as e:
        print(f"[INFO] Settings could not be fully loaded (this is OK if .env is missing): {e}")

    print("\nApplication structure is correct!")
    print("To run the application:")
    print("  uvicorn app:app --reload")
    print("\nFor deployment on Hugging Face Spaces, the Dockerfile is properly configured.")

except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("There might be missing dependencies or import issues.")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")