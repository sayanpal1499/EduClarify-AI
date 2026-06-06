import streamlit as st
from modules.database import save_quiz_result, update_user_preference

DIFFICULTY_LEVELS = ["Class 10 (ELI5)", "Undergraduate", "Postgraduate / Research"]


def calibrate_difficulty(current: str, pct: int) -> str:
    """Return new difficulty level based on quiz score.

    Score >= 85%  → bumps difficulty up one level.
    Score <  50%  → softens to a simpler level.
    """
    idx = DIFFICULTY_LEVELS.index(current) if current in DIFFICULTY_LEVELS else 1
    if pct >= 85 and idx < len(DIFFICULTY_LEVELS) - 1:
        return DIFFICULTY_LEVELS[idx + 1]
    elif pct < 50 and idx > 0:
        return DIFFICULTY_LEVELS[idx - 1]
    return current


def render_quiz(mcqs: list, topic: str, username: str, difficulty: str):
    """Render MCQ quiz with state-based flow:

    Phase 1 (answering): Show questions + radio buttons + Submit button.
    Phase 2 (submitted): Show results + score + download report button.
                         Hide questions and Submit button.
    """
    if not mcqs:
        st.warning("No quiz questions were generated. Try rephrasing your input.")
        return

    # Use a unique key per quiz session based on topic
    submitted_key = f"_quiz_submitted_{topic}"
    results_key = f"_quiz_results_{topic}"

    import time
    start_time_key = f"_quiz_start_{topic}"
    if start_time_key not in st.session_state:
        st.session_state[start_time_key] = time.time()

    # ── PHASE 2: Already submitted — show results only ───────────
    if st.session_state.get(submitted_key):
        results = st.session_state.get(results_key, {})
        if results:
            st.subheader("📊 Quiz Results")

            score = results["score"]
            total = results["total"]
            pct = results["pct"]
            details = results["results_detail"]

            for i, d in enumerate(details):
                if d["is_correct"]:
                    st.success(
                        f"**Q{i+1}: {d['question']}**\n\n"
                        f"✅ Correct — {d['explanation']}"
                    )
                else:
                    st.error(
                        f"**Q{i+1}: {d['question']}**\n\n"
                        f"❌ You answered **{d['user_answer']}**, "
                        f"correct is **{d['correct_answer']}** — "
                        f"{d['explanation']}"
                    )

            st.metric("Score", f"{score}/{total}", f"{pct}%")

            # Difficulty calibration message
            if results.get("new_diff_msg"):
                st.info(results["new_diff_msg"])

            # Download Report button
            try:
                from modules.pdf_export import generate_quiz_report_pdf

                time_taken = results.get("time_taken", "N/A")
                analytics_data = {
                    "Time Taken": time_taken,
                    "Total Questions": str(total),
                    "Correct Answers": str(score),
                    "Accuracy": f"{pct}%",
                    "Difficulty": difficulty
                }
                
                report_pdf = generate_quiz_report_pdf(
                    topic, mcqs, results.get("user_answers", {}),
                    score, total, pct, analytics_data
                )
                st.download_button(
                    "⬇️ Download Quiz Report (PDF)",
                    data=report_pdf,
                    file_name=f"quiz_report_{topic[:20].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key=f"dl_report_{topic}"
                )
            except Exception as e:
                st.error(f"Report generation error: {e}")

            # Retake button
            if st.button(
                "🔄 Take Another Quiz", key=f"retake_{topic}",
                type="primary"
            ):
                st.session_state[submitted_key] = False
                if results_key in st.session_state:
                    del st.session_state[results_key]
                # Clear radio button states
                for i in range(len(mcqs)):
                    key = f"q_{topic}_{i}"
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        return  # Don't render question form

    # ── PHASE 1: Answering — show questions + Submit ─────────────
    st.subheader("📝 Test Your Understanding")

    user_answers = {}
    for i, q in enumerate(mcqs):
        st.markdown(f"**Q{i + 1}: {q['question']}**")
        opts = [f"{k}) {v}" for k, v in sorted(q["options"].items())]
        choice = st.radio(
            f"Select answer for Q{i + 1}",
            opts,
            key=f"q_{topic}_{i}",
            index=None,
            label_visibility="collapsed"
        )
        user_answers[i] = choice[0] if choice else None

    if st.button("Submit Quiz ✅", key=f"submit_{topic}", type="primary"):
        # Check if all questions are answered
        unanswered = [
            i + 1 for i, ans in user_answers.items() if ans is None
        ]
        if unanswered:
            st.warning(
                f"⚠️ Please answer all questions before submitting. "
                f"Unanswered: Q{', Q'.join(map(str, unanswered))}"
            )
            return

        score = 0
        results_detail = []
        for i, q in enumerate(mcqs):
            correct = q["answer"]
            given = user_answers.get(i)
            is_correct = (given == correct)
            if is_correct:
                score += 1
            results_detail.append({
                "question": q["question"],
                "options": q["options"],
                "user_answer": given,
                "correct_answer": correct,
                "is_correct": is_correct,
                "explanation": q.get("explanation", "")
            })

        pct = round((score / len(mcqs)) * 100)

        # Persist to database
        save_quiz_result(
            username, topic[:60], score, len(mcqs), pct, difficulty
        )

        # Difficulty calibration
        new_diff = calibrate_difficulty(difficulty, pct)
        new_diff_msg = ""
        if new_diff != difficulty:
            update_user_preference(username, "difficulty_level", new_diff)
            st.session_state.difficulty = new_diff
            new_diff_msg = (
                f"📊 Difficulty auto-adjusted to **{new_diff}** "
                f"based on your score."
            )

        st.session_state.last_quiz_score = pct

        end_time = time.time()
        start_t = st.session_state.get(start_time_key, end_time)
        time_taken_seconds = int(end_time - start_t)
        mins, secs = divmod(time_taken_seconds, 60)
        time_taken_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

        # Store results and mark as submitted
        st.session_state[results_key] = {
            "score": score,
            "total": len(mcqs),
            "pct": pct,
            "results_detail": results_detail,
            "user_answers": user_answers,
            "new_diff_msg": new_diff_msg,
            "time_taken": time_taken_str
        }
        st.session_state.last_quiz_results = {
            "topic": topic,
            "mcqs": mcqs,
            "user_answers": user_answers,
            "results_detail": results_detail,
            "score": score,
            "total": len(mcqs),
            "pct": pct,
            "difficulty": difficulty,
            "time_taken": time_taken_str
        }
        st.session_state[submitted_key] = True
        st.rerun()
