import streamlit as st
from modules.database import get_due_for_review


def render_due_for_review(username: str):
    """Display spaced repetition reminder list (called within sidebar context)."""
    due = get_due_for_review(username)

    if not due:
        st.success("✅ No topics due for review!")
        return

    st.markdown("**🔁 Due for Review**")
    st.caption("Topics not revisited in 3+ days:")

    for item in due[:5]:
        last_score = item.get("last_score_pct", "?")
        st.markdown(
            f"- **{item['topic'][:35]}** — _{last_score}% last time_"
        )
