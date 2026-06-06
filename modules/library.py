import streamlit as st
from modules.database import get_library, save_to_library, delete_from_library


def render_library(username: str):
    """Render the personal topic library tab."""
    st.subheader("📚 My Topic Library")
    st.caption(
        "Topics you've saved for quick revision. "
        "No re-running the AI needed."
    )

    entries = get_library(username)
    if not entries:
        st.info(
            "No saved topics yet. After analyzing a topic, "
            "click 'Save to Library' on the Explanations tab."
        )
        return

    for entry in entries:
        with st.expander(
            f"📌 {entry['topic']} — saved {entry['saved_at'][:10]}"
        ):
            col1, col2 = st.columns([5, 1])
            with col1:
                tab_a, tab_b, tab_c = st.tabs(
                    ["ELI5", "Conceptual", "Expert"]
                )
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
