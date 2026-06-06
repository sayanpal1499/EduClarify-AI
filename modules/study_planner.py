import streamlit as st
import json
from datetime import datetime, date, timedelta
from modules.database import (
    save_study_plan, get_study_plans,
    update_study_plan, delete_study_plan
)
from modules.syllabus_parser import generate_revision_notes
from modules.gemini_client import call_gemini
from modules.parser import parse_response


def render_study_planner(username: str):
    """Render the full Study Planner tab with 2 sections:
    1. Progress Tracking (check topics, deadlines, analytics)
    2. Quiz & Notes (cross-module quiz, revision notes download)
    """
    st.subheader("📋 Study Planner")
    st.caption(
        "Track your modules, set deadlines, and master each topic. "
        "Add plans from the 🧠 Learn tab using the '📋 Add to Study Plan' button."
    )

    if "planner_quiz_mode" not in st.session_state:
        st.session_state.planner_quiz_mode = None

    saved_plans = get_study_plans(username)

    if not saved_plans:
        st.markdown("")
        st.info(
            "📚 **No study plans yet!**\n\n"
            "Go to the **🧠 Learn** tab → paste or upload your syllabus → "
            "click **✨ Clarify This Topic** → then click **📋 Add to Study Plan** "
            "to automatically create a structured plan with modules and deadlines."
        )
        return

    # ── Display each plan ────────────────────────────────────────
    for plan in saved_plans:
        plan_name_display = plan.get("plan_name", "Untitled Plan")
        modules = json.loads(plan.get("modules_json", "[]"))
        strategy = plan.get("strategy", "")

        if not modules:
            continue

        total_topics = sum(len(m.get("topics", [])) for m in modules)
        completed_topics = sum(
            len(m.get("completed_topics", [])) for m in modules
        )
        progress = completed_topics / total_topics if total_topics > 0 else 0

        st.markdown(f"### 📘 {plan_name_display}")

        # Overview metrics
        prog_col1, prog_col2, prog_col3 = st.columns(3)
        with prog_col1:
            st.metric("📊 Modules", len(modules))
        with prog_col2:
            st.metric("📝 Topics", f"{completed_topics}/{total_topics}")
        with prog_col3:
            st.metric("✅ Progress", f"{round(progress * 100)}%")

        st.progress(
            progress,
            text=f"Overall: {completed_topics}/{total_topics} topics covered"
        )

        if strategy:
            with st.expander("🎯 AI Study Strategy", expanded=False):
                st.markdown(strategy)

        st.markdown("---")

        # ══════════════════════════════════════════════════════════
        # TWO-PART LAYOUT
        # ══════════════════════════════════════════════════════════
        part1_tab, part2_tab = st.tabs([
            "📈 Progress Tracking", "📝 Quiz & Revision Notes"
        ])

        # ══════════════════════════════════════════════════════════
        # PART 1: PROGRESS TRACKING
        # ══════════════════════════════════════════════════════════
        with part1_tab:
            st.markdown("#### ✅ Track Your Learned Topics")
            st.caption(
                "Check the topics you've covered, set deadlines, "
                "then click **Save Progress** to update your plan."
            )

            # Use a session key to track unsaved changes
            changes_key = f"_changes_{plan['id']}"
            if changes_key not in st.session_state:
                st.session_state[changes_key] = False

            # Module expanders for topic tracking
            for mi, module in enumerate(modules):
                mod_name = module.get("name", f"Module {mi + 1}")
                topics = module.get("topics", [])
                completed = list(module.get("completed_topics", []))
                importance = module.get("importance", "MEDIUM")
                weightage = module.get("weightage", 0)
                skippable = module.get("skippable", False)
                est_hours = module.get("estimated_hours", 0)
                deadline = module.get("deadline", None)
                mod_progress = (
                    len(completed) / len(topics) if topics else 0
                )

                imp_emoji = {
                    "HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"
                }.get(importance, "⚪")
                skip_txt = " · 💨 Skip" if skippable else ""

                with st.expander(
                    f"{imp_emoji} **Module {mi+1}: {mod_name}** — "
                    f"{weightage}% · "
                    f"{len(completed)}/{len(topics)} done{skip_txt}",
                    expanded=False
                ):
                    ic1, ic2, ic3 = st.columns(3)
                    with ic1:
                        st.caption(f"⏱️ Est. {est_hours}h")
                    with ic2:
                        st.caption(f"📊 {weightage}% marks")
                    with ic3:
                        st.caption(
                            f"📈 Order: "
                            f"#{module.get('study_order', mi+1)}"
                        )

                    st.progress(mod_progress)

                    # Deadline
                    new_deadline = st.date_input(
                        f"Deadline for {mod_name}",
                        value=(
                            date.fromisoformat(deadline)
                            if deadline else None
                        ),
                        key=f"dl_{plan['id']}_{mi}",
                    )
                    if new_deadline:
                        nd_str = new_deadline.isoformat()
                        if nd_str != deadline:
                            module["deadline"] = nd_str
                            st.session_state[changes_key] = True

                    # Topic checkboxes — NO rerun on change
                    st.markdown("**Topics:**")
                    for ti, topic in enumerate(topics):
                        is_done = topic in completed
                        checked = st.checkbox(
                            topic,
                            value=is_done,
                            key=f"trk_{plan['id']}_{mi}_{ti}"
                        )
                        if checked and not is_done:
                            completed.append(topic)
                            st.session_state[changes_key] = True
                        elif not checked and is_done:
                            completed.remove(topic)
                            st.session_state[changes_key] = True

                    # Update module in memory (not DB yet)
                    module["completed_topics"] = completed
                    new_status = (
                        "completed" if len(completed) == len(topics)
                        else ("in_progress" if completed else "pending")
                    )
                    module["status"] = new_status

            # Save button
            st.markdown("")
            if st.button(
                "💾 Save Progress",
                key=f"save_progress_{plan['id']}",
                type="primary",
                use_container_width=True
            ):
                # Record completion timestamp
                now_str = datetime.now().isoformat()
                history = json.loads(
                    plan.get("progress_history", "[]")
                ) if plan.get("progress_history") else []
                current_completed = sum(
                    len(m.get("completed_topics", []))
                    for m in modules
                )
                history.append({
                    "date": now_str[:10],
                    "completed": current_completed,
                    "total": total_topics
                })
                update_study_plan(
                    plan["id"],
                    {
                        "modules_json": json.dumps(modules),
                        "progress_history": json.dumps(history[-30:])
                    }
                )
                st.session_state[changes_key] = False
                st.success("✅ Progress saved!")

            # ── Study Analytics ──────────────────────────────────
            st.markdown("---")
            st.markdown("#### 📊 Study Progress Analytics")

            # Module completion breakdown
            mod_names = []
            mod_pcts = []
            for m in modules:
                t = m.get("topics", [])
                c = m.get("completed_topics", [])
                mod_names.append(m.get("name", "?")[:20])
                mod_pcts.append(
                    round(len(c) / len(t) * 100) if t else 0
                )

            # Show module completion as metrics
            cols = st.columns(min(len(modules), 4))
            for idx, (name, pct) in enumerate(zip(mod_names, mod_pcts)):
                with cols[idx % len(cols)]:
                    emoji = "✅" if pct == 100 else (
                        "🔵" if pct > 0 else "⬜"
                    )
                    st.metric(
                        f"{emoji} {name}",
                        f"{pct}%"
                    )

            # Deadline tracker
            st.markdown("##### ⏰ Upcoming Deadlines")
            today = date.today()
            deadline_items = []
            for m in modules:
                dl = m.get("deadline")
                if dl:
                    dl_date = date.fromisoformat(dl)
                    days_left = (dl_date - today).days
                    c = m.get("completed_topics", [])
                    t = m.get("topics", [])
                    done = len(c) == len(t)
                    deadline_items.append((
                        m.get("name", "?"), dl_date,
                        days_left, done
                    ))

            if deadline_items:
                deadline_items.sort(key=lambda x: x[1])
                for name, dl_date, days_left, done in deadline_items:
                    if done:
                        st.markdown(
                            f"- ✅ ~~**{name}**~~ — Completed!"
                        )
                    elif days_left < 0:
                        st.markdown(
                            f"- 🚨 **{name}** — **Overdue** by "
                            f"{abs(days_left)} days!"
                        )
                    elif days_left == 0:
                        st.markdown(
                            f"- ⚠️ **{name}** — **Due today!**"
                        )
                    elif days_left <= 3:
                        st.markdown(
                            f"- 🟡 **{name}** — {days_left} days left "
                            f"(Due: {dl_date})"
                        )
                    else:
                        st.markdown(
                            f"- 🟢 **{name}** — {days_left} days left "
                            f"(Due: {dl_date})"
                        )
            else:
                st.caption("No deadlines set yet.")

            # Progress trend (from history if available)
            history_raw = plan.get("progress_history")
            if history_raw:
                try:
                    history = json.loads(history_raw)
                    if len(history) > 1:
                        st.markdown("##### 📈 Progress Over Time")
                        chart_data = {
                            h["date"]: round(
                                h["completed"] / h["total"] * 100
                            ) if h["total"] > 0 else 0
                            for h in history
                        }
                        st.line_chart(chart_data)

                        # Growth indicator
                        if len(history) >= 2:
                            prev = history[-2]["completed"]
                            curr = history[-1]["completed"]
                            diff = curr - prev
                            if diff > 0:
                                st.success(
                                    f"📈 **Growing!** "
                                    f"+{diff} topics since last save"
                                )
                            elif diff == 0:
                                st.info(
                                    "📊 No new topics since last save. "
                                    "Keep going!"
                                )
                            else:
                                st.warning(
                                    f"📉 {abs(diff)} topics unchecked "
                                    f"since last save"
                                )
                except (json.JSONDecodeError, KeyError):
                    pass

        # ══════════════════════════════════════════════════════════
        # PART 2: QUIZ & REVISION NOTES
        # ══════════════════════════════════════════════════════════
        with part2_tab:
            st.markdown("#### 📝 Quiz & Revision Notes")
            st.caption(
                "Select modules and topics below, then generate a "
                "quiz or download revision notes as PDF."
            )

            selected_topics_map = {}

            for mi, module in enumerate(modules):
                mod_name = module.get("name", f"Module {mi + 1}")
                topics = module.get("topics", [])

                select_mod = st.checkbox(
                    f"📦 **{mod_name}** ({len(topics)} topics)",
                    key=f"sel_{plan['id']}_{mi}",
                    value=False
                )

                if select_mod:
                    selected_in_mod = []
                    n_cols = min(len(topics), 3)
                    cols = st.columns(n_cols) if n_cols > 0 else [st]
                    for ti, topic in enumerate(topics):
                        with cols[ti % n_cols]:
                            if st.checkbox(
                                topic,
                                value=True,
                                key=f"sel_t_{plan['id']}_{mi}_{ti}"
                            ):
                                selected_in_mod.append(topic)
                    if selected_in_mod:
                        selected_topics_map[mod_name] = selected_in_mod

            total_selected = sum(
                len(t) for t in selected_topics_map.values()
            )

            if total_selected > 0:
                st.info(
                    f"✅ **{total_selected} topics selected** across "
                    f"**{len(selected_topics_map)} modules**"
                )

                act_col1, act_col2 = st.columns(2)

                with act_col1:
                    if st.button(
                        "📝 Start Quiz",
                        key=f"quiz_{plan['id']}",
                        type="primary",
                        use_container_width=True
                    ):
                        st.session_state.planner_quiz_mode = {
                            "selected_topics_map": selected_topics_map,
                            "plan_id": plan["id"],
                            "plan_name": plan_name_display
                        }
                        st.rerun()

                with act_col2:
                    if st.button(
                        "📝 Generate Revision Notes",
                        key=f"notes_{plan['id']}",
                        use_container_width=True
                    ):
                        st.session_state[
                            f"_gen_notes_{plan['id']}"
                        ] = selected_topics_map

                # Generate & show revision notes
                nk = f"_gen_notes_{plan['id']}"
                if nk in st.session_state:
                    sel_map = st.session_state[nk]
                    all_notes = []

                    for mod_name, tlist in sel_map.items():
                        with st.spinner(
                            f"Generating notes for {mod_name}..."
                        ):
                            notes_text = generate_revision_notes(
                                f"{mod_name}: {', '.join(tlist)}"
                            )
                            all_notes.append({
                                "module_name": mod_name,
                                "topics": tlist,
                                "notes": notes_text
                            })

                    for nd in all_notes:
                        st.markdown(f"### 📘 {nd['module_name']}")
                        st.caption(
                            f"Topics: {', '.join(nd['topics'])}"
                        )
                        st.markdown(nd["notes"])
                        st.markdown("---")

                    try:
                        from modules.pdf_export import (
                            generate_revision_pdf
                        )
                        pdf_bytes = generate_revision_pdf(all_notes)
                        plan_slug = plan_name_display[:20].replace(' ', '_')
                        st.download_button(
                            "⬇️ Download Revision Notes (PDF)",
                            data=pdf_bytes,
                            file_name=f"revision_{plan_slug}.pdf",
                            mime="application/pdf",
                            key=f"dl_rev_{plan['id']}"
                        )
                    except Exception as e:
                        st.error(f"PDF error: {e}")

                    del st.session_state[nk]

            else:
                st.caption(
                    "👆 Select at least one module to enable "
                    "quiz and revision notes."
                )

        # Delete plan
        st.markdown("---")
        if st.button(
            f"🗑️ Delete Plan: {plan_name_display}",
            key=f"del_plan_{plan['id']}"
        ):
            delete_study_plan(plan["id"])
            st.rerun()

        st.markdown("---")

    # ══════════════════════════════════════════════════════════════
    # PLANNER QUIZ MODE
    # ══════════════════════════════════════════════════════════════
    if st.session_state.planner_quiz_mode:
        quiz_info = st.session_state.planner_quiz_mode
        st.markdown("---")
        st.subheader("📝 Study Plan Quiz")

        all_selected = []
        for mod, topics in quiz_info["selected_topics_map"].items():
            all_selected.extend(topics)
            st.markdown(f"- **{mod}**: {', '.join(topics)}")

        if "_planner_mcqs" not in st.session_state:
            num_q = st.slider(
                "Number of questions",
                min_value=3, max_value=20, value=5,
                key="planner_q_num"
            )

            if st.button(
                "🎯 Generate Quiz", key="planner_gen_q",
                type="primary", use_container_width=True
            ):
                with st.spinner("Generating quiz..."):
                    topics_text = ", ".join(all_selected)
                    prompt = (
                        f"Generate exactly {num_q} multiple choice "
                        f"questions testing deep understanding of:\n"
                        f"{topics_text}\n\n"
                        f"Format:\n"
                        f"Q1: [question]\n"
                        f"A) [option]\nB) [option]\n"
                        f"C) [option]\nD) [option]\n"
                        f"ANSWER: [letter]\n"
                        f"EXPLANATION: [one sentence]\n\n"
                        f"Continue for all {num_q} questions."
                    )
                    raw = call_gemini(prompt)
                    parsed = parse_response(f"##MCQ##\n{raw}")
                    mcqs = parsed.get("mcqs", [])
                    if mcqs:
                        st.session_state._planner_mcqs = mcqs
                        st.rerun()
                    else:
                        st.warning("Could not generate quiz. Try again.")

        if "_planner_mcqs" in st.session_state:
            from modules.quiz import render_quiz
            plan_topic = quiz_info.get("plan_name", "Study Plan")
            render_quiz(
                st.session_state._planner_mcqs,
                plan_topic,
                username, "Undergraduate"
            )

        if st.button("← Back to Planner", key="back_planner"):
            # Clean up all quiz session state
            plan_topic = quiz_info.get("plan_name", "Study Plan")
            for key in list(st.session_state.keys()):
                if key in (
                    "_planner_mcqs", "planner_quiz_mode",
                    "last_quiz_results", "last_quiz_score",
                    f"_quiz_submitted_{plan_topic}",
                    f"_quiz_results_{plan_topic}",
                ):
                    del st.session_state[key]
                elif key.startswith(f"q_{plan_topic}_"):
                    del st.session_state[key]
            st.rerun()
