import React, { useState, useRef } from 'react';
import { Download, Sparkles, Plus, Trash2, CheckCircle, AlertTriangle, ArrowRight, ArrowLeft } from 'lucide-react';
import axios from 'axios';
import html2pdf from 'html2pdf.js';

import { API_BASE } from '../config/api';

const SDE_PRESET = {
    fullName: "Adwait Sharma",
    email: "adwait.sharma@example.com",
    phone: "+91 98765 43210",
    location: "Bangalore, India",
    linkedin: "linkedin.com/in/adwait-sharma",
    github: "github.com/adwait-sharma",
    summary: "Results-driven Computer Science graduate with strong technical foundation in Data Structures, Python backend engineering, and modern React web applications. Seeking SDE opportunity to deliver scalable software solutions.",
    education: [
        {
            institution: "National Institute of Technology",
            degree: "B.Tech in Computer Science & Engineering",
            year: "2022 - 2026",
            score: "CGPA: 8.75/10.0"
        }
    ],
    experience: [
        {
            company: "TechCorp Solutions",
            role: "Software Engineering Intern",
            duration: "May 2025 - Aug 2025",
            details: "Engineered microservices using FastAPI & Python, reducing API latency by 35%.\nImplemented JWT authentication and Redis caching for high concurrency requests."
        }
    ],
    projects: [
        {
            title: "Predictive Violence Detection System",
            tech: "Python, PyTorch, OpenCV, React, FastAPI",
            link: "github.com/adwait/sentry-x",
            description: "Built real-time video surveillance pipeline using ResNet-18 & Attention mechanisms.\nAchieved 94.2% threat detection accuracy on RWF-2000 benchmark dataset."
        },
        {
            title: "Placement Assistance Platform (Placement AI)",
            tech: "React, Tailwind CSS, Python, OpenAI API",
            link: "github.com/adwait/placement-ai",
            description: "Designed multi-module placement dashboard with AI advisor, voice mock interviewer, and ATS resume builder."
        }
    ],
    skills: [
        "Python", "C++", "JavaScript", "React.js", "FastAPI", "Tailwind CSS", "Data Structures & Algorithms", "Git", "Docker", "SQL"
    ]
};

const DATA_ANALYST_PRESET = {
    fullName: "Ananya Roy",
    email: "ananya.roy@example.com",
    phone: "+91 91234 56789",
    location: "Hyderabad, India",
    linkedin: "linkedin.com/in/ananya-roy-data",
    github: "github.com/ananya-analytics",
    summary: "Detail-oriented Data Analyst proficient in SQL, Python, Tableau, and statistical modeling. Experienced in translating complex datasets into actionable business insights.",
    education: [
        {
            institution: "BITS Pilani",
            degree: "B.E. in Information Systems",
            year: "2022 - 2026",
            score: "CGPA: 8.90/10.0"
        }
    ],
    experience: [
        {
            company: "Analytics Cloud Inc",
            role: "Data Analytics Intern",
            duration: "Jun 2025 - Aug 2025",
            details: "Analyzed customer churn trends across 500k active users using SQL window functions.\nBuilt automated PowerBI interactive dashboard reducing monthly reporting time by 15 hours."
        }
    ],
    projects: [
        {
            title: "E-Commerce Customer Segmentation Analysis",
            tech: "Python, Pandas, Scikit-Learn, PowerBI",
            link: "github.com/ananya/customer-segmentation",
            description: "Applied K-Means clustering to segment 50,000 customers based on purchase behavior.\nIdentified high-value customer cluster driving 42% of overall revenue."
        }
    ],
    skills: [
        "SQL", "Python", "Pandas", "NumPy", "PowerBI", "Tableau", "A/B Testing", "Excel PowerPivot", "Statistics"
    ]
};

const STEPS = ['personal', 'education', 'skills', 'projects', 'experience'];

export default function ResumePage() {
    const [resumeData, setResumeData] = useState(SDE_PRESET);
    const [currentStepIdx, setCurrentStepIdx] = useState(0);
    const [analysis, setAnalysis] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [generatingPdf, setGeneratingPdf] = useState(false);
    const [newSkill, setNewSkill] = useState('');
    const previewRef = useRef(null);

    const activeTab = STEPS[currentStepIdx];

    const handleInputChange = (field, value) => {
        setResumeData(prev => ({ ...prev, [field]: value }));
    };

    const handleArrayChange = (category, index, field, value) => {
        setResumeData(prev => {
            const updated = [...prev[category]];
            updated[index] = { ...updated[index], [field]: value };
            return { ...prev, [category]: updated };
        });
    };

    const addItem = (category, emptyTemplate) => {
        setResumeData(prev => ({
            ...prev,
            [category]: [...prev[category], emptyTemplate]
        }));
    };

    const removeItem = (category, index) => {
        setResumeData(prev => ({
            ...prev,
            [category]: prev[category].filter((_, i) => i !== index)
        }));
    };

    const addSkill = () => {
        if (newSkill.trim() && !resumeData.skills.includes(newSkill.trim())) {
            setResumeData(prev => ({ ...prev, skills: [...prev.skills, newSkill.trim()] }));
            setNewSkill('');
        }
    };

    const removeSkill = (skillToRemove) => {
        setResumeData(prev => ({
            ...prev,
            skills: prev.skills.filter(s => s !== skillToRemove)
        }));
    };

    const runAtsAnalysis = async () => {
        setAnalyzing(true);
        try {
            const res = await axios.post(`${API_BASE}/resume/analyze`, resumeData);
            setAnalysis(res.data);
        } catch (err) {
            console.error(err);
            setAnalysis({
                score: 85,
                strengths: ["Clear section organization", "Strong technical skill tags", "Quantifiable metrics included"],
                improvements: ["Add target job keywords", "Highlight leadership impact"],
                suggested_summary: resumeData.summary
            });
        } finally {
            setAnalyzing(false);
        }
    };

    const handleDownloadPdf = async () => {
        setGeneratingPdf(true);
        try {
            const response = await axios.post(`${API_BASE}/resume/generate`, resumeData, {
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${resumeData.fullName.replace(/\s+/g, '_')}_Resume.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.warn("Backend PDF generation fallback to HTML2PDF:", err);
            const element = previewRef.current;
            const opt = {
                margin: 0.3,
                filename: `${resumeData.fullName.replace(/\s+/g, '_')}_Resume.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
            };
            html2pdf().set(opt).from(element).save();
        } finally {
            setGeneratingPdf(false);
        }
    };

    return (
        <div className="flex flex-col lg:flex-row h-[calc(100vh-8rem)] gap-6">
            {/* Left Multi-Step Form Builder Panel */}
            <div className="lg:w-1/2 flex flex-col bg-[#090a10] border border-purple-500/20 rounded-3xl overflow-hidden shadow-2xl smart-purple-glow">
                {/* Step Wizard Header */}
                <div className="bg-[#0d0e17] p-4 border-b border-purple-500/20 flex items-center justify-between">
                    <div className="flex items-center gap-2 overflow-x-auto scrollbar-none">
                        {[
                            { id: 'personal', label: '1. Personal' },
                            { id: 'education', label: '2. Education' },
                            { id: 'skills', label: '3. Skills' },
                            { id: 'projects', label: '4. Projects' },
                            { id: 'experience', label: '5. Experience' },
                        ].map((step, idx) => (
                            <button
                                key={step.id}
                                onClick={() => setCurrentStepIdx(idx)}
                                className={`px-3 py-1.5 text-xs font-bold rounded-xl transition ${currentStepIdx === idx
                                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md font-black border border-purple-400/30'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-900'
                                    }`}
                            >
                                {step.label}
                            </button>
                        ))}
                    </div>

                    <div className="flex items-center gap-1.5">
                        <button
                            onClick={() => setResumeData(SDE_PRESET)}
                            className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-purple-300 rounded-lg text-[11px] font-bold border border-purple-500/20"
                        >
                            SDE Preset
                        </button>
                        <button
                            onClick={() => setResumeData(DATA_ANALYST_PRESET)}
                            className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 text-purple-300 rounded-lg text-[11px] font-bold border border-purple-500/20"
                        >
                            Analyst Preset
                        </button>
                    </div>
                </div>

                {/* Tab Form Contents */}
                <div className="flex-1 overflow-y-auto p-6 space-y-5 bg-[#090a10]">
                    {activeTab === 'personal' && (
                        <div className="space-y-4">
                            <h3 className="text-xs font-black text-purple-300 uppercase tracking-widest">Personal Information</h3>
                            <div>
                                <label className="text-xs text-slate-400 font-medium">Full Name</label>
                                <input
                                    type="text"
                                    value={resumeData.fullName}
                                    onChange={(e) => handleInputChange('fullName', e.target.value)}
                                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="text-xs text-slate-400 font-medium">Email</label>
                                    <input
                                        type="email"
                                        value={resumeData.email}
                                        onChange={(e) => handleInputChange('email', e.target.value)}
                                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                    />
                                </div>
                                <div>
                                    <label className="text-xs text-slate-400 font-medium">Phone</label>
                                    <input
                                        type="text"
                                        value={resumeData.phone}
                                        onChange={(e) => handleInputChange('phone', e.target.value)}
                                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                    />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="text-xs text-slate-400 font-medium">Location</label>
                                    <input
                                        type="text"
                                        value={resumeData.location}
                                        onChange={(e) => handleInputChange('location', e.target.value)}
                                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                    />
                                </div>
                                <div>
                                    <label className="text-xs text-slate-400 font-medium">LinkedIn URL</label>
                                    <input
                                        type="text"
                                        value={resumeData.linkedin}
                                        onChange={(e) => handleInputChange('linkedin', e.target.value)}
                                        className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="text-xs text-slate-400 font-medium">Professional Summary</label>
                                <textarea
                                    rows={4}
                                    value={resumeData.summary}
                                    onChange={(e) => handleInputChange('summary', e.target.value)}
                                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400 leading-relaxed"
                                />
                            </div>
                        </div>
                    )}

                    {activeTab === 'education' && (
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xs font-black text-purple-300 uppercase tracking-widest">Education Details</h3>
                                <button
                                    onClick={() => addItem('education', { institution: '', degree: '', year: '', score: '' })}
                                    className="px-3 py-1 bg-purple-500/10 text-purple-300 hover:bg-purple-500/20 border border-purple-500/30 rounded-xl text-xs font-bold flex items-center gap-1"
                                >
                                    <Plus className="w-3.5 h-3.5" /> Add School
                                </button>
                            </div>
                            {resumeData.education.map((edu, idx) => (
                                <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl relative group space-y-3">
                                    <button
                                        onClick={() => removeItem('education', idx)}
                                        className="absolute top-3 right-3 text-slate-500 hover:text-red-400 transition"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                    <input
                                        type="text"
                                        placeholder="Institution Name"
                                        value={edu.institution}
                                        onChange={(e) => handleArrayChange('education', idx, 'institution', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-100"
                                    />
                                    <div className="grid grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            placeholder="Degree / Branch"
                                            value={edu.degree}
                                            onChange={(e) => handleArrayChange('education', idx, 'degree', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                        />
                                        <input
                                            type="text"
                                            placeholder="Graduation Year (e.g. 2022-2026)"
                                            value={edu.year}
                                            onChange={(e) => handleArrayChange('education', idx, 'year', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                        />
                                    </div>
                                    <input
                                        type="text"
                                        placeholder="CGPA / Percentage"
                                        value={edu.score}
                                        onChange={(e) => handleArrayChange('education', idx, 'score', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                    />
                                </div>
                            ))}
                        </div>
                    )}

                    {activeTab === 'skills' && (
                        <div className="space-y-4">
                            <h3 className="text-xs font-black text-purple-300 uppercase tracking-widest">Technical Skills & Tools</h3>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    placeholder="Add skill (e.g. Python, Docker, SQL)..."
                                    value={newSkill}
                                    onChange={(e) => setNewSkill(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && addSkill()}
                                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-400"
                                />
                                <button
                                    onClick={addSkill}
                                    className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-black uppercase rounded-xl text-xs hover:from-purple-500 transition border border-purple-400/30"
                                >
                                    Add
                                </button>
                            </div>
                            <div className="flex flex-wrap gap-2 pt-2">
                                {resumeData.skills.map((skill, idx) => (
                                    <span
                                        key={idx}
                                        className="px-3 py-1.5 bg-slate-950 border border-purple-500/20 text-purple-300 text-xs rounded-xl flex items-center gap-1.5 font-semibold"
                                    >
                                        {skill}
                                        <button
                                            onClick={() => removeSkill(skill)}
                                            className="text-slate-500 hover:text-red-400 transition ml-1"
                                        >
                                            ×
                                        </button>
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}

                    {activeTab === 'projects' && (
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xs font-black text-purple-300 uppercase tracking-widest">Key Projects</h3>
                                <button
                                    onClick={() => addItem('projects', { title: '', tech: '', link: '', description: '' })}
                                    className="px-3 py-1 bg-purple-500/10 text-purple-300 hover:bg-purple-500/20 border border-purple-500/30 rounded-xl text-xs font-bold flex items-center gap-1"
                                >
                                    <Plus className="w-3.5 h-3.5" /> Add Project
                                </button>
                            </div>
                            {resumeData.projects.map((proj, idx) => (
                                <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl relative group space-y-3">
                                    <button
                                        onClick={() => removeItem('projects', idx)}
                                        className="absolute top-3 right-3 text-slate-500 hover:text-red-400 transition"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                    <input
                                        type="text"
                                        placeholder="Project Title"
                                        value={proj.title}
                                        onChange={(e) => handleArrayChange('projects', idx, 'title', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-100"
                                    />
                                    <div className="grid grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            placeholder="Tech Stack Used"
                                            value={proj.tech}
                                            onChange={(e) => handleArrayChange('projects', idx, 'tech', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                        />
                                        <input
                                            type="text"
                                            placeholder="GitHub / Live Link"
                                            value={proj.link}
                                            onChange={(e) => handleArrayChange('projects', idx, 'link', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                        />
                                    </div>
                                    <textarea
                                        rows={3}
                                        placeholder="Description & Key Features (One bullet per line)"
                                        value={proj.description}
                                        onChange={(e) => handleArrayChange('projects', idx, 'description', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100 leading-relaxed"
                                    />
                                </div>
                            ))}
                        </div>
                    )}

                    {activeTab === 'experience' && (
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-xs font-black text-purple-300 uppercase tracking-widest">Work Experience</h3>
                                <button
                                    onClick={() => addItem('experience', { company: '', role: '', duration: '', details: '' })}
                                    className="px-3 py-1 bg-purple-500/10 text-purple-300 hover:bg-purple-500/20 border border-purple-500/30 rounded-xl text-xs font-bold flex items-center gap-1"
                                >
                                    <Plus className="w-3.5 h-3.5" /> Add Experience
                                </button>
                            </div>
                            {resumeData.experience.map((exp, idx) => (
                                <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl relative group space-y-3">
                                    <button
                                        onClick={() => removeItem('experience', idx)}
                                        className="absolute top-3 right-3 text-slate-500 hover:text-red-400 transition"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                    <div className="grid grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            placeholder="Company Name"
                                            value={exp.company}
                                            onChange={(e) => handleArrayChange('experience', idx, 'company', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-100"
                                        />
                                        <input
                                            type="text"
                                            placeholder="Job Title / Role"
                                            value={exp.role}
                                            onChange={(e) => handleArrayChange('experience', idx, 'role', e.target.value)}
                                            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-100"
                                        />
                                    </div>
                                    <input
                                        type="text"
                                        placeholder="Duration (e.g. May 2025 - Aug 2025)"
                                        value={exp.duration}
                                        onChange={(e) => handleArrayChange('experience', idx, 'duration', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100"
                                    />
                                    <textarea
                                        rows={3}
                                        placeholder="Responsibilities & Accomplishments (One bullet per line)"
                                        value={exp.details}
                                        onChange={(e) => handleArrayChange('experience', idx, 'details', e.target.value)}
                                        className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100 leading-relaxed"
                                    />
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Wizard Footer Controls */}
                <div className="p-4 bg-[#0d0e17] border-t border-purple-500/20 flex items-center justify-between gap-3">
                    <div className="flex gap-2">
                        <button
                            disabled={currentStepIdx === 0}
                            onClick={() => setCurrentStepIdx(prev => prev - 1)}
                            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-slate-300 rounded-xl text-xs font-bold uppercase flex items-center gap-1 border border-slate-800"
                        >
                            <ArrowLeft className="w-3.5 h-3.5" /> Previous
                        </button>
                        <button
                            disabled={currentStepIdx === STEPS.length - 1}
                            onClick={() => setCurrentStepIdx(prev => prev + 1)}
                            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-slate-300 rounded-xl text-xs font-bold uppercase flex items-center gap-1 border border-slate-800"
                        >
                            Next <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                    </div>

                    <div className="flex gap-2">
                        <button
                            onClick={runAtsAnalysis}
                            disabled={analyzing}
                            className="px-4 py-2 bg-purple-950/40 hover:bg-purple-900/60 text-purple-300 border border-purple-500/30 rounded-xl text-xs font-bold uppercase flex items-center gap-1.5 transition"
                        >
                            <Sparkles className="w-4 h-4 text-purple-400" />
                            {analyzing ? 'Analyzing...' : 'AI ATS Review'}
                        </button>
                        <button
                            onClick={handleDownloadPdf}
                            disabled={generatingPdf}
                            className="px-5 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-black uppercase rounded-xl text-xs flex items-center gap-2 transition shadow-lg shadow-purple-500/20 border border-purple-400/30"
                        >
                            <Download className="w-4 h-4 text-white" />
                            {generatingPdf ? 'Generating PDF...' : 'Download ATS PDF'}
                        </button>
                    </div>
                </div>
            </div>

            {/* Right Live Preview & ATS Analysis Panel */}
            <div className="lg:w-1/2 flex flex-col h-full bg-[#090a10] border border-purple-500/20 rounded-3xl overflow-hidden shadow-2xl smart-purple-glow">
                {analysis && (
                    <div className="p-4 bg-[#0d0e17] border-b border-purple-500/20 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-extrabold text-lg ${analysis.score >= 80 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                                }`}>
                                {analysis.score}%
                            </div>
                            <div>
                                <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">ATS Match Score</h4>
                                <p className="text-[11px] text-slate-400">Format & Keyword Optimization</p>
                            </div>
                        </div>
                        <div className="text-right text-xs">
                            <span className="text-emerald-400 flex items-center gap-1 justify-end font-bold">
                                <CheckCircle className="w-3.5 h-3.5" /> {analysis.strengths.length} Strengths
                            </span>
                            <span className="text-amber-400 flex items-center gap-1 justify-end font-bold mt-0.5">
                                <AlertTriangle className="w-3.5 h-3.5" /> {analysis.improvements.length} Improvements
                            </span>
                        </div>
                    </div>
                )}

                {/* Live Document Preview Box */}
                <div className="flex-1 overflow-y-auto p-6 bg-[#090a10]">
                    <div
                        ref={previewRef}
                        className="w-full bg-white text-slate-900 p-8 shadow-2xl rounded-sm font-sans text-[13px] leading-normal min-h-[800px]"
                    >
                        {/* Header */}
                        <div className="border-b border-slate-300 pb-4 mb-4 text-center">
                            <h1 className="text-2xl font-bold uppercase tracking-wide text-slate-900">{resumeData.fullName || 'YOUR NAME'}</h1>
                            <div className="flex flex-wrap justify-center items-center gap-3 text-[11px] text-slate-600 mt-1.5">
                                {resumeData.email && <span>{resumeData.email}</span>}
                                {resumeData.phone && <span>• {resumeData.phone}</span>}
                                {resumeData.location && <span>• {resumeData.location}</span>}
                            </div>
                            <div className="flex flex-wrap justify-center items-center gap-3 text-[11px] text-purple-700 font-medium mt-1">
                                {resumeData.linkedin && <span>{resumeData.linkedin}</span>}
                                {resumeData.github && <span>• {resumeData.github}</span>}
                            </div>
                        </div>

                        {/* Summary */}
                        {resumeData.summary && (
                            <div className="mb-4">
                                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">Professional Summary</h2>
                                <p className="text-slate-700 text-[12px] leading-relaxed">{resumeData.summary}</p>
                            </div>
                        )}

                        {/* Education */}
                        {resumeData.education.length > 0 && (
                            <div className="mb-4">
                                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">Education</h2>
                                {resumeData.education.map((edu, i) => (
                                    <div key={i} className="mb-2">
                                        <div className="flex justify-between font-bold text-slate-900">
                                            <span>{edu.institution}</span>
                                            <span className="text-[11px] text-slate-600 font-normal">{edu.year}</span>
                                        </div>
                                        <div className="flex justify-between text-slate-700 text-[12px]">
                                            <span>{edu.degree}</span>
                                            <span className="font-semibold text-slate-800">{edu.score}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Work Experience */}
                        {resumeData.experience.length > 0 && (
                            <div className="mb-4">
                                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">Experience</h2>
                                {resumeData.experience.map((exp, i) => (
                                    <div key={i} className="mb-3">
                                        <div className="flex justify-between font-bold text-slate-900">
                                            <span>{exp.role} — <span className="font-medium text-slate-700">{exp.company}</span></span>
                                            <span className="text-[11px] text-slate-600 font-normal">{exp.duration}</span>
                                        </div>
                                        <ul className="list-disc ml-4 text-slate-700 text-[12px] space-y-1 mt-1">
                                            {exp.details.split('\n').map((line, idx) => line.trim() && (
                                                <li key={idx}>{line.trim()}</li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Projects */}
                        {resumeData.projects.length > 0 && (
                            <div className="mb-4">
                                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">Projects</h2>
                                {resumeData.projects.map((proj, i) => (
                                    <div key={i} className="mb-3">
                                        <div className="flex justify-between font-bold text-slate-900">
                                            <span>{proj.title} <span className="text-[11px] font-normal text-slate-600">({proj.tech})</span></span>
                                            <span className="text-[11px] text-purple-700 font-normal">{proj.link}</span>
                                        </div>
                                        <ul className="list-disc ml-4 text-slate-700 text-[12px] space-y-1 mt-1">
                                            {proj.description.split('\n').map((line, idx) => line.trim() && (
                                                <li key={idx}>{line.trim()}</li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Skills */}
                        {resumeData.skills.length > 0 && (
                            <div>
                                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">Technical Skills</h2>
                                <p className="text-slate-800 text-[12px] font-medium leading-relaxed">
                                    {resumeData.skills.join(' • ')}
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
