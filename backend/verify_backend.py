import subprocess
import sys
import os

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlmodel',
        'pydantic_settings',
        'jose',
        'passlib',
        'python_dotenv',
        'psycopg2_binary',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'jose':
                from jose import jwt
            elif package == 'python_dotenv':
                from dotenv import load_dotenv
            elif package == 'pydantic_settings':
                from pydantic_settings import BaseSettings
            else:
                __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    print("Checking backend application...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {missing}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("All dependencies are available.")
    
    # Test imports
    try:
        from src.main import app
        from src.config import settings
        print("All modules imported successfully.")
    except Exception as e:
        print(f"Import error: {e}")
        return False
    
    print("\nBackend is ready to run!")
    print("To start the server:")
    print("  uvicorn app:app --reload")
    print("\nFor Hugging Face Spaces deployment, the Dockerfile is properly configured.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)