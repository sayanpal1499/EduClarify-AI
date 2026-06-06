# EduClarify AI 🎓

<div align="center">

### An AI-Powered Adaptive Learning & Study Planning Agent

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/AI%20Engine-Groq%20%7C%20Llama%203.3-F55036?style=for-the-badge)](https://groq.com)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=for-the-badge&logo=supabase)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **SDG 4: Quality Education**

[🚀 Live Demo](#11-deployment) · [📖 Features](#4-feature-set) · [🛠️ Setup](#9-setup-guide) · [📐 Architecture](#5-architecture)

</div>

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Our Solution](#2-our-solution)
3. [What Makes It Unique](#3-what-makes-it-unique)
4. [Feature Set](#4-feature-set)
5. [Architecture](#5-architecture)
6. [Tech Stack](#6-tech-stack)
7. [File Structure](#7-file-structure)
8. [Database Schema](#8-database-schema)
9. [Setup Guide](#9-setup-guide)
10. [Security](#10-security)
11. [Deployment](#11-deployment)
12. [SDG Alignment](#12-sdg-alignment)

---

## 1. Problem Statement

Students across schools, colleges, and competitive exams face a persistent challenge: **academic content is dense, jargon-heavy, and poorly structured for independent self-learning.** Textbooks and syllabi are written for information density — not comprehension.

The downstream effects:
- Students memorize without understanding, leading to poor performance in applied assessments
- No personalized feedback loop exists — a student doesn't know *which* concepts they're weak in until the exam
- Progress made one day is forgotten the next because no tool tracks cross-session learning history
- Existing tools (ChatGPT, Google) provide raw information but offer no structured learning pathway, self-assessment, or retention scheduling

---

## 2. Our Solution

**EduClarify AI** transforms any raw academic text — a syllabus PDF, a textbook paragraph, or just a topic name — into a complete, personalized learning session.

A student enters their username once. The agent then:

1. **Simplifies** content across three adaptive explanation layers
2. **Maps prerequisites** — foundational concepts to understand first
3. **Builds a visual concept map** showing how sub-topics connect
4. **Generates adaptive quizzes** with auto-calibrating difficulty and instant feedback
5. **Parses an entire syllabus** into structured modules with study strategies
6. **Creates a personalized study plan** with deadlines and progress tracking
7. **Tracks learning progress** with analytics — streaks, topic completion, growth indicators
8. **Exports content as PDF** — explanations, revision notes, and quiz reports

---

## 3. What Makes It Unique

| Feature | EduClarify AI | ChatGPT | Quizlet | Notion AI | Khan Academy |
|---|:---:|:---:|:---:|:---:|:---:|
| 3-layer adaptive explanation | ✅ | ❌ | ❌ | ❌ | Partial |
| Prerequisite concept mapper | ✅ | ❌ | ❌ | ❌ | ❌ |
| Visual concept map | ✅ | ❌ | ❌ | ❌ | ❌ |
| Syllabus PDF → structured modules | ✅ | ❌ | ❌ | ❌ | ❌ |
| Study planner with deadlines | ✅ | ❌ | ❌ | Partial | ❌ |
| Progress tracking + analytics | ✅ | ❌ | Partial | ❌ | ✅ |
| Auto difficulty calibration | ✅ | ❌ | ❌ | ❌ | Partial |
| Spaced repetition scheduling | ✅ | ❌ | ✅ | ❌ | ❌ |
| Quiz time tracking | ✅ | ❌ | ❌ | ❌ | ❌ |
| PDF export (3 types) | ✅ | ❌ | ❌ | Partial | ❌ |
| Cross-device persistent data | ✅ | ❌ | Partial | ❌ | ✅ |
| Zero installation, browser-based | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 4. Feature Set

### 🧠 Learn Tab
- **Input Flexibility:** Paste any topic text OR upload a PDF syllabus to instantly generate a learning session.
- **3-Layer Explanations:** View content explained at 3 adaptive depths: ELI5 (Beginner), Conceptual (Intermediate), and Expert.
- **Prerequisites & Concept Map:** Automatically maps out foundational knowledge required and visualizes how sub-topics connect.
- **Save & Plan:** One-click options to save sessions to your Library or schedule them in your Study Planner.

### 📝 Smart Quiz
- **Dynamic Generation:** Generates multiple-choice questions based on the exact learning material.
- **Auto-Calibrating Difficulty:** Your score automatically adjusts the difficulty of future quizzes and explanations.
- **Detailed PDF Reports:** Download a comprehensive PDF report containing all questions, correct answers, explanations, and your specific time/accuracy analytics.

### 🗂️ Study Planner Tab
- **Progress Tracking:** Check off learned topics across modules and set visual deadlines (Overdue, Due Today, etc.).
- **Targeted Quizzes:** Select specific topics across multiple modules and generate a custom quiz just for those areas.
- **Revision Notes Export:** Generate AI summary notes for your selected modules and download them as a formatted PDF.

### 📚 My Library & 📊 Analytics
- **Personal Library:** Browse, read, or download PDFs of any previously saved learning session.
- **Data-Driven Insights:** Track your daily study streak, overall accuracy, time spent, and identify your weakest topics over the last 7 days.
- **Spaced Repetition:** The dashboard automatically flags topics you haven't reviewed recently if you scored poorly on them.

---

## 5. Architecture

### System Overview

```
┌────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                           │
│                                                                │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────┐  ┌────────┐ │
│  │  Learn   │  │Study Planner │  │  My Library │  │Analytic│ │
│  │   Tab    │  │     Tab      │  │     Tab     │  │  Tab   │ │
│  └────┬─────┘  └──────┬───────┘  └──────┬──────┘  └───┬────┘ │
│       └───────────────┴─────────────────┴──────────────┘      │
│                               │                                │
│                    ┌──────────▼──────────┐                     │
│                    │       app.py        │                     │
│                    │  (Main Orchestrator)│                     │
│                    └──────────┬──────────┘                     │
│            ┌──────────────────┼───────────────────┐           │
│            │                  │                   │           │
│  ┌─────────▼──────┐  ┌────────▼──────────┐  ┌────▼─────────┐ │
│  │ gemini_client  │  │   database.py      │  │ pdf_export   │ │
│  │ (Groq/Llama3)  │  │  (Supabase R/W)    │  │ (ReportLab)  │ │
│  └─────────┬──────┘  └────────┬──────────┘  └──────────────┘ │
│            │                  │                                │
│  ┌─────────▼──────┐  ┌────────▼──────────┐                    │
│  │   parser.py    │  │  Supabase Postgres │                    │
│  └────────────────┘  └───────────────────┘                    │
│                                                                │
│  ┌─────────────┐  ┌────────────────┐  ┌────────────────────┐  │
│  │   quiz.py   │  │study_planner.py│  │  syllabus_parser   │  │
│  │  (2-Phase)  │  │  (2-Part UI)   │  │  (Module Parser)   │  │
│  └─────────────┘  └────────────────┘  └────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Main Streamlit entry point, tab routing, sidebar, session state management |
| `modules/gemini_client.py` | Groq (Llama 3.3-70B) API wrapper — send prompt, return raw text |
| `modules/prompt_builder.py` | Builds the full system prompt with user input, difficulty level, and output schema |
| `modules/parser.py` | Regex-based parser — splits `##TAGGED##` LLM response into structured dict |
| `modules/quiz.py` | Full 2-phase MCQ renderer with time tracking, scoring, and difficulty calibration |
| `modules/study_planner.py` | Study plan creation, 2-part progress/quiz UI, module tracking, analytics |
| `modules/syllabus_parser.py` | Parses raw syllabus text into modules/topics using AI |
| `modules/analytics.py` | Full analytics dashboard — reads Supabase, renders all charts and metrics |
| `modules/database.py` | All Supabase read/write operations — single source of truth |
| `modules/spaced_rep.py` | Computes topics due for review based on `last_studied` + score |
| `modules/library.py` | Save/load/delete topic explanations from personal library |
| `modules/pdf_reader.py` | Extracts text from uploaded PDF using PyMuPDF |
| `modules/pdf_export.py` | Generates 3 types of PDFs: Learning, Revision Notes, and Quiz Report |

### Data Flow

```
User inputs topic / uploads PDF
        │
        ▼ [pdf_reader.py if PDF]
[prompt_builder.py] ── injects topic + difficulty + output schema
        │
        ▼
[gemini_client.py] ── Groq API → llama-3.3-70b-versatile
        │
        ▼
[parser.py] ── splits ##TAGS## → { eli5, conceptual, expert, prerequisites, concept_graph, mcqs }
        │
        ├── Render explanation tabs
        ├── Render concept map
        └── [quiz.py] ── Phase 1: Questions → Phase 2: Results + PDF
                │
                ▼
        [database.py] ── write quiz_history, update topic_tracker, update streak
                │
                ├── [analytics.py] ── charts and metrics
                ├── [spaced_rep.py] ── due-for-review list
                └── [pdf_export.py] ── generate quiz_report PDF
```

---

## 6. Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| UI Framework | Streamlit | ≥ 1.35.0 | Rapid Python-based web UI, zero JS needed |
| LLM Engine | Groq — Llama 3.3 70B Versatile | Latest | Ultra-fast inference, strong structured output |
| Cloud Database | Supabase (Postgres) | Free tier | Cross-device persistent storage |
| PDF Parsing (input) | PyMuPDF (`fitz`) | ≥ 1.24.0 | Lightweight, accurate text extraction from PDFs |
| PDF Generation | ReportLab | ≥ 4.2.0 | Programmatic A4 PDF generation |
| Charts | Plotly | ≥ 5.18.0 | Interactive analytics charts |
| Secrets | Streamlit Secrets | — | API keys kept out of source code |
| Hosting | Streamlit Community Cloud | — | Free public URL from GitHub |

### `requirements.txt`
```
streamlit>=1.35.0
groq>=0.9.0
supabase>=2.4.0
PyMuPDF>=1.24.0
reportlab>=4.2.0
plotly>=5.18.0
```

---

## 7. File Structure

```
EduClarify/
│
├── app.py                        # Main Streamlit entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── .streamlit/
│   ├── config.toml               # Dark theme configuration
│   └── secrets.toml              # 🔐 API keys — NEVER commit this file
│
└── modules/
    ├── __init__.py               # Package init
    ├── gemini_client.py          # Groq API wrapper (Llama 3.3)
    ├── prompt_builder.py         # System prompt + prompt construction
    ├── parser.py                 # LLM response parser (regex-based)
    ├── quiz.py                   # 2-phase MCQ renderer with time tracking
    ├── study_planner.py          # Study plan UI — progress tracking + quiz/notes
    ├── syllabus_parser.py        # Syllabus → module structure parser
    ├── analytics.py              # Analytics dashboard renderer
    ├── database.py               # All Supabase read/write operations
    ├── spaced_rep.py             # Spaced repetition scheduling logic
    ├── library.py                # Topic library save/load/delete
    ├── pdf_reader.py             # PDF input text extractor
    └── pdf_export.py             # PDF generator (3 modes: learning / revision / quiz)
```

---

## 8. Database Schema

Create these tables in your Supabase project via the **SQL Editor**.

### `users`
```sql
CREATE TABLE users (
    username         TEXT PRIMARY KEY,
    difficulty_level TEXT DEFAULT 'Undergraduate',
    study_goal       INTEGER DEFAULT 3,
    streak           INTEGER DEFAULT 0,
    last_active_date DATE,
    created_at       TIMESTAMP DEFAULT NOW()
);
```

### `quiz_history`
```sql
CREATE TABLE quiz_history (
    id              SERIAL PRIMARY KEY,
    username        TEXT NOT NULL REFERENCES users(username),
    topic           TEXT NOT NULL,
    score           INTEGER NOT NULL,
    total           INTEGER NOT NULL,
    pct             INTEGER NOT NULL,
    difficulty_used TEXT,
    questions_json  JSONB,
    attempted_at    TIMESTAMP DEFAULT NOW()
);
```

### `topic_tracker`
```sql
CREATE TABLE topic_tracker (
    id             SERIAL PRIMARY KEY,
    username       TEXT NOT NULL REFERENCES users(username),
    topic          TEXT NOT NULL,
    last_studied   TIMESTAMP DEFAULT NOW(),
    review_count   INTEGER DEFAULT 1,
    last_score_pct INTEGER,
    UNIQUE(username, topic)
);
```

### `library`
```sql
CREATE TABLE library (
    id           SERIAL PRIMARY KEY,
    username     TEXT NOT NULL REFERENCES users(username),
    topic        TEXT NOT NULL,
    eli5         TEXT,
    conceptual   TEXT,
    expert       TEXT,
    prerequisites TEXT,
    concept_graph TEXT,
    saved_at     TIMESTAMP DEFAULT NOW()
);
```

### `study_plans`
```sql
CREATE TABLE study_plans (
    id                SERIAL PRIMARY KEY,
    username          TEXT NOT NULL REFERENCES users(username),
    plan_name         TEXT NOT NULL,
    modules_json      JSONB,
    deadlines_json    JSONB,
    progress_json     JSONB,
    progress_history  JSONB DEFAULT '[]',
    created_at        TIMESTAMP DEFAULT NOW()
);
```

### Helper SQL Function
```sql
CREATE OR REPLACE FUNCTION increment_review_count(p_username TEXT, p_topic TEXT)
RETURNS void AS $$
BEGIN
  UPDATE topic_tracker
  SET review_count = review_count + 1
  WHERE username = p_username AND topic = p_topic;
END;
$$ LANGUAGE plpgsql;
```

> **Row Level Security:** Disable RLS on all tables for development (Table Editor → RLS → Disable). Do not store sensitive personal data.

---

## 9. Setup Guide

### Prerequisites
- Python 3.10 or higher
- A [Groq API Key](https://console.groq.com) (free)
- A [Supabase](https://supabase.com) project (free)

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/EduClarify-AI.git
cd EduClarify-AI
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure secrets
Create the file `.streamlit/secrets.toml` (this file is in `.gitignore` and will **never** be committed):

```toml
GROQ_API_KEY     = "gsk_your_groq_api_key_here"
SUPABASE_URL     = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key_here"
```

### Step 5 — Set up the database
1. Go to your Supabase project → **SQL Editor**
2. Run each `CREATE TABLE` block from [Section 8](#8-database-schema) in order
3. Run the `increment_review_count` helper function SQL

### Step 6 — Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🚀

---

## 10. Security

| What | How It's Protected |
|---|---|
| **Groq API Key** | Stored in `.streamlit/secrets.toml` — never in source code. Loaded via `st.secrets`. |
| **Supabase URL & Key** | Same as above — loaded via `st.secrets` in `modules/database.py`. |
| **secrets.toml** | Explicitly listed in `.gitignore` — can **never** be accidentally pushed to GitHub. |
| **User Passwords** | This app uses simple username-based access (no passwords). No sensitive credentials are stored. |
| **User Data** | All data is stored in your own private Supabase project — you own and control it. |
| **Deployed Secrets** | On Streamlit Community Cloud, secrets are stored encrypted in the dashboard — not in the repository. |

> ⚠️ **Never share your `secrets.toml` file or paste your API keys anywhere publicly.**

---

## 11. Deployment

### Deploy to GitHub

```bash
# Add your GitHub repo as remote (create an empty repo on GitHub first)
git remote add origin https://github.com/YOUR-USERNAME/EduClarify-AI.git
git branch -M main
git push -u origin main
```

> Your `secrets.toml` is in `.gitignore` — your API keys are **not** pushed.

### Deploy to Streamlit Community Cloud (Free)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**
3. Select your repository, branch `main`, and main file `app.py`
4. Click **Advanced settings…** → paste your secrets in the **Secrets** box:
   ```toml
   GROQ_API_KEY      = "gsk_..."
   SUPABASE_URL      = "https://..."
   SUPABASE_ANON_KEY = "eyJ..."
   ```
5. Click **Save**, then **Deploy!**

In 2–3 minutes you will have a live public URL like `https://educlarify-ai.streamlit.app` 🌐

---

## 12. SDG Alignment

**SDG 4 — Quality Education:** *Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.*

| SDG 4 Sub-target | How EduClarify Addresses It |
|---|---|
| 4.1 — Free quality education | Fully free to use, browser-based, no installation |
| 4.4 — Skills for employment | Builds deep conceptual understanding, not just memorization |
| 4.6 — Literacy and numeracy | Adaptive ELI5 mode makes complex topics accessible to all levels |
| 4.a — Educational infrastructure | Cloud-first, works on any device with a browser |

---

<div align="center">

Built with ❤️ for AI-Powered Learning

*EduClarify AI — Learn Smarter, Not Harder*

</div>
