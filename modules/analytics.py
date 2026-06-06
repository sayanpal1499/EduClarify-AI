import streamlit as st
import plotly.graph_objects as go
from modules.database import get_quiz_history, get_topics_studied_today
from collections import defaultdict
from datetime import datetime, timedelta


def _create_score_bar_chart(avg_by_topic: dict) -> go.Figure:
    """Create a styled horizontal bar chart for score by topic."""
    topics = list(avg_by_topic.keys())
    scores = list(avg_by_topic.values())

    # Color-code bars by performance
    colors = []
    for s in scores:
        if s >= 80:
            colors.append("#4ade80")  # green
        elif s >= 60:
            colors.append("#818cf8")  # indigo
        elif s >= 40:
            colors.append("#fbbf24")  # amber
        else:
            colors.append("#f87171")  # red

    fig = go.Figure(go.Bar(
        x=scores,
        y=topics,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(255,255,255,0.1)", width=1),
            cornerradius=6,
        ),
        text=[f"{s}%" for s in scores],
        textposition="auto",
        textfont=dict(color="#ffffff", size=13, family="Inter"),
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="Inter", size=13),
        xaxis=dict(
            title="Average Score (%)",
            range=[0, 105],
            gridcolor="rgba(48,54,61,0.5)",
            zeroline=False,
        ),
        yaxis=dict(
            automargin=True,
            tickfont=dict(size=12),
        ),
        margin=dict(l=10, r=20, t=10, b=40),
        height=max(200, len(topics) * 50 + 60),
    )
    return fig


def _create_trend_line_chart(daily_avg: dict) -> go.Figure:
    """Create a styled area chart for 7-day score trend."""
    days = list(daily_avg.keys())
    scores = list(daily_avg.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=scores,
        mode="lines+markers+text",
        text=[f"{s}%" for s in scores],
        textposition="top center",
        textfont=dict(color="#a5b4fc", size=12),
        line=dict(color="#818cf8", width=3, shape="spline"),
        marker=dict(size=10, color="#a5b4fc", line=dict(color="#6366f1", width=2)),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.1)",
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="Inter", size=13),
        xaxis=dict(
            gridcolor="rgba(48,54,61,0.3)",
            zeroline=False,
        ),
        yaxis=dict(
            title="Score (%)",
            range=[0, 105],
            gridcolor="rgba(48,54,61,0.3)",
            zeroline=False,
        ),
        margin=dict(l=10, r=20, t=10, b=40),
        height=300,
    )
    return fig


def _create_difficulty_pie(history: list) -> go.Figure:
    """Create a donut chart showing difficulty distribution of sessions."""
    diff_counts = defaultdict(int)
    for h in history:
        diff_counts[h.get("difficulty_used", "Unknown")] += 1

    labels = list(diff_counts.keys())
    values = list(diff_counts.values())
    colors = ["#4ade80", "#818cf8", "#f472b6", "#fbbf24", "#38bdf8"]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors[:len(labels)], line=dict(color="#0d1117", width=2)),
        textfont=dict(color="#e2e8f0", size=13),
        textinfo="label+percent",
        hoverinfo="label+value+percent",
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="Inter", size=13),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        showlegend=False,
    )
    return fig


def _create_accuracy_gauge(avg: float) -> go.Figure:
    """Create a gauge chart showing overall accuracy."""
    if avg >= 80:
        bar_color = "#4ade80"
    elif avg >= 60:
        bar_color = "#818cf8"
    elif avg >= 40:
        bar_color = "#fbbf24"
    else:
        bar_color = "#f87171"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg,
        number=dict(suffix="%", font=dict(size=36, color="#e2e8f0")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#6e7681", dtick=20),
            bar=dict(color=bar_color, thickness=0.75),
            bgcolor="rgba(22,27,34,0.8)",
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color="rgba(248,113,113,0.15)"),
                dict(range=[40, 60], color="rgba(251,191,36,0.15)"),
                dict(range=[60, 80], color="rgba(129,140,248,0.15)"),
                dict(range=[80, 100], color="rgba(74,222,128,0.15)"),
            ],
            threshold=dict(
                line=dict(color="#e2e8f0", width=2),
                thickness=0.8, value=avg,
            ),
        ),
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", family="Inter"),
        margin=dict(l=30, r=30, t=30, b=10),
        height=220,
    )
    return fig


def render_analytics(username: str, study_goal: int):
    """Render the full analytics dashboard."""
    st.subheader("📊 Learning Analytics")

    history = get_quiz_history(username)
    if not history:
        st.info("🎓 Complete your first quiz to see analytics here!")
        return

    # ── Summary Metrics ──────────────────────────────────────────
    total = len(history)
    avg = round(sum(h["pct"] for h in history) / total, 1)
    best = max(history, key=lambda x: x["pct"])
    worst = min(history, key=lambda x: x["pct"])
    today_count = get_topics_studied_today(username)

    # Top-level stats in styled columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Total Sessions", total)
    col2.metric("📈 Avg Score", f"{avg}%")
    col3.metric("🏆 Best Topic", best["topic"][:18], f"↑ {best['pct']}%")
    col4.metric("📅 Today's Progress", f"{today_count}/{study_goal}")

    # Daily goal progress bar
    st.progress(
        min(today_count / study_goal, 1.0),
        text=f"Daily Goal: {today_count}/{study_goal} topics"
    )

    st.markdown("---")

    # ── Row 1: Accuracy Gauge + Difficulty Distribution ──────────
    st.markdown("### 🎯 Performance Overview")
    gauge_col, pie_col = st.columns(2)

    with gauge_col:
        st.markdown("**Overall Accuracy**")
        fig_gauge = _create_accuracy_gauge(avg)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    with pie_col:
        st.markdown("**Difficulty Distribution**")
        fig_pie = _create_difficulty_pie(history)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")

    # ── Row 2: Score by Topic ────────────────────────────────────
    st.markdown("### 📊 Score by Topic")
    topic_scores = defaultdict(list)
    for h in history:
        topic_scores[h["topic"][:30]].append(h["pct"])
    avg_by_topic = {
        t: round(sum(s) / len(s)) for t, s in topic_scores.items()
    }

    fig_bar = _create_score_bar_chart(avg_by_topic)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")

    # ── Row 3: 7-Day Score Trend ─────────────────────────────────
    st.markdown("### 📈 7-Day Score Trend")
    daily = defaultdict(list)
    for h in history:
        day = h["attempted_at"][:10]
        daily[day].append(h["pct"])
    daily_avg = {
        d: round(sum(v) / len(v))
        for d, v in sorted(daily.items())[-7:]
    }
    if len(daily_avg) > 1:
        fig_line = _create_trend_line_chart(daily_avg)
        st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
    else:
        st.caption("📅 Study across multiple days to see the trend chart.")

    st.markdown("---")

    # ── Row 4: Weak Topics + Strengths ───────────────────────────
    st.markdown("### 🔍 Strengths & Weaknesses")
    weak_col, strong_col = st.columns(2)

    weak = [(t, s) for t, s in avg_by_topic.items() if s < 60]
    strong = [(t, s) for t, s in avg_by_topic.items() if s >= 80]

    with weak_col:
        st.markdown("**⚠️ Needs Improvement (< 60%)**")
        if weak:
            for topic, score in sorted(weak, key=lambda x: x[1]):
                st.markdown(
                    f"- 🔴 **{topic}** — {score}%"
                )
        else:
            st.success("✅ No weak topics! Great work!")

    with strong_col:
        st.markdown("**💪 Strengths (≥ 80%)**")
        if strong:
            for topic, score in sorted(strong, key=lambda x: x[1], reverse=True):
                st.markdown(
                    f"- 🟢 **{topic}** — {score}%"
                )
        else:
            st.info("Keep studying — you'll get there! 💪")

    st.markdown("---")

    # ── Row 5: Quick Stats Summary ───────────────────────────────
    st.markdown("### 📋 Quick Stats")
    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        total_questions = sum(h["total"] for h in history)
        total_correct = sum(h["score"] for h in history)
        st.metric("✏️ Questions Attempted", total_questions)
    with stat2:
        st.metric("✅ Correct Answers", total_correct)
    with stat3:
        streak_days = len(set(h["attempted_at"][:10] for h in history))
        st.metric("🔥 Active Days", streak_days)

    st.markdown("---")

    # ── Session Log ──────────────────────────────────────────────
    with st.expander("📜 Full Session Log", expanded=False):
        for i, h in enumerate(history, 1):
            dt = h["attempted_at"][:16].replace("T", " ")
            pct_val = h["pct"]
            emoji = "🟢" if pct_val >= 80 else ("🟡" if pct_val >= 60 else "🔴")
            st.markdown(
                f"{i}. {emoji} **{h['topic']}** — "
                f"{h['score']}/{h['total']} ({pct_val}%) "
                f"| 📅 {dt} | 🎯 {h.get('difficulty_used', 'N/A')}"
            )
