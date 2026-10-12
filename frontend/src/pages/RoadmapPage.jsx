import React, { useState } from 'react';
import { Compass, CheckCircle2, Sparkles } from 'lucide-react';
import axios from 'axios';

import { API_BASE } from '../config/api';

export default function RoadmapPage() {
    const [targetRole, setTargetRole] = useState('Software Development Engineer (SDE-1)');
    const [timeframe, setTimeframe] = useState('6 Months');
    const [skillLevel, setSkillLevel] = useState('Intermediate (CSE Undergrad)');
    const [roadmap, setRoadmap] = useState(null);
    const [loading, setLoading] = useState(false);
    const [completedSteps, setCompletedSteps] = useState({});

    const handleGenerate = async (e) => {
        if (e) e.preventDefault();
        setLoading(true);

        try {
            const res = await axios.post(`${API_BASE}/roadmap/generate`, {
                target_role: targetRole,
                timeframe_months: parseInt(timeframe) || 6,
                current_skill_level: skillLevel
            });

            setRoadmap(res.data);
        } catch (err) {
            console.error(err);
            const totalMonths = parseInt(timeframe) || 6;
            const generatedPhases = [];
            const topics = [
                { title: "DSA Foundations & Language Mastery", focus: "Master C++/Java/Python fundamentals, Time/Space complexity analysis, Arrays, Strings, and Two Pointers.", action_items: ["Solve 40 Easy problems on LeetCode", "Implement custom Stack & Queue structures", "Learn Big-O notation analysis"], resources: ["NeetCode 150", "Striver A2Z DSA Sheet"] },
                { title: "Advanced Data Structures & Problem Solving", focus: "Linked Lists, Binary Trees, Binary Search Trees, Recursion & Backtracking.", action_items: ["Solve 30 Medium Tree problems", "Practice BFS/DFS traversals", "Build 1 Full-Stack project"], resources: ["LeetCode Tree Card", "FreeCodeCamp Backend"] },
                { title: "Graphs, Dynamic Programming & System Design", focus: "Graphs (Dijkstra, BFS/DFS), DP patterns (Knapsack, LCS), and High Level System Design basics.", action_items: ["Solve 25 DP & Graph problems", "Learn Load Balancers, Caching, Databases", "Optimize ATS Resume"], resources: ["Grokking System Design", "Striver DP Series"] },
                { title: "Core CS Subjects & Mock Interviews", focus: "Operating Systems, DBMS, SQL, Computer Networks, Object-Oriented Programming (OOP).", action_items: ["Revise OS & DBMS fundamentals", "Complete 5 Voice Mock Interviews", "Apply for campus & off-campus drives"], resources: ["Gate Smashers Core CS", "SQLZoo Interactive"] }
            ];

            for (let i = 1; i <= totalMonths; i++) {
                const tpl = topics[(i - 1) % topics.length];
                generatedPhases.push({
                    month: i,
                    title: `Month ${i}: ${tpl.title}`,
                    focus: tpl.focus,
                    action_items: tpl.action_items,
                    recommended_resources: tpl.resources
                });
            }

            setRoadmap({
                title: `${timeframe} Placement Roadmap for ${targetRole}`,
                summary: `Structured month-by-month preparation plan focusing on Data Structures & Algorithms, System Design, Core CS subjects, and Portfolio projects.`,
                phases: generatedPhases
            });
        } finally {
            setLoading(false);
        }
    };

    const toggleStep = (phaseIdx, itemIdx) => {
        const key = `${phaseIdx}_${itemIdx}`;
        setCompletedSteps(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const calculateProgress = () => {
        if (!roadmap || !roadmap.phases) return 0;
        let total = 0;
        let completed = 0;
        roadmap.phases.forEach((phase, pIdx) => {
            phase.action_items.forEach((_, iIdx) => {
                total++;
                if (completedSteps[`${pIdx}_${iIdx}`]) completed++;
            });
        });
        return total === 0 ? 0 : Math.round((completed / total) * 100);
    };

    return (
        <div className="space-y-6">
            {/* Top Config Bento Card */}
            <div className="p-6 bg-[#090a10] border border-purple-500/20 rounded-3xl shadow-2xl smart-purple-glow space-y-4">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-purple-500/30">
                        <Compass className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h2 className="text-base font-black font-jakarta text-white uppercase tracking-wider flex items-center gap-2">
                            Placement AI Career Roadmap Generator
                            <span className="px-2 py-0.5 bg-purple-500/10 text-purple-300 border border-purple-500/30 rounded-full text-[10px] tracking-widest font-mono">MODULE 03</span>
                        </h2>
                        <p className="text-xs text-slate-400">Generate a custom month-by-month placement preparation timeline (1 to 12 months).</p>
                    </div>
                </div>

                <form onSubmit={handleGenerate} className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                    <div>
                        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Target Placement Role</label>
                        <input
                            type="text"
                            value={targetRole}
                            onChange={(e) => setTargetRole(e.target.value)}
                            placeholder="e.g. SDE-1, Data Analyst, Full-Stack Dev..."
                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-purple-400"
                        />
                    </div>

                    <div>
                        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Timeframe</label>
                        <select
                            value={timeframe}
                            onChange={(e) => setTimeframe(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-purple-400"
                        >
                            <option value="3 Months">3 Months (Intensive)</option>
                            <option value="6 Months">6 Months (Recommended)</option>
                            <option value="12 Months">12 Months (Comprehensive)</option>
                        </select>
                    </div>

                    <div>
                        <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Skill Level</label>
                        <select
                            value={skillLevel}
                            onChange={(e) => setSkillLevel(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 focus:outline-none focus:border-purple-400"
                        >
                            <option value="Beginner (Basic Coding Knowledge)">Beginner (Basic Coding)</option>
                            <option value="Intermediate (CSE Undergrad)">Intermediate (CSE Undergrad)</option>
                            <option value="Advanced (LeetCode Medium Specialist)">Advanced (LeetCode Specialist)</option>
                        </select>
                    </div>

                    <div className="md:col-span-3 flex justify-end">
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-6 py-3 bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-black uppercase text-xs rounded-xl flex items-center gap-2 transition shadow-lg shadow-purple-500/25 border border-purple-400/30"
                        >
                            <Sparkles className="w-4 h-4 text-purple-300" />
                            {loading ? 'Generating Timeline...' : 'Generate Roadmap'}
                        </button>
                    </div>
                </form>
            </div>

            {/* Generated Timeline Display */}
            {roadmap && (
                <div className="space-y-6">
                    {/* Progress Header */}
                    <div className="p-5 bg-[#090a10] border border-purple-500/20 rounded-3xl shadow-xl flex items-center justify-between">
                        <div>
                            <h3 className="text-sm font-black font-jakarta text-white uppercase tracking-wider">{roadmap.title}</h3>
                            <p className="text-xs text-slate-400 mt-0.5">{roadmap.summary}</p>
                        </div>
                        <div className="text-right">
                            <span className="text-2xl font-black font-jakarta bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">{calculateProgress()}%</span>
                            <span className="text-[10px] text-slate-400 uppercase font-bold tracking-widest block">Completed</span>
                        </div>
                    </div>

                    {/* Timeline Phases */}
                    <div className="relative pl-6 space-y-6 border-l-2 border-purple-500/30 ml-4">
                        {roadmap.phases.map((phase, pIdx) => (
                            <div key={pIdx} className="relative group">
                                {/* Glowing Timeline Node Circle */}
                                <div className="absolute -left-[31px] top-1.5 w-6 h-6 rounded-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-black text-[11px] flex items-center justify-center shadow-lg shadow-purple-500/50">
                                    {phase.month}
                                </div>

                                <div className="p-6 bg-[#0c0d16] border border-slate-800 group-hover:border-purple-500/40 rounded-3xl shadow-xl transition space-y-4">
                                    <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                                        <h4 className="text-sm font-black font-jakarta text-purple-300 uppercase tracking-wide">{phase.title}</h4>
                                        <span className="text-[10px] px-2.5 py-0.5 bg-slate-900 text-slate-400 border border-slate-800 rounded-full font-mono">
                                            Phase {phase.month}
                                        </span>
                                    </div>

                                    <p className="text-xs text-slate-300 leading-relaxed font-sans">{phase.focus}</p>

                                    {/* Action Items */}
                                    <div className="space-y-2 pt-1">
                                        <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 block">Milestones & Action Items</span>
                                        {phase.action_items.map((item, iIdx) => {
                                            const isDone = completedSteps[`${pIdx}_${iIdx}`];
                                            return (
                                                <div
                                                    key={iIdx}
                                                    onClick={() => toggleStep(pIdx, iIdx)}
                                                    className={`p-3 rounded-xl border text-xs cursor-pointer transition flex items-center justify-between ${isDone
                                                        ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300 line-through'
                                                        : 'bg-slate-950 border-slate-800 text-slate-200 hover:border-purple-500/30'
                                                        }`}
                                                >
                                                    <span>{item}</span>
                                                    <CheckCircle2 className={`w-4 h-4 flex-shrink-0 ${isDone ? 'text-emerald-400' : 'text-slate-600'}`} />
                                                </div>
                                            );
                                        })}
                                    </div>

                                    {/* Recommended Resources */}
                                    {phase.recommended_resources && (
                                        <div className="pt-2">
                                            <span className="text-[10px] font-black uppercase tracking-widest text-purple-400/80 block mb-1.5">Recommended Study Resources</span>
                                            <div className="flex flex-wrap gap-2">
                                                {phase.recommended_resources.map((res, rIdx) => (
                                                    <span key={rIdx} className="px-2.5 py-1 bg-slate-900 border border-slate-800 text-slate-300 rounded-lg text-[11px] font-semibold">
                                                        📖 {res}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
