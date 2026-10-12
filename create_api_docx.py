import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()

    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles & Colors
    PRIMARY_COLOR = RGBColor(30, 27, 75)      # Deep Indigo #1E1B4B
    SECONDARY_COLOR = RGBColor(79, 70, 229)   # Indigo Accent #4F46E5
    DARK_TEXT = RGBColor(31, 41, 55)         # Slate 800 #1F2937
    MUTED_TEXT = RGBColor(100, 116, 139)     # Slate 500 #64748B
    CODE_COLOR = RGBColor(67, 56, 202)       # Indigo Code #4338CA

    # Helper function for setting cell background color
    def set_cell_background(cell, hex_color):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    # Helper function for setting table borders
    def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    # Helper for adding formatted Headings
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(26)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(24)
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = SECONDARY_COLOR
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_COLOR
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_COLOR
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(10.5)
        run.font.color.rgb = DARK_TEXT
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix + " ")
        r_bold.font.name = 'Segoe UI'
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = PRIMARY_COLOR

        r_text = p.add_run(text)
        r_text.font.name = 'Segoe UI'
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = DARK_TEXT
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.5)

        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F5F3FF")

        # Set left border color
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="4F46E5"/>
                <w:top w:val="none"/>
                <w:right w:val="none"/>
                <w:bottom w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.1)
        p.paragraph_format.line_spacing = 1.1

        lines = code_text.strip().split('\n')
        for i, line in enumerate(lines):
            if i > 0:
                p = cell.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.left_indent = Inches(0.1)
                p.paragraph_format.line_spacing = 1.1

            run = p.add_run(line)
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = CODE_COLOR

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # DOCUMENT CONTENT GENERATION
    # -------------------------------------------------------------

    # Title Banner
    add_title("AI Placement Assistant")
    add_subtitle("Backend & Frontend API Connection Architecture & Integration Documentation")

    # Metadata Card Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(2.2)
    meta_table.columns[1].width = Inches(4.3)
    set_table_borders(meta_table, "E2E8F0", "6")

    meta_data = [
        ("Platform Name", "AI Placement Assistant"),
        ("Backend Framework", "Python 3.11+ / FastAPI / Uvicorn"),
        ("Frontend Framework", "React 18 / Vite / Axios / React Router v6"),
        ("Base API Base URL", "http://127.0.0.1:8005/api")
    ]

    for row_idx, (label, val) in enumerate(meta_data):
        cell_lbl = meta_table.cell(row_idx, 0)
        cell_val = meta_table.cell(row_idx, 1)

        set_cell_background(cell_lbl, "EEF2FF")
        set_cell_background(cell_val, "FAFAFA")

        p_lbl = cell_lbl.paragraphs[0]
        r1 = p_lbl.add_run(label)
        r1.font.name = 'Segoe UI'
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = PRIMARY_COLOR

        p_val = cell_val.paragraphs[0]
        r2 = p_val.add_run(val)
        r2.font.name = 'Segoe UI'
        r2.font.size = Pt(10)
        r2.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Executive Overview
    add_h1("1. Executive Overview & Architecture")
    add_p("The AI Placement Assistant application is built using a modern decoupled client-server architecture designed for high throughput, real-time interactive evaluation, and seamless scalability. The backend service is powered by FastAPI (Python), providing asynchronous non-blocking request handling, auto-generated OpenAPI schemas, and strict data validation via Pydantic models. The frontend application is constructed with React 18 and Vite, utilizing Axios as the HTTP client to manage asynchronous requests, state persistence, binary streams, and UI notifications.")
    
    add_p("The frontend communicates with the backend exclusively via RESTful JSON APIs over HTTP/HTTPS. Cross-Origin Resource Sharing (CORS) is explicitly enabled on the FastAPI application middleware to ensure secure and seamless inter-service communication during local development and production deployment.")

    # System Architecture Summary Table
    add_h2("1.1 Core Technology Stack & Responsibilities")
    tech_table = doc.add_table(rows=6, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False
    tech_table.columns[0].width = Inches(1.5)
    tech_table.columns[1].width = Inches(2.2)
    tech_table.columns[2].width = Inches(2.8)
    set_table_borders(tech_table, "CBD5E1", "6")

    headers = ["Layer", "Technology / Library", "Key Responsibility"]
    hdr_cells = tech_table.rows[0].cells
    for i, title in enumerate(headers):
        set_cell_background(hdr_cells[i], "1E1B4B")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(title)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    tech_rows = [
        ("Frontend UI", "React 18 + Vite", "Component-based user interface, state management, SPA routing"),
        ("HTTP Client", "Axios", "RESTful API client, error handling, JSON serialization, Blob downloads"),
        ("Backend Framework", "FastAPI + Uvicorn", "Async REST API server, routing, request validation, CORS middleware"),
        ("AI / LLM Engine", "Groq / OpenAI / Fallback", "Generative response synthesis for career guidance, resume audits, mock feedback"),
        ("PDF Service", "ReportLab", "Dynamic PDF canvas generation for ATS-ready resume downloads")
    ]

    for r_idx, data in enumerate(tech_rows, start=1):
        row_cells = tech_table.rows[r_idx].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(data):
            set_cell_background(row_cells[c_idx], bg_color)
            p = row_cells[c_idx].paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Segoe UI'
            r.font.size = Pt(9.5)
            r.font.color.rgb = DARK_TEXT
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 2: Connection Protocol & Configuration
    add_h1("2. Backend-Frontend Connection Protocol & Configuration")
    add_p("The connection between the React frontend and FastAPI backend relies on standard HTTP REST protocols over TCP port 8005. Below are the key structural components of this connection:")

    add_bullet("Base API Endpoint:", "All modular service endpoints are grouped under the '/api' prefix. The standard local base URL defined in the frontend is `http://127.0.0.1:8005/api`.")
    add_bullet("CORS Authorization:", "FastAPI enables `CORSMiddleware` with `allow_origins=['*']`, `allow_credentials=True`, `allow_methods=['*']`, and `allow_headers=['*']` to prevent cross-origin blockages during fetch operations.")
    add_bullet("Request Headers:", "All JSON payloads use `Content-Type: application/json`. Audio file uploads use `multipart/form-data`. PDF downloads expect `Response` with binary data and attachment disposition headers.")
    add_bullet("Resilience & Fallbacks:", "Every backend endpoint includes algorithmic fallback logic. If an external LLM API rate-limits or fails, the backend returns precision heuristic evaluations so the frontend never crashes.")

    add_h2("2.1 FastAPI CORS Middleware Configuration (backend/app/main.py)")
    add_code_block("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, chatbot, resume, roadmap, interview, dsa

app = FastAPI(title="AI Placement Assistant", version="1.0.0")

# Enable Cross-Origin Resource Sharing (CORS) for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Modular Feature Routers under /api
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(resume.router, prefix="/api/resume", tags=["Resume Generator"])
app.include_router(roadmap.router, prefix="/api/roadmap", tags=["Roadmap Generator"])
app.include_router(interview.router, prefix="/api/interview", tags=["Mock Interview"])
app.include_router(dsa.router, prefix="/api/dsa", tags=["Technical DSA"])""")

    # Section 3: Detailed API Endpoint Mapping
    add_h1("3. Detailed API Endpoint Mapping & Data Schemas")
    add_p("The system contains 6 core functional backend routers containing 12 distinct API endpoints. Each feature module on the React frontend maps directly to corresponding backend endpoints.")

    # 3.1 System & Health API
    add_h2("3.1 System & Health Monitor API")
    add_bullet("Endpoint Path:", "GET /api/health")
    add_bullet("Frontend Caller:", "Application initialization / System status component")
    add_bullet("Purpose:", "Verifies backend operational status, version number, and app instance health.")
    add_p("Response Payload Schema:")
    add_code_block("""{
  "status": "online",
  "app": "AI Placement Assistant",
  "version": "1.0.0"
}""")

    # 3.2 Chatbot API
    add_h2("3.2 Chatbot / AI Placement Advisor API")
    add_bullet("Endpoint Path:", "POST /api/chatbot/chat")
    add_bullet("Frontend Page:", "frontend/src/pages/ChatbotPage.jsx")
    add_bullet("Purpose:", "Provides conversational AI guidance for campus placement rounds, interview tips, company-specific hiring criteria, and algorithmic strategy.")
    add_p("Frontend Integration Call (Axios):")
    add_code_block("""const res = await axios.post('http://127.0.0.1:8005/api/chatbot/chat', {
    message: queryText,
    session_id: sessionId
});
setSessionId(res.data.session_id);
setMessages((prev) => [...prev, { role: 'assistant', content: res.data.reply }]);""")

    add_p("Request Payload Schema (Pydantic model: ChatRequest):")
    add_code_block("""{
  "message": "Amazon SDE Placement Process & Principles",
  "session_id": "session_1725790000123",
  "history": []
}""")

    add_p("Response Payload Schema (Pydantic model: ChatResponse):")
    add_code_block("""{
  "reply": "### Amazon SDE Recruitment Overview 🎯\\n\\n1. **Online Assessment (OA):** 2 Coding Questions (90 mins) + Work Style Assessment.\\n2. **Technical Interviews (3-4 Rounds):** Data Structures, Algorithms, System Design, and Amazon 16 Leadership Principles...",
  "session_id": "session_1725790000123",
  "suggestions": [
    "Amazon SDE Recruitment Rounds & Principles",
    "How to make my resume ATS-friendly?",
    "High-frequency DSA topics for campus placements",
    "Behavioral interview STAR method explanation"
  ]
}""")

    # 3.3 Resume Generator & ATS Audit API
    add_h2("3.3 Resume Generator & ATS Audit API")
    add_p("The Resume module features two primary backend connection endpoints: one for PDF compilation and binary streaming, and another for deep ATS analysis.")

    add_bullet("Endpoint 1 Path:", "POST /api/resume/generate")
    add_bullet("Frontend Page:", "frontend/src/pages/ResumePage.jsx")
    add_bullet("Purpose:", "Accepts structured candidate profile data, generates a clean ATS-formatted PDF using ReportLab, and streams the binary blob back to the browser for instant download.")
    add_p("Frontend Download Integration (Axios Blob Stream):")
    add_code_block("""const res = await axios.post('http://127.0.0.1:8005/api/resume/generate', resumeData, {
    responseType: 'blob'
});
const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
const link = document.createElement('a');
link.href = url;
link.setAttribute('download', `${resumeData.fullName}_Resume.pdf`);
document.body.appendChild(link);
link.click();""")

    add_bullet("Endpoint 2 Path:", "POST /api/resume/analyze")
    add_bullet("Frontend Page:", "frontend/src/pages/ResumePage.jsx")
    add_bullet("Purpose:", "Evaluates candidate resume data against FAANG recruiter criteria, providing an ATS compatibility score (0-100), key strengths, actionable Google XYZ bullet points, and an optimized summary.")

    add_p("Request Payload Schema (Pydantic model: ResumeData):")
    add_code_block("""{
  "fullName": "Alex Rivera",
  "email": "alex.rivera@example.com",
  "phone": "+1 (555) 234-5678",
  "location": "Seattle, WA",
  "github": "https://github.com/alexrivera",
  "linkedin": "https://linkedin.com/in/alexrivera",
  "summary": "Full Stack Engineer with 2+ years of experience...",
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "institution": "State University",
      "year": "2024",
      "gpa": "3.8/4.0"
    }
  ],
  "experience": [
    {
      "role": "Software Engineering Intern",
      "company": "Tech Corp",
      "duration": "Summer 2023",
      "bullet1": "Optimized REST API database queries reducing latency by 35%.",
      "bullet2": "Built microservice endpoint using Python FastAPI and Docker."
    }
  ],
  "projects": [
    {
      "title": "E-Commerce Platform",
      "techStack": "React, Node.js, MongoDB",
      "description": "Implemented payment gateway & live inventory tracking."
    }
  ],
  "skills": ["Python", "FastAPI", "React", "TypeScript", "Docker", "PostgreSQL", "Git", "AWS"]
}""")

    add_p("ATS Analysis Response Payload Schema:")
    add_code_block("""{
  "score": 88,
  "strengths": [
    "Comprehensive technical stack (8 verified skills including core engineering tools)",
    "Solid practical experience showcasing 1 substantial software projects",
    "Demonstrates quantifiable impact with metrics and percentages"
  ],
  "improvements": [
    "Apply Google XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'",
    "Add at least 2 full-stack/domain projects with live deployment links"
  ],
  "suggested_summary": "Results-driven Software Engineer with expertise in Python, FastAPI, React, TypeScript, Docker. Proven track record in building scalable applications and delivering measurable project results."
}""")

    # 3.4 Roadmap Generator API
    add_h2("3.4 Career Roadmap Generator API")
    add_bullet("Endpoint Path:", "POST /api/roadmap/generate")
    add_bullet("Frontend Page:", "frontend/src/pages/RoadmapPage.jsx")
    add_bullet("Purpose:", "Generates a dynamic month-by-month placement preparation timeline tailored to target role, current skill level, and target duration.")

    add_p("Request Payload Schema (Pydantic model: RoadmapRequest):")
    add_code_block("""{
  "target_role": "Software Development Engineer",
  "current_skill_level": "Beginner",
  "target_months": 6
}""")

    add_p("Response Payload Schema:")
    add_code_block("""{
  "title": "6-Month Placement Preparation Roadmap for Software Development Engineer",
  "target_role": "Software Development Engineer",
  "current_skill_level": "Beginner",
  "duration": "6 Months",
  "summary": "Structured month-by-month preparation plan focusing on Data Structures & Algorithms, System Design, Core CS, and Portfolio projects.",
  "phases": [
    {
      "month": 1,
      "title": "Month 1: DSA Foundations, Language Syntax & Complexity Analysis",
      "focus": "Master C++/Java/Python fundamentals, Big-O Time & Space complexity analysis, Arrays, Strings, and Two Pointer techniques.",
      "action_items": [
        "Solve 30 Easy problems on LeetCode / HackerRank",
        "Implement custom Array & Dynamic Array structures",
        "Learn Time & Space Complexity analysis (Big-O notation)"
      ],
      "recommended_resources": [
        "NeetCode 150 - Arrays & Hashing",
        "Striver A2Z DSA Sheet Module 1"
      ]
    }
  ]
}""")

    # 3.5 AI Mock Interview Studio API
    add_h2("3.5 Voice & AI Mock Interview Studio API")
    add_p("The Mock Interview module provides voice recording evaluation, speech transcription, questions bank fetch, and technical feedback scoring.")

    add_bullet("1. Questions Bank Endpoint:", "GET /api/interview/questions")
    add_bullet("2. Audio Transcription Endpoint:", "POST /api/interview/transcribe (Multipart Form-Data)")
    add_bullet("3. Response Evaluation Endpoint:", "POST /api/interview/evaluate (JSON Payload)")
    add_bullet("4. Speech Synthesis Endpoint:", "POST /api/interview/synthesize")

    add_p("Evaluation Request Schema (Pydantic model: InterviewEvaluationRequest):")
    add_code_block("""{
  "question": "Tell me about a time you faced a difficult technical challenge in a project and how you resolved it.",
  "user_transcript": "During our team capstone project, our database queries were bottlenecking during stress testing. I benchmarked execution times, added composite indices in PostgreSQL, and implemented Redis caching for user sessions. This reduced p99 latency by 45%.",
  "role": "Software Engineer"
}""")

    add_p("Evaluation Response Schema:")
    add_code_block("""{
  "score": 92,
  "clarity_rating": "Excellent",
  "technical_accuracy": "95% High Accuracy",
  "overall_feedback": "Demonstrated solid technical grasp (key engineering terms detected: optimize, latency, query, database, cache, redis). Answer length: 34 words.",
  "follow_up_question": "What specific metrics or benchmarking tools did you use to validate your time/space trade-offs?",
  "strengths": [
    "Included technical terms such as database, cache",
    "Communicated problem-solving strategy clearly"
  ],
  "improvements": [
    "Structure response strictly into Situation, Task, Action, and Result (STAR method)",
    "Quantify impact with percentage or latency numbers"
  ],
  "ideal_sample_answer": "**Situation:** During my software project, we encountered bottlenecks...\\n\\n**Action:** I benchmarked execution times and replaced naive loops with hash lookups.\\n\\n**Result:** Reduced query latency by 45% and improved concurrent throughput."
}""")

    # 3.6 Technical DSA Workbench API
    add_h2("3.6 Technical DSA Coding Workbench API")
    add_p("The DSA Coding Workbench API allows candidates to solve algorithm challenges, run code submissions inside an execution sandbox, and request AI hints.")

    add_bullet("1. Get Problems Endpoint:", "GET /api/dsa/problems?difficulty=All")
    add_bullet("2. Code Submission & Execution Endpoint:", "POST /api/dsa/submit (or /api/dsa/run)")
    add_bullet("3. AI Tutor Hint Endpoint:", "POST /api/dsa/hint")

    add_p("Code Submission Request Schema (Pydantic model: CodeRunRequest):")
    add_code_block("""{
  "problem_id": "two-sum",
  "code": "class Solution:\\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\\n        seen = {}\\n        for i, n in enumerate(nums):\\n            diff = target - n\\n            if diff in seen:\\n                return [seen[diff], i]\\n            seen[n] = i\\n        return []"
}""")

    add_p("Execution Response Schema (from dsa_runner service):")
    add_code_block("""{
  "passed": true,
  "passed_count": 3,
  "total_count": 3,
  "details": [
    {
      "test_case": 1,
      "input": {"nums": [2, 7, 11, 15], "target": 9},
      "expected": [0, 1],
      "actual": [0, 1],
      "status": "PASSED"
    },
    {
      "test_case": 2,
      "input": {"nums": [3, 2, 4], "target": 6},
      "expected": [1, 2],
      "actual": [1, 2],
      "status": "PASSED"
    }
  ]
}""")

    add_p("AI Tutor Hint Response Schema:")
    add_code_block("""{
  "hint": "Try using a Hash Map to store elements you have seen along with their indices.",
  "logic_explanation": "As you iterate through array x, check if (target - x) exists in hash map. If found, return [map[target - x], i].",
  "time_complexity": "O(N) - single pass through array",
  "space_complexity": "O(N) - storing elements in Hash Map"
}""")

    # Section 4: Security & Performance
    add_h1("4. Security, Isolation Sandbox & System Resiliency")
    add_p("Connecting frontend user code execution and external LLM services safely requires robust backend safeguards:")

    add_bullet("Code Execution Sandbox (app/services/dsa_runner.py):", "User Python code submissions are dynamically compiled and executed in a restricted context using `exec()`. Globals are scoped to prevent unauthorized system calls or filesystem access.")
    add_bullet("Asynchronous LLM Gateway (app/services/llm_service.py):", "Requests to LLM APIs (Groq / Gemini / OpenAI) use asynchronous HTTP client calls (`async/await`), ensuring the FastAPI event loop is never blocked.")
    add_bullet("Graceful Degradation & Heuristic Fallbacks:", "Every single AI endpoint (Chatbot, Resume, Roadmap, Interview, DSA) has an embedded algorithmic fallback engine. If network connectivity fails or API keys expire, the backend instantly computes deterministic heuristic feedback.")
    add_bullet("Stateless Session Management:", "Chatbot and interview sessions pass explicit `session_id` tokens between frontend and backend, maintaining thread context without imposing memory leaks on the backend server.")

    # Section 5: Verification & Summary Table
    add_h1("5. API Verification & Testing Checklist")
    add_p("The table below outlines the status and verification method for all backend-frontend API connections:")

    verify_table = doc.add_table(rows=7, cols=4)
    verify_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    verify_table.autofit = False
    verify_table.columns[0].width = Inches(1.2)
    verify_table.columns[1].width = Inches(2.3)
    verify_table.columns[2].width = Inches(1.8)
    verify_table.columns[3].width = Inches(1.2)
    set_table_borders(verify_table, "CBD5E1", "6")

    v_headers = ["Module", "Endpoints", "Verification Method", "Status"]
    v_hdr_cells = verify_table.rows[0].cells
    for i, title in enumerate(v_headers):
        set_cell_background(v_hdr_cells[i], "1E1B4B")
        p = v_hdr_cells[i].paragraphs[0]
        r = p.add_run(title)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    v_rows = [
        ("System Health", "GET /api/health", "Axios status check & FastAPI /docs", "VERIFIED"),
        ("Chatbot", "POST /api/chatbot/chat", "Interactive chat & history persistence", "VERIFIED"),
        ("Resume Studio", "POST /api/resume/generate\nPOST /api/resume/analyze", "Blob stream PDF download & ATS JSON score audit", "VERIFIED"),
        ("Roadmap Studio", "POST /api/roadmap/generate", "Dynamic phase generation & custom duration", "VERIFIED"),
        ("Mock Interview", "GET /api/interview/questions\nPOST /api/interview/evaluate\nPOST /api/interview/transcribe", "Voice recording transcript & STAR scoring engine", "VERIFIED"),
        ("DSA Workbench", "GET /api/dsa/problems\nPOST /api/dsa/submit\nPOST /api/dsa/hint", "Isolated test-case execution & AI tutor hints", "VERIFIED")
    ]

    for r_idx, data in enumerate(v_rows, start=1):
        row_cells = verify_table.rows[r_idx].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(data):
            set_cell_background(row_cells[c_idx], bg_color)
            p = row_cells[c_idx].paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Segoe UI'
            r.font.size = Pt(9)
            r.font.color.rgb = DARK_TEXT
            if c_idx == 0:
                r.font.bold = True
            if c_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Conclusion note
    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("--- End of API Connection Architecture Documentation ---")
    r_end.font.name = 'Segoe UI'
    r_end.font.size = Pt(10)
    r_end.font.italic = True
    r_end.font.color.rgb = MUTED_TEXT

    # Save output document
    output_filename = "c:\\Users\\adwai\\Ai Placement assistant\\Backend_and_Frontend_API_Connection_Documentation.docx"
    doc.save(output_filename)
    print(f"Successfully generated Word document at: {output_filename}")

if __name__ == "__main__":
    create_document()
