# 🚀 AI Placement Assistant

A full-stack, AI-powered campus and off-campus placement preparation platform designed to help software engineering students and graduates crack technical and behavioral interviews at top-tier product and service MNCs (Amazon, Google, Microsoft, Meta, TCS, Infosys, and high-growth startups).

---

## 🌟 Key Features

### 1. 🤖 AI Placement Advisor & Chatbot
* **Intelligent Guidance:** In-depth advice on hiring processes, online assessments (OA), cutoff criteria, and interview structures across Tier-1 Product MNCs and IT Service companies.
* **Multi-Provider LLM Integration:** Flexible architecture supporting **Groq (Llama 3.3 70B)**, **OpenAI (GPT-3.5/4)**, and **Google Gemini 1.5 Flash**.
* **Zero-Downtime Smart Intent Engine:** Built-in offline fallback engine with curated domain knowledge (DSA roadmaps, STAR method, Google XYZ bullet points, SQL guides).

### 2. 📄 ATS-Optimized Resume Builder & Analyzer
* **Automated ATS Scoring:** Evaluates resume structure, action verbs, quantified metrics, and role-specific keywords.
* **Google XYZ Formula Integration:** Actionable recommendations to transform weak bullet points into high-impact accomplishments.
* **Instant PDF Export:** Clean, single-column export format compliant with automated ATS parsers using `html2pdf.js`.

### 3. 🗺️ Personalized Career Roadmap Generator
* **Role-Specific Milestones:** Customized week-by-week learning paths for SDE, Frontend, Backend, Full-Stack, Machine Learning, and DevOps roles.
* **Curated Learning Links:** Direct recommendations for high-yield documentation, practice problems, and study materials.

### 4. 🎙️ AI Mock Interview & Speech Evaluator
* **Simulated Interview Rounds:** Technical deep-dives and behavioral rounds.
* **Automated Transcription & Evaluation:** Analyzes candidate responses using the **STAR Method** (Situation, Task, Action, Result) with detailed rubrics and constructive feedback.

### 5. 💻 Technical DSA Studio & Code Runner
* **Monaco Code Editor:** Interactive code workspace powered by the VS Code editor engine (`@monaco-editor/react`).
* **Problem Bank & Test Cases:** Curated algorithmic problem bank across Arrays, Two Pointers, Trees, Dynamic Programming, and Graphs.
* **Secure Code Runner:** Automated test runner executing and validating Python code against public and hidden test cases.
* **AI Hint Assistant:** Progressive hints that guide candidates without giving away the complete solution.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 19, Vite, Tailwind CSS v4, Monaco Editor (`@monaco-editor/react`), Lucide React, React Router v7, Axios, html2pdf.js |
| **Backend** | FastAPI, Uvicorn, Python 3.10+, Pydantic v2, HTTPX, Requests, Python-dotenv |
| **AI / LLMs** | Groq (Llama 3.3), OpenAI API, Google Gemini, Custom Rule-Based Intent Engine |
| **Styling & UI** | Tailwind CSS v4, Modern Glassmorphism & Responsive Dark/Light Layouts |

---

## 📂 Project Structure

```text
Ai Placement assistant/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── chatbot.py        # /api/chatbot endpoints
│   │   │   ├── dsa.py            # /api/dsa problems & code runner
│   │   │   ├── health.py         # /api/health check
│   │   │   ├── interview.py      # /api/interview mock evaluation
│   │   │   ├── resume.py         # /api/resume generation & analysis
│   │   │   └── roadmap.py        # /api/roadmap generation
│   │   ├── services/
│   │   │   ├── dsa_runner.py     # Python code runner sandbox
│   │   │   ├── llm_service.py    # Multi-provider LLM & intent engine
│   │   │   └── pdf_service.py    # Resume formatting & PDF utilities
│   │   ├── config.py             # App settings & environment loaders
│   │   └── main.py               # FastAPI entry point & CORS configuration
│   ├── .env.example              # Sample environment template
│   ├── requirements.txt          # Python dependencies
│   └── test_backend.py           # Comprehensive endpoint verification script
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI widgets & Navbar
│   │   ├── config/               # API endpoint configurations
│   │   ├── context/              # Global state & user context
│   │   ├── pages/                # App views (Chatbot, Resume, Roadmap, Interview, DSA)
│   │   ├── App.jsx               # React Router & shell
│   │   ├── main.jsx              # Application root
│   │   └── index.css             # Tailwind CSS entry
│   ├── package.json              # Frontend dependencies and scripts
│   ├── vite.config.js            # Vite configuration
│   └── index.html                # HTML entry point
├── Backend_and_Frontend_API_Connection_Documentation.docx
├── Placement_AI_Assistant_3DVerse_Presentation.pptx
├── Placement_AI_Chatbot_Presentation.pptx
├── .gitignore                    # Git ignore file for Python & Node
└── README.md                     # Project documentation
```

---

## ⚡ Getting Started

### 1. Prerequisites
* **Python 3.10+**
* **Node.js 18+** and **npm**
* Git

---

### 2. Backend Setup

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   *(Optional: Add your `GROQ_API_KEY`, `OPENAI_API_KEY`, or `GEMINI_API_KEY` in `.env`. If left empty, the application seamlessly runs using its built-in offline knowledge engine.)*

5. Start the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```
   The interactive Swagger documentation will be available at: **http://127.0.0.1:8000/docs**

---

### 3. Frontend Setup

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```
   The application will be accessible at: **http://localhost:5173**

---

### 4. Running Backend Verification Tests

To verify that all backend modules and API routes are healthy and responding correctly:
```bash
cd backend
python test_backend.py
```

---

## 📄 Documentation & Presentation Assets
Included directly in the root directory:
* **API Documentation**: `Backend_and_Frontend_API_Connection_Documentation.docx`
* **Project Pitch Decks**:
  * `Placement_AI_Assistant_3DVerse_Presentation.pptx`
  * `Placement_AI_Chatbot_Presentation.pptx`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues tab.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
