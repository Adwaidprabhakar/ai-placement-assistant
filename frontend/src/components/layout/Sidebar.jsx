import React from 'react';
import { NavLink } from 'react-router-dom';
import { MessageSquare, FileText, Compass, Mic, Code2, X, Sparkles } from 'lucide-react';

const NAV_ITEMS = [
    { path: '/chatbot', label: 'Placement Advisor', icon: MessageSquare, badge: 'AI Chat' },
    { path: '/resume', label: 'ATS Resume Studio', icon: FileText, badge: 'ATS v2' },
    { path: '/roadmap', label: 'Career Roadmap', icon: Compass, badge: '1-12 Mo' },
    { path: '/interview', label: 'Mock Interview AI', icon: Mic, badge: 'Voice' },
    { path: '/dsa', label: 'Technical DSA Studio', icon: Code2, badge: 'IDE' }
];

export default function Sidebar({ isMobileOpen, closeMobileSidebar }) {
    return (
        <>
            {/* Mobile Backdrop */}
            {isMobileOpen && (
                <div
                    onClick={closeMobileSidebar}
                    className="fixed inset-0 bg-[#06070B]/80 backdrop-blur-sm z-40 md:hidden"
                />
            )}

            {/* Sidebar Container */}
            <aside
                className={`fixed md:static top-0 left-0 bottom-0 z-50 w-64 bg-[#090a10] border-r border-purple-500/20 flex flex-col transition-transform duration-300 ${isMobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
                    }`}
            >
                {/* Header Mobile Title */}
                <div className="p-4 border-b border-slate-800/80 flex items-center justify-between md:hidden">
                    <span className="text-xs font-black text-purple-400 uppercase tracking-widest">Placement AI Navigation</span>
                    <button onClick={closeMobileSidebar} className="text-slate-400 hover:text-white">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Navigation Items */}
                <div className="p-3 space-y-2 flex-1 overflow-y-auto">
                    <div className="px-3 py-2 text-[10px] font-black text-purple-400/80 uppercase tracking-[0.2em]">
                        Placement AI Modules
                    </div>

                    {NAV_ITEMS.map((item) => {
                        const Icon = item.icon;
                        return (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                onClick={closeMobileSidebar}
                                className={({ isActive }) =>
                                    `flex items-center justify-between px-3.5 py-3 rounded-2xl text-xs font-bold transition-all duration-200 group ${isActive
                                        ? 'bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 text-white shadow-lg shadow-purple-500/25 font-black border border-purple-400/30'
                                        : 'text-slate-400 hover:bg-purple-950/20 hover:text-purple-300 hover:border-purple-500/30'
                                    }`
                                }
                            >
                                <div className="flex items-center gap-3">
                                    <Icon className="w-4 h-4 flex-shrink-0" />
                                    <span className="tracking-wide">{item.label}</span>
                                </div>
                                <span className="text-[9px] px-2 py-0.5 rounded-full bg-slate-950/80 border border-purple-500/20 text-slate-400 group-hover:border-purple-500/40">
                                    {item.badge}
                                </span>
                            </NavLink>
                        );
                    })}
                </div>

                {/* Footer Info Box */}
                <div className="p-4 border-t border-slate-800/80">
                    <div className="p-3 bg-gradient-to-br from-purple-950/30 via-slate-950 to-indigo-950/30 border border-purple-500/20 rounded-2xl backdrop-blur-md">
                        <div className="flex items-center gap-2 text-xs font-extrabold text-purple-300 uppercase tracking-wider">
                            <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" /> Smart Business AI
                        </div>
                        <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">Elevating Software Placement Preparation.</p>
                    </div>
                </div>
            </aside>
        </>
    );
}
