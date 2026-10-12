import os
import httpx
import json
import time
import re
from typing import List, Dict, Optional
from app.config import settings

PLACEMENT_SYSTEM_PROMPT = """You are Placement AI Advisor, an elite campus & off-campus career guidance counselor.
You specialize in helping software engineering students and graduates prepare for technical & behavioral placement drives at top technology companies (Amazon, Google, Microsoft, Meta, Flipkart, TCS, Infosys, Wipro, Accenture, Goldman Sachs, Adobe, startups).

Your expertise covers:
1. Recruitment processes, OA patterns, cutoff criteria, and interview round structures.
2. Data Structures & Algorithms (DSA), High-Level & Low-Level System Design, Core CS (Operating Systems, DBMS & SQL, Computer Networks, OOP).
3. ATS-optimized resume formatting, Google XYZ formula bullet points, and project portfolio presentation.
4. Voice & written interview strategies, behavioral questions using the STAR method, and compensation negotiation tips.

Always provide structured, highly accurate, and actionable advice with clear GitHub-style markdown formatting (headers, bold keyphrases, code blocks, bullet points). Keep your tone professional, motivating, and precise."""

# Extended Knowledge Base
KNOWLEDGE_BASE = {
    "mnc_hiring": """### Active Recruiting MNCs & Placement Drive Landscape 🌐

**1. Tier-1 Product MNCs (High Pay: ₹18 LPA - ₹45+ LPA):**
* **Amazon:** Continuous off-campus SDE-1 drives via Amazon Jobs portal. Focuses on 2 OA coding questions + 16 Leadership Principles.
* **Google:** Google University Hiring (STEP Internship & Full-time SDE). Focuses on Graph Theory, DP, and clean algorithmic code.
* **Microsoft:** Microsoft Engage & University Careers portal. 3 Codility coding questions + System architecture.
* **Meta (Facebook):** SDE-1 hiring via Meta Careers. Fast-paced 45-min screening (2 LeetCode Mediums).
* **Adobe & Goldman Sachs:** HackerRank/Codepair tests featuring Advanced DSA + Probability & Math (Goldman).

**2. Major IT Service MNCs (Mass Hiring: ₹4 LPA - ₹11+ LPA):**
* **TCS (NQT / Digital / Prime):** Annual National Qualifier Test for Ninja (3.36 LPA), Digital (7 LPA), and Prime (11.5 LPA) profiles.
* **Infosys (HackWithInfy & InfyTQ):** HackWithInfy competitive coding challenge offering Specialist Programmer (8 LPA) & Digital Specialist Engineer (6.25 LPA) roles.
* **Wipro (NLTH / Elite / Turbo):** National Talent Hunt for Project Engineer and Turbo roles.
* **Accenture & Cognizant:** Off-campus hiring for Associate Software Engineer (ASE) & Advanced ASE roles.

**3. Active Off-Campus Hiring Portals & Tools:**
* **Unstop (Formerly Dare2Compete):** Campus hackathons & nationwide hiring challenges.
* **GitHub Off-Campus Repos:** Follow community repositories like `off-campus-jobs-india`.
* **LinkedIn Jobs & Hirist:** Filter by "0-1 Years Experience" and set alerts for "Software Engineer Trainee" / "Graduate Engineer".

**4. Strategic Action Plan:**
1. Keep 1-page ATS-ready PDF Resume updated.
2. Maintain active LeetCode (150+ solved) and GitHub project links.
3. Practice STAR behavioral responses for HR/Managerial rounds.""",

    "amazon": """### Amazon Placement & Hiring Guide 📦

**1. Selection & Interview Rounds:**
* **Online Assessment (OA):** 2 Coding Questions (Medium-Hard DSA) + 20-min Work Simulation + Amazon 16 Leadership Principles Behavioral Assessment.
* **Technical Interview 1 (DSA Focus):** Deep dive into Trees, Graphs, Dynamic Programming, and Array manipulation with time/space complexity analysis.
* **Technical Interview 2 (LLD / OOD Focus):** Low-Level Design (e.g., Design Parking Lot, Elevators, Online Bookstore) + Object-Oriented Principles.
* **Bar Raiser Round:** Strict evaluation of Amazon Leadership Principles (Customer Obsession, Ownership, Bias for Action, Invent and Simplify) + 1 Hard Coding/Architecture Question.

**2. High-Frequency Topics:**
* Binary Trees (BFS/DFS, LCA, Diameter), Graphs (Dijkstra, Topological Sort), Sliding Window, HashMaps.

**3. Behavioral Strategy:**
* Structure every answer strictly using the **STAR Method** (Situation, Task, Action, Result). Quantify results with metrics (e.g., "Reduced latency by 35%").""",

    "google": """### Google Placement & Hiring Guide 🔍

**1. Selection & Interview Rounds:**
* **Screening Round:** 1-2 Online Technical Phone Screens focusing on algorithmic problem solving and data structures.
* **Onsite Technical Rounds (4 Rounds):**
  * 3 Algorithmic Coding Rounds: Heavy focus on Graph Theory, Dynamic Programming, Segment Trees, Trie, and Heap.
  * 1 "Googleyness & Leadership" Round: Behavioral evaluation on collaboration, handling ambiguity, and ethics.

**2. Key Preparation Focus:**
* Code cleanly on a blank document/editor without syntax highlighting.
* Focus on optimal time/space complexity analysis before writing a single line of code.""",

    "microsoft": """### Microsoft Placement & Hiring Guide 🪟

**1. Selection Rounds:**
* **OA (Codility / HackerRank):** 3 Algorithmic Coding Questions (60-90 mins).
* **Technical Round 1 & 2:** Data Structures, Bit Manipulation, String Algorithms, LinkedLists, and System Fundamentals.
* **AA (Appropriate Authority) Round:** Senior Director/Engineering Manager interview combining technical depth, project architecture, and cultural fit.

**2. Key Topics:**
* Linked List Manipulation, Tree Traversals, OS Concurrency/Threads, Memory Management.""",

    "meta": """### Meta (Facebook) Placement & Hiring Guide ♾️

**1. Selection Rounds:**
* **Screening Round:** 2 Medium Coding Questions in 45 minutes (speed & accuracy are crucial).
* **Onsite Technical Rounds:**
  * 2 Coding Rounds: Focus on Top 100 Meta Tagged LeetCode questions (Arrays, Graphs, Recursion).
  * 1 System Design Round: Scalable infrastructure (e.g., Design News Feed, WhatsApp Messenger).
  * 1 Behavioral Round: Focus on impact, moving fast, and resolving conflict.""",

    "service_mnc": """### IT Service MNCs Blueprint (TCS, Wipro, Infosys, Accenture, Cognizant) 🏢

**1. Selection Process:**
* **Round 1 (Aptitude & Technical MCQ):** Quantitative Aptitude, Logical Reasoning, Verbal, Pseudo-code analysis, SQL basics.
* **Round 2 (Coding Round):** 2 Fundamental Coding Questions (String Reversal, Matrix operations, Fibonacci, Array filtering).
* **Round 3 (Technical TR):** Core CS questions (OOP concepts, SQL Queries, Project discussion).
* **Round 4 (HR Round):** Willingness to relocate, night shifts, communication skills check, career baseline.

**2. High-Yield Preparation Strategy:**
* Master SQL `SELECT`, `JOIN`, `GROUP BY`, `HAVING`, and `NESTED QUERIES`.
* Be prepared to explain your final-year college project end-to-end with architecture diagrams.""",

    "resume": """### ATS-Optimized Resume Masterclass 📄

**1. Structural Guidelines for 90+ ATS Score:**
* Single-column standard layout (no tables, floating text boxes, or graphic icons).
* Standard fonts: Inter, Arial, Calibri, 10-12pt text size.
* Explicit Section Headings: `EDUCATION`, `TECHNICAL SKILLS`, `WORK EXPERIENCE`, `PROJECTS`, `CERTIFICATIONS`.

**2. The Google XYZ Bullet Formula:**
* *Format:* Accomplished **[X]**, as measured by **[Y]**, by implementing **[Z]**.
* *Weak:* "Worked on a web backend using Node.js."
* *Strong:* "Engineered a microservices backend in Node.js/Redis, handling 50k+ daily requests with 99.9% uptime and 40% lower response latency."

**3. Keyword Optimization:**
* Match exact job description keywords (e.g., "React.js", "Docker", "REST APIs", "PostgreSQL", "CI/CD").""",

    "dsa": """### Data Structures & Algorithms Mastery Roadmap 💻

**1. Core Topics & Order of Learning:**
* **Level 1 (Foundations):** Arrays, Strings, Two Pointers, Sliding Window, Fast & Slow Pointers.
* **Level 2 (Linear Data Structures):** Stacks, Queues, Hash Tables, Linked Lists.
* **Level 3 (Hierarchical & Graphs):** Binary Search Trees, Tries, Heaps/Priority Queues, Graph Traversal (BFS/DFS, Topological Sort, Union-Find).
* **Level 4 (Advanced):** Dynamic Programming (1D, 2D, Knapsack, LCS), Backtracking, Greedy Algorithms.

**2. Daily Coding Routine:**
* Solve 2 Medium + 1 Easy problem daily.
* Spend 20 mins planning the solution on paper before coding.""",

    "system_design": """### System Design Interview Strategy 🏗️

**1. High-Level Design (HLD) Checklist:**
* **Requirements Clarification:** Functional (e.g. post tweet, view timeline) & Non-Functional (e.g. 99.99% availability, 100ms latency, 100M DAU).
* **Back-of-the-envelope Estimations:** QPS (Queries Per Second), Storage requirements, Bandwidth.
* **Core Components:** API Gateway, Load Balancer, Web/Application Servers, Cache Cluster (Redis), Database (Relational vs NoSQL), Message Queue (Kafka/RabbitMQ).

**2. Key Architecture Patterns:**
* Microservices, Database Sharding, Database Indexing, Master-Slave Replication, CDN for Static Content.""",

    "behavioral": """### Behavioral Interview & STAR Method Mastery ⭐

**1. The STAR Response Framework:**
* **S - Situation:** Set the context (Company/Project, constraint, timeline). Keep it brief (15-20% of response).
* **T - Task:** Define your specific responsibility or challenge.
* **A - Action:** Describe the concrete steps YOU took, tools used, and technical trade-offs evaluated (50% of response).
* **R - Result:** Highlight quantifiable outcomes, metrics, lessons learned, and business impact (20-25% of response).

**2. Answering "Tell me about a time you failed":**
* **Situation:** Describe a real project deadline or technical oversight.
* **Action:** Explain how you owned the mistake immediately, communicated with the team, and deployed a fix.
* **Result:** Detail what system safeguards or automated tests you put in place to ensure it never happened again.""",

    "sql": """### DBMS & SQL Interview Master Guide 🗄️

**1. Crucial SQL Topics:**
* **Joins:** INNER, LEFT, RIGHT, FULL OUTER, CROSS JOIN.
* **Window Functions:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()`.
* **Indexing:** B-Tree Indexes, Hash Indexes, Composite Indexes, Clustered vs Non-Clustered.
* **Transactions:** ACID Properties (Atomicity, Consistency, Isolation, Durability) & Isolation Levels.

**2. Sample Interview Query:**
```sql
-- Find 2nd Highest Salary per Department
SELECT department_id, salary
FROM (
    SELECT department_id, salary,
           DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rnk
    FROM employees
) t
WHERE rnk = 2;
```"""
}


class LLMService:
    def __init__(self):
        # Session Memory: session_id -> list of {"role": str, "content": str}
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        # In-Memory Response Cache: prompt_hash -> (timestamp, response_str)
        self.cache: Dict[str, tuple] = {}
        self.cache_ttl = 3600  # 1 hour cache validity

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(session_id, [])

    def append_message(self, session_id: str, role: str, content: str):
        if not session_id:
            return
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        # Prevent exact back-to-back duplicate messages
        if self.sessions[session_id] and self.sessions[session_id][-1]["role"] == role and self.sessions[session_id][-1]["content"] == content:
            return
        self.sessions[session_id].append({"role": role, "content": content})
        if len(self.sessions[session_id]) > 20:
            self.sessions[session_id] = self.sessions[session_id][-20:]

    async def _call_openai(self, messages: List[dict]) -> Optional[str]:
        api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "temperature": 0.7
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLMService] OpenAI API call failed: {e}")
        return None

    async def _call_groq(self, messages: List[dict]) -> Optional[str]:
        api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "temperature": 0.7
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLMService] Groq API call failed: {e}")
        return None

    async def _call_gemini(self, prompt: str, system_prompt: str) -> Optional[str]:
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\nUser Question: {prompt}"}]}]
            }
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLMService] Gemini API call failed: {e}")
        return None

    def _match_smart_intent(self, prompt: str) -> str:
        p = prompt.lower().strip()

        # 1. Resume & Google XYZ Formula specific
        if any(w in p for w in ["xyz", "xyz formula", "bullet point", "bullet", "resume bullet"]):
            return """### Google XYZ Formula & ATS Resume Bullet Blueprint 📄

The **Google XYZ Formula** is the gold standard for writing high-impact resume bullet points:
> *"Accomplished **[X]**, as measured by **[Y]**, by doing **[Z]**."*

---

#### 💡 Concrete Examples by Domain:

**1. Software Engineering (Backend / Full-Stack):**
* ❌ *Weak:* "Created backend REST APIs for a web project using Python and FastAPI."
* ✅ *Google XYZ Format:* "Engineered 12 RESTful microservices in **FastAPI & Redis**, reducing API response latency by **38%** and serving **15,000+ daily requests** with 99.9% uptime."

**2. Machine Learning / Data Science:**
* ❌ *Weak:* "Built a machine learning model to detect computer vision threats."
* ✅ *Google XYZ Format:* "Trained a ResNet-18 computer vision classifier using **PyTorch & CUDA**, boosting detection accuracy by **14.2%** over baseline on a 50,000-frame benchmark dataset."

**3. Frontend Development:**
* ❌ *Weak:* "Redesigned web pages using React and Tailwind CSS."
* ✅ *Google XYZ Format:* "Modernized frontend architecture with **React 19 & Tailwind CSS v4**, accelerating First Contentful Paint (FCP) by **1.2s** and raising user session duration by **22%**."

---

#### 🎯 Key Resume Rules for 90+ ATS Score:
1. **Always lead with strong action verbs** (*Engineered, Architected, Optimized, Spearheaded, Implemented*).
2. **Quantify every result** using percentages, latencies, request volumes, or accuracy metrics.
3. **Use single-column ATS format** without images, icons, or multi-column table layouts."""

        # 2. Behavioral Questions & STAR Method
        if any(w in p for w in ["failed", "failure", "mistake", "conflict", "weakness", "star method", "behavioral"]):
            if "fail" in p:
                return """### How to Answer: "Tell me about a time you failed" 🌟

Use the **STAR Method** (*Situation, Task, Action, Result*) with an emphasis on **Ownership & Learning**:

---

#### 🗣️ Recommended Response Script:

* **Situation (15%):** "During my final semester project, our team built a high-throughput video analytics service scheduled for launch before campus placements."
* **Task (15%):** "My responsibility was implementing the database query pipeline to handle real-time streaming metadata."
* **Action (50% - The Crucial Part):** "Under peak simulated traffic, database connections saturated, causing 504 timeouts. I took immediate ownership: rather than blaming constraints, I benchmarked queries using `EXPLAIN ANALYZE`, identified unindexed foreign keys, introduced Redis caching for read queries, and added database connection pooling."
* **Result (20%):** "We resolved the latency spikes, lowering query times from **450ms to 42ms**. More importantly, I created automated performance benchmark scripts in CI/CD so regression issues are caught before production."

---

#### ⚠️ Pro-Tips for HR & Managerial Rounds:
1. **Never say "I haven't failed"** – interviewers evaluate self-awareness and accountability.
2. **Focus 50% of your time on Action & Retrospective Learning**.
3. **End on a triumphant system improvement or positive outcome**."""

        # 3. Amazon Placement Process & Leadership Principles
        if "amazon" in p:
            return KNOWLEDGE_BASE["amazon"]

        # 4. Google Placement Guide
        if "google" in p:
            return KNOWLEDGE_BASE["google"]

        # 5. Microsoft / Meta Placement Guide
        if "microsoft" in p:
            return KNOWLEDGE_BASE["microsoft"]
        if "meta" in p or "facebook" in p:
            return KNOWLEDGE_BASE["meta"]

        # 6. MNC Hiring & Service Companies
        if any(w in p for w in ["mnc", "hiring", "off campus", "recruiting", "drives"]):
            return KNOWLEDGE_BASE["mnc_hiring"]
        if any(w in p for w in ["tcs", "infosys", "wipro", "accenture", "cognizant"]):
            return KNOWLEDGE_BASE["service_mnc"]

        # 7. High-frequency DSA Topics & Algorithms
        if any(w in p for w in ["dsa", "leetcode", "algorithm", "data structure", "topic", "array", "tree", "dp", "graph"]):
            return KNOWLEDGE_BASE["dsa"]

        # 8. System Design
        if any(w in p for w in ["system design", "hld", "lld", "architecture", "microservice", "scalability"]):
            return KNOWLEDGE_BASE["system_design"]

        # 9. SQL & Databases
        if any(w in p for w in ["sql", "dbms", "database", "query", "join"]):
            return KNOWLEDGE_BASE["sql"]

        # 10. Dynamic Fallback Synthesis tailored specifically to user prompt
        clean_q = prompt.strip()
        return f"""### Placement AI Masterclass: {clean_q} 🎯

Here is an actionable strategy and technical roadmap addressing **"{clean_q}"**:

---

#### 1. Core Technical Concepts & Action Items:
* **Algorithmic Preparation:** Practice high-frequency patterns (Two Pointers, Sliding Window, Graph BFS/DFS, Dynamic Programming).
* **System & Architecture:** Understand modular microservices, REST API design principles, database indexing, and caching trade-offs.
* **Resume & Portfolio:** Highlight 2+ production-deployed projects with GitHub repositories, clear documentation, and quantified metrics.

---

#### 2. Key Placement Round Milestones:
1. **Online Coding Assessment (OA):** Target 100% test case pass rate within timed limits. Focus on edge case handling ($N=0, N=1$, overflow).
2. **Technical Interview:** Communicate your thought process out loud before typing code. Start with a brute-force $O(N^2)$ solution, then optimize to $O(N)$ or $O(N \log N)$.
3. **HR & Culture Fit:** Prepare STAR method responses focusing on leadership, conflict resolution, and technical problem solving.

---

💡 *Pro-Tip: Select any prompt chips above or try out the **Voice Mock Interview** or **Technical DSA Sandbox** modules in the sidebar!*"""

    async def generate_response(self, prompt: str, session_id: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
        cache_key = f"{session_id or 'anon'}:{prompt.strip().lower()}"
        
        # Check LRU cache
        if cache_key in self.cache:
            ts, cached_resp = self.cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return cached_resp

        sys_prompt = system_prompt or PLACEMENT_SYSTEM_PROMPT
        
        if session_id:
            self.append_message(session_id, "user", prompt)

        messages = [{"role": "system", "content": sys_prompt}]
        if session_id and session_id in self.sessions:
            messages.extend(self.sessions[session_id][-10:])
        else:
            messages.append({"role": "user", "content": prompt})

        # Try Providers in order: Groq -> OpenAI -> Gemini
        bot_reply = await self._call_groq(messages)
        if not bot_reply:
            bot_reply = await self._call_openai(messages)
        if not bot_reply:
            bot_reply = await self._call_gemini(prompt, sys_prompt)

        # Fall back to Smart Intent Domain Engine if external API calls are unavailable
        if not bot_reply:
            bot_reply = self._match_smart_intent(prompt)

        if session_id:
            self.append_message(session_id, "assistant", bot_reply)
            
        self.cache[cache_key] = (time.time(), bot_reply)
        return bot_reply

llm_service = LLMService()
