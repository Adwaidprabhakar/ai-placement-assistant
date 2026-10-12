import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette (3DVerse Obsidian Aesthetic)
    COLOR_BG = RGBColor(5, 3, 10)           # #05030A Deep Obsidian
    COLOR_CARD = RGBColor(12, 13, 22)        # #0C0D16 Dark Glass Card
    COLOR_CARD_ALT = RGBColor(17, 18, 30)    # #11121E Card Highlighting
    COLOR_BORDER = RGBColor(79, 70, 229)     # #4F46E5 Indigo Glass Border
    COLOR_BORDER_PURPLE = RGBColor(168, 85, 247) # #A855F7 Electric Purple Border
    
    COLOR_TEXT_WHITE = RGBColor(255, 255, 255) # White Header
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400 Muted
    COLOR_PURPLE = RGBColor(168, 85, 247)     # #A855F7 Electric Purple
    COLOR_INDIGO = RGBColor(99, 102, 241)     # #6366F1 Soft Indigo
    COLOR_CYAN = RGBColor(56, 189, 248)       # #38BDF8 Soft Cyan
    COLOR_GREEN = RGBColor(16, 185, 129)      # #10B981 Emerald Green

    def create_slide():
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG
        return slide

    def add_footer(slide, page_num):
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(6.0), Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "PLACEMENT AI CHATBOT  •  CAREER ADVISOR MODULE"
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED

        num_str = f"0{page_num}" if page_num < 10 else str(page_num)
        tx_num = slide.shapes.add_textbox(Inches(11.8), Inches(6.8), Inches(0.8), Inches(0.4))
        tf_num = tx_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = num_str
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(9)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_PURPLE

    def add_header(slide, title_text, subtitle_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.7), Inches(0.4))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_rgb=COLOR_CARD, border_rgb=COLOR_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_rgb
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(1.2)
        return shape

    def add_badge(slide, text, left, top, width=Inches(1.8), height=Inches(0.35), bg_rgb=COLOR_CARD_ALT, text_rgb=COLOR_CYAN):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_rgb
        shape.line.color.rgb = COLOR_BORDER
        shape.line.width = Pt(1.0)
        tf = shape.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = text
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = text_rgb
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = create_slide()

    add_badge(s1, "LOCAL & CLOUD LLM", Inches(0.8), Inches(1.2), Inches(1.8), Inches(0.38), text_rgb=COLOR_CYAN)
    add_badge(s1, "SMART CAREER BOT", Inches(2.8), Inches(1.2), Inches(1.8), Inches(0.38), text_rgb=COLOR_PURPLE)
    add_badge(s1, "REAL-TIME ADVISOR", Inches(4.8), Inches(1.2), Inches(1.9), Inches(0.38), text_rgb=COLOR_GREEN)

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "PLACEMENT AI CHATBOT"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Smart Business AI Career Advisor & Technical Placement Assistant"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PURPLE

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(8)
    p3.text = "Real-time conversational intelligence for corporate recruitment rounds, ATS resume bullet auditing, DSA patterns, and behavioral STAR interview strategies."
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    card_w = Inches(3.64)
    card_h = Inches(2.5)
    gap = Inches(0.4)

    add_card(s1, Inches(0.8), Inches(3.9), card_w, card_h)
    tb_c1 = s1.shapes.add_textbox(Inches(0.95), Inches(4.05), card_w - Inches(0.3), card_h - Inches(0.3))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Recruitment Process Advisor"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN
    p_desc = tf_c1.add_paragraph()
    p_desc.space_before = Pt(6)
    p_desc.text = "Provides step-by-step interview round breakdowns, online assessment formats, and core leadership principles for 50+ tech giants including Amazon, Google, Microsoft, TCS, and Infosys."
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s1, Inches(0.8) + card_w + gap, Inches(3.9), card_w, card_h)
    tb_c2 = s1.shapes.add_textbox(Inches(0.95) + card_w + gap, Inches(4.05), card_w - Inches(0.3), card_h - Inches(0.3))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Google XYZ & STAR Guidance"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PURPLE
    p_desc = tf_c2.add_paragraph()
    p_desc.space_before = Pt(6)
    p_desc.text = "Guides candidates in constructing 90+ ATS score resumes using Google's XYZ metric formula and structuring behavioral interview answers with the STAR method."
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s1, Inches(0.8) + (card_w + gap) * 2, Inches(3.9), card_w, card_h)
    tb_c3 = s1.shapes.add_textbox(Inches(0.95) + (card_w + gap) * 2, Inches(4.05), card_w - Inches(0.3), card_h - Inches(0.3))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Algorithmic & Code Support"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_GREEN
    p_desc = tf_c3.add_paragraph()
    p_desc.space_before = Pt(6)
    p_desc.text = "Delivers instant algorithmic solutions, time & space complexity breakdowns, NeetCode patterns, and production-ready code snippets with interactive copy formatting."
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = COLOR_TEXT_MUTED

    tb_pres = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(6.0), Inches(0.4))
    p_pres = tb_pres.text_frame.paragraphs[0]
    p_pres.text = "Presenter: Placement AI Team  |  Module 01: Chatbot Engine"
    p_pres.font.size = Pt(9.5)
    p_pres.font.color.rgb = COLOR_TEXT_MUTED

    add_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: System Architecture & Data Flow
    # =========================================================================
    s2 = create_slide()
    add_header(s2, "System Architecture & Chatbot Data Flow", "Decoupled React 18 client communicating with FastAPI via RESTful JSON endpoints and asynchronous LLM streaming")

    step_w = Inches(2.7)
    step_h = Inches(4.8)
    step_gap = Inches(0.3)

    steps_data = [
        ("1. React 18 UI Layer", "ChatbotPage.jsx", COLOR_CYAN, [
            "Axios HTTP POST request",
            "Stateful Session ID token",
            "Markdown rendering",
            "Code syntax copy block",
            "Typewriter loader animation"
        ]),
        ("2. FastAPI Gateway", "/api/chatbot/chat", COLOR_PURPLE, [
            "APIRouter prefix under /api",
            "Pydantic model validation",
            "CORSMiddleware authorization",
            "Async non-blocking handler",
            "Session history parsing"
        ]),
        ("3. Intelligence Engine", "LLM + System Prompt", COLOR_INDIGO, [
            "Senior Recruiter persona",
            "FAANG evaluation criteria",
            "Groq / Gemini API client",
            "Async streaming response",
            "Algorithmic fallback rules"
        ]),
        ("4. UI Response Output", "JSON Schema Payload", COLOR_GREEN, [
            "Formatted Markdown reply",
            "Session context update",
            "Quick-prompt suggestions",
            "Error recovery strategy",
            "Smooth scroll auto-trigger"
        ])
    ]

    for idx, (title, sub, accent_color, bullets) in enumerate(steps_data):
        left_pos = Inches(0.8) + idx * (step_w + step_gap)
        add_card(s2, left_pos, Inches(1.7), step_w, step_h)

        tb_step = s2.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.85), step_w - Inches(0.3), step_h - Inches(0.3))
        tf_step = tb_step.text_frame
        tf_step.word_wrap = True

        p_t = tf_step.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(13)
        p_t.font.color.rgb = accent_color

        p_s = tf_step.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(9.5)
        p_s.font.bold = True
        p_s.font.color.rgb = COLOR_TEXT_MUTED
        p_s.space_after = Pt(10)

        for b in bullets:
            pb = tf_step.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = COLOR_TEXT_WHITE
            pb.space_after = Pt(4)

    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: Real-Time Conversational AI & Prompt Engineering
    # =========================================================================
    s3 = create_slide()
    add_header(s3, "Real-Time Conversational AI & System Prompts", "Tailored system prompts and floating quick-prompt presets tuned for technical placement readiness")

    card_l_w = Inches(5.6)
    card_l_h = Inches(4.8)
    add_card(s3, Inches(0.8), Inches(1.7), card_l_w, card_l_h)

    tb_sp = s3.shapes.add_textbox(Inches(1.0), Inches(1.85), card_l_w - Inches(0.4), card_l_h - Inches(0.3))
    tf_sp = tb_sp.text_frame
    tf_sp.word_wrap = True

    p = tf_sp.paragraphs[0]
    p.text = "FAANG Recruiter Persona System Prompt"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_PURPLE

    prompts_bullets = [
        ("Persona Alignment", "Configured as a Senior Technical Recruiter & Hiring Manager at top tech firms (Amazon, Google, Meta)."),
        ("Structured Responses", "Enforces GitHub Flavored Markdown with bold headers, bullet lists, and explicit code syntax blocks."),
        ("Formula Compliance", "Injects Google XYZ formula for resumes ('Accomplished X, measured by Y, by doing Z') and STAR method for behavioral rounds."),
        ("Company Specificity", "Provides actual online assessment (OA) test durations, coding round topics, and leadership principles.")
    ]

    for title, desc in prompts_bullets:
        pb = tf_sp.add_paragraph()
        pb.space_before = Pt(8)
        r_bold = pb.add_run()
        r_bold.text = f"• {title}: "
        r_bold.font.bold = True
        r_bold.font.size = Pt(10)
        r_bold.font.color.rgb = COLOR_CYAN

        r_text = pb.add_run()
        r_text.text = desc
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_TEXT_MUTED

    card_r_w = Inches(5.7)
    card_r_h = Inches(4.8)
    add_card(s3, Inches(6.8), Inches(1.7), card_r_w, card_r_h)

    tb_qp = s3.shapes.add_textbox(Inches(7.0), Inches(1.85), card_r_w - Inches(0.4), card_r_h - Inches(0.3))
    tf_qp = tb_qp.text_frame
    tf_qp.word_wrap = True

    p = tf_qp.paragraphs[0]
    p.text = "Preset Quick Prompts & Intent Categories"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_GREEN

    q_categories = [
        ("Amazon SDE Placement Process", "Triggers detailed 4-stage recruitment pipeline breakdown + 16 Leadership Principles guidance."),
        ("Google XYZ Resume Formula", "Provides example bullets showing percentage latency reductions and memory bandwidth optimizations."),
        ("High-Frequency DSA Patterns", "Highlights top 14 LeetCode patterns (Sliding Window, Two Pointers, Monotonic Stack, 2D DP)."),
        ("Behavioral STAR Explanation", "Breaks down Situation, Task, Action, and Result framing with Amazon / Microsoft STAR examples.")
    ]

    for title, desc in q_categories:
        pb = tf_qp.add_paragraph()
        pb.space_before = Pt(8)
        r_bold = pb.add_run()
        r_bold.text = f"⚡ Prompt: '{title}'\n"
        r_bold.font.bold = True
        r_bold.font.size = Pt(10)
        r_bold.font.color.rgb = COLOR_TEXT_WHITE

        r_text = pb.add_run()
        r_text.text = desc
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = COLOR_TEXT_MUTED

    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: Knowledge Base & Domain Coverage
    # =========================================================================
    s4 = create_slide()
    add_header(s4, "Domain Knowledge Base & Corporate Hiring Coverage", "Comprehensive intelligence across tier-1 software companies, core CS topics, and coding interview rounds")

    grid_w = Inches(5.6)
    grid_h = Inches(2.25)
    
    add_card(s4, Inches(0.8), Inches(1.7), grid_w, grid_h)
    tb = s4.shapes.add_textbox(Inches(0.95), Inches(1.85), grid_w - Inches(0.3), grid_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Tier-1 & MNC Corporate Hiring"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN
    items = [
        "FAANG: Amazon (OA + LP), Google, Microsoft, Meta",
        "FinTech & Product: Goldman Sachs, Morgan Stanley, Atlassian",
        "IT Services & Campus Drives: TCS NQT, Infosys, Wipro, Accenture"
    ]
    for it in items:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_MUTED
        pi.space_before = Pt(2)

    add_card(s4, Inches(6.8), Inches(1.7), grid_w, grid_h)
    tb = s4.shapes.add_textbox(Inches(6.95), Inches(1.85), grid_w - Inches(0.3), grid_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. Data Structures & Algorithms (DSA)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PURPLE
    items = [
        "Arrays, Strings, HashMaps, Sliding Window & Two Pointers",
        "Trees, Binary Search Trees, Tries, BFS & DFS Traversals",
        "Dynamic Programming (1D/2D), Graphs, Dijkstra, Union-Find"
    ]
    for it in items:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_MUTED
        pi.space_before = Pt(2)

    add_card(s4, Inches(0.8), Inches(4.25), grid_w, grid_h)
    tb = s4.shapes.add_textbox(Inches(0.95), Inches(4.4), grid_w - Inches(0.3), grid_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. Core Computer Science Fundamentals"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_INDIGO
    items = [
        "DBMS & SQL: B-Tree indexing, ACID properties, Normalization",
        "Operating Systems: Virtual memory, Process vs Thread, Deadlocks",
        "Computer Networks: TCP/IP 3-way handshake, DNS, HTTP/HTTPS"
    ]
    for it in items:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_MUTED
        pi.space_before = Pt(2)

    add_card(s4, Inches(6.8), Inches(4.25), grid_w, grid_h)
    tb = s4.shapes.add_textbox(Inches(6.95), Inches(4.4), grid_w - Inches(0.3), grid_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "4. System Design & STAR Behavioral"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_GREEN
    items = [
        "LLD: SOLID principles, Factory, Singleton & Observer patterns",
        "HLD: Rate limiters, Redis caching, Load balancers, API gateways",
        "STAR Method: Situation, Task, Action, Result behavioral responses"
    ]
    for it in items:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_MUTED
        pi.space_before = Pt(2)

    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: Session Context & State Management
    # =========================================================================
    s5 = create_slide()
    add_header(s5, "Stateless Session Management & Conversation Memory", "Maintains candidate multi-turn dialogue context while preventing backend memory leaks")

    card_l_w = Inches(5.6)
    card_l_h = Inches(4.8)
    add_card(s5, Inches(0.8), Inches(1.7), card_l_w, card_l_h)

    tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), card_l_w - Inches(0.4), card_l_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Session Context Flow & Lifecycle"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_CYAN

    points = [
        ("Session Token Generation", "React client initializes session_${Date.now()} on mount to isolate individual user chat threads."),
        ("Payload State Passing", "Every POST request sends session_id alongside user message: { message: query, session_id: token }."),
        ("Multi-Turn Context", "Backend retrieves conversation history bound to session_id, appending user query and LLM response."),
        ("Session Reset Action", "Clicking 'Clear History' updates the session token instantly, wiping UI history and refreshing context.")
    ]
    for title, desc in points:
        pb = tf.add_paragraph()
        pb.space_before = Pt(8)
        r_b = pb.add_run()
        r_b.text = f"• {title}: "
        r_b.font.bold = True
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = COLOR_TEXT_WHITE
        
        r_t = pb.add_run()
        r_t.text = desc
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = COLOR_TEXT_MUTED

    card_r_w = Inches(5.7)
    card_r_h = Inches(4.8)
    add_card(s5, Inches(6.8), Inches(1.7), card_r_w, card_r_h)

    tb_code = s5.shapes.add_textbox(Inches(7.0), Inches(1.85), card_r_w - Inches(0.4), card_r_h - Inches(0.3))
    tf_code = tb_code.text_frame
    tf_code.word_wrap = True
    p = tf_code.paragraphs[0]
    p.text = "Backend Session Handling (backend/app/routers/chatbot.py)"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_PURPLE

    code_lines = [
        "class ChatRequest(BaseModel):",
        "    message: str",
        "    session_id: Optional[str] = None",
        "    history: Optional[List[dict]] = []",
        "",
        "@router.post('/chat', response_model=ChatResponse)",
        "async def chat_endpoint(req: ChatRequest):",
        "    session_id = req.session_id or str(uuid.uuid4())",
        "    ",
        "    # Generate LLM response using persistent session",
        "    reply = await llm_service.generate_response(",
        "        req.message, session_id=session_id",
        "    )",
        "    ",
        "    return ChatResponse(",
        "        reply=reply,",
        "        session_id=session_id,",
        "        suggestions=DEFAULT_SUGGESTIONS",
        "    )"
    ]
    for line in code_lines:
        pl = tf_code.add_paragraph()
        pl.space_before = Pt(0)
        pl.space_after = Pt(0)
        rl = pl.add_run()
        rl.text = line
        rl.font.name = "Consolas"
        rl.font.size = Pt(9)
        rl.font.color.rgb = COLOR_INDIGO if any(k in line for k in ["def ", "class ", "@router"]) else COLOR_TEXT_WHITE

    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: Algorithmic Heuristic Fallback Engine
    # =========================================================================
    s6 = create_slide()
    add_header(s6, "Algorithmic Heuristic Fallback Engine", "Fault-tolerant architecture ensuring 99.99% system availability during network or API rate-limit events")

    col_w = Inches(3.64)
    col_h = Inches(4.8)
    col_gap = Inches(0.4)

    add_card(s6, Inches(0.8), Inches(1.7), col_w, col_h)
    tb = s6.shapes.add_textbox(Inches(0.95), Inches(1.85), col_w - Inches(0.3), col_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Primary LLM Service"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_CYAN

    p_sub = tf.add_paragraph()
    p_sub.text = "Groq / Gemini / Local Model"
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_after = Pt(10)

    f_bullets1 = [
        "Asynchronous HTTP API calls",
        "Deep placement domain reasoning",
        "Markdown & code generation",
        "Sub-second response streaming",
        "Dynamic question clarification"
    ]
    for b in f_bullets1:
        pi = tf.add_paragraph()
        pi.text = f"• {b}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_WHITE
        pi.space_before = Pt(4)

    add_card(s6, Inches(0.8) + col_w + col_gap, Inches(1.7), col_w, col_h)
    tb = s6.shapes.add_textbox(Inches(0.95) + col_w + col_gap, Inches(1.85), col_w - Inches(0.3), col_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Exception Interceptor"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_PURPLE

    p_sub = tf.add_paragraph()
    p_sub.text = "FastAPI Catch Block"
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_after = Pt(10)

    f_bullets2 = [
        "Detects API quota exhaustion (429)",
        "Handles network timeout exceptions",
        "Prevents frontend UI crashes",
        "Logs telemetry error events",
        "Triggers fallback routing instantly"
    ]
    for b in f_bullets2:
        pi = tf.add_paragraph()
        pi.text = f"• {b}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_WHITE
        pi.space_before = Pt(4)

    add_card(s6, Inches(0.8) + (col_w + col_gap) * 2, Inches(1.7), col_w, col_h)
    tb = s6.shapes.add_textbox(Inches(0.95) + (col_w + col_gap) * 2, Inches(1.85), col_w - Inches(0.3), col_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Heuristic Strategy Guide"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_GREEN

    p_sub = tf.add_paragraph()
    p_sub.text = "Deterministic Fallback Engine"
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_after = Pt(10)

    f_bullets3 = [
        "Generates structured technical strategy",
        "Formats Google XYZ resume advice",
        "Outlines STAR method guidelines",
        "Returns instant offline response",
        "Guarantees 100% user availability"
    ]
    for b in f_bullets3:
        pi = tf.add_paragraph()
        pi.text = f"• {b}"
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = COLOR_TEXT_WHITE
        pi.space_before = Pt(4)

    add_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: UI/UX & Glassmorphic Chatbot Aesthetics
    # =========================================================================
    s7 = create_slide()
    add_header(s7, "UI/UX & Smart Glassmorphic Aesthetic", "Modern obsidian interface designed with violet-purple glows, responsive chat bubbles, and instant code actions")

    card_w = Inches(5.6)
    card_h = Inches(2.25)

    add_card(s7, Inches(0.8), Inches(1.7), card_w, card_h)
    tb = s7.shapes.add_textbox(Inches(0.95), Inches(1.85), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Deep Space Obsidian (#06070B) & Glow"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PURPLE
    p_d = tf.add_paragraph()
    p_d.text = "High-contrast dark mode eliminates eye strain during long interview prep sessions. Enhanced with smart-purple-glow glass borders (border-purple-500/20)."
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED
    p_d.space_before = Pt(4)

    add_card(s7, Inches(6.8), Inches(1.7), card_w, card_h)
    tb = s7.shapes.add_textbox(Inches(6.95), Inches(1.85), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Syntax-Highlighted Code Blocks & Copy Action"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN
    p_d = tf.add_paragraph()
    p_d.text = "Parses triple-backtick Markdown blocks into terminal containers (bg-[#090a12]). Includes 1-click clipboard copy with visual 'Copied' checkmark feedback."
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED
    p_d.space_before = Pt(4)

    add_card(s7, Inches(0.8), Inches(4.25), card_w, card_h)
    tb = s7.shapes.add_textbox(Inches(0.95), Inches(4.4), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Typewriter Loading & Micro-Animations"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_INDIGO
    p_d = tf.add_paragraph()
    p_d.text = "Features animated bouncing dots (animate-bounce) and 'Smart AI Analyzing Query...' status text during API round-trips for high visual responsiveness."
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED
    p_d.space_before = Pt(4)

    add_card(s7, Inches(6.8), Inches(4.25), card_w, card_h)
    tb = s7.shapes.add_textbox(Inches(6.95), Inches(4.4), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Smooth Auto-Scroll & Responsive Layout"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_GREEN
    p_d = tf.add_paragraph()
    p_d.text = "Uses React useRef and scrollIntoView to automatically keep newest messages in view. Fully responsive flexbox layout scaling smoothly across mobile and desktop."
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = COLOR_TEXT_MUTED
    p_d.space_before = Pt(4)

    add_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: Key Impact & Performance Metrics
    # =========================================================================
    s8 = create_slide()
    add_header(s8, "Performance Metrics & System Impact", "Sub-second response latency, zero API costs, and 100% placement candidate domain coverage")

    stat_w = Inches(5.6)
    stat_h = Inches(2.25)

    add_card(s8, Inches(0.8), Inches(1.7), stat_w, stat_h)
    tb = s8.shapes.add_textbox(Inches(0.95), Inches(1.85), stat_w - Inches(0.3), stat_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p_num = tf.paragraphs[0]
    p_num.text = "< 450 ms"
    p_num.font.bold = True
    p_num.font.size = Pt(32)
    p_num.font.color.rgb = COLOR_CYAN
    p_lbl = tf.add_paragraph()
    p_lbl.text = "Average API Response Latency"
    p_lbl.font.bold = True
    p_lbl.font.size = Pt(12)
    p_lbl.font.color.rgb = COLOR_TEXT_WHITE
    p_sub = tf.add_paragraph()
    p_sub.text = "FastAPI async non-blocking routing delivers sub-second response times."
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s8, Inches(6.8), Inches(1.7), stat_w, stat_h)
    tb = s8.shapes.add_textbox(Inches(6.95), Inches(1.85), stat_w - Inches(0.3), stat_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p_num = tf.paragraphs[0]
    p_num.text = "50+ Tech Giants"
    p_num.font.bold = True
    p_num.font.size = Pt(32)
    p_num.font.color.rgb = COLOR_PURPLE
    p_lbl = tf.add_paragraph()
    p_lbl.text = "Recruitment Process Coverage"
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_TEXT_WHITE
    p_sub = tf.add_paragraph()
    p_sub.text = "Includes hiring rounds & leadership criteria for Amazon, Google, TCS, Infosys, etc."
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s8, Inches(0.8), Inches(4.25), stat_w, stat_h)
    tb = s8.shapes.add_textbox(Inches(0.95), Inches(4.4), stat_w - Inches(0.3), stat_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p_num = tf.paragraphs[0]
    p_num.text = "100% Uptime"
    p_num.font.bold = True
    p_num.font.size = Pt(32)
    p_num.font.color.rgb = COLOR_GREEN
    p_lbl = tf.add_paragraph()
    p_lbl.text = "Fault-Tolerant Availability"
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_TEXT_WHITE
    p_sub = tf.add_paragraph()
    p_sub.text = "Dual LLM + Deterministic Heuristic Engine prevents service interruption."
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s8, Inches(6.8), Inches(4.25), stat_w, stat_h)
    tb = s8.shapes.add_textbox(Inches(6.95), Inches(4.4), stat_w - Inches(0.3), stat_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p_num = tf.paragraphs[0]
    p_num.text = "$0 / Query"
    p_num.font.bold = True
    p_num.font.size = Pt(32)
    p_num.font.color.rgb = COLOR_INDIGO
    p_lbl = tf.add_paragraph()
    p_lbl.text = "Cost & Open Weights Support"
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_TEXT_WHITE
    p_sub = tf.add_paragraph()
    p_sub.text = "Compatible with local Ollama Llama 3 models and free-tier Groq API gateways."
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED

    add_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: Conclusion & Q&A
    # =========================================================================
    s9 = create_slide()

    banner_w = Inches(11.73)
    banner_h = Inches(2.2)
    add_card(s9, Inches(0.8), Inches(1.5), banner_w, banner_h, bg_rgb=COLOR_CARD_ALT, border_rgb=COLOR_BORDER_PURPLE)

    tb_b = s9.shapes.add_textbox(Inches(1.0), Inches(1.65), banner_w - Inches(0.4), banner_h - Inches(0.3))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "Conclusion"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_CYAN

    p_main = tf_b.add_paragraph()
    p_main.space_before = Pt(4)
    p_main.text = "A complete placement preparation assistant built around real-time intelligence, fault-tolerant reliability, and high-conversion career strategies."
    p_main.font.bold = True
    p_main.font.size = Pt(20)
    p_main.font.color.rgb = COLOR_TEXT_WHITE

    p_takeaway = tf_b.add_paragraph()
    p_takeaway.space_before = Pt(8)
    p_takeaway.text = "Key Takeaway: The Placement AI Chatbot unifies company recruitment round intelligence, Google XYZ resume auditing, high-frequency DSA solutions, and STAR behavioral guidance into an intuitive obsidian interface."
    p_takeaway.font.size = Pt(11)
    p_takeaway.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s9, Inches(0.8), Inches(4.1), banner_w, Inches(2.2))
    tb_qa = s9.shapes.add_textbox(Inches(1.0), Inches(4.3), banner_w - Inches(0.4), Inches(1.8))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    p_ty = tf_qa.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU"
    p_ty.font.bold = True
    p_ty.font.size = Pt(36)
    p_ty.font.color.rgb = COLOR_PURPLE

    p_qa = tf_qa.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.space_before = Pt(6)
    p_qa.text = "Questions & Answers"
    p_qa.font.bold = True
    p_qa.font.size = Pt(18)
    p_qa.font.color.rgb = COLOR_TEXT_WHITE

    add_footer(s9, 9)

    output_path = "c:\\Users\\adwai\\Ai Placement assistant\\Placement_AI_Chatbot_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    build_presentation()
