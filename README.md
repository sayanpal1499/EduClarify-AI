# EduClarify AI 🎓
### An AI-Powered Adaptive Micro-Learning & Concept Clarity Agent

> **ESD Spring 2025–26 | SDG 4: Quality Education**
> Team: CodeVeda

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Our Solution](#2-our-solution)
3. [What Makes It Unique](#3-what-makes-it-unique)
4. [Complete Feature Set](#4-complete-feature-set)
5. [App Architecture](#5-app-architecture)
6. [Database Schema (Supabase)](#6-database-schema-supabase)
7. [Tech Stack](#7-tech-stack)
8. [File Structure](#8-file-structure)
9. [Step-by-Step Build Instructions](#9-step-by-step-build-instructions)
10. [System Prompt Engineering](#10-system-prompt-engineering)
11. [Deployment Guide](#11-deployment-guide)
12. [Testing Checklist](#12-testing-checklist)
13. [SDG Alignment](#13-sdg-alignment)

---

## 1. Problem Statement

Students across schools, colleges, and competitive exams face a persistent challenge:
**academic content is dense, jargon-heavy, and poorly structured for independent self-learning.**
Textbook chapters, university syllabi, and research papers are written for information density —
not comprehension.

The downstream effects are severe:

- Students memorize without understanding, leading to poor performance in applied or viva-style assessments.
- Under exam pressure, learners resort to passive reading of summaries with zero retention testing.
- No personalized feedback loop exists — a student does not know *which* concepts they are weak in until the exam itself.
- Progress made one day is forgotten the next because no tool tracks cross-session learning history.
- Existing tools (ChatGPT, Google, Wikipedia) provide raw information but offer no structured learning pathway, self-assessment, or retention scheduling.

**The result:** A generation of students who can locate information but cannot deeply understand,
retain, or apply it across time.

---

## 2. Our Solution

**EduClarify AI** is a web-based AI learning agent that transforms any raw academic text —
a syllabus module, a textbook paragraph, or just a topic name — into a complete, personalized
micro-learning session. It is the only tool that combines explanation, self-assessment, spaced
repetition, and cross-session progress tracking in a single zero-installation browser app.

A student enters their username once. The agent then:

1. **Simplifies** content across three adaptive explanation layers (ELI5, Conceptual, Expert).
2. **Maps prerequisites** — tells the student what foundational concepts to understand first.
3. **Generates an interactive quiz** (MCQs) with instant feedback and auto-calibrating difficulty.
4. **Builds a concept dependency graph** showing how sub-topics relate to each other.
5. **Persists all progress to a cloud database** — accessible across devices, across days.
6. **Schedules spaced repetition reviews** — surfaces topics due for re-study based on the forgetting curve.
7. **Maintains a personal Topic Library** — saved explanations available as revision notes anytime.
8. **Tracks daily study goals** and study streaks for habit formation.
9. **Allows feedback on explanations** with one-click regeneration if unclear.
10. **Exports any session** as a downloadable PDF for offline revision.

---

## 3. What Makes It Unique

| Feature | EduClarify AI | ChatGPT | Quizlet | Notion AI | Khan Academy |
|---|---|---|---|---|---|
| 3-layer adaptive explanation depth | ✅ | ❌ | ❌ | ❌ | Partial |
| Prerequisite concept mapper | ✅ | ❌ | ❌ | ❌ | ❌ |
| Concept dependency graph | ✅ | ❌ | ❌ | ❌ | ❌ |
| Syllabus PDF → instant quiz | ✅ | ❌ | ❌ | ❌ | ❌ |
| Spaced repetition scheduling | ✅ | ❌ | ✅ | ❌ | ❌ |
| Cross-device persistent analytics | ✅ | ❌ | Partial | ❌ | ✅ |
| Auto difficulty calibration from scores | ✅ | ❌ | ❌ | ❌ | Partial |
| Explanation feedback + AI regeneration | ✅ | ❌ | ❌ | ❌ | ❌ |
| Personal topic library / notes bank | ✅ | ❌ | ✅ | ✅ | ❌ |
| Session PDF export for offline revision | ✅ | ❌ | ❌ | Partial | ❌ |
| Zero installation, fully browser-based | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 4. Complete Feature Set

### Core Learning Engine
- **3-Layer Explanations:** ELI5 (analogy-driven) → Conceptual (mechanism-focused) → Expert (technical depth). All three generated in one API call.
- **Prerequisite Mapper:** Lists 3–5 foundational concepts the student must understand before this topic.
- **Concept Dependency Graph:** Text-based tree showing how sub-concepts within the topic connect and sequence.
- **PDF Syllabus Upload:** Upload any PDF; text is extracted and fed directly into the learning pipeline.

### Adaptive Intelligence
- **Auto Difficulty Calibration:** After each quiz, the system adjusts the recommended explanation depth for the next topic. Score ≥ 85% → bumps difficulty up one level. Score < 50% → softens to a simpler level. Stored per-user in the database.
- **Explanation Feedback Loop:** Thumbs up / thumbs down on each explanation layer. On thumbs-down, a "Regenerate" button fires a new API call with an instruction to try a different approach.

### Retention & Progress System
- **Supabase Cloud Persistence:** All quiz results, saved topics, and user preferences written to a Postgres database. Accessible from any device, any browser.
- **Spaced Repetition Scheduler:** Topics are tagged with `last_studied` and `review_count`. The dashboard surfaces a "Due for Review" list — topics not revisited in 3+ days where the last score was under 80%.
- **Personal Topic Library:** "Save to Library" button on the Explanation tab stores the full explanation (all three layers + prerequisites) to the database. Student can browse and re-read saved topics anytime without re-running the AI.
- **Study Streak Counter:** Tracks consecutive days on which the student completed at least one quiz. Displayed prominently in the sidebar.

### Analytics Dashboard
- Sessions completed (lifetime)
- Average quiz score (lifetime and last 7 days)
- Score-by-topic bar chart (all time)
- 7-day score trend line chart
- Weak topics list (lifetime score < 60%)
- Best and worst performing topics
- Study streak and last active date
- Due-for-review topic list

### Daily Habit Features
- **Study Goal:** Student sets a daily target (1–10 topics). Progress bar in sidebar shows today's completion.
- **Session PDF Export:** "Download Session Summary" button generates a clean A4 PDF containing the topic, all three explanations, concept graph, prerequisites, and quiz results. No extra AI call needed.

---

## 5. App Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                               │
│                                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │ Input Panel │  │ Explanation  │  │  Quiz Tab   │  │ Analytics │ │
│  │ (Text/PDF)  │  │    Tabs      │  │  + Results  │  │ Dashboard │ │
│  └──────┬──────┘  └──────▲───────┘  └──────▲──────┘  └─────▲─────┘ │
│         │                │                  │               │        │
│         └────────────────┴──────────────────┴───────────────┘        │
│                                    │                                  │
│                        ┌───────────▼────────────┐                    │
│                        │     app.py             │                    │
│                        │  (Streamlit Router)    │                    │
│                        └───────────┬────────────┘                    │
│                                    │                                  │
│          ┌─────────────────────────┼──────────────────────┐          │
│          │                         │                      │          │
│  ┌───────▼────────┐    ┌───────────▼──────────┐  ┌───────▼───────┐ │
│  │  gemini_       │    │     database.py       │  │  pdf_export   │ │
│  │  client.py     │    │  (Supabase R/W)       │  │  .py          │ │
│  └───────┬────────┘    └───────────┬──────────┘  └───────────────┘ │
│          │                         │                                  │
│  ┌───────▼────────┐                │                                  │
│  │  parser.py     │       ┌────────▼──────────┐                      │
│  └───────┬────────┘       │   Supabase        │                      │
│          │                │   (Postgres DB)   │                      │
│   ┌──────┴───────┐        └───────────────────┘                      │
│   │              │                                                    │
│   ▼              ▼                                                    │
│ quiz.py     analytics.py                                              │
│ library.py  spaced_rep.py                                             │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Student enters username
        │
        ▼
[Auth Check] ── username stored in localStorage via st.query_params
        │
        ├── Load: difficulty_level, study_goal, streak from DB
        └── Load: due_for_review topics from DB
                │
                ▼
        ┌───────────────┐
        │  Topic Input  │ ←── text paste  OR  PDF upload → pdf_reader.py
        └───────┬───────┘
                │
                ▼
        [prompt_builder.py] ── injects: text + difficulty + output schema
                │
                ▼
        [gemini_client.py] ── Gemini 1.5 Flash API call
                │
                ▼
        [parser.py] ── splits ##TAGS## into structured dict
                │
        ┌───────┴────────────────────────────────────┐
        │           │            │          │         │
        ▼           ▼            ▼          ▼         ▼
     [ELI5]  [Conceptual]  [Expert]  [Prereqs]  [Graph]
        │
        ▼
  [quiz.py] ── renders MCQs, scores, applies difficulty calibration
        │
        ▼
  [database.py] ── writes quiz_history row to Supabase
        │
        ├── updates difficulty_level if calibration triggers
        ├── updates last_studied, review_count on topic
        └── updates streak + today's topic count
                │
                ▼
        [analytics.py] ── reads from Supabase, renders charts
        [spaced_rep.py] ── queries topics due for review
        [library.py] ── read/write saved explanations
        [pdf_export.py] ── generates downloadable PDF summary
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit entry point, routing, layout, session state init, username handling |
| `modules/gemini_client.py` | Gemini API wrapper — takes prompt string, returns raw text |
| `modules/prompt_builder.py` | Builds full prompt from user input + difficulty + system schema |
| `modules/parser.py` | Regex-based parser — splits tagged LLM response into structured dict |
| `modules/quiz.py` | MCQ renderer, scoring, difficulty calibration trigger |
| `modules/analytics.py` | Full analytics dashboard — reads Supabase, renders all charts and metrics |
| `modules/database.py` | All Supabase read/write operations — single source of truth for DB calls |
| `modules/spaced_rep.py` | Computes which topics are due for review based on last_studied + score |
| `modules/library.py` | Save/load/delete topic explanations from personal library |
| `modules/pdf_reader.py` | Extracts text from uploaded PDF using PyMuPDF |
| `modules/pdf_export.py` | Generates session summary PDF using ReportLab |

---

## 6. Database Schema (Supabase)

Create these four tables in your Supabase project. Run each SQL block in the Supabase SQL Editor.

### Table 1: `users`
Stores per-user preferences and streak data.

```sql
CREATE TABLE users (
    username        TEXT PRIMARY KEY,
    difficulty_level TEXT DEFAULT 'Undergraduate',
    study_goal      INTEGER DEFAULT 3,
    streak          INTEGER DEFAULT 0,
    last_active_date DATE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### Table 2: `quiz_history`
One row per quiz submission.

```sql
CREATE TABLE quiz_history (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL REFERENCES users(username),
    topic           TEXT NOT NULL,
    score           INTEGER NOT NULL,
    total           INTEGER NOT NULL,
    pct             INTEGER NOT NULL,
    difficulty_used TEXT,
    attempted_at    TIMESTAMP DEFAULT NOW()
);
```

### Table 3: `topic_tracker`
Tracks study recency and review scheduling per topic per user.

```sql
CREATE TABLE topic_tracker (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL REFERENCES users(username),
    topic           TEXT NOT NULL,
    last_studied    TIMESTAMP DEFAULT NOW(),
    review_count    INTEGER DEFAULT 1,
    last_score_pct  INTEGER,
    UNIQUE(username, topic)
);
```

### Table 4: `library`
Stores saved explanation content per user.

```sql
CREATE TABLE library (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL REFERENCES users(username),
    topic           TEXT NOT NULL,
    eli5            TEXT,
    conceptual      TEXT,
    expert          TEXT,
    prerequisites   TEXT,
    concept_graph   TEXT,
    saved_at        TIMESTAMP DEFAULT NOW()
);
```

### Supabase Setup Steps

1. Go to https://supabase.com → "New Project"
2. Name it `educlarify`, choose a strong DB password, select nearest region
3. Go to **SQL Editor** → paste and run each CREATE TABLE block above
4. Go to **Project Settings → API**
5. Copy: `Project URL` and `anon public` key
6. These go into `.streamlit/secrets.toml` (see Phase 0 below)

> **Row Level Security:** For this project, disable RLS on all four tables (Table Editor → RLS → Disable). This simplifies the build. Do not store sensitive personal data.

---

## 7. Tech Stack

| Layer | Technology | Version | Why |
|---|---|---|---|
| UI Framework | Streamlit | ≥ 1.35.0 | Zero HTML/CSS needed, rapid Python UI |
| LLM Engine | Google Gemini 1.5 Flash | API v1 | Free tier, fast, strong structured output |
| Cloud Database | Supabase (Postgres) | Free tier | Cross-device persistence, generous limits |
| Supabase Python Client | `supabase-py` | ≥ 2.4.0 | Official Python SDK for Supabase |
| PDF Parsing (input) | PyMuPDF (`fitz`) | ≥ 1.24.0 | Lightweight, accurate text extraction |
| PDF Generation (export) | ReportLab | ≥ 4.2.0 | Programmatic A4 PDF creation in Python |
| Charts | Streamlit native + `st.line_chart` | — | No extra setup, sufficient for analytics |
| Session State | `st.session_state` + `st.query_params` | — | Username persistence within and across tabs |
| Secrets Management | Streamlit Secrets | — | Keeps API keys out of source code |
| Deployment | Streamlit Community Cloud | — | Free, instant public URL from GitHub |

### `requirements.txt`

```
streamlit>=1.35.0
google-generativeai>=0.7.0
supabase>=2.4.0
PyMuPDF>=1.24.0
reportlab>=4.2.0
```

---

## 8. File Structure

```
educlarify-ai/
│
├── app.py                        # Main Streamlit entry point
├── requirements.txt              # Python dependencies
│
├── .streamlit/
│   └── secrets.toml              # API keys — NEVER commit this file
│
├── modules/
│   ├── __init__.py               # Empty init
│   ├── gemini_client.py          # Gemini API wrapper
│   ├── prompt_builder.py         # System prompt + prompt construction
│   ├── parser.py                 # LLM response parser (regex-based)
│   ├── quiz.py                   # MCQ renderer, scoring, calibration
│   ├── analytics.py              # Analytics dashboard renderer
│   ├── database.py               # All Supabase read/write operations
│   ├── spaced_rep.py             # Spaced repetition logic
│   ├── library.py                # Topic library save/load/delete
│   ├── pdf_reader.py             # PDF input text extractor
│   └── pdf_export.py             # Session summary PDF generator
│
└── README.md
```

---

## 9. Step-by-Step Build Instructions

Build each phase in order. Each phase is independently testable before moving to the next.

---

### Phase 0 — Environment Setup

**Step 1: Get API credentials**

*Gemini API Key:*
- Go to https://aistudio.google.com
- Sign in → "Get API Key" → "Create API key in new project"
- Copy the key

*Supabase credentials:*
- Complete Supabase setup from Section 6 above
- Copy your Project URL and anon public key

**Step 2: Create project and virtual environment**
```bash
mkdir educlarify-ai && cd educlarify-ai
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install streamlit google-generativeai supabase PyMuPDF reportlab
pip freeze > requirements.txt
```

**Step 4: Create secrets file**
```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY     = "your_gemini_api_key_here"
SUPABASE_URL       = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY  = "your_supabase_anon_key_here"
```

**Step 5: Initialize Git**
```bash
git init
cat > .gitignore << 'EOF'
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
.env
EOF
git add .
git commit -m "Initial project setup"
```

Push to a new GitHub repository (create at github.com, then follow the remote add instructions shown there).

---

### Phase 1 — Database Module

Build this first. Everything else depends on it.

**Step 6: Create `modules/__init__.py`**
```python
# empty
```

**Step 7: Create `modules/database.py`**

This module handles every Supabase interaction. All other modules import from here — no other module should call Supabase directly.

```python
import streamlit as st
from supabase import create_client, Client
from datetime import date, datetime, timedelta

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )

# ── USER ─────────────────────────────────────────────────────────────

def get_or_create_user(username: str) -> dict:
    """Return user row, creating it if it doesn't exist."""
    sb = get_supabase()
    res = sb.table("users").select("*").eq("username", username).execute()
    if res.data:
        user = res.data[0]
        # Update streak
        today = date.today()
        last = user.get("last_active_date")
        if last:
            last_date = date.fromisoformat(last)
            if last_date == today:
                pass  # already active today, streak unchanged
            elif last_date == today - timedelta(days=1):
                user["streak"] += 1
                sb.table("users").update({
                    "streak": user["streak"],
                    "last_active_date": today.isoformat()
                }).eq("username", username).execute()
            else:
                user["streak"] = 1
                sb.table("users").update({
                    "streak": 1,
                    "last_active_date": today.isoformat()
                }).eq("username", username).execute()
        else:
            sb.table("users").update({
                "last_active_date": today.isoformat()
            }).eq("username", username).execute()
        return user
    else:
        new_user = {
            "username": username,
            "difficulty_level": "Undergraduate",
            "study_goal": 3,
            "streak": 1,
            "last_active_date": date.today().isoformat()
        }
        sb.table("users").insert(new_user).execute()
        return new_user

def update_user_preference(username: str, field: str, value) -> None:
    get_supabase().table("users").update({field: value}).eq("username", username).execute()

# ── QUIZ HISTORY ─────────────────────────────────────────────────────

def save_quiz_result(username: str, topic: str, score: int, total: int,
                     pct: int, difficulty: str) -> None:
    sb = get_supabase()
    sb.table("quiz_history").insert({
        "username": username,
        "topic": topic,
        "score": score,
        "total": total,
        "pct": pct,
        "difficulty_used": difficulty
    }).execute()
    # Upsert topic tracker
    sb.table("topic_tracker").upsert({
        "username": username,
        "topic": topic,
        "last_studied": datetime.now().isoformat(),
        "last_score_pct": pct
    }, on_conflict="username,topic").execute()
    # Increment review_count if topic already exists
    sb.rpc("increment_review_count", {
        "p_username": username, "p_topic": topic
    }).execute()

def get_quiz_history(username: str) -> list:
    res = get_supabase().table("quiz_history").select("*")\
        .eq("username", username).order("attempted_at", desc=True).execute()
    return res.data or []

def get_topics_studied_today(username: str) -> int:
    today_start = datetime.combine(date.today(), datetime.min.time()).isoformat()
    res = get_supabase().table("quiz_history").select("id")\
        .eq("username", username).gte("attempted_at", today_start).execute()
    return len(res.data) if res.data else 0

# ── TOPIC TRACKER ─────────────────────────────────────────────────────

def get_due_for_review(username: str) -> list:
    """Topics not studied in 3+ days AND last score < 80%."""
    cutoff = (datetime.now() - timedelta(days=3)).isoformat()
    res = get_supabase().table("topic_tracker").select("*")\
        .eq("username", username)\
        .lt("last_studied", cutoff)\
        .lt("last_score_pct", 80)\
        .order("last_studied").execute()
    return res.data or []

# ── LIBRARY ───────────────────────────────────────────────────────────

def save_to_library(username: str, topic: str, parsed: dict) -> None:
    get_supabase().table("library").insert({
        "username": username,
        "topic": topic,
        "eli5": parsed.get("eli5", ""),
        "conceptual": parsed.get("conceptual", ""),
        "expert": parsed.get("expert", ""),
        "prerequisites": parsed.get("prerequisites", ""),
        "concept_graph": parsed.get("concept_graph", "")
    }).execute()

def get_library(username: str) -> list:
    res = get_supabase().table("library").select("*")\
        .eq("username", username).order("saved_at", desc=True).execute()
    return res.data or []

def delete_from_library(entry_id: int) -> None:
    get_supabase().table("library").delete().eq("id", entry_id).execute()
```

> **Note on `increment_review_count`:** Create this SQL function in Supabase SQL Editor:
> ```sql
> CREATE OR REPLACE FUNCTION increment_review_count(p_username TEXT, p_topic TEXT)
> RETURNS void AS $$
> BEGIN
>   UPDATE topic_tracker
>   SET review_count = review_count + 1
>   WHERE username = p_username AND topic = p_topic;
> END;
> $$ LANGUAGE plpgsql;
> ```

---

### Phase 2 — Core AI Modules

**Step 8: Create `modules/gemini_client.py`**
```python
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
_model = genai.GenerativeModel("gemini-1.5-flash")

def call_gemini(prompt: str) -> str:
    """Send prompt to Gemini 1.5 Flash. Returns raw response text."""
    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR:{str(e)}"
```

**Step 9: Create `modules/prompt_builder.py`**

The system prompt schema is the backbone of the entire app. Tags must match exactly what the parser expects.

```python
SYSTEM_PROMPT = """
You are EduClarify AI — a structured educational assistant.
Given an academic topic or text, respond ONLY using the exact section tags below.
Do NOT add any text, preamble, or commentary outside these tags.

##ELI5##
Explain using a real-world analogy as if talking to a complete beginner with no prior knowledge.
Use everyday language. Maximum 5 sentences.

##CONCEPTUAL##
Explain the core mechanism, how it works, why it matters, and how its parts relate.
Use clear academic language suitable for a university student. Maximum 8 sentences.

##EXPERT##
Give a technical explanation with formal terminology, edge cases, and nuanced considerations.
Assume strong prior knowledge of the field. Maximum 6 sentences.

##PREREQUISITES##
List 3 to 5 foundational concepts the student must understand before this topic.
Format as a numbered list, one concept per line. Include a one-line description for each.

##CONCEPT_GRAPH##
Show how sub-concepts within this topic relate using an indented text tree.
Use dashes, box-drawing characters, and arrows (→) to show dependencies.
Format example:
Main Topic
  ├── Sub-concept A → leads to Sub-concept B
  ├── Sub-concept C
  │     └── Detail of C
  └── Sub-concept D → connects to Sub-concept A

##MCQ##
Generate exactly 5 multiple choice questions testing understanding (not just recall).
Each question MUST use this exact format — no deviations:

Q1: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
ANSWER: [single correct letter A/B/C/D]
EXPLANATION: [one sentence explaining why that answer is correct]

Q2: [repeat format]
Q3: [repeat format]
Q4: [repeat format]
Q5: [repeat format]
"""

REGENERATE_PROMPT = """
The previous explanation was unclear to the student.
Explain the same topic using a completely different approach, different analogy, and different examples.
Respond ONLY with the ##ELI5##, ##CONCEPTUAL##, and ##EXPERT## sections in the same tagged format.
Do not repeat or reuse any phrasing from the previous explanation.
"""

def build_prompt(user_input: str, difficulty: str) -> str:
    return f"""{SYSTEM_PROMPT}

Target audience level: {difficulty}

Topic or text to analyze:
{user_input}
"""

def build_regenerate_prompt(user_input: str, difficulty: str) -> str:
    return f"""{REGENERATE_PROMPT}

Target audience level: {difficulty}

Original topic:
{user_input}
"""
```

**Step 10: Create `modules/parser.py`**
```python
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
            lines = [l.strip() for l in part.splitlines() if l.strip()]
            if len(lines) < 6:
                continue
            q = {"question": lines[0], "options": {}, "answer": "", "explanation": ""}
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
        "eli5":         extract("ELI5"),
        "conceptual":   extract("CONCEPTUAL"),
        "expert":       extract("EXPERT"),
        "prerequisites":extract("PREREQUISITES"),
        "concept_graph":extract("CONCEPT_GRAPH"),
        "mcqs":         parse_mcqs(extract("MCQ"))
    }
```

**Step 11: Create `modules/pdf_reader.py`**
```python
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile PDF object."""
    try:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        return text[:4000]  # Cap to stay within prompt token budget
    except Exception as e:
        return f"PDF extraction failed: {str(e)}"
```

---

### Phase 3 — Quiz, Spaced Repetition, Library

**Step 12: Create `modules/quiz.py`**
```python
import streamlit as st
from modules.database import save_quiz_result, update_user_preference

DIFFICULTY_LEVELS = ["Class 10 (ELI5)", "Undergraduate", "Postgraduate / Research"]

def calibrate_difficulty(current: str, pct: int) -> str:
    """Return new difficulty level based on quiz score."""
    idx = DIFFICULTY_LEVELS.index(current) if current in DIFFICULTY_LEVELS else 1
    if pct >= 85 and idx < len(DIFFICULTY_LEVELS) - 1:
        return DIFFICULTY_LEVELS[idx + 1]
    elif pct < 50 and idx > 0:
        return DIFFICULTY_LEVELS[idx - 1]
    return current

def render_quiz(mcqs: list, topic: str, username: str, difficulty: str):
    if not mcqs:
        st.warning("No quiz questions were generated. Try rephrasing your input.")
        return

    st.subheader("📝 Test Your Understanding")

    user_answers = {}
    for i, q in enumerate(mcqs):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        opts = [f"{k}) {v}" for k, v in sorted(q["options"].items())]
        choice = st.radio("", opts, key=f"q_{topic}_{i}", label_visibility="collapsed")
        user_answers[i] = choice[0] if choice else None

    if st.button("Submit Quiz ✅", key=f"submit_{topic}", type="primary"):
        score = 0
        st.markdown("---")
        st.subheader("Results")
        for i, q in enumerate(mcqs):
            correct = q["answer"]
            given = user_answers.get(i)
            if given == correct:
                score += 1
                st.success(f"**Q{i+1}:** ✅ Correct — {q['explanation']}")
            else:
                st.error(f"**Q{i+1}:** ❌ You answered **{given}**, correct is **{correct}** — {q['explanation']}")

        pct = round((score / len(mcqs)) * 100)
        st.metric("Score", f"{score}/{len(mcqs)}", f"{pct}%")

        # Persist to database
        save_quiz_result(username, topic[:60], score, len(mcqs), pct, difficulty)

        # Difficulty calibration
        new_diff = calibrate_difficulty(difficulty, pct)
        if new_diff != difficulty:
            update_user_preference(username, "difficulty_level", new_diff)
            st.session_state.difficulty = new_diff
            st.info(f"📊 Difficulty auto-adjusted to **{new_diff}** based on your score.")

        st.session_state.last_quiz_score = pct
```

**Step 13: Create `modules/spaced_rep.py`**
```python
import streamlit as st
from modules.database import get_due_for_review

def render_due_for_review(username: str):
    """Display spaced repetition reminder list in sidebar."""
    due = get_due_for_review(username)
    if not due:
        st.sidebar.success("✅ No topics due for review!")
        return
    st.sidebar.markdown("### 🔁 Due for Review")
    st.sidebar.caption("These topics haven't been revisited in 3+ days.")
    for item in due[:5]:  # Show max 5
        last_score = item.get("last_score_pct", "?")
        st.sidebar.markdown(f"- **{item['topic'][:35]}** _{last_score}% last time_")
```

**Step 14: Create `modules/library.py`**
```python
import streamlit as st
from modules.database import get_library, save_to_library, delete_from_library

def render_library(username: str):
    """Render the personal topic library tab."""
    st.subheader("📚 My Topic Library")
    st.caption("Topics you've saved for quick revision. No re-running the AI needed.")

    entries = get_library(username)
    if not entries:
        st.info("No saved topics yet. After analyzing a topic, click 'Save to Library' on the Explanations tab.")
        return

    for entry in entries:
        with st.expander(f"📌 {entry['topic']} — saved {entry['saved_at'][:10]}"):
            col1, col2 = st.columns([5, 1])
            with col1:
                tab_a, tab_b, tab_c = st.tabs(["ELI5", "Conceptual", "Expert"])
                with tab_a:
                    st.write(entry.get("eli5", ""))
                with tab_b:
                    st.write(entry.get("conceptual", ""))
                with tab_c:
                    st.write(entry.get("expert", ""))
                if entry.get("prerequisites"):
                    st.markdown("**Prerequisites:**")
                    st.write(entry["prerequisites"])
            with col2:
                if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
                    delete_from_library(entry["id"])
                    st.rerun()

def save_button(username: str, topic: str, parsed: dict):
    """Render Save to Library button. Call this from Explanation tab."""
    if st.button("📌 Save to My Library", key=f"save_{topic}"):
        save_to_library(username, topic[:60], parsed)
        st.success("Saved to your library!")
```

---

### Phase 4 — Analytics and PDF Export

**Step 15: Create `modules/analytics.py`**
```python
import streamlit as st
from modules.database import get_quiz_history, get_topics_studied_today
from collections import defaultdict
from datetime import datetime

def render_analytics(username: str, study_goal: int):
    st.subheader("📊 Learning Analytics")

    history = get_quiz_history(username)
    if not history:
        st.info("Complete your first quiz to see analytics.")
        return

    # ── Summary Metrics ──────────────────────────────────────────
    total = len(history)
    avg = round(sum(h["pct"] for h in history) / total, 1)
    best = max(history, key=lambda x: x["pct"])
    worst = min(history, key=lambda x: x["pct"])
    today_count = get_topics_studied_today(username)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sessions", total)
    col2.metric("Avg Score", f"{avg}%")
    col3.metric("🏆 Best", best["topic"][:20], f"{best['pct']}%")
    col4.metric("Today's Progress", f"{today_count}/{study_goal}")

    st.progress(min(today_count / study_goal, 1.0),
                text=f"Daily Goal: {today_count}/{study_goal} topics")

    st.markdown("---")

    # ── Score by Topic (bar chart) ───────────────────────────────
    st.markdown("**Score by Topic (All Time)**")
    topic_scores = defaultdict(list)
    for h in history:
        topic_scores[h["topic"][:30]].append(h["pct"])
    avg_by_topic = {t: round(sum(s)/len(s)) for t, s in topic_scores.items()}
    st.bar_chart(avg_by_topic)

    # ── 7-Day Score Trend ────────────────────────────────────────
    st.markdown("**7-Day Score Trend**")
    daily = defaultdict(list)
    for h in history:
        day = h["attempted_at"][:10]
        daily[day].append(h["pct"])
    daily_avg = {d: round(sum(v)/len(v)) for d, v in sorted(daily.items())[-7:]}
    if len(daily_avg) > 1:
        st.line_chart(daily_avg)
    else:
        st.caption("Study across multiple days to see the trend chart.")

    # ── Weak Topics ──────────────────────────────────────────────
    st.markdown("---")
    weak = [(t, s) for t, s in avg_by_topic.items() if s < 60]
    if weak:
        st.markdown("**⚠️ Weak Topics (avg < 60%) — Focus Here**")
        for topic, score in sorted(weak, key=lambda x: x[1]):
            st.markdown(f"- **{topic}** — {score}%")
    else:
        st.success("No weak topics detected. Keep it up!")

    # ── Session Log ──────────────────────────────────────────────
    with st.expander("Full Session Log"):
        for i, h in enumerate(history, 1):
            dt = h["attempted_at"][:16].replace("T", " ")
            st.markdown(
                f"{i}. **{h['topic']}** — {h['score']}/{h['total']} ({h['pct']}%) "
                f"| {dt} | {h.get('difficulty_used', '')}"
            )
```

**Step 16: Create `modules/pdf_export.py`**
```python
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                  HRFlowable, Preformatted)

def generate_session_pdf(topic: str, parsed: dict, score: int, total: int) -> bytes:
    """
    Generate an A4 PDF session summary.
    Returns bytes that can be passed to st.download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=20, textColor=colors.HexColor("#6c63ff"), spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"],
        fontSize=13, textColor=colors.HexColor("#4a4a8a"), spaceBefore=12, spaceAfter=4
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, leading=14, spaceAfter=6
    )
    mono_style = ParagraphStyle(
        "Mono", parent=styles["Code"],
        fontSize=9, leading=12, fontName="Courier",
        backColor=colors.HexColor("#f5f5f5"), spaceAfter=6
    )

    story = []

    # Header
    story.append(Paragraph("EduClarify AI — Session Summary", title_style))
    story.append(Paragraph(f"<b>Topic:</b> {topic}", body_style))
    pct = round((score / total) * 100) if total else 0
    story.append(Paragraph(f"<b>Quiz Score:</b> {score}/{total} ({pct}%)", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#6c63ff")))
    story.append(Spacer(1, 6))

    # Sections
    sections = [
        ("ELI5 — Beginner Explanation", parsed.get("eli5", "")),
        ("Conceptual Explanation",       parsed.get("conceptual", "")),
        ("Expert Explanation",           parsed.get("expert", "")),
        ("Prerequisites",                parsed.get("prerequisites", "")),
    ]
    for heading, content in sections:
        if content:
            story.append(Paragraph(heading, h2_style))
            story.append(Paragraph(content.replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 4))

    # Concept graph (monospace)
    if parsed.get("concept_graph"):
        story.append(Paragraph("Concept Dependency Graph", h2_style))
        story.append(Preformatted(parsed["concept_graph"], mono_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Generated by EduClarify AI · CodeVeda · SDG 4: Quality Education",
        ParagraphStyle("Footer", parent=styles["Normal"],
                       fontSize=8, textColor=colors.grey)
    ))

    doc.build(story)
    return buffer.getvalue()
```

---

### Phase 5 — Main App

**Step 17: Create `app.py`**

This is the complete main application. Build it after all modules are in place.

```python
import streamlit as st
from modules.gemini_client import call_gemini
from modules.prompt_builder import build_prompt, build_regenerate_prompt
from modules.parser import parse_response
from modules.quiz import render_quiz, DIFFICULTY_LEVELS
from modules.analytics import render_analytics
from modules.database import get_or_create_user, update_user_preference
from modules.spaced_rep import render_due_for_review
from modules.library import render_library, save_button
from modules.pdf_reader import extract_text_from_pdf
from modules.pdf_export import generate_session_pdf

# ─── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduClarify AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0f1117; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 600; padding: 10px 20px; }
    .concept-box {
        background: #1e2130; border-left: 4px solid #6c63ff;
        border-radius: 8px; padding: 16px 20px; margin: 8px 0;
        font-size: 15px; line-height: 1.7;
    }
    .prereq-box {
        background: #1a2a1a; border-left: 4px solid #4caf50;
        border-radius: 8px; padding: 12px 16px; margin: 8px 0;
    }
    .graph-box {
        background: #1a1a2e; border: 1px solid #3a3a6e;
        border-radius: 8px; padding: 16px;
        font-family: monospace; white-space: pre; font-size: 13px;
    }
    .feedback-row { display: flex; gap: 10px; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Username Gate ────────────────────────────────────────────────────
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.title("🎓 EduClarify AI")
    st.markdown("### Welcome! Enter your name to get started.")
    st.caption("Your learning progress will be saved and available across devices.")
    name_input = st.text_input("Your name or student ID:", max_chars=30,
                                placeholder="e.g. Sayan or STU2023001")
    if st.button("Start Learning →", type="primary") and name_input.strip():
        username = name_input.strip().lower().replace(" ", "_")
        user = get_or_create_user(username)
        st.session_state.username = username
        st.session_state.difficulty = user.get("difficulty_level", "Undergraduate")
        st.session_state.study_goal = user.get("study_goal", 3)
        st.session_state.streak = user.get("streak", 0)
        st.rerun()
    st.stop()

# ─── Load user from session ───────────────────────────────────────────
username   = st.session_state.username
difficulty = st.session_state.get("difficulty", "Undergraduate")
study_goal = st.session_state.get("study_goal", 3)
streak     = st.session_state.get("streak", 0)

# ─── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🎓 EduClarify AI")
    st.markdown(f"👤 **{username}**")
    st.markdown(f"🔥 Streak: **{streak} day{'s' if streak != 1 else ''}**")
    st.markdown("---")

    new_difficulty = st.select_slider(
        "🎯 Explanation Depth",
        options=DIFFICULTY_LEVELS,
        value=difficulty
    )
    if new_difficulty != difficulty:
        st.session_state.difficulty = new_difficulty
        update_user_preference(username, "difficulty_level", new_difficulty)

    new_goal = st.number_input("📅 Daily Topic Goal", min_value=1,
                                max_value=20, value=study_goal)
    if new_goal != study_goal:
        st.session_state.study_goal = new_goal
        update_user_preference(username, "study_goal", new_goal)

    st.markdown("---")
    render_due_for_review(username)
    st.markdown("---")
    st.caption("EduClarify AI · CodeVeda\nESD 2025–26 · SDG 4")

# ─── Header ───────────────────────────────────────────────────────────
st.title("🎓 EduClarify AI")
st.markdown("*Paste any topic or syllabus text. Instant explanations, concept map, quiz, and progress tracking.*")
st.markdown("---")

# ─── Tabs (top-level navigation) ──────────────────────────────────────
main_tab, library_tab, analytics_tab = st.tabs([
    "🧠 Learn", "📚 My Library", "📊 Analytics"
])

# ══════════════════════════════════════════════════════════════════════
# LEARN TAB
# ══════════════════════════════════════════════════════════════════════
with main_tab:

    # Input section
    col_text, col_pdf = st.columns([2, 1])
    with col_text:
        user_text = st.text_area(
            "📋 Paste topic or syllabus text",
            placeholder="e.g. 'Explain Deadlock in Operating Systems'\nor paste a full syllabus unit here...",
            height=160, key="input_text"
        )
    with col_pdf:
        st.markdown("**Or upload a PDF syllabus:**")
        pdf_file = st.file_uploader("", type=["pdf"])
        if pdf_file:
            extracted = extract_text_from_pdf(pdf_file)
            st.success(f"Extracted {len(extracted)} chars.")
            if st.button("Use PDF as Input"):
                st.session_state.input_text = extracted
                st.rerun()

    final_input = user_text.strip() if user_text else ""

    clarify = st.button("✨ Clarify This Topic", type="primary",
                         use_container_width=True)

    if clarify and final_input:
        with st.spinner("Analyzing..."):
            prompt = build_prompt(final_input, st.session_state.difficulty)
            raw = call_gemini(prompt)
            if raw.startswith("ERROR:"):
                st.error(f"API Error: {raw}")
            else:
                parsed = parse_response(raw)
                st.session_state.last_parsed = parsed
                st.session_state.last_topic = final_input[:60]
    elif clarify:
        st.warning("Please enter a topic or upload a PDF first.")

    # ── Output ──────────────────────────────────────────────────────
    if "last_parsed" in st.session_state:
        parsed     = st.session_state.last_parsed
        topic      = st.session_state.last_topic
        difficulty = st.session_state.difficulty

        st.markdown("---")
        t1, t2, t3 = st.tabs(["📖 Explanations", "🗺️ Concept Map", "📝 Quiz"])

        # ── Explanations Tab ──────────────────────────────────────
        with t1:
            st.subheader("Layered Explanations")

            for label, key, color in [
                ("🟢 Beginner — ELI5 (Analogy)",     "eli5",       "#6c63ff"),
                ("🔵 Conceptual — Core Mechanism",   "conceptual", "#2196f3"),
                ("🔴 Expert — Technical Depth",       "expert",     "#f44336"),
            ]:
                with st.expander(label, expanded=(key == "eli5")):
                    content = parsed.get(key, "")
                    st.markdown(
                        f'<div class="concept-box">{content}</div>',
                        unsafe_allow_html=True
                    )
                    # Feedback buttons
                    fb_col1, fb_col2, _ = st.columns([1, 1, 6])
                    with fb_col1:
                        if st.button("👍", key=f"up_{key}_{topic}"):
                            st.toast("Thanks for the feedback!")
                    with fb_col2:
                        if st.button("👎 Regenerate", key=f"down_{key}_{topic}"):
                            with st.spinner("Regenerating explanation..."):
                                regen_prompt = build_regenerate_prompt(
                                    st.session_state.last_topic, difficulty
                                )
                                regen_raw = call_gemini(regen_prompt)
                                regen_parsed = parse_response(regen_raw)
                                if regen_parsed.get(key):
                                    st.session_state.last_parsed[key] = regen_parsed[key]
                                    st.rerun()

            st.markdown("---")
            st.subheader("✅ Prerequisites")
            st.markdown(
                f'<div class="prereq-box">{parsed.get("prerequisites", "")}</div>',
                unsafe_allow_html=True
            )
            st.markdown("")
            save_button(username, topic, parsed)

            # PDF Export
            st.markdown("---")
            last_score = st.session_state.get("last_quiz_score", 0)
            pdf_bytes = generate_session_pdf(
                topic, parsed,
                score=round(last_score * 5 / 100),
                total=5
            )
            st.download_button(
                label="⬇️ Download Session as PDF",
                data=pdf_bytes,
                file_name=f"educlarify_{topic[:30].replace(' ','_')}.pdf",
                mime="application/pdf"
            )

        # ── Concept Map Tab ───────────────────────────────────────
        with t2:
            st.subheader("🗺️ Concept Dependency Graph")
            st.caption("Follow arrows (→) to trace concept dependencies. Start from the top.")
            st.markdown(
                f'<div class="graph-box">{parsed.get("concept_graph", "")}</div>',
                unsafe_allow_html=True
            )

        # ── Quiz Tab ──────────────────────────────────────────────
        with t3:
            render_quiz(parsed.get("mcqs", []), topic, username, difficulty)

    else:
        # Landing cards
        st.markdown("### What EduClarify Does For You")
        c1, c2, c3, c4 = st.columns(4)
        c1.info("**📖 3-Layer Explanations**\nELI5 → Conceptual → Expert, auto-calibrated to your level")
        c2.info("**🗺️ Concept Map**\nDependency tree of all sub-concepts within the topic")
        c3.info("**📝 Smart Quiz**\n5 MCQs, instant scoring, spaced repetition scheduling")
        c4.info("**📊 Persistent Analytics**\nCross-device history, weak topics, 7-day trend")

# ══════════════════════════════════════════════════════════════════════
# LIBRARY TAB
# ══════════════════════════════════════════════════════════════════════
with library_tab:
    render_library(username)

# ══════════════════════════════════════════════════════════════════════
# ANALYTICS TAB
# ══════════════════════════════════════════════════════════════════════
with analytics_tab:
    render_analytics(username, st.session_state.get("study_goal", 3))
```

---

### Phase 6 — Local Test

**Step 18: Run and test**
```bash
streamlit run app.py
```

Open `http://localhost:8501`. Test the full flow:

1. Enter a username → verify user is created in Supabase (`users` table)
2. Paste a topic → verify all 4 sections render
3. Submit a quiz → verify row appears in `quiz_history` and `topic_tracker`
4. Check Analytics tab → verify charts load from database
5. Save a topic to Library → verify it persists after refreshing the page
6. Come back tomorrow with the same username → verify history is intact
7. Score < 50% on purpose → verify difficulty auto-adjusts downward

**Three recommended test inputs:**
```
# Test 1 — Single concept
Explain the concept of Deadlock in Operating Systems

# Test 2 — Syllabus module
Unit 4: Compiler Design
Topics: Lexical Analysis, Tokens, Regular Expressions,
Finite Automata, Top-Down Parsing, LR Parsing

# Test 3 — Dense text
The TCP/IP model describes how data is transmitted across networks
using a layered architecture where each layer communicates only
with adjacent layers through defined interfaces.
```

**Expected results:**
- ELI5 uses a non-technical real-world analogy
- Prerequisites list has 3–5 items with descriptions
- Concept graph shows tree with arrows
- All 5 MCQs have 4 options, an ANSWER, and an EXPLANATION
- Quiz submission updates both the Analytics tab and Supabase tables
- Spaced repetition sidebar updates after scoring below 80%

---

## 10. System Prompt Engineering

**Why `##TAG##` delimiters?**
Double-hash tags are rare in academic text, preventing accidental collisions. The regex
`##TAG##\s*(.*?)(?=##[A-Z_]+##|$)` reliably extracts each section regardless of ordering.

**Why cap at 5 MCQs with strict per-question format?**
The parser uses `Q\d+:` as split anchors. Fewer questions per call reduces API latency.
Strict `ANSWER:` and `EXPLANATION:` labels make field extraction deterministic.

**Why a separate `REGENERATE_PROMPT`?**
The regenerate call only needs three sections (ELI5, Conceptual, Expert), reducing tokens
by ~40% over a full prompt. The instruction "do not reuse any phrasing" prevents the model
from returning the same explanation with minor wording changes.

**Why 4000 char PDF cap?**
Covers a full university syllabus unit comfortably (typically 800–1500 chars). Longer inputs
slow Gemini response from ~3s to 10s+, hurting UX without proportional explanation quality gain.

**Debugging rule:** If a section renders blank, the problem is always in the system prompt
formatting instruction for that section — not in the parser. Make the tag instruction more
explicit and re-test.

---

## 11. Deployment Guide

**Step 1: Push to GitHub**
```bash
git add .
git commit -m "EduClarify AI — complete build"
git push origin main
```
Confirm `.streamlit/secrets.toml` is in `.gitignore` and NOT pushed.

**Step 2: Deploy on Streamlit Community Cloud**
1. Go to https://share.streamlit.io
2. Click **New app** → select your repo, branch `main`, file `app.py`
3. Open **Advanced settings → Secrets** and paste exactly:
```toml
GEMINI_API_KEY    = "your_gemini_key"
SUPABASE_URL      = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key"
```
4. Click **Deploy**

Your live URL (format: `https://username-educlarify-ai-xxxx.streamlit.app`) is the
**AI Tool Demonstration Link** for the ESD portal Stage 2 submission.

**Step 3: Verify deployment**
- Open the live URL in an incognito window
- Complete the full flow: enter username → analyze topic → take quiz → check analytics
- Confirm data persists on page refresh

---

## 12. Testing Checklist

Before submitting the ESD portal demo link, verify every item:

### Core Flow
- [ ] Username entry creates user row in Supabase `users` table
- [ ] Text input → all 5 response sections render (ELI5, Conceptual, Expert, Prerequisites, Graph)
- [ ] PDF upload extracts text and feeds it into the pipeline
- [ ] Quiz renders 5 questions with 4 options each
- [ ] Quiz submission writes to `quiz_history` and `topic_tracker`

### Persistence
- [ ] Refresh page with same username → quiz history still shows in Analytics
- [ ] Open on a different browser/device with same username → same history visible

### Smart Features
- [ ] Score ≥ 85% → difficulty bumps up one level (check sidebar slider)
- [ ] Score < 50% → difficulty softens one level
- [ ] "Save to Library" button → topic appears in Library tab after save
- [ ] Delete from Library works
- [ ] 👎 Regenerate button produces a different explanation

### Analytics
- [ ] Bar chart renders with topic names on X-axis
- [ ] Weak topics section lists topics with avg < 60%
- [ ] Daily goal progress bar moves after each quiz

### Spaced Repetition
- [ ] Sidebar "Due for Review" section appears for topics not revisited in 3+ days with score < 80%

### Export
- [ ] "Download Session as PDF" button downloads a valid, readable PDF

---

## 13. SDG Alignment

**Primary: SDG 4 — Quality Education**

| Target | How EduClarify Addresses It |
|---|---|
| 4.1 — Inclusive, equitable quality education | Free, zero-installation, browser-based — usable on any device by any student |
| 4.4 — Digital and technical skills for youth | Trains students to use AI as a structured learning tool, not just a search engine |
| 4.6 — Functional literacy and numeracy | ELI5 explanations with analogies lower the barrier for students with weak foundations |
| 4.7 — Education for sustainable development | Reduces dependence on paid tutoring; accessible to students who cannot afford coaching |

**Secondary: SDG 10 — Reduced Inequalities**
Spaced repetition and persistent analytics give students from under-resourced backgrounds
the same evidence-based learning system used by premium EdTech platforms — at zero cost.

---

*EduClarify AI · Team CodeVeda · ESD Spring 2025–26 · SDG 4: Quality Education*
