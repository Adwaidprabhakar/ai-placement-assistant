import React, { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/layout/Header';
import HeroSection from './components/layout/HeroSection';
import ChatbotPage from './pages/ChatbotPage';
import ResumePage from './pages/ResumePage';
import RoadmapPage from './pages/RoadmapPage';
import InterviewPage from './pages/InterviewPage';
import DsaPage from './pages/DsaPage';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';

export default function App() {
    const [isDark, setIsDark] = useState(true);

    const toggleTheme = () => setIsDark(!isDark);

    return (
        <AuthProvider>
            <ToastProvider>
                <div className={`min-h-screen ${isDark ? 'bg-[#06070B] text-slate-100' : 'bg-slate-50 text-slate-900'} flex flex-col font-sans transition-colors duration-300`}>
                    <Header
                        isDark={isDark}
                        toggleTheme={toggleTheme}
                    />

                    <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-[#06070B]">
                        <div className="max-w-7xl mx-auto h-full space-y-6">
                            <HeroSection />

                            <Routes>
                                <Route path="/" element={<Navigate to="/chatbot" replace />} />
                                <Route path="/chatbot" element={<ChatbotPage />} />
                                <Route path="/resume" element={<ResumePage />} />
                                <Route path="/roadmap" element={<RoadmapPage />} />
                                <Route path="/interview" element={<InterviewPage />} />
                                <Route path="/dsa" element={<DsaPage />} />
                            </Routes>
                        </div>
                    </main>
                </div>
            </ToastProvider>
        </AuthProvider>
    );
}
