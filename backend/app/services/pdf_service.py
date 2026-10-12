import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFService:
    @staticmethod
    def generate_ats_resume_pdf(data: dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom ATS Typography Styles
        name_style = ParagraphStyle(
            'ATS_Name',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            alignment=1, # Center
            textColor=colors.HexColor("#0F172A")
        )

        contact_style = ParagraphStyle(
            'ATS_Contact',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            alignment=1, # Center
            textColor=colors.HexColor("#334155")
        )

        heading_style = ParagraphStyle(
            'ATS_Heading',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=8,
            spaceAfter=3,
            textTransform='uppercase'
        )

        body_style = ParagraphStyle(
            'ATS_Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1E293B")
        )

        bold_sub_style = ParagraphStyle(
            'ATS_BoldSub',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0F172A")
        )

        bullet_style = ParagraphStyle(
            'ATS_Bullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            leftIndent=12,
            textColor=colors.HexColor("#334155")
        )

        story = []

        # Header Name
        full_name = data.get("fullName", "CANDIDATE NAME").upper()
        story.append(Paragraph(full_name, name_style))
        story.append(Spacer(1, 4))

        # Contact Info
        contacts = []
        if data.get("email"): contacts.append(data["email"])
        if data.get("phone"): contacts.append(data["phone"])
        if data.get("location"): contacts.append(data["location"])
        if data.get("linkedin"): contacts.append(data["linkedin"])
        if data.get("github"): contacts.append(data["github"])

        contact_line = " | ".join(contacts)
        story.append(Paragraph(contact_line, contact_style))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=8))

        # Professional Summary
        if data.get("summary"):
            story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            story.append(Paragraph(data["summary"], body_style))
            story.append(Spacer(1, 8))

        # Education
        education = data.get("education", [])
        if education:
            story.append(Paragraph("EDUCATION", heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=4))
            for edu in education:
                inst = edu.get("institution", "")
                deg = edu.get("degree", "")
                yr = edu.get("year", "")
                score = edu.get("score", "")
                line = f"<b>{inst}</b> — {deg} ({yr}) {f'| {score}' if score else ''}"
                story.append(Paragraph(line, body_style))
            story.append(Spacer(1, 8))

        # Work Experience
        experience = data.get("experience", [])
        if experience:
            story.append(Paragraph("WORK EXPERIENCE", heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=4))
            for exp in experience:
                role = exp.get("role", "")
                comp = exp.get("company", "")
                dur = exp.get("duration", "")
                story.append(Paragraph(f"<b>{role}</b> at <b>{comp}</b> ({dur})", bold_sub_style))
                details = exp.get("details", "").split('\n')
                for d in details:
                    if d.strip():
                        story.append(Paragraph(f"• {d.strip()}", bullet_style))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 4))

        # Projects
        projects = data.get("projects", [])
        if projects:
            story.append(Paragraph("KEY PROJECTS", heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=4))
            for proj in projects:
                title = proj.get("title", "")
                tech = proj.get("tech", "")
                link = proj.get("link", "")
                story.append(Paragraph(f"<b>{title}</b> | <i>{tech}</i> {f'({link})' if link else ''}", bold_sub_style))
                desc_lines = proj.get("description", "").split('\n')
                for dl in desc_lines:
                    if dl.strip():
                        story.append(Paragraph(f"• {dl.strip()}", bullet_style))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 4))

        # Technical Skills
        skills = data.get("skills", [])
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=4))
            skills_text = " • ".join(skills)
            story.append(Paragraph(skills_text, body_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

pdf_service = PDFService()
