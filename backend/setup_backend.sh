#!/bin/bash

echo "======================================"
echo "Resume Screening Bot - Backend Setup"
echo "======================================"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directory structure..."
mkdir -p uploads
mkdir -p models
mkdir -p data/resumes
mkdir -p data/job_descriptions

# Create .gitignore
echo "Creating .gitignore..."
cat > .gitignore << 'GITIGNORE'
# Virtual Environment
venv/
env/
ENV/
.venv/

# Python Cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Models (these get regenerated)
models/
*.pkl

# Uploads (temporary files)
uploads/
*.pdf
*.docx

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
GITIGNORE

# Create .gitkeep files
touch uploads/.gitkeep
touch models/.gitkeep
touch data/resumes/.gitkeep
touch data/job_descriptions/.gitkeep

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the server: python app.py"
echo ""
echo "The API will be available at http://localhost:5000"
echo ""
echo "Note: The ML model will be trained automatically on first use."
echo "======================================"