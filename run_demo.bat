@echo off
echo Multimodal RAG System - SIH 2025 Demo
echo =====================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Installing/updating requirements...
pip install -r requirements.txt

echo.
echo Launching the demo application...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
python run_demo.py

pause
