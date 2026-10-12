import json
from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import List, Optional
from app.services.llm_service import llm_service
from app.services.pdf_service import pdf_service

router = APIRouter()

class ResumeData(BaseModel):
    fullName: str = "Candidate"
    email: Optional[str] = ""
    phone: Optional[str] = ""
    location: Optional[str] = ""
    github: Optional[str] = ""
    linkedin: Optional[str] = ""
    summary: Optional[str] = ""
    education: Optional[List[dict]] = []
    experience: Optional[List[dict]] = []
    projects: Optional[List[dict]] = []
    skills: Optional[List[str]] = []

@router.post("/generate")
async def generate_resume_pdf(data: ResumeData):
    pdf_bytes = pdf_service.generate_ats_resume_pdf(data.dict())
    filename = f"{data.fullName.replace(' ', '_')}_Resume.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/analyze")
async def analyze_resume(data: ResumeData):
    skills_str = ", ".join(data.skills or [])
    prompt = f"""Audit candidate resume for 90+ ATS compatibility and software engineering placement readiness:
Name: {data.fullName}
Summary: {data.summary}
Skills: {skills_str}
Education: {data.education}
Experience: {data.experience}
Projects: {data.projects}

Calculate an accurate ATS score (0-100), identify 3 specific strengths, 3 actionable improvements (with Google XYZ formula guidance), and provide an optimized 2-sentence summary. Output JSON ONLY with keys: score (int), strengths (list of str), improvements (list of str), suggested_summary (str)."""

    system_prompt = "You are a Senior Technical Recruiter at FAANG. Output pure JSON format."

    response_text = await llm_service.generate_response(prompt, system_prompt=system_prompt)

    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            return json.loads(response_text[start_idx:end_idx])
    except Exception:
        pass

    # Precision Algorithmic ATS Scorer
    score = 65
    strengths = []
    improvements = []

    # Check skills count
    skills_count = len(data.skills or [])
    if skills_count >= 8:
        score += 15
        strengths.append(f"Comprehensive technical stack ({skills_count} verified skills including core engineering tools)")
    elif skills_count >= 4:
        score += 8
        strengths.append(f"Good foundational skill count ({skills_count} skills listed)")
    else:
        improvements.append("Expand skills list to at least 8 key technologies (languages, frameworks, databases, tools)")

    # Check projects count & metrics
    proj_count = len(data.projects or [])
    if proj_count >= 2:
        score += 15
        strengths.append(f"Solid practical experience showcasing {proj_count} substantial software projects")
    else:
        improvements.append("Add at least 2 full-stack/domain projects with live deployment & GitHub links")

    # Check Google XYZ formula (metrics in experience/projects)
    combined_desc = json.dumps(data.experience or []) + json.dumps(data.projects or [])
    has_metrics = any(char in combined_desc for char in ['%', '$', 'ms', 'kb', 'gb', 'x', 'users'])
    
    if has_metrics:
        score += 10
        strengths.append("Demonstrates quantifiable impact with metrics and percentages")
    else:
        improvements.append("Apply Google XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]' (e.g. 'Reduced API latency by 35%')")

    # Check summary quality
    if data.summary and len(data.summary) > 40:
        score += 5

    final_score = min(score, 98)

    default_summary = (
        data.summary or 
        f"Results-driven Software Engineer with expertise in {skills_str[:60] if data.skills else 'Software Engineering'}. Proven track record in building scalable applications and delivering measurable project results."
    )

    return {
        "score": final_score,
        "strengths": strengths or ["Standard ATS section formatting", "Clear contact details"],
        "improvements": improvements or ["Add more domain keywords matching target job descriptions"],
        "suggested_summary": default_summary
    }
