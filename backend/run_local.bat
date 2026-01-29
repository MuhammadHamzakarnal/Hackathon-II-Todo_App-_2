@echo off
echo Starting the backend server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not found in your PATH.
    echo Please make sure Python is installed and added to your PATH.
    pause
    exit /b 1
)

REM Install dependencies if not already installed
echo Installing/updating dependencies...
python -m pip install --upgrade -r requirements.txt

REM Start the server
echo.
echo Starting the FastAPI server on http://localhost:7860
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn src.main:app --host localhost --port 7860 --reload

pause