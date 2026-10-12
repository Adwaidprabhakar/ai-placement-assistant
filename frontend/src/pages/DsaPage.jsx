import React, { useState, useEffect } from 'react';
import { Play, Lightbulb, Terminal, CheckCircle2, XCircle, AlertCircle, Clock } from 'lucide-react';
import Editor from '@monaco-editor/react';
import axios from 'axios';

import { API_BASE } from '../config/api';

export default function DsaPage() {
    const [problems, setProblems] = useState([]);
    const [selectedProblem, setSelectedProblem] = useState(null);
    const [difficulty, setDifficulty] = useState('All');
    const [code, setCode] = useState('');
    const [running, setRunning] = useState(false);
    const [executionResult, setExecutionResult] = useState(null);
    const [gettingHint, setGettingHint] = useState(false);
    const [hint, setHint] = useState(null);

    useEffect(() => {
        fetchProblems();
    }, [difficulty]);

    const fetchProblems = async () => {
        try {
            const url = difficulty === 'All' ? `${API_BASE}/dsa/problems` : `${API_BASE}/dsa/problems?difficulty=${difficulty}`;
            const res = await axios.get(url);
            setProblems(res.data);
            if (res.data.length > 0 && (!selectedProblem || difficulty !== 'All')) {
                const prob = res.data[0];
                setSelectedProblem(prob);
                setCode(prob.starter_code);
            }
        } catch (err) {
            console.error(err);
            const fallback = [
                {
                    id: "two-sum",
                    title: "1. Two Sum",
                    difficulty: "Easy",
                    description: "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
                    starter_code: "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        seen = {}\n        for i, num in enumerate(nums):\n            complement = target - num\n            if complement in seen:\n                return [seen[complement], i]\n            seen[num] = i\n        return []\n",
                    sample_cases: [{ input: "nums = [2, 7, 11, 15], target = 9", expected: "[0, 1]" }]
                },
                {
                    id: "valid-anagram",
                    title: "2. Valid Anagram",
                    difficulty: "Easy",
                    description: "Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.",
                    starter_code: "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        return sorted(s) == sorted(t)\n",
                    sample_cases: [{ input: "s = 'anagram', t = 'nagaram'", expected: "True" }]
                }
            ];
            setProblems(fallback);
            setSelectedProblem(fallback[0]);
            setCode(fallback[0].starter_code);
        }
    };

    const handleRunCode = async () => {
        if (!code.trim() || running) return;
        setRunning(true);
        setExecutionResult(null);

        try {
            const res = await axios.post(`${API_BASE}/dsa/run`, {
                problem_id: selectedProblem?.id || "two-sum",
                code: code
            });
            setExecutionResult(res.data);
        } catch (err) {
            console.error(err);
            setExecutionResult({
                success: false,
                passed_cases: 0,
                total_cases: 0,
                results: [],
                stdout: "",
                error: "Execution Error: Could not connect to Python backend execution engine."
            });
        } finally {
            setRunning(false);
        }
    };

    const handleGetHint = async () => {
        if (gettingHint) return;
        setGettingHint(true);

        try {
            const res = await axios.post(`${API_BASE}/dsa/hint`, {
                problem_id: selectedProblem?.id || "two-sum",
                user_code: code
            });
            setHint(res.data.hint);
        } catch (err) {
            console.error(err);
            setHint("💡 **Hint**: Try using a Hash Map to store elements you have seen along with their indices.");
        } finally {
            setGettingHint(false);
        }
    };

    return (
        <div className="flex flex-col lg:flex-row h-[calc(100vh-8rem)] gap-6">
            {/* Left Problem List & Description Pane */}
            <div className="lg:w-2/5 flex flex-col bg-[#090a10] border border-purple-500/20 rounded-3xl overflow-hidden shadow-2xl smart-purple-glow">
                {/* Header & Filter */}
                <div className="p-4 bg-[#0d0e17] border-b border-purple-500/20 space-y-3">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xs font-black font-jakarta text-white uppercase tracking-wider flex items-center gap-2">
                            Technical DSA Studio
                            <span className="px-2 py-0.5 bg-purple-500/10 text-purple-300 border border-purple-500/30 rounded-full text-[10px] tracking-widest font-mono">MODULE 05</span>
                        </h2>
                    </div>

                    {/* Difficulty Filters */}
                    <div className="flex items-center gap-2">
                        {['All', 'Easy', 'Medium', 'Hard'].map((diff) => (
                            <button
                                key={diff}
                                onClick={() => setDifficulty(diff)}
                                className={`px-3 py-1 rounded-xl text-[11px] font-extrabold uppercase transition ${difficulty === diff
                                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                                    : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                                    }`}
                            >
                                {diff}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Problem Selector Pills */}
                <div className="p-3 bg-[#07080d] border-b border-slate-800 flex items-center gap-2 overflow-x-auto scrollbar-none">
                    {problems.map((prob) => (
                        <button
                            key={prob.id}
                            onClick={() => {
                                setSelectedProblem(prob);
                                setCode(prob.starter_code);
                                setExecutionResult(null);
                                setHint(null);
                            }}
                            className={`px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition flex items-center gap-2 border ${selectedProblem?.id === prob.id
                                ? 'bg-purple-950/40 text-purple-300 border-purple-500/40'
                                : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
                                }`}
                        >
                            <span className={`w-2 h-2 rounded-full ${prob.difficulty === 'Easy' ? 'bg-emerald-400' : prob.difficulty === 'Medium' ? 'bg-amber-400' : 'bg-red-400'
                                }`} />
                            {prob.title}
                        </button>
                    ))}
                </div>

                {/* Problem Description Details */}
                {selectedProblem && (
                    <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#090a10]">
                        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                            <h3 className="text-sm font-black font-jakarta text-white uppercase tracking-wide">{selectedProblem.title}</h3>
                            <span className={`px-2.5 py-0.5 text-[10px] font-black uppercase rounded-full border ${selectedProblem.difficulty === 'Easy'
                                ? 'bg-emerald-950/40 text-emerald-300 border-emerald-500/30'
                                : selectedProblem.difficulty === 'Medium'
                                    ? 'bg-amber-950/40 text-amber-300 border-amber-500/30'
                                    : 'bg-red-950/40 text-red-300 border-red-500/30'
                                }`}>
                                {selectedProblem.difficulty}
                            </span>
                        </div>

                        <div className="text-xs text-slate-300 leading-relaxed font-sans space-y-2">
                            {selectedProblem.description.split('\n\n').map((para, idx) => (
                                <p key={idx}>{para}</p>
                            ))}
                        </div>

                        {/* Sample Cases */}
                        {selectedProblem.test_cases && (
                            <div className="space-y-2 pt-2">
                                <span className="text-[10px] font-black uppercase tracking-widest text-purple-400 block">Sample Test Cases</span>
                                {selectedProblem.test_cases.map((tc, idx) => (
                                    <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs space-y-1 font-mono">
                                        <div className="text-slate-400"><strong className="text-slate-200">Input:</strong> {JSON.stringify(tc.args)}</div>
                                        <div className="text-purple-300"><strong className="text-slate-200">Expected:</strong> {JSON.stringify(tc.expected)}</div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* AI Hint Drawer */}
                        {hint && (
                            <div className="p-4 bg-purple-950/30 border border-purple-500/40 rounded-2xl space-y-2 smart-purple-glow">
                                <span className="text-xs font-black uppercase tracking-widest text-purple-300 flex items-center gap-1.5">
                                    <Lightbulb className="w-4 h-4 text-purple-400" /> AI Guidance Hint
                                </span>
                                <p className="text-xs text-purple-200 leading-relaxed">{hint}</p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Right Monaco Code Editor & Execution Console Pane */}
            <div className="lg:w-3/5 flex flex-col bg-[#090a10] border border-purple-500/20 rounded-3xl overflow-hidden shadow-2xl smart-purple-glow">
                {/* Editor Header Bar */}
                <div className="p-3 bg-[#0d0e17] border-b border-purple-500/20 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 bg-slate-900 border border-slate-800 rounded-lg text-xs font-bold text-purple-400 uppercase tracking-wider font-mono">
                            Python 3.10
                        </span>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleGetHint}
                            disabled={gettingHint}
                            className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-purple-300 border border-purple-500/30 rounded-xl text-xs font-bold uppercase flex items-center gap-1.5 transition"
                        >
                            <Lightbulb className="w-3.5 h-3.5" />
                            {gettingHint ? 'Hint...' : 'AI Hint'}
                        </button>

                        <button
                            onClick={handleRunCode}
                            disabled={running}
                            className="px-5 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 text-white font-black uppercase text-xs rounded-xl flex items-center gap-1.5 transition shadow-lg shadow-purple-500/20 border border-purple-400/30"
                        >
                            <Play className="w-3.5 h-3.5 text-white" />
                            {running ? 'Executing...' : 'Run Code'}
                        </button>
                    </div>
                </div>

                {/* Monaco Code Editor Pane */}
                <div className="flex-1 min-h-[300px]">
                    <Editor
                        height="100%"
                        defaultLanguage="python"
                        theme="vs-dark"
                        value={code}
                        onChange={(value) => setCode(value || '')}
                        options={{
                            fontSize: 13,
                            minimap: { enabled: false },
                            scrollBeyondLastLine: false,
                            automaticLayout: true,
                            tabSize: 4
                        }}
                    />
                </div>

                {/* Execution Output Console */}
                <div className="h-64 bg-[#06070b] border-t border-purple-500/20 p-4 flex flex-col justify-between overflow-y-auto space-y-3">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-800 shrink-0">
                        <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-1.5">
                            <Terminal className="w-3.5 h-3.5 text-purple-400" /> Execution Console Output
                        </span>

                        {executionResult && (
                            <span className={`text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full flex items-center gap-1 ${executionResult.success
                                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                                : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                                }`}>
                                {executionResult.success ? (
                                    <>
                                        <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                                        ACCEPTED ({executionResult.passed_cases}/{executionResult.total_cases})
                                    </>
                                ) : (
                                    <>
                                        <XCircle className="w-3 h-3 text-rose-400" />
                                        {executionResult.error ? 'RUNTIME ERROR' : `WRONG ANSWER (${executionResult.passed_cases}/${executionResult.total_cases})`}
                                    </>
                                )}
                            </span>
                        )}
                    </div>

                    {/* Execution Details Output */}
                    <div className="flex-1 font-mono text-xs text-slate-300 space-y-2">
                        {executionResult ? (
                            <div className="space-y-3">
                                {/* Execution Error Traceback */}
                                {executionResult.error && (
                                    <div className="p-3 bg-rose-950/40 border border-rose-500/30 rounded-xl space-y-1">
                                        <span className="text-[10px] font-extrabold uppercase text-rose-400 flex items-center gap-1">
                                            <AlertCircle className="w-3.5 h-3.5" /> Exception Traceback:
                                        </span>
                                        <pre className="text-rose-200 whitespace-pre-wrap text-[11px] font-mono leading-relaxed">
                                            {executionResult.error}
                                        </pre>
                                    </div>
                                )}

                                {/* Individual Test Case Results */}
                                {executionResult.results && executionResult.results.length > 0 && (
                                    <div className="space-y-2">
                                        <div className="flex items-center justify-between text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                                            <span>Test Case Results</span>
                                            <span className="flex items-center gap-1">
                                                <Clock className="w-3 h-3 text-purple-400" />
                                                {executionResult.total_execution_time_ms} ms
                                            </span>
                                        </div>

                                        <div className="grid grid-cols-1 gap-2">
                                            {executionResult.results.map((tc) => (
                                                <div
                                                    key={tc.test_case}
                                                    className={`p-2.5 rounded-xl border text-xs flex flex-col space-y-1 ${tc.passed
                                                        ? 'bg-emerald-950/20 border-emerald-500/20'
                                                        : 'bg-rose-950/20 border-rose-500/20'
                                                        }`}
                                                >
                                                    <div className="flex items-center justify-between">
                                                        <span className="font-bold text-slate-200">Test Case #{tc.test_case}</span>
                                                        <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded-md ${tc.passed
                                                            ? 'bg-emerald-500/20 text-emerald-400'
                                                            : 'bg-rose-500/20 text-rose-400'
                                                            }`}>
                                                            {tc.passed ? 'PASSED' : 'FAILED'} ({tc.execution_time_ms}ms)
                                                        </span>
                                                    </div>

                                                    <div className="text-[11px] text-slate-400 grid grid-cols-3 gap-2 pt-1 border-t border-slate-800/60">
                                                        <div><strong className="text-slate-300">Input:</strong> {JSON.stringify(tc.input)}</div>
                                                        <div><strong className="text-slate-300">Expected:</strong> {JSON.stringify(tc.expected)}</div>
                                                        <div><strong className="text-slate-300">Actual:</strong> <span className={tc.passed ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}>{JSON.stringify(tc.actual)}</span></div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Stdout output */}
                                {executionResult.stdout && (
                                    <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                                        <span className="text-[10px] font-extrabold uppercase text-purple-400 block">stdout:</span>
                                        <pre className="text-slate-300 whitespace-pre-wrap">{executionResult.stdout}</pre>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="text-slate-500 italic py-4 text-center text-xs">
                                Click "Run Code" above to execute Python solution against test cases...
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
