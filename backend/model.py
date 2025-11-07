import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import preprocess_text, extract_keywords, extract_skills, extract_experience
import re

class ResumeScreeningModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=2000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95
        )
        self.model_path = 'models/resume_classifier.pkl'
        self.load_or_initialize_model()
    
    def load_or_initialize_model(self):
        """Load existing model or initialize new one"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.vectorizer = saved_data['vectorizer']
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Initializing new model")
        else:
            print("No existing model found. Model will be fitted on first use.")
    
    def save_model(self):
        """Save the trained model"""
        os.makedirs('models', exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({'vectorizer': self.vectorizer}, f)
        print("Model saved successfully")
    
    def train_model(self):
        """Train the model with sample data"""
        sample_resumes = [
            "Python developer with 5 years experience in Django, Flask, and REST APIs. Machine learning enthusiast.",
            "Java backend engineer skilled in Spring Boot, microservices, and AWS cloud infrastructure.",
            "Frontend developer specializing in React, Vue.js, TypeScript, and modern web technologies.",
            "Data scientist with expertise in Python, TensorFlow, scikit-learn, and statistical analysis.",
            "Full stack developer proficient in JavaScript, Node.js, React, MongoDB, and Docker."
        ]
        self.vectorizer.fit(sample_resumes)
        self.save_model()
        print("Model training completed")

    def analyze_resume(self, resume_text, job_description):
        """
        Enhanced AI-powered analysis that evaluates:
        1. Technical skill alignment (40%)
        2. Experience level match (25%)
        3. Contextual understanding (20%)
        4. Role compatibility (15%)
        """
        resume_processed = preprocess_text(resume_text)
        job_processed = preprocess_text(job_description)

        # Ensure vectorizer is fitted
        try:
            resume_vector = self.vectorizer.transform([resume_processed])
            job_vector = self.vectorizer.transform([job_processed])
        except:
            self.vectorizer.fit([resume_processed, job_processed])
            self.save_model()
            resume_vector = self.vectorizer.transform([resume_processed])
            job_vector = self.vectorizer.transform([job_processed])

        # 1. Semantic similarity (contextual understanding)
        semantic_similarity = cosine_similarity(resume_vector, job_vector)[0][0]
        semantic_score = semantic_similarity * 100

        # 2. Technical skills analysis
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        skills_analysis = self._analyze_skills(resume_skills, job_skills)

        # 3. Experience analysis
        experience_analysis = self._analyze_experience(resume_text, job_description)

        # 4. Role compatibility analysis
        role_compatibility = self._analyze_role_compatibility(resume_text, job_description)

        # Calculate weighted final score
        weights = {
            'skills': 0.40,
            'experience': 0.25,
            'semantic': 0.20,
            'role': 0.15
        }

        final_score = (
            weights['skills'] * skills_analysis['score'] +
            weights['experience'] * experience_analysis['score'] +
            weights['semantic'] * semantic_score +
            weights['role'] * role_compatibility['score']
        )

        final_score = min(100, round(final_score, 1))

        # Generate intelligent recommendation
        recommendation_data = self._generate_recommendation(
            final_score,
            skills_analysis,
            experience_analysis,
            role_compatibility
        )

        print(f"[DEBUG] Scores - Skills: {skills_analysis['score']:.1f}, Experience: {experience_analysis['score']:.1f}, Semantic: {semantic_score:.1f}, Role: {role_compatibility['score']:.1f}, Final: {final_score}")

        return {
            'match_score': final_score,
            'prediction': recommendation_data['prediction'],
            'recommendation': recommendation_data['recommendation'],
            'should_apply': recommendation_data['should_apply'],
            'confidence': recommendation_data['confidence'],
            'strengths': recommendation_data['strengths'],
            'improvements': recommendation_data['improvements'],
            'matched_skills': skills_analysis['matched'][:15],
            'missing_skills': skills_analysis['missing'][:15],
            'experience_match': experience_analysis['match_description'],
            'details': {
                'skills_score': round(skills_analysis['score'], 1),
                'experience_score': round(experience_analysis['score'], 1),
                'semantic_score': round(semantic_score, 1),
                'role_score': round(role_compatibility['score'], 1),
                'resume_years': experience_analysis['resume_years'],
                'required_years': experience_analysis['required_years'],
                'critical_skills_met': skills_analysis['critical_met'],
                'total_skills_matched': len(skills_analysis['matched']),
                'total_skills_required': len(job_skills)
            }
        }
    
    def _analyze_skills(self, resume_skills, job_skills):
        """Analyze technical skills with priority weighting"""
        matched = []
        missing = []
        
        # Critical skills (programming languages, frameworks)
        critical_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 
                            'django', 'flask', 'spring', 'nodejs', 'aws', 'azure', 'gcp',
                            'docker', 'kubernetes', 'sql', 'mongodb', 'postgresql']
        
        critical_matched = 0
        critical_required = 0
        
        for job_skill in job_skills:
            is_critical = any(crit in job_skill.lower() for crit in critical_keywords)
            if is_critical:
                critical_required += 1
            
            found = False
            for resume_skill in resume_skills:
                if self._skills_match(job_skill, resume_skill):
                    matched.append(job_skill)
                    if is_critical:
                        critical_matched += 1
                    found = True
                    break
            
            if not found:
                missing.append(job_skill)
        
        # Calculate skill score with emphasis on critical skills
        if len(job_skills) > 0:
            base_match_rate = len(matched) / len(job_skills)
            
            # Bonus for critical skills
            if critical_required > 0:
                critical_rate = critical_matched / critical_required
                score = (base_match_rate * 0.6 + critical_rate * 0.4) * 100
            else:
                score = base_match_rate * 100
        else:
            score = 0
        
        return {
            'score': min(100, score),
            'matched': matched,
            'missing': missing,
            'critical_met': critical_matched,
            'critical_total': critical_required
        }
    
    def _analyze_experience(self, resume_text, job_description):
        """Analyze years of experience and seniority level"""
        resume_exp = extract_experience(resume_text)
        job_exp = extract_experience(job_description)
        
        resume_years = resume_exp['years']
        required_years = job_exp['years']
        
        # Determine experience match
        if required_years == 0:
            score = 80  # No specific requirement
            match_desc = "No specific experience requirement"
        elif resume_years >= required_years:
            # Exact or exceeds requirement
            score = 100
            match_desc = f"Meets requirement ({resume_years}+ years vs {required_years}+ required)"
        elif resume_years >= required_years * 0.75:
            # Close to requirement
            score = 85
            match_desc = f"Close to requirement ({resume_years}+ years vs {required_years}+ required)"
        elif resume_years >= required_years * 0.5:
            # Moderate gap
            score = 60
            match_desc = f"Some gap in experience ({resume_years}+ years vs {required_years}+ required)"
        else:
            # Significant gap
            score = 30
            match_desc = f"Significant experience gap ({resume_years}+ years vs {required_years}+ required)"
        
        return {
            'score': score,
            'resume_years': resume_years,
            'required_years': required_years,
            'match_description': match_desc
        }
    
    def _analyze_role_compatibility(self, resume_text, job_description):
        """Analyze role type compatibility (frontend, backend, full-stack, etc.)"""
        role_keywords = {
            'frontend': ['frontend', 'front-end', 'react', 'angular', 'vue', 'ui', 'ux', 'css', 'html'],
            'backend': ['backend', 'back-end', 'api', 'server', 'database', 'sql', 'microservices'],
            'fullstack': ['full-stack', 'fullstack', 'full stack'],
            'data': ['data scientist', 'data analyst', 'machine learning', 'ml', 'ai', 'analytics'],
            'devops': ['devops', 'kubernetes', 'docker', 'ci/cd', 'jenkins', 'terraform'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter', 'swift', 'kotlin']
        }
        
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Detect job role type
        job_role = None
        for role, keywords in role_keywords.items():
            if any(kw in job_lower for kw in keywords):
                job_role = role
                break
        
        if not job_role:
            return {'score': 70, 'match': 'General match'}
        
        # Check if resume matches the role
        resume_matches = sum(1 for kw in role_keywords[job_role] if kw in resume_lower)
        total_keywords = len(role_keywords[job_role])
        
        match_rate = resume_matches / total_keywords if total_keywords > 0 else 0
        score = match_rate * 100
        
        if score >= 60:
            match_desc = f"Strong {job_role} role alignment"
        elif score >= 30:
            match_desc = f"Moderate {job_role} role alignment"
        else:
            match_desc = f"Limited {job_role} role alignment"
        
        return {
            'score': score,
            'match': match_desc
        }
    
    def _skills_match(self, skill1, skill2):
        """Check if two skills match with variations"""
        skill1_lower = skill1.lower()
        skill2_lower = skill2.lower()
        
        variations = {
            'rest': ['restful', 'rest api', 'restapi'],
            'nodejs': ['node.js', 'node js'],
            'postgresql': ['postgres', 'psql'],
            'kubernetes': ['k8s'],
            'javascript': ['js'],
            'typescript': ['ts'],
        }
        
        if skill1_lower == skill2_lower:
            return True
        
        for key, vals in variations.items():
            if (skill1_lower == key and skill2_lower in vals) or \
               (skill2_lower == key and skill1_lower in vals):
                return True
        
        if len(skill1_lower) > 3 and len(skill2_lower) > 3:
            if skill1_lower in skill2_lower or skill2_lower in skill1_lower:
                return True
        
        return False
    
    def _generate_recommendation(self, score, skills_analysis, experience_analysis, role_compatibility):
        """Generate intelligent recommendation with actionable insights"""
        strengths = []
        improvements = []
        
        # Analyze strengths
        if skills_analysis['score'] >= 70:
            strengths.append(f"Strong technical skill match ({len(skills_analysis['matched'])} key skills aligned)")
        if experience_analysis['score'] >= 80:
            strengths.append(f"Experience level meets or exceeds requirements")
        if role_compatibility['score'] >= 60:
            strengths.append(f"Good role compatibility")
        
        # Analyze improvements
        if skills_analysis['score'] < 60:
            improvements.append(f"Consider developing these skills: {', '.join(skills_analysis['missing'][:5])}")
        if experience_analysis['score'] < 60:
            improvements.append(f"Gain more experience in the required domain")
        if len(skills_analysis['missing']) > 0:
            critical_missing = [s for s in skills_analysis['missing'] if any(c in s.lower() for c in ['python', 'java', 'react', 'aws'])]
            if critical_missing:
                improvements.append(f"Critical skills missing: {', '.join(critical_missing[:3])}")
        
        # Determine recommendation
        if score >= 75:
            prediction = "Strongly Recommended"
            should_apply = True
            confidence = "High"
            recommendation = "Excellent match! Your skills and experience align very well with this position. You should definitely apply."
        elif score >= 60:
            prediction = "Recommended"
            should_apply = True
            confidence = "Medium-High"
            recommendation = "Good match! You meet most requirements. Apply and highlight your relevant experience."
        elif score >= 45:
            prediction = "Consider Applying"
            should_apply = True
            confidence = "Medium"
            recommendation = "Moderate match. You have some relevant skills. Consider applying if you're willing to learn and grow."
        else:
            prediction = "Not Recommended"
            should_apply = False
            confidence = "Low"
            recommendation = "Limited match. This role may require skills or experience you don't currently have. Focus on building relevant expertise first."
        
        return {
            'prediction': prediction,
            'should_apply': should_apply,
            'confidence': confidence,
            'recommendation': recommendation,
            'strengths': strengths if strengths else ["Review the missing skills to identify growth areas"],
            'improvements': improvements if improvements else ["Continue building your current skillset"]
        }