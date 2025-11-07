# AI Resume Screening Bot

A full-stack machine learning application that intelligently analyzes resumes against job descriptions using advanced Natural Language Processing (NLP) and provides holistic candidate evaluation with detailed insights.

Author: Mustafa Hadi 

## Features

- **PDF & DOCX Support**: Upload resumes in multiple formats
- **Holistic AI Analysis**: Multi-factor evaluation system analyzing skills, experience, context, and role fit
- **Smart Scoring System**: Weighted analysis across 4 key dimensions (not just keyword matching)
- **Intelligent Recommendations**: Clear guidance on whether to apply with confidence levels
- **Skills Gap Analysis**: Identifies matched skills and growth opportunities
- **Experience Matching**: Compares years of experience and seniority levels
- **Role Compatibility**: Detects frontend/backend/full-stack/data science alignment
- **Actionable Insights**: Lists specific strengths and improvement areas
- **Real-time Results**: Instant analysis with stunning visualizations
- **Modern UI**: Responsive design with animated backgrounds, glassmorphic cards, and circular progress meters

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - REST API framework
- **scikit-learn** - Machine Learning library (TF-IDF + Cosine Similarity)
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction

### Frontend
- **React 18**
- **Tailwind CSS** - Styling with custom animations
- **Lucide React** - Beautiful icons

## Structure
```
resume-screening-bot/
├── package.json
├── README.md
├── requirements.txt
├── SETUP_INSTRUCTIONS.md
├── backend/
│   ├── app.py                      # Flask API
│   ├── model.py                    # Enhanced ML model with multi-factor analysis
│   ├── utils.py                    # Helper functions (skills/experience extraction)
│   ├── setup_backend.sh            # Setup script (Mac)
│   ├── setup_backend.bat           # Setup script (Windows)
│   ├── package.json
│   │
│   ├── data/
│   │   ├── resumes/               # Training resumes
│   │   └── job_descriptions/      # Training job descriptions
│   │
│   ├── models/
│   │   └── resume_classifier.pkl  # Trained model
│   │
│   ├── uploads/                   # Temp uploads
│   └── venv/                   
│
└── frontend/
    ├── node_modules/
    ├── src/
    │   ├── App.js                 # Enhanced React component with stunning UI
    │   ├── index.js
    │   └── index.css              # Custom animations and scrollbar
    │   └── App.css              
    ├── public/
    │   └── index.html             # Added to avoid runtime errors
    ├── package.json
    ├── tailwind.config.js
    └── postcss.config.js
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip
- npm

### Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python app.py
```

Backend runs on: **http://localhost:5000**

### Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

## How The Enhanced AI Works

### Multi-Factor Analysis System

The bot evaluates candidates across **4 weighted dimensions**:

#### 1. Technical Skills Match (40% weight)
- Extracts technical skills from both resume and job description
- Identifies critical skills (languages, frameworks, tools)
- Performs intelligent fuzzy matching (e.g., "Node.js" matches "nodejs")
- Prioritizes critical skills over general ones

#### 2. Experience Level (25% weight)
- Extracts years of experience using regex patterns
- Compares candidate experience vs. required experience
- Evaluates seniority levels (entry, mid, senior)
- Provides experience gap analysis

#### 3. Contextual Understanding (20% weight)
- Uses TF-IDF vectorization for semantic analysis
- Calculates cosine similarity between documents
- Understands context beyond exact keyword matches
- Captures overall candidate-role alignment

#### 4. Role Compatibility (15% weight)
- Detects role type (frontend, backend, full-stack, data science, DevOps, mobile)
- Analyzes role-specific keyword presence
- Evaluates specialized skill alignment
- Determines role fit percentage

### Scoring & Recommendations

**Final Score Calculation:**
```
Final Score = (0.40 × Skills) + (0.25 × Experience) + (0.20 × Context) + (0.15 × Role)
```

**Intelligent Recommendations:**
- **75%+**: "Strongly Recommended" - Excellent match, definitely apply
- **60-74%**: "Recommended" - Good match, apply with confidence
- **45-59%**: "Consider Applying" - Moderate match, growth opportunity
- **<45%**: "Not Recommended" - Limited match, build skills first

### Key Improvements Over Basic Keyword Matching

**Holistic evaluation** instead of simple word counting  
**Weighted scoring** prioritizes important factors  
**Intelligent skill matching** with variations and synonyms  
**Experience analysis** beyond just detecting years  
**Role-specific insights** for different job types  
**Actionable feedback** with strengths and growth areas  
**Clear application guidance** with confidence levels  

## Testing

### Test Backend

```bash
# Health check
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","message":"Resume Screening Bot API is running"}
```

### Test Full Application

1. Open http://localhost:3000
2. Upload a resume (PDF or DOCX)
3. Paste a complete job description
4. Click "Analyze Match"
5. View comprehensive results:
   - Overall match score with confidence level
   - Clear recommendation (should you apply?)
   - Score breakdown across 4 dimensions
   - Your strengths
   - Growth opportunities
   - Matched skills
   - Skills to develop
   - Experience analysis

## API Endpoints

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Resume Screening Bot API is running"
}
```

### `POST /api/screen-resume`
Analyze resume against job description with enhanced AI

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `resume`: File (PDF or DOCX)
  - `job_description`: String

**Response:**
```json
{
  "success": true,
  "match_score": 78.5,
  "prediction": "Recommended",
  "recommendation": "Good match! You meet most requirements...",
  "should_apply": true,
  "confidence": "Medium-High",
  "strengths": [
    "Strong technical skill match (15 key skills aligned)",
    "Experience level meets or exceeds requirements"
  ],
  "improvements": [
    "Consider developing these skills: Kubernetes, GraphQL"
  ],
  "matched_skills": ["python", "django", "aws", "docker", "postgresql"],
  "missing_skills": ["kubernetes", "graphql", "redis"],
  "experience_match": "Meets requirement (5+ years vs 3+ required)",
  "details": {
    "skills_score": 75.0,
    "experience_score": 100.0,
    "semantic_score": 68.5,
    "role_score": 82.3,
    "resume_years": 5,
    "required_years": 3,
    "critical_skills_met": 8,
    "total_skills_matched": 15,
    "total_skills_required": 20
  }
}
```

## UI Features

### Visual Design Elements

- **Animated Background**: Floating gradient blobs with smooth blob animations
- **Glassmorphic Cards**: Backdrop blur effects with elegant borders
- **Circular Progress Meter**: Animated SVG circle with gradient fills
- **Color-Coded Scoring**:
  - Green (75%+): Strongly Recommended
  - Blue (60-74%): Recommended
  - Yellow (45-59%): Consider Applying
  - Red (<45%): Not Recommended
- **Hover Effects**: Scale transformations and glow shadows
- **Smooth Animations**: Fade-in effects and transitions
- **Responsive Layout**: Beautiful on all screen sizes
- **Custom Scrollbar**: Styled with purple theme

## Troubleshooting

### CORS Errors
Ensure Flask-CORS is installed and backend is running on port 5000

### Module Not Found
```bash
pip install -r requirements.txt
```

### PDF Extraction Fails
Ensure PyPDF2 is installed:
```bash
pip install PyPDF2==3.0.1
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

Update frontend API URL in `App.js`:
```javascript
const response = await fetch('http://localhost:5001/api/screen-resume', {
```

### "Cannot read properties of undefined" Error
This has been fixed in the enhanced version with proper null checking using `(result.property || [])`

## Deployment

### Backend (Heroku)
```bash
# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Add gunicorn to requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Deploy
heroku create your-app-name
git push heroku main
```

### Frontend (Vercel)
```bash
npm run build
vercel --prod
```

## Future Add-Ons

- [ ] Add user authentication
- [ ] Save analysis history with database
- [ ] Batch resume processing
- [ ] Export results to PDF report
- [ ] Advanced ML models (BERT, GPT for deeper understanding)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Email notifications for results
- [ ] Resume ranking system for multiple candidates
- [ ] Interactive skills gap visualization charts
- [ ] Interview scheduling integration
- [ ] ATS (Applicant Tracking System) compatibility checker
- [ ] Resume improvement suggestions with AI
- [ ] Industry-specific scoring models

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - feel free to use this project for learning and portfolio purposes!

## Author

Built by Mustafa Hadi as a portfolio project demonstrating:
- Machine Learning fundamentals
- Natural Language Processing
- Multi-factor AI analysis systems
- Full-stack development
- REST API design
- Modern UI/UX with animations
- Advanced React patterns

## Acknowledgments

- scikit-learn for ML algorithms (TF-IDF, Cosine Similarity)
- Flask for the backend framework
- React and Tailwind CSS for the stunning frontend
- Lucide React for beautiful icons
- The open-source community