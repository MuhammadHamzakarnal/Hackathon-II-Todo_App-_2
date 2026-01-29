#!/bin/bash

echo "Starting the backend server..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not found in your PATH."
    echo "Please make sure Python3 is installed and added to your PATH."
    exit 1
fi

# Install dependencies if not already installed
echo "Installing/updating dependencies..."
pip3 install --upgrade -r requirements.txt

# Start the server
echo
echo "Starting the FastAPI server on http://localhost:7860"
echo "Press Ctrl+C to stop the server"
echo
uvicorn src.main:app --host localhost --port 7860 --reload