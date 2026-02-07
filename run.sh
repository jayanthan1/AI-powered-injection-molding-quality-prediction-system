#!/bin/bash

# Injection Molding Quality Checker - Setup and Run Script (Linux/macOS)

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   Injection Molding Quality Checker - Setup Script     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "✅ Python found"
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Train models if needed
echo ""
echo "🧠 Checking if models need training..."
if [ ! -f "models/warpage_model.pkl" ]; then
    echo "Training models for the first time..."
    python3 quality_predictor.py
fi

# Run the application
echo ""
echo "🚀 Starting Injection Molding Quality Checker..."
echo ""
echo "┌────────────────────────────────────────────────────────┐"
echo "│ Application will open at: http://localhost:8501        │"
echo "│ Press Ctrl+C to stop the server                        │"
echo "└────────────────────────────────────────────────────────┘"
echo ""

streamlit run app.py
