import io
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, ListFlowable, ListItem, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _clean_markdown(text: str) -> str:
    """Convert markdown to ReportLab-compatible HTML and strip emojis."""
    if not text:
        return ""
    # Remove emojis (ReportLab can't render them)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    # Convert markdown bold to HTML bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Convert markdown italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Clean up bullet characters
    text = text.replace("•", "-")
    return text.strip()


def _split_into_paragraphs(text: str) -> list:
    """Split text into paragraph blocks for better PDF formatting."""
    lines = text.split("\n")
    paragraphs = []
    current = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("\n".join(current))
                current = []
        else:
            current.append(stripped)
    if current:
        paragraphs.append("\n".join(current))
    return paragraphs


# ---------------------------------------------------------------------------
# Shared style factory
# ---------------------------------------------------------------------------

def _get_styles():
    """Return a dict of custom ParagraphStyles used across all PDF types."""
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "CustomTitle", parent=base["Title"],
        fontSize=22, textColor=colors.HexColor("#4f46e5"),
        spaceAfter=8, fontName="Helvetica-Bold"
    )
    subtitle = ParagraphStyle(
        "CustomSubtitle", parent=base["Heading2"],
        fontSize=12, textColor=colors.HexColor("#64748b"),
        spaceAfter=10, fontName="Helvetica"
    )
    h2 = ParagraphStyle(
        "CustomH2", parent=base["Heading2"],
        fontSize=14, textColor=colors.HexColor("#6366f1"),
        spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold"
    )
    h3 = ParagraphStyle(
        "CustomH3", parent=base["Heading3"],
        fontSize=12, textColor=colors.HexColor("#4338ca"),
        spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold"
    )
    body = ParagraphStyle(
        "CustomBody", parent=base["Normal"],
        fontSize=10.5, leading=16, spaceAfter=6,
        fontName="Helvetica"
    )
    bullet = ParagraphStyle(
        "CustomBullet", parent=base["Normal"],
        fontSize=10.5, leading=16, spaceAfter=4,
        leftIndent=20, bulletIndent=8,
        fontName="Helvetica"
    )
    score = ParagraphStyle(
        "ScoreStyle", parent=base["Normal"],
        fontSize=12, textColor=colors.HexColor("#059669"),
        spaceAfter=6, fontName="Helvetica-Bold"
    )
    footer = ParagraphStyle(
        "CustomFooter", parent=base["Normal"],
        fontSize=8, textColor=colors.grey, fontName="Helvetica"
    )
    correct_style = ParagraphStyle(
        "CorrectOption", parent=base["Normal"],
        fontSize=10, leading=14, fontName="Helvetica",
        textColor=colors.HexColor("#059669")
    )
    wrong_style = ParagraphStyle(
        "WrongOption", parent=base["Normal"],
        fontSize=10, leading=14, fontName="Helvetica",
        textColor=colors.HexColor("#dc2626")
    )
    option_style = ParagraphStyle(
        "OptionStyle", parent=base["Normal"],
        fontSize=10, leading=14, fontName="Helvetica",
        textColor=colors.HexColor("#374151")
    )

    return {
        "base": base,
        "title": title,
        "subtitle": subtitle,
        "h2": h2,
        "h3": h3,
        "body": body,
        "bullet": bullet,
        "score": score,
        "footer": footer,
        "correct": correct_style,
        "wrong": wrong_style,
        "option": option_style,
    }


def _build_doc(buffer):
    """Create a SimpleDocTemplate with standard margins."""
    return SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm
    )


def _add_section_content(story, content: str, styles: dict):
    """Render cleaned markdown content as body paragraphs / bullet lists."""
    cleaned = _clean_markdown(content)
    paragraphs = _split_into_paragraphs(cleaned)
    for para in paragraphs:
        bullet_lines = [
            l for l in para.split("\n") if l.strip().startswith(("-", "*"))
        ]
        if bullet_lines:
            for bl in bullet_lines:
                bl_text = re.sub(r'^[-*]\s*', '', bl.strip())
                story.append(Paragraph(f"  - {bl_text}", styles["bullet"]))
        else:
            story.append(
                Paragraph(para.replace("\n", "<br/>"), styles["body"])
            )
    story.append(Spacer(1, 6))


def _add_footer(story, styles: dict):
    """Append a standard footer to the story."""
    story.append(Spacer(1, 10))
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey)
    )
    story.append(Paragraph("Generated by EduClarify AI", styles["footer"]))


def _hr(color_hex: str = "#6366f1", thickness: float = 1.5):
    """Return a styled horizontal rule."""
    return HRFlowable(
        width="100%", thickness=thickness,
        color=colors.HexColor(color_hex)
    )


# ---------------------------------------------------------------------------
# 1. Learning PDF  (Learn tab)
# ---------------------------------------------------------------------------

def generate_learning_pdf(topic: str, parsed: dict) -> bytes:
    """Generate an A4 PDF with learning explanations, prerequisites,
    and learning roadmap.  No quiz score is included.

    Parameters
    ----------
    topic : str
        The topic that was studied.
    parsed : dict
        Keys used: eli5, conceptual, expert, prerequisites, concept_graph.

    Returns
    -------
    bytes
        PDF file contents suitable for ``st.download_button``.
    """
    buffer = io.BytesIO()
    doc = _build_doc(buffer)
    s = _get_styles()
    story = []

    # Header
    story.append(Paragraph("EduClarify AI - Learning Summary", s["title"]))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(f"<b>Topic:</b> {_clean_markdown(topic)}", s["body"])
    )
    story.append(_hr())
    story.append(Spacer(1, 8))

    # Content sections
    sections = [
        ("Beginner (ELI5) Explanation", parsed.get("eli5", "")),
        ("Conceptual Explanation", parsed.get("conceptual", "")),
        ("Expert Explanation", parsed.get("expert", "")),
        ("Prerequisites", parsed.get("prerequisites", "")),
        ("Learning Roadmap", parsed.get("concept_graph", "")),
    ]
    for heading, content in sections:
        if content:
            story.append(Paragraph(heading, s["h2"]))
            _add_section_content(story, content, s)

    _add_footer(story, s)
    doc.build(story)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# 2. Revision PDF  (Study Planner)
# ---------------------------------------------------------------------------

def generate_revision_pdf(modules_data: list) -> bytes:
    """Generate an A4 PDF organised by modules for revision.

    Parameters
    ----------
    modules_data : list[dict]
        Each dict has:
        - ``module_name`` (str): display name for the module heading.
        - ``topics`` (list[str]): topics covered in that module.
        - ``notes`` (str): revision notes text.

    Returns
    -------
    bytes
        PDF file contents.
    """
    buffer = io.BytesIO()
    doc = _build_doc(buffer)
    s = _get_styles()
    story = []

    # Header
    story.append(Paragraph("EduClarify AI - Revision Notes", s["title"]))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            f"<b>Modules covered:</b> {len(modules_data)}",
            s["body"]
        )
    )
    story.append(_hr())
    story.append(Spacer(1, 8))

    for idx, module in enumerate(modules_data, start=1):
        module_name = module.get("module_name", f"Module {idx}")
        topics = module.get("topics", [])
        notes = module.get("notes", "")

        # Module heading
        story.append(Paragraph(f"{module_name}", s["h2"]))

        # Topics list
        if topics:
            story.append(Paragraph("<b>Topics</b>", s["h3"]))
            for t in topics:
                cleaned_topic = _clean_markdown(str(t))
                story.append(
                    Paragraph(f"  - {cleaned_topic}", s["bullet"])
                )
            story.append(Spacer(1, 4))

        # Revision notes
        if notes:
            story.append(Paragraph("<b>Revision Notes</b>", s["h3"]))
            _add_section_content(story, notes, s)

        # Separator between modules (except after the last one)
        if idx < len(modules_data):
            story.append(Spacer(1, 4))
            story.append(
                _hr(color_hex="#e2e8f0", thickness=0.75)
            )
            story.append(Spacer(1, 4))

    _add_footer(story, s)
    doc.build(story)
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# 3. Quiz Report PDF  (Quiz section)
# ---------------------------------------------------------------------------

def generate_quiz_report_pdf(
    topic: str,
    mcqs: list,
    user_answers: list,
    score: int,
    total: int,
    pct: float,
    analytics_data: dict,
) -> bytes:
    """Generate a detailed quiz report PDF.

    Parameters
    ----------
    topic : str
        The quiz topic.
    mcqs : list[dict]
        Each dict has ``question`` (str) and ``options`` (list[str])
        and ``answer`` (str — the correct answer text).
    user_answers : list
        User-selected answers (same length as *mcqs*).
    score : int
        Number of correct answers.
    total : int
        Total number of questions.
    pct : float
        Percentage score (0-100).
    analytics_data : dict
        Keys used: ``total_sessions``, ``avg_score``, ``active_days``.

    Returns
    -------
    bytes
        PDF file contents.
    """
    buffer = io.BytesIO()
    doc = _build_doc(buffer)
    s = _get_styles()
    story = []

    # Header
    story.append(Paragraph("EduClarify AI - Quiz Report", s["title"]))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(f"<b>Topic:</b> {_clean_markdown(topic)}", s["body"])
    )
    story.append(
        Paragraph(f"<b>Total Questions:</b> {total}", s["body"])
    )
    story.append(_hr())
    story.append(Spacer(1, 10))

    # --- Questions ---
    for i, mcq in enumerate(mcqs):
        q_text = _clean_markdown(mcq.get("question", ""))
        options_dict = mcq.get("options", {})
        correct_ans_key = str(mcq.get("answer", "")).strip()
        # user_answers could be dict or list depending on how it was passed
        if isinstance(user_answers, dict):
            user_ans_key = str(user_answers.get(i, "")).strip()
        else:
            user_ans_key = str(user_answers[i]).strip() if i < len(user_answers) else ""
            
        explanation = _clean_markdown(str(mcq.get("explanation", "")))

        # Question heading
        story.append(
            Paragraph(f"<b>Q{i + 1}.</b> {q_text}", s["h3"])
        )

        # Options
        if isinstance(options_dict, dict):
            for key, text in options_dict.items():
                opt_str = f"{key}) {_clean_markdown(str(text))}"
                is_user = (key == user_ans_key)
                is_correct = (key == correct_ans_key)

                if is_user and is_correct:
                    label = f">> {opt_str}  (Your answer - Correct)"
                    style = s["correct"]
                elif is_user and not is_correct:
                    label = f">> {opt_str}  (Your answer)"
                    style = s["wrong"]
                elif is_correct:
                    label = f"   {opt_str}  (Correct answer)"
                    style = s["correct"]
                else:
                    label = f"   {opt_str}"
                    style = s["option"]

                story.append(Paragraph(label, style))
        else:
            # Fallback if options is somehow a list
            for opt in options_dict:
                story.append(Paragraph(f"   {_clean_markdown(str(opt))}", s["option"]))

        if user_ans_key != correct_ans_key and explanation:
            story.append(Spacer(1, 4))
            story.append(Paragraph(f"<b>Explanation:</b> {explanation}", s["body"]))

        story.append(Spacer(1, 8))

    # --- Score Summary ---
    story.append(_hr())
    story.append(Spacer(1, 6))
    story.append(Paragraph("Score Summary", s["h2"]))

    score_color = "#059669" if pct >= 60 else "#dc2626"
    score_display = ParagraphStyle(
        "ScoreDisplay", parent=s["base"]["Normal"],
        fontSize=16, fontName="Helvetica-Bold",
        textColor=colors.HexColor(score_color),
        spaceAfter=6
    )
    story.append(
        Paragraph(f"{score} / {total}  ({pct:.0f}%)", score_display)
    )

    if pct >= 80:
        remark = "Excellent work!"
    elif pct >= 60:
        remark = "Good job - keep practising!"
    elif pct >= 40:
        remark = "Fair attempt - review the topic and try again."
    else:
        remark = "Needs improvement - revisit the learning material."
    story.append(Paragraph(remark, s["body"]))
    story.append(Spacer(1, 10))

    # --- Analytics Summary ---
    if analytics_data:
        story.append(Paragraph("Analytics Overview", s["h2"]))

        analytics_table_data = [["Metric", "Value"]]
        for key, val in analytics_data.items():
            analytics_table_data.append([str(key), str(val)])

        table = Table(analytics_table_data, colWidths=[200, 150])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366f1")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f8fafc")]),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ]))
        story.append(table)

    _add_footer(story, s)
    doc.build(story)
    return buffer.getvalue()
