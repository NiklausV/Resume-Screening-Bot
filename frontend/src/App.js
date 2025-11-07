import React, { useState } from 'react';
import { Upload, FileText, Search, CheckCircle, XCircle, AlertCircle, Loader, TrendingUp, Award, Lightbulb, Target, Sparkles } from 'lucide-react';

export default function ResumeScreeningApp() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please upload a PDF or DOCX file');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a resume');
      return;
    }
    
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://localhost:5000/api/screen-resume', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setResult(data);
      } else {
        setError(data.error || 'An error occurred while processing your request');
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 75) return 'from-green-400 to-emerald-500';
    if (score >= 60) return 'from-blue-400 to-cyan-500';
    if (score >= 45) return 'from-yellow-400 to-orange-500';
    return 'from-red-400 to-rose-500';
  };

  const getPredictionStyle = (prediction) => {
    if (prediction === 'Strongly Recommended') return {
      bg: 'bg-gradient-to-r from-green-500/20 to-emerald-500/20',
      border: 'border-green-500/50',
      icon: <Award className="text-green-400" size={40} />,
      glow: 'shadow-lg shadow-green-500/30'
    };
    if (prediction === 'Recommended') return {
      bg: 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20',
      border: 'border-blue-500/50',
      icon: <CheckCircle className="text-blue-400" size={40} />,
      glow: 'shadow-lg shadow-blue-500/30'
    };
    if (prediction === 'Consider Applying') return {
      bg: 'bg-gradient-to-r from-yellow-500/20 to-orange-500/20',
      border: 'border-yellow-500/50',
      icon: <AlertCircle className="text-yellow-400" size={40} />,
      glow: 'shadow-lg shadow-yellow-500/30'
    };
    return {
      bg: 'bg-gradient-to-r from-red-500/20 to-rose-500/20',
      border: 'border-red-500/50',
      icon: <XCircle className="text-red-400" size={40} />,
      glow: 'shadow-lg shadow-red-500/30'
    };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 p-4 sm:p-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 space-y-4">
          <div className="flex justify-center mb-4">
            <div className="relative">
              <Sparkles className="text-purple-400 animate-pulse" size={48} />
              <div className="absolute inset-0 bg-purple-500 blur-xl opacity-50"></div>
            </div>
          </div>
          <h1 className="text-5xl sm:text-7xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
            AI Resume Analyzer
          </h1>
          <p className="text-gray-300 text-lg sm:text-xl max-w-3xl mx-auto">
            Powered by advanced machine learning to evaluate your candidacy holistically - skills, experience, and role fit
          </p>
        </div>

        {/* Main Form */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Upload Resume */}
          <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30 hover:border-purple-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/20">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Upload className="mr-3 text-purple-400" size={28} />
              Upload Your Resume
            </h2>
            
            <label className="block">
              <div className="border-2 border-dashed border-purple-500/40 rounded-2xl p-10 text-center hover:border-purple-400 hover:bg-purple-500/5 transition-all duration-300 cursor-pointer group">
                <FileText className="mx-auto mb-4 text-purple-400 group-hover:scale-110 transition-transform" size={56} />
                <p className="text-gray-200 mb-2 font-medium">
                  {file ? file.name : 'Click to upload or drag and drop'}
                </p>
                <p className="text-gray-500 text-sm">PDF or DOCX • Max 16MB</p>
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf,.docx,.doc"
                  onChange={handleFileChange}
                />
              </div>
            </label>

            {file && (
              <div className="mt-4 p-4 bg-gradient-to-r from-purple-600/20 to-pink-600/20 rounded-xl flex items-center justify-between border border-purple-500/30 animate-fadeIn">
                <div className="flex items-center">
                  <FileText className="mr-3 text-purple-400" size={24} />
                  <span className="text-sm font-medium">{file.name}</span>
                </div>
                <button
                  onClick={() => setFile(null)}
                  className="text-red-400 hover:text-red-300 text-sm font-semibold hover:scale-110 transition-transform"
                >
                  Remove
                </button>
              </div>
            )}
          </div>

          {/* Job Description */}
          <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30 hover:border-purple-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/20">
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Search className="mr-3 text-purple-400" size={28} />
              Job Description
            </h2>
            
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the complete job description here...

Example:
Senior Python Developer needed with 5+ years experience in Django, Flask, and RESTful APIs. Strong knowledge of AWS, Docker, PostgreSQL, and microservices architecture. Experience with machine learning libraries is a plus."
              className="w-full h-72 bg-slate-900/60 border border-purple-500/30 rounded-2xl p-5 text-white placeholder-gray-500 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-500/20 resize-none transition-all"
            />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/20 border-2 border-red-500/50 rounded-2xl p-5 mb-8 flex items-center animate-fadeIn backdrop-blur-sm">
            <XCircle className="mr-3 text-red-400 flex-shrink-0" size={28} />
            <span className="font-medium">{error}</span>
          </div>
        )}

        {/* Submit Button */}
        <div className="text-center mb-12">
          <button
            onClick={handleSubmit}
            disabled={loading || !file || !jobDescription.trim()}
            className="px-10 py-5 bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 hover:from-purple-500 hover:via-pink-500 hover:to-purple-500 rounded-2xl font-bold text-lg shadow-2xl shadow-purple-500/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto hover:scale-105 disabled:hover:scale-100 group"
          >
            {loading ? (
              <>
                <Loader className="mr-3 animate-spin" size={28} />
                Analyzing Your Resume...
              </>
            ) : (
              <>
                <Search className="mr-3 group-hover:rotate-12 transition-transform" size={28} />
                Analyze Match
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-8 animate-fadeIn">
            {/* Main Score Card */}
            <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl p-10 border border-purple-500/30 shadow-2xl">
              <h2 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                Analysis Results
              </h2>

              {/* Match Score Circular Progress */}
              <div className="mb-10 text-center">
                <div className="inline-block relative">
                  <svg className="transform -rotate-90 w-64 h-64" viewBox="0 0 200 200">
                    <circle
                      cx="100"
                      cy="100"
                      r="85"
                      stroke="currentColor"
                      strokeWidth="16"
                      fill="transparent"
                      className="text-slate-700/50"
                    />
                    <circle
                      cx="100"
                      cy="100"
                      r="85"
                      stroke="url(#gradient)"
                      strokeWidth="16"
                      fill="transparent"
                      strokeDasharray={`${2 * Math.PI * 85}`}
                      strokeDashoffset={`${2 * Math.PI * 85 * (1 - result.match_score / 100)}`}
                      strokeLinecap="round"
                      className="transition-all duration-1000 ease-out"
                      style={{
                        filter: 'drop-shadow(0 0 20px rgba(168, 85, 247, 0.6))'
                      }}
                    />
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#10b981" />
                        <stop offset="100%" stopColor="#059669" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center flex-col">
                    <span className={`text-6xl font-black bg-gradient-to-r ${getScoreColor(result.match_score)} bg-clip-text text-transparent`}>
                      {result.match_score}%
                    </span>
                    <span className="text-gray-400 text-lg font-semibold mt-2">Match Score</span>
                    <span className="text-gray-500 text-sm mt-1">{result.confidence} Confidence</span>
                  </div>
                </div>
              </div>

              {/* Prediction Card */}
              <div className={`mb-8 p-8 ${getPredictionStyle(result.prediction).bg} rounded-2xl border-2 ${getPredictionStyle(result.prediction).border} ${getPredictionStyle(result.prediction).glow} transition-all duration-300`}>
                <div className="flex items-center justify-center mb-4">
                  {getPredictionStyle(result.prediction).icon}
                  <span className="ml-4 text-3xl font-bold">{result.prediction}</span>
                </div>
                <p className="text-center text-gray-200 text-lg mb-4">{result.recommendation}</p>
                {result.should_apply !== undefined && (
                  <div className="text-center">
                    <span className={`inline-block px-6 py-2 rounded-full font-bold text-sm ${result.should_apply ? 'bg-green-500/30 text-green-300 border border-green-500' : 'bg-red-500/30 text-red-300 border border-red-500'}`}>
                      {result.should_apply ? '✓ You Should Apply' : '✗ Consider Other Opportunities'}
                    </span>
                  </div>
                )}
              </div>

              {/* Score Breakdown */}
              {result.details && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  <div className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 rounded-2xl p-5 border border-purple-500/30 text-center hover:scale-105 transition-transform">
                    <div className="text-3xl font-bold text-purple-300">{result.details.skills_score}%</div>
                    <div className="text-sm text-gray-400 mt-2">Skills Match</div>
                  </div>
                  <div className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 rounded-2xl p-5 border border-blue-500/30 text-center hover:scale-105 transition-transform">
                    <div className="text-3xl font-bold text-blue-300">{result.details.experience_score}%</div>
                    <div className="text-sm text-gray-400 mt-2">Experience</div>
                  </div>
                  <div className="bg-gradient-to-br from-pink-600/20 to-pink-800/20 rounded-2xl p-5 border border-pink-500/30 text-center hover:scale-105 transition-transform">
                    <div className="text-3xl font-bold text-pink-300">{result.details.semantic_score}%</div>
                    <div className="text-sm text-gray-400 mt-2">Context</div>
                  </div>
                  <div className="bg-gradient-to-br from-cyan-600/20 to-cyan-800/20 rounded-2xl p-5 border border-cyan-500/30 text-center hover:scale-105 transition-transform">
                    <div className="text-3xl font-bold text-cyan-300">{result.details.role_score}%</div>
                    <div className="text-sm text-gray-400 mt-2">Role Fit</div>
                  </div>
                </div>
              )}
            </div>

            {/* Strengths & Improvements */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Strengths */}
              <div className="bg-gradient-to-br from-green-900/20 to-emerald-900/20 backdrop-blur-xl border-2 border-green-500/40 rounded-3xl p-8 hover:shadow-xl hover:shadow-green-500/20 transition-all">
                <h3 className="text-2xl font-bold mb-6 flex items-center text-green-400">
                  <Award className="mr-3" size={28} />
                  Your Strengths
                </h3>
                <ul className="space-y-3">
                  {(result.strengths || []).length > 0 ? (
                    result.strengths.map((strength, idx) => (
                      <li key={idx} className="flex items-start">
                        <CheckCircle className="mr-3 text-green-400 flex-shrink-0 mt-1" size={20} />
                        <span className="text-gray-200">{strength}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-gray-400">Analyzing your profile...</li>
                  )}
                </ul>
              </div>

              {/* Improvements */}
              <div className="bg-gradient-to-br from-orange-900/20 to-amber-900/20 backdrop-blur-xl border-2 border-orange-500/40 rounded-3xl p-8 hover:shadow-xl hover:shadow-orange-500/20 transition-all">
                <h3 className="text-2xl font-bold mb-6 flex items-center text-orange-400">
                  <Lightbulb className="mr-3" size={28} />
                  Growth Opportunities
                </h3>
                <ul className="space-y-3">
                  {(result.improvements || []).length > 0 ? (
                    result.improvements.map((improvement, idx) => (
                      <li key={idx} className="flex items-start">
                        <TrendingUp className="mr-3 text-orange-400 flex-shrink-0 mt-1" size={20} />
                        <span className="text-gray-200">{improvement}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-gray-400">Keep building on your strengths!</li>
                  )}
                </ul>
              </div>
            </div>

            {/* Skills Analysis */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Matched Skills */}
              <div className="bg-gradient-to-br from-green-900/10 to-emerald-900/10 backdrop-blur-xl border border-green-500/30 rounded-3xl p-8 hover:shadow-xl hover:shadow-green-500/10 transition-all">
                <h3 className="text-2xl font-bold mb-6 flex items-center text-green-400">
                  <Target className="mr-3" size={28} />
                  Matched Skills ({(result.matched_skills || []).length})
                </h3>
                <div className="flex flex-wrap gap-3">
                  {(result.matched_skills || []).length > 0 ? (
                    result.matched_skills.map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-4 py-2 bg-green-600/30 border border-green-500/60 rounded-xl text-sm font-semibold hover:bg-green-600/40 hover:scale-105 transition-all cursor-default"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="text-gray-400">No matching skills detected</p>
                  )}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="bg-gradient-to-br from-red-900/10 to-rose-900/10 backdrop-blur-xl border border-red-500/30 rounded-3xl p-8 hover:shadow-xl hover:shadow-red-500/10 transition-all">
                <h3 className="text-2xl font-bold mb-6 flex items-center text-red-400">
                  <AlertCircle className="mr-3" size={28} />
                  Skills to Develop ({(result.missing_skills || []).length})
                </h3>
                <div className="flex flex-wrap gap-3">
                  {(result.missing_skills || []).length > 0 ? (
                    result.missing_skills.map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-4 py-2 bg-red-600/30 border border-red-500/60 rounded-xl text-sm font-semibold hover:bg-red-600/40 hover:scale-105 transition-all cursor-default"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="text-gray-400">You have all required skills!</p>
                  )}
                </div>
              </div>
            </div>

            {/* Experience Match */}
            {result.experience_match && (
              <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30">
                <h3 className="text-xl font-bold mb-4 text-purple-300">Experience Analysis</h3>
                <p className="text-gray-300 text-lg">{result.experience_match}</p>
                {result.details && (
                  <div className="mt-4 flex gap-6 text-sm">
                    <span className="text-gray-400">
                      Your Experience: <span className="font-bold text-white">{result.details.resume_years}+ years</span>
                    </span>
                    <span className="text-gray-400">
                      Required: <span className="font-bold text-white">{result.details.required_years}+ years</span>
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* Reset Button */}
            <div className="text-center pt-6">
              <button
                onClick={() => {
                  setResult(null);
                  setFile(null);
                  setJobDescription('');
                }}
                className="px-8 py-4 bg-gradient-to-r from-slate-700 to-slate-600 hover:from-slate-600 hover:to-slate-500 rounded-2xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
              >
                Analyze Another Resume
              </button>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-16 text-center space-y-3 text-gray-400 text-sm">
          <p className="font-semibold">Powered by Advanced Machine Learning</p>
          <p>Multi-factor AI Analysis: Skills • Experience • Context • Role Fit</p>
          <p className="text-xs">Built with Python, Flask, scikit-learn, React & Tailwind CSS</p>
        </div>
      </div>

      <style>{`
        @keyframes blob {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-blob {
          animation: blob 7s infinite;
        }
        
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        
        .animation-delay-4000 {
          animation-delay: 4s;
        }
        
        .animate-gradient {
          background-size: 200% 200%;
          animation: gradient 3s ease infinite;
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes gradient {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }
      `}</style>
    </div>
  );
}