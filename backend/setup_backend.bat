@echo off
echo ======================================
echo Resume Screening Bot - Backend Setup
echo ======================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directory structure...
if not exist "uploads" mkdir uploads
if not exist "models" mkdir models
if not exist "data\resumes" mkdir data\resumes
if not exist "data\job_descriptions" mkdir data\job_descriptions

REM Create .gitignore
echo Creating .gitignore...
(
echo # Virtual Environment
echo venv/
echo env/
echo ENV/
echo .venv/
echo.
echo # Python Cache
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo.
echo # Models ^(these get regenerated^)
echo models/
echo *.pkl
echo.
echo # Uploads ^(temporary files^)
echo uploads/
echo *.pdf
echo *.docx
echo.
echo # Environment variables
echo .env
echo .env.local
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
) > .gitignore

REM Create .gitkeep files
type nul > uploads\.gitkeep
type nul > models\.gitkeep
type nul > data\resumes\.gitkeep
type nul > data\job_descriptions\.gitkeep

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next Steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the server: python app.py
echo.
echo The API will be available at http://localhost:5000
echo.
echo Note: The ML model will be trained automatically on first use.
echo ======================================
pause