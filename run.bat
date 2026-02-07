@echo off
REM Injection Molding Quality Checker - Setup and Run Script
REM This script sets up the environment and runs the application

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Injection Molding Quality Checker - Setup Script     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Train models if needed
echo.
echo 🧠 Checking if models need training...
if not exist "models\warpage_model.pkl" (
    echo Training models for the first time...
    python quality_predictor.py
)

REM Run the application
echo.
echo 🚀 Starting Injection Molding Quality Checker...
echo.
echo ┌────────────────────────────────────────────────────────┐
echo │ Application will open at: http://localhost:8501        │
echo │ Press Ctrl+C to stop the server                        │
echo └────────────────────────────────────────────────────────┘
echo.

streamlit run app.py

pause
