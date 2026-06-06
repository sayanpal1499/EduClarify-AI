import streamlit as st
from supabase import create_client, Client
from datetime import date, datetime, timedelta


@st.cache_resource
def get_supabase() -> Client:
    """Create and cache a Supabase client instance."""
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
    """Update a single field on the user's row."""
    get_supabase().table("users").update(
        {field: value}
    ).eq("username", username).execute()


# ── QUIZ HISTORY ─────────────────────────────────────────────────────

def save_quiz_result(username: str, topic: str, score: int, total: int,
                     pct: int, difficulty: str) -> None:
    """Save a quiz result and update topic tracker + review count."""
    sb = get_supabase()

    # Insert quiz history row
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

    # Increment review_count via RPC
    try:
        sb.rpc("increment_review_count", {
            "p_username": username, "p_topic": topic
        }).execute()
    except Exception:
        pass  # RPC may not exist yet during initial setup


def get_quiz_history(username: str) -> list:
    """Return all quiz history rows for a user, newest first."""
    res = get_supabase().table("quiz_history").select("*") \
        .eq("username", username).order("attempted_at", desc=True).execute()
    return res.data or []


def get_topics_studied_today(username: str) -> int:
    """Count how many quiz sessions the user completed today."""
    today_start = datetime.combine(
        date.today(), datetime.min.time()
    ).isoformat()
    res = get_supabase().table("quiz_history").select("id") \
        .eq("username", username).gte("attempted_at", today_start).execute()
    return len(res.data) if res.data else 0


# ── TOPIC TRACKER ─────────────────────────────────────────────────────

def get_due_for_review(username: str) -> list:
    """Topics not studied in 3+ days AND last score < 80%."""
    cutoff = (datetime.now() - timedelta(days=3)).isoformat()
    res = get_supabase().table("topic_tracker").select("*") \
        .eq("username", username) \
        .lt("last_studied", cutoff) \
        .lt("last_score_pct", 80) \
        .order("last_studied").execute()
    return res.data or []


# ── LIBRARY ───────────────────────────────────────────────────────────

def save_to_library(username: str, topic: str, parsed: dict) -> None:
    """Save a full explanation set to the user's personal library."""
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
    """Return all saved library entries for a user, newest first."""
    res = get_supabase().table("library").select("*") \
        .eq("username", username).order("saved_at", desc=True).execute()
    return res.data or []


def delete_from_library(entry_id: int) -> None:
    """Delete a single library entry by ID."""
    get_supabase().table("library").delete().eq("id", entry_id).execute()


# ── STUDY PLANS ──────────────────────────────────────────────────────

def save_study_plan(username: str, plan_data: dict) -> None:
    """Save or update a study plan for the user."""
    sb = get_supabase()
    existing = sb.table("study_plans").select("id").eq("username", username).eq("plan_name", plan_data["plan_name"]).execute()
    if existing.data:
        sb.table("study_plans").update(plan_data).eq("id", existing.data[0]["id"]).execute()
    else:
        plan_data["username"] = username
        sb.table("study_plans").insert(plan_data).execute()


def get_study_plans(username: str) -> list:
    """Return all study plans for a user."""
    res = get_supabase().table("study_plans").select("*") \
        .eq("username", username).order("created_at", desc=True).execute()
    return res.data or []


def update_study_plan(plan_id: int, updates: dict) -> None:
    """Update a study plan by ID."""
    get_supabase().table("study_plans").update(updates).eq("id", plan_id).execute()


def delete_study_plan(plan_id: int) -> None:
    """Delete a study plan by ID."""
    get_supabase().table("study_plans").delete().eq("id", plan_id).execute()


def get_past_quiz_questions(username: str, topic: str) -> list:
    """Get previously asked quiz questions for anti-repetition."""
    res = get_supabase().table("quiz_history").select("questions_json") \
        .eq("username", username).eq("topic", topic).execute()
    questions = []
    for row in (res.data or []):
        if row.get("questions_json"):
            questions.extend(row["questions_json"])
    return questions


def save_quiz_result_with_questions(username: str, topic: str, score: int, total: int,
                                     pct: int, difficulty: str, questions: list) -> None:
    """Save a quiz result with the question texts for anti-repetition tracking."""
    sb = get_supabase()
    sb.table("quiz_history").insert({
        "username": username,
        "topic": topic,
        "score": score,
        "total": total,
        "pct": pct,
        "difficulty_used": difficulty,
        "questions_json": questions
    }).execute()
    # Upsert topic tracker
    sb.table("topic_tracker").upsert({
        "username": username,
        "topic": topic,
        "last_studied": __import__('datetime').datetime.now().isoformat(),
        "last_score_pct": pct
    }, on_conflict="username,topic").execute()
