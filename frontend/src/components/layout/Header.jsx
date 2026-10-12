import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Sun, Moon, Sparkles, User, ChevronDown, Check, Monitor, Bot, FileText, MapPin, Mic, Code2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const MODULES = [
    {
        id: 'chatbot',
        label: 'Placement Advisor',
        path: '/chatbot',
        icon: Bot,
        badge: 'AI Chat'
    },
    {
        id: 'resume',
        label: 'ATS Resume Studio',
        path: '/resume',
        icon: FileText,
        badge: 'ATS v2'
    },
    {
        id: 'roadmap',
        label: 'Career Roadmap',
        path: '/roadmap',
        icon: MapPin,
        badge: '1-12 Mo'
    },
    {
        id: 'interview',
        label: 'Mock Interview AI',
        path: '/interview',
        icon: Mic,
        badge: 'Voice'
    },
    {
        id: 'dsa',
        label: 'Technical DSA Studio',
        path: '/dsa',
        icon: Code2,
        badge: 'IDE'
    }
];

export default function Header({ isDark, toggleTheme }) {
    const { user, login } = useAuth();
    const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
    const [nameInput, setNameInput] = useState(user.name);
    const [emailInput, setEmailInput] = useState(user.email);
    const [roleInput, setRoleInput] = useState(user.targetRole);

    const handleSaveProfile = (e) => {
        e.preventDefault();
        login(nameInput, emailInput, roleInput);
        setIsProfileModalOpen(false);
    };

    return (
        <header className="bg-[#090a10]/90 border-b border-purple-500/20 backdrop-blur-2xl px-4 md:px-8 py-3 sticky top-0 z-30 shadow-2xl space-y-3">
            {/* Top Bar: Brand, Navigation, User Profile */}
            <div className="flex items-center justify-between gap-4">
                {/* Brand Logo */}
                <div className="flex items-center gap-3 shrink-0">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 via-violet-600 to-indigo-600 flex items-center justify-center text-white font-black text-lg shadow-lg shadow-purple-500/30">
                        P
                    </div>
                    <div>
                        <h1 className="text-base font-black font-jakarta text-white tracking-wider uppercase flex items-center gap-2">
                            PLACEMENT <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent font-extrabold">AI</span>
                            <span className="text-[9px] px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 uppercase font-mono tracking-widest flex items-center gap-1">
                                <Sparkles className="w-2.5 h-2.5 text-purple-400" /> Smart AI 2.0
                            </span>
                        </h1>
                    </div>
                </div>

                {/* Right Session & Settings Controls */}
                <div className="flex items-center gap-3 shrink-0">
                    {/* Target Role Chip */}
                    <div className="hidden lg:flex items-center gap-2 px-3 py-1 bg-purple-950/30 border border-purple-500/30 rounded-full text-[11px] backdrop-blur-md">
                        <Monitor className="w-3.5 h-3.5 text-purple-400" />
                        <span className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Role:</span>
                        <span className="font-extrabold text-purple-200">{user.targetRole}</span>
                    </div>

                    {/* Candidate Profile Button */}
                    <div className="relative">
                        <button
                            onClick={() => setIsProfileModalOpen(!isProfileModalOpen)}
                            className="flex items-center gap-2 px-3.5 py-1.5 bg-slate-900/90 hover:bg-slate-800 border border-purple-500/30 rounded-xl text-xs text-white transition font-bold shadow-sm hover:border-purple-400/50"
                        >
                            <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600 text-white flex items-center justify-center font-black text-[11px] shadow-sm">
                                {user.name.charAt(0)}
                            </div>
                            <span className="hidden sm:inline font-semibold">{user.name}</span>
                            <ChevronDown className="w-3.5 h-3.5 text-purple-400" />
                        </button>

                        {/* Profile Modal Dropdown */}
                        {isProfileModalOpen && (
                            <div className="absolute right-0 top-12 w-72 bg-[#0d0e17] border border-purple-500/30 rounded-2xl shadow-2xl z-50 p-4 space-y-3 smart-purple-glow">
                                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                                    <div className="flex items-center gap-2">
                                        <User className="w-4 h-4 text-purple-400" />
                                        <span className="text-xs font-black uppercase text-white tracking-wider">Candidate Session</span>
                                    </div>
                                    <button
                                        onClick={() => setIsProfileModalOpen(false)}
                                        className="text-slate-400 hover:text-white"
                                    >
                                        ×
                                    </button>
                                </div>

                                <form onSubmit={handleSaveProfile} className="space-y-3">
                                    <div>
                                        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Full Name</label>
                                        <input
                                            type="text"
                                            value={nameInput}
                                            onChange={(e) => setNameInput(e.target.value)}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-400"
                                        />
                                    </div>

                                    <div>
                                        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Email Address</label>
                                        <input
                                            type="email"
                                            value={emailInput}
                                            onChange={(e) => setEmailInput(e.target.value)}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-400"
                                        />
                                    </div>

                                    <div>
                                        <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Target Placement Role</label>
                                        <input
                                            type="text"
                                            value={roleInput}
                                            onChange={(e) => setRoleInput(e.target.value)}
                                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-400"
                                        />
                                    </div>

                                    <div className="pt-2 flex items-center gap-2">
                                        <button
                                            type="submit"
                                            className="flex-1 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-black uppercase rounded-xl text-xs transition flex items-center justify-center gap-1 shadow-md shadow-purple-500/20"
                                        >
                                            <Check className="w-3.5 h-3.5" /> Save Session
                                        </button>
                                    </div>
                                </form>
                            </div>
                        )}
                    </div>

                    {/* Dark/Light Mode Toggle Button */}
                    <button
                        onClick={toggleTheme}
                        className="p-2 rounded-xl bg-slate-900/90 border border-purple-500/20 text-slate-400 hover:text-purple-400 transition"
                        title="Toggle Dark / Light Mode"
                    >
                        {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-300" />}
                    </button>
                </div>
            </div>

            {/* Horizontal Top Navigation Bar */}
            <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pt-1 border-t border-purple-500/10">
                <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 mr-2 shrink-0 hidden md:inline">
                    MODULES:
                </span>
                {MODULES.map((item) => {
                    const Icon = item.icon;
                    return (
                        <NavLink
                            key={item.id}
                            to={item.path}
                            className={({ isActive }) =>
                                `px-4 py-2 rounded-2xl text-xs font-bold transition flex items-center gap-2.5 shrink-0 border ${isActive
                                    ? 'bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 text-white border-purple-400/50 shadow-lg shadow-purple-500/30'
                                    : 'bg-[#0d0e17]/80 text-slate-400 border-slate-800/80 hover:text-white hover:border-purple-500/30'
                                }`
                            }
                        >
                            {({ isActive }) => (
                                <>
                                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-purple-400'}`} />
                                    <span>{item.label}</span>
                                    <span className={`text-[9px] px-2 py-0.5 rounded-full font-mono font-extrabold uppercase ${isActive
                                        ? 'bg-white/20 text-white'
                                        : 'bg-purple-950/40 text-purple-300 border border-purple-500/20'
                                        }`}>
                                        {item.badge}
                                    </span>
                                </>
                            )}
                        </NavLink>
                    );
                })}
            </div>
        </header>
    );
}
