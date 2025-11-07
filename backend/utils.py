import PyPDF2
from docx import Document
import re
import string
from collections import Counter

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)
        return "\n".join(text)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def preprocess_text(text):
    """Preprocess text while preserving important keywords"""
    text = text.lower()
    
    # Remove URLs and emails
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    
    # Preserve important compound words
    text = text.replace("node.js", "nodejs")
    text = text.replace("node js", "nodejs")
    text = text.replace("rest api", "restapi")
    text = text.replace("restful api", "restapi")
    text = text.replace("ci/cd", "cicd")
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    
    # Keep alphanumeric, spaces, and + for experience years
    text = re.sub(r'[^a-z0-9\s+]', ' ', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text, top_n=100):
    """Enhanced keyword extraction"""
    keywords = set()
    text_lower = text.lower()
    
    # Experience patterns
    exp_patterns = re.findall(r'(\d+)\+?\s*(?:year|yr)s?', text_lower)
    for exp in exp_patterns:
        keywords.add(f"{exp}+ years")
    
    # Comprehensive technical keywords
    tech_keywords = [
        # Languages
        'python', 'java', 'javascript', 'typescript', 'sql', 'c++', 'c#', 
        'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'scala',
        
        # Frameworks
        'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue',
        'nodejs', 'node.js', 'express', 'nextjs', 'nest',
        
        # Databases
        'postgresql', 'postgres', 'mysql', 'mongodb', 'redis', 'sqlite',
        'cassandra', 'dynamodb', 'elasticsearch', 'oracle',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'k8s', 'jenkins',
        'gitlab', 'github', 'terraform', 'ansible', 'ci/cd', 'cicd',
        
        # ML & Data
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn',
        'pandas', 'numpy', 'machine learning', 'ml', 'ai', 'data science',
        
        # Web & API
        'api', 'rest', 'restful', 'graphql', 'soap', 'microservices',
        'websocket', 'http', 'https', 'json', 'xml',
        
        # Architecture
        'backend', 'frontend', 'full-stack', 'fullstack', 'microservices',
        'serverless', 'scalable', 'scalability',
        
        # Methodologies
        'agile', 'scrum', 'kanban', 'devops', 'tdd', 'bdd',
        
        # General tech
        'git', 'linux', 'unix', 'bash', 'shell', 'testing', 'deployment'
    ]
    
    for keyword in tech_keywords:
        pattern = re.escape(keyword)
        pattern = pattern.replace(r'\-', r'[\s\-]?')
        pattern = pattern.replace(r'\.', r'\.?')
        
        try:
            if re.search(r'\b' + pattern + r'\b', text_lower):
                keywords.add(keyword)
        except:
            if keyword in text_lower:
                keywords.add(keyword)
    
    return list(keywords)

def extract_skills(text):
    """Extract technical skills from text"""
    skills = set()
    text_lower = text.lower()
    
    # Primary technical skills
    skill_list = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
        'go', 'rust', 'kotlin', 'swift', 'scala', 'sql', 'html', 'css',
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'nodejs',
        'express', 'fastapi', 'nextjs', 'laravel', 'rails',
        'postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'elasticsearch',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab',
        'terraform', 'ansible', 'ci/cd', 'git',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'rest', 'restful', 'api', 'graphql', 'microservices', 'websocket',
        'agile', 'scrum', 'devops', 'tdd', 'linux', 'bash'
    ]
    
    for skill in skill_list:
        pattern = re.escape(skill)
        pattern = pattern.replace(r'\-', r'[\s\-]?')
        pattern = pattern.replace(r'\.', r'\.?')
        pattern = pattern.replace(r'\+', r'\+?')
        
        try:
            if re.search(r'\b' + pattern + r'\b', text_lower):
                skills.add(skill)
        except:
            if skill in text_lower:
                skills.add(skill)
    
    return list(skills)

def extract_experience(text):
    """Extract years of experience from text"""
    text_lower = text.lower()
    
    patterns = [
        r'(\d+)\+\s*years?',
        r'(\d+)\s*years?',
        r'(\d+)[-–]\d+\s*years?'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        years.extend([int(m) for m in matches])
    
    max_years = max(years) if years else 0
    
    # Also check for seniority levels
    seniority = 'entry'
    if 'senior' in text_lower or 'lead' in text_lower or max_years >= 5:
        seniority = 'senior'
    elif 'mid-level' in text_lower or 'intermediate' in text_lower or max_years >= 3:
        seniority = 'mid'
    
    return {
        'years': max_years,
        'seniority': seniority
    }

def format_skills_for_display(skills):
    """Format skills for better display"""
    formatted = []
    for skill in skills:
        if skill in ['api', 'rest', 'restful', 'sql', 'aws', 'gcp', 'ml', 'ai', 'ci/cd', 'html', 'css', 'xml', 'json', 'http', 'tdd', 'bdd']:
            formatted.append(skill.upper())
        elif skill in ['nodejs', 'node.js']:
            formatted.append('Node.js')
        elif skill == 'postgresql':
            formatted.append('PostgreSQL')
        elif skill == 'mongodb':
            formatted.append('MongoDB')
        elif skill == 'mysql':
            formatted.append('MySQL')
        elif skill == 'javascript':
            formatted.append('JavaScript')
        elif skill == 'typescript':
            formatted.append('TypeScript')
        else:
            formatted.append(skill.title())
    return formatted