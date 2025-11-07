from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from model import ResumeScreeningModel
from utils import extract_text_from_pdf, extract_text_from_docx, preprocess_text

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the ML model
model = ResumeScreeningModel()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Resume Screening Bot API is running'
    }), 200

@app.route('/api/screen-resume', methods=['POST'])
def screen_resume():
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not job_description.strip():
            return jsonify({'success': False, 'error': 'Job description is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from resume
        try:
            if filename.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf(filepath)
            elif filename.lower().endswith(('.docx', '.doc')):
                resume_text = extract_text_from_docx(filepath)
            else:
                return jsonify({'success': False, 'error': 'Unsupported file format'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': f'Failed to extract text: {str(e)}'}), 400
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        
        # Validate extracted text
        if not resume_text.strip():
            return jsonify({'success': False, 'error': 'Could not extract text from resume'}), 400
        
        # Analyze resume
        result = model.analyze_resume(resume_text, job_description)
        
        return jsonify({
            'success': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Optional endpoint to train/retrain the model"""
    try:
        model.train_model()
        return jsonify({
            'success': True,
            'message': 'Model trained successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Training failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Resume Screening Bot API Starting...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"ML Model: {'Loaded' if model else 'Not loaded'}")
    app.run(debug=True, host='0.0.0.0', port=5000)