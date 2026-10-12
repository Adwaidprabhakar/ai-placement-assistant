import React from 'react';
import { Sparkles, ArrowRight, Code2, MessageSquare } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function HeroSection() {
    const navigate = useNavigate();

    return (
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#0c0d16] via-[#090a10] to-[#06070b] border border-purple-500/20 p-6 md:p-10 shadow-2xl smart-purple-glow">
            {/* Ambient Purple & Violet Neon Background Glow Orbs */}
            <div className="absolute top-0 right-1/4 w-96 h-96 bg-purple-600/15 rounded-full blur-[100px] pointer-events-none -translate-y-1/2"></div>
            <div className="absolute bottom-0 left-1/3 w-80 h-80 bg-indigo-600/15 rounded-full blur-[100px] pointer-events-none translate-y-1/2"></div>

            <div className="relative z-10 max-w-5xl mx-auto space-y-8">
                {/* Badge Tag */}
                <div className="flex items-center gap-3">
                    <span className="px-3.5 py-1 bg-purple-500/10 border border-purple-500/30 text-purple-300 font-extrabold text-[10px] tracking-[0.25em] uppercase rounded-full flex items-center gap-1.5 shadow-sm">
                        <Sparkles className="w-3.5 h-3.5 animate-pulse text-purple-400" />
                        Smart Business AI Studio
                    </span>
                    <span className="text-[11px] text-slate-400 font-semibold tracking-wider uppercase hidden sm:inline">
                        Placement AI Platform v2.0
                    </span>
                </div>

                {/* Main Hero Header with Instrument Serif Italic Accent */}
                <div className="space-y-4">
                    <h1 className="text-3xl md:text-5xl lg:text-6xl font-black font-jakarta tracking-tight text-white uppercase leading-[1.1]">
                        Accelerate Placements With <br />
                        <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-300 bg-clip-text text-transparent font-serif-title italic font-normal tracking-normal text-4xl md:text-6xl lg:text-7xl lowercase">
                            Smart Business AI.
                        </span>
                    </h1>
                    <p className="text-slate-300 text-xs md:text-sm max-w-2xl leading-relaxed font-sans">
                        Empower your software engineering placement workflow with 24/7 AI placement advisors, ATS resume scoring, dynamic 1-12 month roadmaps, voice-to-voice mock interviews, and Python DSA execution.
                    </p>
                </div>

                {/* CTA Action Triggers */}
                <div className="flex flex-wrap items-center gap-3 pt-1">
                    <button
                        onClick={() => navigate('/chatbot')}
                        className="px-6 py-3 bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-black uppercase text-xs tracking-wider rounded-xl transition shadow-lg shadow-purple-500/25 flex items-center gap-2 border border-purple-400/30"
                    >
                        <MessageSquare className="w-4 h-4" /> Start AI Advisor <ArrowRight className="w-4 h-4" />
                    </button>
                    <button
                        onClick={() => navigate('/dsa')}
                        className="px-6 py-3 bg-slate-900/90 hover:bg-slate-800 text-purple-300 border border-purple-500/30 hover:border-purple-400 font-bold uppercase text-xs tracking-wider rounded-xl transition flex items-center gap-2"
                    >
                        <Code2 className="w-4 h-4 text-purple-400" /> Launch DSA Studio
                    </button>
                </div>

                {/* Placement AI Bento Stats Counter Bar */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6 border-t border-slate-800/80">
                    <div className="p-4 bg-slate-950/70 border border-purple-500/20 rounded-2xl flex flex-col justify-center backdrop-blur-md hover:border-purple-500/40 transition">
                        <span className="text-2xl md:text-3xl font-extrabold font-jakarta text-purple-400">230+</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mt-1">Completed Problems</span>
                    </div>

                    <div className="p-4 bg-slate-950/70 border border-purple-500/20 rounded-2xl flex flex-col justify-center backdrop-blur-md hover:border-purple-500/40 transition">
                        <span className="text-2xl md:text-3xl font-extrabold font-jakarta text-indigo-400">1068+</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mt-1">Happy Candidates</span>
                    </div>

                    <div className="p-4 bg-slate-950/70 border border-purple-500/20 rounded-2xl flex flex-col justify-center backdrop-blur-md hover:border-purple-500/40 transition">
                        <span className="text-2xl md:text-3xl font-extrabold font-jakarta text-pink-400">98%</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mt-1">ATS Target Score</span>
                    </div>

                    <div className="p-4 bg-slate-950/70 border border-purple-500/20 rounded-2xl flex flex-col justify-center backdrop-blur-md hover:border-purple-500/40 transition">
                        <span className="text-2xl md:text-3xl font-extrabold font-jakarta text-cyan-400">24/7</span>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mt-1">Smart Placement AI</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
