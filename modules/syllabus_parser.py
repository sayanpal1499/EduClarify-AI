import re
from modules.gemini_client import call_gemini


SYLLABUS_PARSE_PROMPT = """
You are a syllabus analysis AI. Given the following syllabus text, break it down into structured modules/chapters.

Rules:
- Identify ALL distinct modules, units, or chapters from the syllabus.
- If the syllabus already has pre-defined modules/units, use those exact names.
- If there are no pre-defined modules, intelligently group related topics into logical modules.
- For EACH module, list ALL sub-topics within it.
- Estimate a marks weightage percentage for each module (must total 100%).
- Rate each module's importance as: HIGH, MEDIUM, or LOW.
- Suggest a study order (1 = study first).
- Indicate if a module can be skipped (only LOW importance ones).

Respond ONLY in this exact format:

##MODULE_1##
Name: [Module Name]
Topics: [Topic 1], [Topic 2], [Topic 3]
Weightage: [X]%
Importance: [HIGH/MEDIUM/LOW]
Study Order: [number]
Skippable: [Yes/No]
Estimated Hours: [X]

##MODULE_2##
[repeat format]

##MODULE_3##
[repeat format]

(continue for all modules)

##STUDY_STRATEGY##
Provide a brief 4-5 bullet study strategy for covering this syllabus efficiently.
Use emojis and bold text for key advice.
"""


def parse_syllabus(syllabus_text: str) -> dict:
    """Send syllabus text to AI and return structured module breakdown."""
    prompt = f"""{SYLLABUS_PARSE_PROMPT}

Syllabus text:
{syllabus_text}
"""
    raw = call_gemini(prompt)
    if raw.startswith("ERROR:"):
        return {"error": raw, "modules": [], "strategy": ""}
    return _parse_modules_response(raw)


def _parse_modules_response(raw: str) -> dict:
    """Parse the AI response into structured module data."""
    modules = []
    # Find all MODULE blocks
    module_blocks = re.findall(
        r'##MODULE_\d+##\s*(.*?)(?=##MODULE_\d+##|##STUDY_STRATEGY##|$)',
        raw, re.DOTALL
    )
    
    for i, block in enumerate(module_blocks):
        module = {
            "id": i + 1,
            "name": "",
            "topics": [],
            "weightage": 0,
            "importance": "MEDIUM",
            "study_order": i + 1,
            "skippable": False,
            "estimated_hours": 0,
            "completed_topics": [],
            "deadline": None,
            "status": "pending"  # pending, in_progress, completed
        }
        for line in block.strip().splitlines():
            line = line.strip()
            if line.startswith("Name:"):
                module["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Topics:"):
                topics_str = line.split(":", 1)[1].strip()
                module["topics"] = [t.strip() for t in topics_str.split(",") if t.strip()]
            elif line.startswith("Weightage:"):
                try:
                    module["weightage"] = int(re.search(r'\d+', line).group())
                except (AttributeError, ValueError):
                    module["weightage"] = 0
            elif line.startswith("Importance:"):
                imp = line.split(":", 1)[1].strip().upper()
                if imp in ("HIGH", "MEDIUM", "LOW"):
                    module["importance"] = imp
            elif line.startswith("Study Order:"):
                try:
                    module["study_order"] = int(re.search(r'\d+', line).group())
                except (AttributeError, ValueError):
                    pass
            elif line.startswith("Skippable:"):
                module["skippable"] = "yes" in line.lower()
            elif line.startswith("Estimated Hours:"):
                try:
                    module["estimated_hours"] = int(re.search(r'\d+', line).group())
                except (AttributeError, ValueError):
                    pass
        if module["name"]:
            modules.append(module)
    
    # Parse study strategy
    strategy_match = re.search(r'##STUDY_STRATEGY##\s*(.*)', raw, re.DOTALL)
    strategy = strategy_match.group(1).strip() if strategy_match else ""
    
    # Sort by study order
    modules.sort(key=lambda m: m["study_order"])
    
    return {"modules": modules, "strategy": strategy, "error": None}


def generate_revision_notes(topic: str, weak_areas: list = None) -> str:
    """Generate targeted revision notes for a module or weak topics."""
    weak_text = ""
    if weak_areas:
        weak_text = f"\nThe student specifically struggled with: {', '.join(weak_areas)}. Focus extra on these."
    
    prompt = f"""You are a study revision assistant. Generate comprehensive, well-structured revision notes for:

Topic: {topic}
{weak_text}

Rules:
- Use markdown formatting with headers (##), bold (**), and bullet points.
- Include key definitions, important formulas, diagrams described in text, and exam tips.
- Use emojis to make the notes visually engaging.
- Structure the notes so they can be used for quick last-minute revision.
- Keep it concise but comprehensive (aim for 500-800 words).
- Include a "🎯 Key Takeaways" section at the end with 3-5 bullet points.
- Include a "⚠️ Common Mistakes" section highlighting what students typically get wrong.
"""
    return call_gemini(prompt)
