import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, RefreshCw, Copy, Check, Sparkles, MessageSquare, Terminal } from 'lucide-react';
import axios from 'axios';

import { API_BASE } from '../config/api';

const QUICK_PROMPTS = [
    "Amazon SDE Placement Process & Principles",
    "How to structure resume bullet points using XYZ formula?",
    "High-frequency DSA topics for technical rounds",
    "How to answer 'Tell me about a time you failed'?"
];

export default function ChatbotPage() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: "### Welcome to Placement AI Advisor 🎯\n\nI am your **Smart Business AI Career Advisor**. Ask me anything about:\n* **Recruitment Rounds & Cutoffs** (Amazon, Google, Microsoft, Meta, TCS, Infosys, Wipro, Accenture, Goldman Sachs)\n* **Data Structures & Algorithms** (Arrays, Trees, Graphs, Dynamic Programming)\n* **ATS Resumes & Behavioral Strategy** (Google XYZ formula & STAR method)\n\nSelect a prompt below or type your question!"
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [sessionId, setSessionId] = useState(`session_${Date.now()}`);
    const [copiedIndex, setCopiedIndex] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const handleSend = async (textToSend) => {
        const query = textToSend || input;
        if (!query.trim() || loading) return;

        const userMsg = { role: 'user', content: query };
        setMessages((prev) => [...prev, userMsg]);
        if (!textToSend) setInput('');
        setLoading(true);

        try {
            const res = await axios.post(`${API_BASE}/chatbot/chat`, {
                message: query,
                session_id: sessionId
            });

            if (res.data.session_id) {
                setSessionId(res.data.session_id);
            }

            const botReply = res.data.reply || res.data.response || "I have received your placement request. Let me analyze the requirements and provide guidance.";
            setMessages((prev) => [...prev, { role: 'assistant', content: botReply }]);
        } catch (err) {
            console.error("Chatbot API Error:", err);
            const errorMsg = err.response?.data?.detail || "⚠️ Connection Error: Unable to reach the Placement AI Server at http://127.0.0.1:8000/api/chatbot/chat. Please ensure the backend server is running.";
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: errorMsg
                }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleClearHistory = () => {
        setMessages([
            {
                role: 'assistant',
                content: "Chat history cleared. What placement topic shall we tackle next?"
            }
        ]);
        setSessionId(`session_${Date.now()}`);
    };

    const handleCopy = (text, idx) => {
        navigator.clipboard.writeText(text);
        setCopiedIndex(idx);
        setTimeout(() => setCopiedIndex(null), 2000);
    };

    const renderFormattedMessage = (content, msgIdx) => {
        const lines = content.split('\n');
        let inCodeBlock = false;
        let codeLines = [];
        let formattedElements = [];

        lines.forEach((line, lineIdx) => {
            if (line.trim().startsWith('```')) {
                if (inCodeBlock) {
                    const codeText = codeLines.join('\n');
                    formattedElements.push(
                        <div key={`code_${lineIdx}`} className="my-3 rounded-2xl bg-[#090a12] border border-purple-500/30 overflow-hidden shadow-xl">
                            <div className="flex items-center justify-between px-4 py-2 bg-purple-950/40 border-b border-purple-500/20 text-[11px] font-mono text-purple-300">
                                <span className="flex items-center gap-1.5 font-bold">
                                    <Terminal className="w-3.5 h-3.5 text-purple-400" /> Code Solution
                                </span>
                                <button
                                    onClick={() => handleCopy(codeText, `${msgIdx}_${lineIdx}`)}
                                    className="flex items-center gap-1 text-slate-400 hover:text-white transition"
                                >
                                    {copiedIndex === `${msgIdx}_${lineIdx}` ? (
                                        <>
                                            <Check className="w-3 h-3 text-emerald-400" /> <span className="text-emerald-400">Copied</span>
                                        </>
                                    ) : (
                                        <>
                                            <Copy className="w-3 h-3" /> <span>Copy</span>
                                        </>
                                    )}
                                </button>
                            </div>
                            <pre className="p-4 text-xs font-mono text-slate-100 overflow-x-auto leading-relaxed">
                                <code>{codeText}</code>
                            </pre>
                        </div>
                    );
                    codeLines = [];
                    inCodeBlock = false;
                } else {
                    inCodeBlock = true;
                }
                return;
            }

            if (inCodeBlock) {
                codeLines.push(line);
                return;
            }

            if (line.startsWith('### ')) {
                formattedElements.push(
                    <h3 key={lineIdx} className="text-sm font-black font-jakarta text-purple-300 uppercase tracking-wide my-3 border-b border-purple-500/20 pb-1 flex items-center gap-2">
                        {line.replace('### ', '')}
                    </h3>
                );
            } else if (line.startsWith('## ')) {
                formattedElements.push(
                    <h2 key={lineIdx} className="text-base font-black font-jakarta text-white uppercase tracking-wide my-3">
                        {line.replace('## ', '')}
                    </h2>
                );
            } else if (line.startsWith('* ') || line.startsWith('- ')) {
                const text = line.substring(2);
                formattedElements.push(
                    <li key={lineIdx} className="ml-4 list-disc text-xs text-slate-200 my-1 font-sans leading-relaxed">
                        {renderInlineFormatting(text)}
                    </li>
                );
            } else if (line.trim() !== '') {
                formattedElements.push(
                    <p key={lineIdx} className="text-xs text-slate-200 my-1.5 font-sans leading-relaxed">
                        {renderInlineFormatting(line)}
                    </p>
                );
            }
        });

        return formattedElements;
    };

    const renderInlineFormatting = (text) => {
        const parts = text.split(/(\*\*.*?\*\*|`.*?`)/g);
        return parts.map((part, index) => {
            if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={index} className="font-extrabold text-white">{part.slice(2, -2)}</strong>;
            }
            if (part.startsWith('`') && part.endsWith('`')) {
                return <code key={index} className="px-1.5 py-0.5 rounded-md bg-purple-950/60 border border-purple-500/30 text-purple-200 font-mono text-[11px]">{part.slice(1, -1)}</code>;
            }
            return part;
        });
    };

    return (
        <div className="flex flex-col h-[calc(100vh-10rem)] max-h-[850px] bg-[#090a10] border border-purple-500/20 rounded-3xl shadow-2xl overflow-hidden smart-purple-glow">
            {/* Header Control Bar */}
            <div className="p-4 bg-[#0d0e17]/90 border-b border-purple-500/20 backdrop-blur-xl flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-purple-500/30">
                        <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div>
                        <h2 className="text-xs font-black font-jakarta text-white uppercase tracking-wider flex items-center gap-2">
                            Placement AI Advisor
                            <span className="px-2 py-0.5 bg-purple-500/10 text-purple-300 border border-purple-500/30 rounded-full text-[9px] font-mono">MODULE 01</span>
                        </h2>
                        <p className="text-[10px] text-slate-400 font-mono">Session ID: {sessionId.substring(0, 16)}...</p>
                    </div>
                </div>

                <button
                    onClick={handleClearHistory}
                    className="px-3 py-1.5 bg-slate-900/90 hover:bg-slate-800 border border-purple-500/30 text-slate-300 rounded-xl text-xs font-bold transition flex items-center gap-1.5"
                >
                    <RefreshCw className="w-3.5 h-3.5 text-purple-400" /> Clear History
                </button>
            </div>

            {/* Floating Quick Prompts Bar */}
            <div className="px-4 py-2.5 bg-[#07080d]/80 border-b border-slate-800/80 flex items-center gap-2 overflow-x-auto scrollbar-none">
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-purple-400/80 flex-shrink-0 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-purple-400" /> Prompts:
                </span>
                {QUICK_PROMPTS.map((prompt, idx) => (
                    <button
                        key={idx}
                        onClick={() => handleSend(prompt)}
                        className="px-3 py-1 bg-slate-900/90 hover:bg-purple-950/40 border border-slate-800 hover:border-purple-500/40 rounded-full text-[11px] text-slate-300 hover:text-purple-200 flex-shrink-0 transition font-medium"
                    >
                        {prompt}
                    </button>
                ))}
            </div>

            {/* Messages Viewport */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex items-start gap-3 max-w-4xl ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
                    >
                        <div
                            className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold shadow-md ${msg.role === 'user'
                                ? 'bg-gradient-to-tr from-purple-600 to-indigo-600'
                                : 'bg-gradient-to-tr from-violet-600 to-purple-600 shadow-purple-500/30'
                                }`}
                        >
                            {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                        </div>

                        <div
                            className={`p-4 md:p-5 rounded-3xl border shadow-xl relative group max-w-[85%] ${msg.role === 'user'
                                ? 'bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 border-purple-400/30 text-white font-medium'
                                : 'bg-[#0c0d16] border-purple-500/20 text-slate-100'
                                }`}
                        >
                            {msg.role === 'user' ? (
                                <p className="text-xs font-sans leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                            ) : (
                                <div>
                                    {renderFormattedMessage(msg.content, idx)}
                                    <button
                                        onClick={() => handleCopy(msg.content, idx)}
                                        className="absolute right-3 bottom-3 p-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-purple-300 transition"
                                        title="Copy response"
                                    >
                                        {copiedIndex === idx ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-xl bg-purple-600/40 animate-pulse flex items-center justify-center text-white">
                            <Bot className="w-4 h-4" />
                        </div>
                        <div className="p-4 rounded-3xl bg-[#0c0d16] border border-purple-500/20 flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" />
                            <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce delay-150" />
                            <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce delay-300" />
                            <span className="text-xs text-purple-300 font-mono ml-2">Smart AI Analyzing Query...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Bottom Input Area */}
            <div className="p-4 bg-[#0d0e17]/90 border-t border-purple-500/20 backdrop-blur-xl">
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        handleSend();
                    }}
                    className="flex items-center gap-3"
                >
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask placement questions (e.g. Amazon recruitment rounds, DSA topics, ATS resume tips)..."
                        className="flex-1 bg-slate-950 border border-slate-800 focus:border-purple-400/80 rounded-2xl px-4 py-3 text-xs text-white placeholder-slate-500 focus:outline-none transition shadow-inner"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="px-5 py-3 bg-gradient-to-r from-purple-600 via-violet-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-black text-xs uppercase tracking-wider rounded-2xl transition shadow-lg shadow-purple-500/25 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed border border-purple-400/30"
                    >
                        <Send className="w-4 h-4" /> Send
                    </button>
                </form>
            </div>
        </div>
    );
}
