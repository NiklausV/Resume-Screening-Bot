# Quick Setup Instructions - AI Resume Screening Bot

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

---

## Backend Setup 

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Run the Setup Script

**On macOS/Linux:**
```bash
chmod +x setup_backend.sh
./setup_backend.sh
```

**On Windows:**
```bash
setup_backend.bat
```

This script will:
- Create a Python virtual environment
- Install all required packages
- Create necessary directories (uploads, models, data)
- Generate .gitignore file

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Start the Backend Server
```bash
python app.py
```

**Expected Output:**
```
Resume Screening Bot API Starting...
Upload folder: uploads
ML Model: Loaded
 * Running on http://0.0.0.0:5000
```

Backend is ready!!

---

## Frontend Setup

### Step 1: Open New Terminal
Keep the backend running and open a new terminal window.

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Install Dependencies
```bash
npm install
```

This will install:
- React 18
- Tailwind CSS
- Lucide React 
- All other dependencies

### Step 4: Start Development Server
```bash
npm start
```

The browser will automatically open to `http://localhost:3000`

Frontend is ready!!

---

## Testing the Application

### Prepare Test Files

**Option 1: Create Your Own**
- Resume: Your actual resume in PDF or DOCX format
- Job Description: Copy from a job posting you're interested in

**Option 2: Use Sample Data**
Create `test_resume.txt` and `test_job.txt` with relevant content.

### Using the Application

1. **Upload Resume**: Click the upload area and select your resume (PDF or DOCX)
2. **Paste Job Description**: Copy the full job description into the text area
3. **Click "Analyze Match"**: Wait a few seconds for AI analysis
4. **View Results**:
   - Overall match score (0-100%)
   - Clear recommendation with confidence level
   - Should you apply? (Yes/No)
   - Score breakdown (Skills, Experience, Context, Role Fit)
   - Your strengths
   - Growth opportunities
   - Matched skills
   - Skills to develop
   - Experience analysis

### What Makes a Good Match?

- **75%+**: Strongly Recommended - Excellent fit, definitely apply!
- **60-74%**: Recommended - Good match, apply with confidence
- **45-59%**: Consider Applying - Moderate match, growth opportunity
- **<45%**: Not Recommended - Build relevant skills first

---

## Common Issues & Solutions

### Backend Issues

**Issue:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** 
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

**Issue:** `Permission denied: setup_backend.sh`

**Solution:**
```bash
chmod +x setup_backend.sh
```

---

**Issue:** Port 5000 already in use

**Solution:** Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Also update frontend API URL in `App.js`:
```javascript
const response = await fetch('http://localhost:5001/api/screen-resume', {
```

---

**Issue:** PDF extraction fails

**Solution:**
```bash
pip install --upgrade PyPDF2
```

---

### Frontend Issues

**Issue:** `npm: command not found`

**Solution:** Install Node.js from https://nodejs.org/ (choose LTS version)

---

**Issue:** Port 3000 already in use

**Solution:** The app will automatically ask:
```
? Something is already running on port 3000. Would you like to run the app on another port instead? (Y/n)
```
Type `Y` and press Enter.

---

**Issue:** "Failed to connect to server" error

**Solution:**
1. Ensure backend is running on port 5000
2. Check browser console (F12) for detailed errors
3. Verify CORS is enabled (Flask-CORS should be installed)
4. Try restarting both backend and frontend

---

**Issue:** Tailwind styles not loading

**Solution:**
```bash
npm install -D tailwindcss postcss autoprefixer
npm start
```

## How the Enhanced AI Works

The bot uses a **multi-factor analysis system**:

1. **Technical Skills Match (40%)**: Identifies and matches programming languages, frameworks, and tools
2. **Experience Level (25%)**: Compares years of experience and seniority
3. **Contextual Understanding (20%)**: Uses TF-IDF and cosine similarity for semantic analysis
4. **Role Compatibility (15%)**: Detects role type (frontend, backend, full-stack, etc.)

**Final Score = (0.40 × Skills) + (0.25 × Experience) + (0.20 × Context) + (0.15 × Role)**

## Quick Test Commands

### Test Backend Health
```bash
curl http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Resume Screening Bot API is running"
}
```

### Test Full Analysis (with curl)
```bash
curl -X POST http://localhost:5000/api/screen-resume \
  -F "resume=@path/to/resume.pdf" \
  -F "job_description=Senior Python Developer with 5+ years..."
```

---

## Environment Variables (Optional)

Create `.env` file in backend directory:

```env
FLASK_ENV=development
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216
PORT=5000
DEBUG=True
```

---

## Next Steps

1. **Test thoroughly** - Try different resumes and job descriptions
2. **Customize UI** - Modify colors in `App.js` (Tailwind classes)
3. **Add training data** - Expand `backend/data/` for better accuracy
4. **Deploy** - Follow deployment guide in README.md

---

## Performance Tips

- **Resume Quality**: Use well-formatted resumes with clear sections
- **Job Description**: Paste complete job descriptions for better analysis
- **File Size**: Keep resumes under 5MB for faster processing
- **Keywords**: Include relevant technical skills in your resume

---

## Features Overview

### What You'll See:
- **Match Score**: Percentage-based compatibility (0-100%)
- **Clear Recommendation**: Should you apply?
- **Score Breakdown**: Individual scores for each factor
- **Your Strengths**: What you're doing well
- **Growth Opportunities**: Skills to develop
- **Matched Skills**: Technologies you have
- **Missing Skills**: Technologies to learn
- **Experience Analysis**: Years comparison

---

## Need Help?

- Check the full **README.md** for detailed documentation
- Review code comments in each file
- Check the troubleshooting section above
- Use browser DevTools (F12) to inspect errors


