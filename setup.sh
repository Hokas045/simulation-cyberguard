#!/bin/bash

# Phishing Simulation Platform - Setup Script

echo "🎣 Phishing Simulation Platform - Setup"
echo "========================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env created (please configure it)"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your SMTP settings:"
    echo "   nano .env"
    echo ""
else
    echo "✓ .env file exists"
fi

# Initialize database
echo "📊 Initializing database..."
python cli.py init

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure SMTP settings in .env"
echo "  2. python cli.py templates list"
echo "  3. python cli.py campaign create"
echo "  4. python cli.py server start"
echo ""
echo "Or read QUICKSTART.md for detailed instructions"
echo ""
