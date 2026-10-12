import json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.llm_service import llm_service

router = APIRouter()

class RoadmapRequest(BaseModel):
    target_role: str = "Software Development Engineer"
    current_skill_level: Optional[str] = "Beginner"
    target_months: Optional[int] = 6
    timeframe_months: Optional[int] = None

    def get_months(self) -> int:
        return self.timeframe_months or self.target_months or 6

def build_dynamic_phases(target_role: str, skill_level: str, months: int) -> List[dict]:
    # Master template of monthly topics for placement preparation
    topic_templates = [
        {
            "title_suffix": "DSA Foundations, Language Syntax & Complexity Analysis",
            "focus": "Master C++/Java/Python fundamentals, Big-O Time & Space complexity analysis, Arrays, Strings, and Two Pointer techniques.",
            "action_items": [
                "Solve 30 Easy problems on LeetCode / HackerRank",
                "Implement custom Array & Dynamic Array structures",
                "Learn Time & Space Complexity analysis (Big-O notation)"
            ],
            "resources": ["NeetCode 150 - Arrays & Hashing", "Striver A2Z DSA Sheet Module 1"]
        },
        {
            "title_suffix": "Hashing, Sliding Window & Fast/Slow Pointers",
            "focus": "Deep dive into HashMap internals, collision resolution, variable & fixed sliding window patterns.",
            "action_items": [
                "Solve 25 Hash & Sliding Window problems on LeetCode",
                "Implement custom Hash Table with chaining",
                "Practice Prefix Sum and Two-Pointer optimization"
            ],
            "resources": ["LeetCode 75 - Sliding Window", "GeeksforGeeks Hashing Guide"]
        },
        {
            "title_suffix": "Linked Lists, Stacks & Queues",
            "focus": "Singly & Doubly Linked Lists, Monotonic Stacks, Queues, and Deque data structures.",
            "action_items": [
                "Solve 20 Linked List & Stack/Queue problems",
                "Implement LRU Cache using HashMap + Doubly Linked List",
                "Master Monotonic Stack pattern for Next Greater Element"
            ],
            "resources": ["NeetCode - Linked Lists", "Striver Stack & Queue Sheet"]
        },
        {
            "title_suffix": "Binary Trees, Binary Search Trees & Recursion",
            "focus": "Tree traversals (BFS, DFS, Inorder, Preorder, Postorder), BST operations, and Backtracking.",
            "action_items": [
                "Solve 30 Tree & Recursion problems on LeetCode",
                "Implement Lowest Common Ancestor (LCA) and Tree Diameter",
                "Practice Subsets, Permutations, and N-Queens Backtracking"
            ],
            "resources": ["LeetCode Tree Card", "Striver Tree Series"]
        },
        {
            "title_suffix": "Graph Algorithms, BFS/DFS & Shortest Paths",
            "focus": "Adjacency list/matrix representation, Topological Sort, Dijkstra, Kahn's Algorithm, Union-Find.",
            "action_items": [
                "Solve 25 Graph problems (Connected Components, Cycle Detection)",
                "Implement Dijkstra's Algorithm using Min-Heap PriorityQueue",
                "Learn Disjoint Set Union (DSU) with Path Compression"
            ],
            "resources": ["WilliamFiset Graph Theory Playlist", "NeetCode Graphs"]
        },
        {
            "title_suffix": "Dynamic Programming Foundations & 1D/2D DP",
            "focus": "Memoization vs Tabulation, 1D DP (Fibonacci, House Robber), 2D DP (Knapsack, LCS, Edit Distance).",
            "action_items": [
                "Solve 25 classic DP problems on LeetCode",
                "Master 0/1 Knapsack, Unbounded Knapsack, and Subset Sum",
                "Practice Longest Common Subsequence & Matrix Chain Multiplication"
            ],
            "resources": ["Aditya Verma DP Playlist", "Striver DP Series"]
        },
        {
            "title_suffix": "Low-Level Design (LLD) & Object-Oriented Design",
            "focus": "SOLID Principles, Design Patterns (Factory, Singleton, Observer, Strategy), Class Diagrams.",
            "action_items": [
                "Design Parking Lot / Elevator System / BookMyShow LLD",
                "Write clean, extensible Python/Java code using OOP principles",
                "Draw UML Class Diagrams and Sequence Diagrams"
            ],
            "resources": ["Head First Design Patterns", "Grokking the Low Level Design"]
        },
        {
            "title_suffix": "High-Level System Design (HLD) & Architecture",
            "focus": "Scalability, Load Balancers, API Gateways, Caching (Redis), Database Sharding, Message Queues (Kafka).",
            "action_items": [
                "Design Rate Limiter / URL Shortener / Microservice Architecture",
                "Understand SQL vs NoSQL trade-offs and CAP Theorem",
                "Implement JWT Authentication & Redis Caching in FastAPI"
            ],
            "resources": ["System Design Primer (GitHub)", "Grokking System Design"]
        },
        {
            "title_suffix": "Full-Stack Project Development & Microservices",
            "focus": "Build & deploy robust production-ready web application with frontend (React) and backend (FastAPI/Node).",
            "action_items": [
                "Build 1 Full-Stack Project with REST/GraphQL endpoints",
                "Write Unit & Integration tests, Dockerize application",
                "Deploy project on AWS / Vercel / Render with CI/CD pipeline"
            ],
            "resources": ["Full Stack Open", "FastAPI Official Documentation"]
        },
        {
            "title_suffix": "DBMS, SQL Query Optimization & Operating Systems",
            "focus": "B-Tree Indexing, ACID Properties, Normalization, SQL Window Functions, Processes, Threads & Memory Management.",
            "action_items": [
                "Solve 30 Complex SQL Query challenges on LeetCode",
                "Revise OS Memory Management, Paging, Virtual Memory, Deadlocks",
                "Understand Process Synchronization, Mutexes & Semaphores"
            ],
            "resources": ["Gate Smashers OS & DBMS", "SQLZoo Interactive"]
        },
        {
            "title_suffix": "Computer Networks, Web Security & Core CS Revision",
            "focus": "TCP/IP vs OSI model, HTTP/HTTPS, DNS, Sockets, CORS, OAuth2, and CS Core Revision.",
            "action_items": [
                "Understand TCP 3-way handshake and TLS Encryption",
                "Revise Top 50 CS Core Interview Questions",
                "Refine Resume using Google XYZ Bullet Formula"
            ],
            "resources": ["Computer Networking: A Top-Down Approach", "Placement AI Resume Studio"]
        },
        {
            "title_suffix": "Behavioral STAR Framework & Mock Interview Sprint",
            "focus": "Amazon Leadership Principles, STAR Method, Behavioral Responses, and Live Mock Interviews.",
            "action_items": [
                "Prepare 5 STAR stories (Technical Challenge, Conflict, Failure, Success)",
                "Complete 10 Voice Mock Interviews on Placement AI Interview Studio",
                "Apply to campus drives & off-campus tech roles"
            ],
            "resources": ["Placement AI Interview Studio", "Pramp Mock Interviews"]
        }
    ]

    phases = []
    # Generate exactly `months` phases
    for i in range(1, months + 1):
        # Choose or interpolate template index
        idx = min(i - 1, len(topic_templates) - 1)
        if months <= 4:
            # Compression for short durations
            step_stride = len(topic_templates) // months
            idx = min((i - 1) * step_stride, len(topic_templates) - 1)
            
        tpl = topic_templates[idx]
        phases.append({
            "month": i,
            "title": f"Month {i}: {tpl['title_suffix']}",
            "focus": tpl["focus"],
            "action_items": tpl["action_items"],
            "recommended_resources": tpl["resources"]
        })
    return phases


@router.post("/generate")
async def generate_roadmap(req: RoadmapRequest):
    months = req.get_months()
    title = f"{months}-Month Placement Preparation Roadmap for {req.target_role}"
    summary = f"Structured month-by-month preparation plan focusing on Data Structures & Algorithms, System Design, Core CS, and Portfolio projects."

    prompt = f"Create a structured month-by-month learning roadmap for target role: '{req.target_role}' starting at skill level '{req.current_skill_level}' over {months} months. Output JSON with fields: title (str), summary (str), phases (list of {months} objects with month (int 1 to {months}), title (str), focus (str), action_items (list of strings), recommended_resources (list of strings))."
    system_prompt = "You are a Tech Career Advisor. Output pure JSON for the career roadmap."

    fallback_phases = build_dynamic_phases(req.target_role, req.current_skill_level or "Beginner", months)

    response_text = await llm_service.generate_response(prompt, system_prompt=system_prompt)

    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            data = json.loads(response_text[start_idx:end_idx])
            phases = data.get("phases") or data.get("timeline")
            if phases and len(phases) >= months:
                return {
                    "title": data.get("title", title),
                    "target_role": req.target_role,
                    "current_skill_level": req.current_skill_level,
                    "duration": f"{months} Months",
                    "summary": data.get("summary", summary),
                    "phases": phases,
                    "timeline": phases
                }
    except Exception:
        pass

    return {
        "title": title,
        "target_role": req.target_role,
        "current_skill_level": req.current_skill_level,
        "duration": f"{months} Months",
        "summary": summary,
        "phases": fallback_phases,
        "timeline": fallback_phases
    }
