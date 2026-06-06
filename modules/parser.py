import re


def parse_response(raw: str) -> dict:
    """Parse tagged LLM response into structured dict."""

    def extract(tag: str) -> str:
        pattern = rf"##{tag}##\s*(.*?)(?=##[A-Z_]+##|$)"
        match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def parse_mcqs(block: str) -> list:
        questions = []
        parts = re.split(r"\bQ\d+:", block)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            lines = [line.strip() for line in part.splitlines() if line.strip()]
            if len(lines) < 6:
                continue
            q = {
                "question": lines[0],
                "options": {},
                "answer": "",
                "explanation": ""
            }
            for line in lines[1:]:
                if re.match(r"^[ABCD]\)", line):
                    q["options"][line[0]] = line[3:].strip()
                elif line.upper().startswith("ANSWER:"):
                    q["answer"] = line.split(":", 1)[1].strip().upper()[0]
                elif line.upper().startswith("EXPLANATION:"):
                    q["explanation"] = line.split(":", 1)[1].strip()
            if q["question"] and len(q["options"]) == 4 and q["answer"]:
                questions.append(q)
        return questions

    return {
        "eli5":          extract("ELI5"),
        "conceptual":    extract("CONCEPTUAL"),
        "expert":        extract("EXPERT"),
        "prerequisites": extract("PREREQUISITES"),
        "concept_graph": extract("CONCEPT_GRAPH"),
        "mcqs":          parse_mcqs(extract("MCQ"))
    }
