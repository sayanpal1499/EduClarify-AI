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
from modules.pdf_export import generate_learning_pdf

# ─── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduClarify AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Study-Friendly Theme CSS ─────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import font ───────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Animations ────────────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 8px rgba(251,191,36,0.3); }
        50%      { box-shadow: 0 0 18px rgba(251,191,36,0.6); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes slideDown {
        from { opacity: 0; max-height: 0; }
        to   { opacity: 1; max-height: 2000px; }
    }

    /* ── Global ────────────────────────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: #0b0f14;
        color: #e0e6ed;
    }
    [data-testid="stAppViewContainer"] > .main {
        background: #0b0f14;
        animation: fadeInUp 0.5s ease-out;
    }

    /* ── Typography ────────────────────────────────────────────── */
    .stMarkdown p, .stMarkdown li {
        font-size: 16px !important;
        line-height: 1.9 !important;
        color: #e0e6ed !important;
    }
    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.5em !important;
        margin-bottom: 1em !important;
    }
    .stMarkdown li {
        margin-bottom: 8px !important;
    }
    .stMarkdown strong {
        color: #f0f4f8 !important;
        font-weight: 700 !important;
    }
    .stCaption, .stMarkdown .stCaption {
        font-size: 13px !important;
        color: #8b949e !important;
    }

    /* ── Sidebar ───────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #131920 0%, #0b0f14 100%);
        border-right: 1px solid #1c2128;
        padding-top: 0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #1c2128 !important;
        margin: 16px 0 !important;
    }

    /* Sidebar custom elements */
    .sb-app-name {
        font-size: 26px; font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #818cf8 50%, #6366f1 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: -0.5px;
        padding: 8px 0 2px; margin-bottom: 0;
    }
    .sb-section-title {
        font-size: 11px; font-weight: 700;
        color: #6e7681 !important;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 20px 0 8px; padding: 0;
    }
    .sb-user-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #21262d; border-radius: 14px;
        padding: 16px 18px; margin: 12px 0;
    }
    .sb-username {
        font-size: 20px; font-weight: 700;
        color: #f0f4f8; margin-bottom: 4px;
    }
    .sb-streak {
        display: inline-block;
        font-size: 16px; font-weight: 800; color: #fbbf24;
        background: rgba(251,191,36,0.12);
        padding: 6px 16px; border-radius: 10px;
        margin-top: 6px;
        animation: pulse-glow 2.5s ease-in-out infinite;
    }

    /* ── Headers ───────────────────────────────────────────────── */
    h1 {
        color: #f0f4f8 !important;
        font-weight: 900 !important;
        font-size: 2.4rem !important;
        letter-spacing: -0.8px;
    }
    h2 {
        color: #e0e6ed !important;
        font-weight: 700 !important;
        font-size: 1.55rem !important;
    }
    h3 {
        color: #d0d7de !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
    }

    /* ── Tabs ──────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: #131920;
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
        border: 1px solid #1c2128;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 600;
        padding: 11px 24px;
        border-radius: 10px;
        color: #8b949e;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #e0e6ed;
        background: #1c2333;
    }
    .stTabs [aria-selected="true"] {
        color: #a5b4fc !important;
        background: #1c2333 !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ── Buttons ───────────────────────────────────────────────── */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        padding: 11px 26px;
        border: 1px solid #30363d;
        background: #161b22;
        color: #e0e6ed;
        font-size: 15px;
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        background: #1c2333;
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #818cf8 50%, #a78bfa 100%);
        background-size: 200% auto;
        border: none;
        color: #fff;
        font-weight: 700;
        font-size: 16px;
        animation: shimmer 3s linear infinite;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #818cf8 100%);
        background-size: 200% auto;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    /* ── Text Inputs ──────────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-family: 'Inter', sans-serif;
        background: #131920 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px;
        color: #e0e6ed !important;
        padding: 14px 18px;
        font-size: 16px !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stSlider label, .stFileUploader label {
        color: #b0bec5 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    /* ── Metric Cards ──────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: #131920;
        border: 1px solid #1c2128;
        border-radius: 14px;
        padding: 18px;
        transition: all 0.25s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: #30363d;
        transform: translateY(-1px);
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #f0f4f8 !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }

    /* ── Expander — DARK BACKGROUND FIX ───────────────────────── */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 16px !important;
        background: #131920 !important;
        border-radius: 12px;
        border: 1px solid #1c2128 !important;
        color: #e0e6ed !important;
        padding: 16px 20px;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        background: #1c2333 !important;
        border-color: #30363d !important;
    }
    .streamlit-expanderContent {
        background: #0f1419 !important;
        border: 1px solid #1c2128 !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px 24px !important;
        animation: slideDown 0.3s ease-out;
    }
    /* Fix for newer Streamlit expander selectors */
    details {
        background: #131920 !important;
        border: 1px solid #1c2128 !important;
        border-radius: 12px !important;
        margin-bottom: 10px;
    }
    details summary {
        background: #131920 !important;
        color: #e0e6ed !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
    }
    details summary:hover {
        background: #1c2333 !important;
    }
    details[open] summary {
        border-radius: 12px 12px 0 0 !important;
        border-bottom: 1px solid #1c2128 !important;
    }
    details > div {
        background: #0f1419 !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px 24px !important;
    }
    details > div p, details > div li, details > div span {
        color: #e0e6ed !important;
    }

    /* ── Tooltip / hover text fix ──────────────────────────────── */
    [data-testid="stTooltipContent"] {
        background: #1c2333 !important;
        color: #e0e6ed !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="tooltip"] {
        background: #1c2333 !important;
        color: #e0e6ed !important;
    }

    /* ── Info / Warning / Success / Error ──────────────────────── */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    .stAlert [data-testid="stMarkdownContainer"] p,
    .stAlert [data-testid="stMarkdownContainer"] span {
        color: #f0f4f8 !important;
        font-size: 15.5px !important;
    }
    [data-testid="stNotification"] {
        border-radius: 12px !important;
    }

    /* ── File Uploader ─────────────────────────────────────────── */
    [data-testid="stFileUploader"] {
        background: #131920;
        border-radius: 12px;
        border: 2px dashed #30363d;
        padding: 18px;
        transition: border-color 0.25s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }

    /* ── Progress Bar ──────────────────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1, #818cf8, #a78bfa);
        border-radius: 8px;
    }

    /* ── Radio Buttons ─────────────────────────────────────────── */
    .stRadio > div {
        gap: 8px;
    }
    .stRadio label {
        font-family: 'Inter', sans-serif;
        font-size: 15px !important;
        padding: 6px 8px;
        border-radius: 10px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        color: #e0e6ed !important;
    }
    /* Target the actual option text in the radio group */
    .stRadio [role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        color: #e0e6ed !important;
        font-size: 16px !important;
    }
    .stRadio label:hover {
        background: #1c2333;
        border-color: #30363d;
    }

    /* ── Slider ────────────────────────────────────────────────── */
    .stSlider > div > div > div[role="slider"] {
        background: #6366f1;
    }

    /* ── Number Input ──────────────────────────────────────────── */
    .stNumberInput input {
        background: #131920 !important;
        color: #e0e6ed !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-size: 16px !important;
    }

    /* ── Select Slider ─────────────────────────────────────────── */
    .stSlider label {
        font-size: 14px !important;
    }

    /* ── Download Button ───────────────────────────────────────── */
    .stDownloadButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 12px;
        background: #131920;
        border: 1px solid #30363d;
        color: #e0e6ed;
        transition: all 0.25s ease;
    }
    .stDownloadButton > button:hover {
        background: #1c2333;
        border-color: #6366f1;
        transform: translateY(-1px);
    }

    /* ── Checkbox ──────────────────────────────────────────────── */
    .stCheckbox label div[data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #e0e6ed !important;
    }
    .stCheckbox label span {
        font-size: 16px !important;
    }

    /* ── Dividers ──────────────────────────────────────────────── */
    hr {
        border: none;
        border-top: 1px solid #1c2128;
        margin: 28px 0;
    }

    /* ── Welcome Card ──────────────────────────────────────────── */
    .welcome-card {
        background: linear-gradient(135deg, #131920 0%, #1c2333 50%, #1a1f2e 100%);
        border: 1px solid #21262d;
        border-radius: 24px;
        padding: 64px 48px 52px;
        text-align: center;
        max-width: 540px;
        margin: 80px auto 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    .welcome-card::before {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #818cf8, #a78bfa, #818cf8, #6366f1);
        background-size: 200% auto;
        border-radius: 24px 24px 0 0;
        animation: shimmer 3s linear infinite;
    }
    .welcome-card .app-icon { font-size: 64px; margin-bottom: 14px; display: block; }
    .welcome-card .app-title {
        font-size: 40px; font-weight: 900;
        color: #f0f4f8; margin-bottom: 6px;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #a78bfa 0%, #818cf8 50%, #6366f1 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .welcome-card .app-subtitle {
        color: #8b949e; font-size: 16px;
        margin-bottom: 36px; line-height: 1.7;
    }

    /* ── Feature Cards ─────────────────────────────────────────── */
    .feature-card {
        background: linear-gradient(135deg, #131920 0%, #1c2333 100%);
        border: 1px solid #1c2128;
        border-radius: 16px;
        padding: 30px 24px;
        text-align: center;
        transition: all 0.35s ease;
        height: 100%;
    }
    .feature-card:hover {
        border-color: #6366f1;
        transform: translateY(-4px);
        box-shadow: 0 14px 36px rgba(99, 102, 241, 0.15);
    }
    .feature-icon { font-size: 40px; margin-bottom: 16px; }
    .feature-title {
        font-weight: 700; font-size: 16px;
        color: #f0f4f8; margin-bottom: 10px;
    }
    .feature-desc {
        font-size: 14px; color: #8b949e; line-height: 1.65;
    }

    /* ── Scrollbar ─────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0b0f14; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #6e7681; }

    /* ── Hide Streamlit Branding ───────────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background-color: transparent !important;}
</style>
""", unsafe_allow_html=True)


# ─── Username Gate ────────────────────────────────────────────────────
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.markdown("""
    <div class="welcome-card">
        <span class="app-icon">🎓</span>
        <div class="app-title">EduClarify AI</div>
        <p class="app-subtitle">
            Your AI-powered adaptive learning companion.<br>
            Upload a syllabus, get structured explanations,<br>
            take smart quizzes, and track your mastery.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        name_input = st.text_input(
            "Enter your name or student ID",
            max_chars=30,
            placeholder="e.g. Sayan or STU2023001",
            label_visibility="collapsed"
        )
        if st.button(
            "Start Learning →", type="primary", use_container_width=True
        ) and name_input.strip():
            username = name_input.strip().lower().replace(" ", "_")
            user = get_or_create_user(username)
            st.session_state.username = username
            st.session_state.difficulty = user.get(
                "difficulty_level", "Undergraduate"
            )
            st.session_state.study_goal = user.get("study_goal", 3)
            st.session_state.streak = user.get("streak", 0)
            st.rerun()
    st.stop()


# ─── Load user from session ───────────────────────────────────────────
username   = st.session_state.username
difficulty = st.session_state.get("difficulty", "Undergraduate")
study_goal = st.session_state.get("study_goal", 3)
streak     = st.session_state.get("streak", 0)


# ─── Sidebar (categorized, fully utilized) ────────────────────────────
with st.sidebar:
    # App branding
    st.markdown(
        '<p class="sb-app-name">🎓 EduClarify AI</p>',
        unsafe_allow_html=True
    )

    # User profile card
    st.markdown(
        '<p class="sb-section-title">👤 Profile</p>',
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div class="sb-user-card">
        <div class="sb-username">{username}</div>
        <div class="sb-streak">🔥 {streak} day{"s" if streak != 1 else ""} streak</div>
    </div>
    """, unsafe_allow_html=True)

    # Study settings
    st.markdown(
        '<p class="sb-section-title">⚙️ Study Settings</p>',
        unsafe_allow_html=True
    )
    new_difficulty = st.select_slider(
        "🎯 Explanation Depth",
        options=DIFFICULTY_LEVELS,
        value=difficulty
    )
    if new_difficulty != difficulty:
        st.session_state.difficulty = new_difficulty
        update_user_preference(username, "difficulty_level", new_difficulty)

    new_goal = st.number_input(
        "📅 Daily Topic Goal",
        min_value=1, max_value=20, value=study_goal
    )
    if new_goal != study_goal:
        st.session_state.study_goal = new_goal
        update_user_preference(username, "study_goal", new_goal)

    # Review reminders
    st.markdown(
        '<p class="sb-section-title">🔁 Revision Reminders</p>',
        unsafe_allow_html=True
    )
    render_due_for_review(username)


# ─── Header ───────────────────────────────────────────────────────────
st.title("🎓 EduClarify AI")
st.markdown(
    "*Paste any topic or syllabus text. Instant explanations, "
    "concept map, quiz, and progress tracking.*"
)
st.markdown("---")


# ─── Tabs (top-level navigation) ──────────────────────────────────────
main_tab, planner_tab, library_tab, analytics_tab = st.tabs([
    "🧠 Learn", "📋 Study Planner", "📚 My Library", "📊 Analytics"
])


# ══════════════════════════════════════════════════════════════════════
# LEARN TAB
# ══════════════════════════════════════════════════════════════════════
with main_tab:

    # Load PDF text into the widget key BEFORE the widget renders
    if "_pdf_text_to_load" in st.session_state:
        st.session_state.input_text = st.session_state.pop("_pdf_text_to_load")

    # Input section
    col_text, col_pdf = st.columns([2, 1])
    with col_text:
        user_text = st.text_area(
            "📋 Paste topic or syllabus text",
            placeholder=(
                "e.g. 'Explain Deadlock in Operating Systems'\n"
                "or paste a full syllabus unit here..."
            ),
            height=160, key="input_text"
        )
    with col_pdf:
        st.markdown("**Or upload a PDF syllabus:**")
        pdf_file = st.file_uploader(
            "Upload PDF", type=["pdf"], label_visibility="collapsed"
        )
        if pdf_file:
            extracted = extract_text_from_pdf(pdf_file)
            st.success(f"✅ Extracted {len(extracted)} chars from PDF.")
            if not user_text.strip():
                st.session_state._pdf_text_to_load = extracted
                st.rerun()

    final_input = user_text.strip() if user_text else ""

    clarify = st.button(
        "✨ Clarify This Topic", type="primary",
        use_container_width=True
    )

    if clarify and final_input:
        with st.spinner("🧠 Analyzing with AI..."):
            prompt = build_prompt(final_input, st.session_state.difficulty)
            raw = call_gemini(prompt)
            if raw.startswith("ERROR:"):
                st.error(f"API Error: {raw}")
            else:
                parsed = parse_response(raw)
                st.session_state.last_parsed = parsed
                st.session_state.last_topic = final_input[:60]
                st.session_state.last_full_input = final_input
    elif clarify:
        st.warning("Please enter a topic or upload a PDF first.")

    # ── Output ──────────────────────────────────────────────────────
    if "last_parsed" in st.session_state:
        parsed     = st.session_state.last_parsed
        topic      = st.session_state.last_topic
        difficulty = st.session_state.difficulty

        st.markdown("---")
        t1, t2, t3 = st.tabs([
            "📖 Explanations", "🗺️ Concept Map", "📝 Quiz"
        ])

        # ── Explanations Tab ──────────────────────────────────────
        with t1:
            st.subheader("📖 Layered Explanations")

            for exp_label, key, color in [
                ("🟢 Beginner — ELI5 (Analogy)",     "eli5",       "#4ade80"),
                ("🔵 Conceptual — Core Mechanism",   "conceptual", "#38bdf8"),
                ("🔴 Expert — Technical Depth",       "expert",     "#f472b6"),
            ]:
                with st.expander(exp_label, expanded=(key == "eli5")):
                    content = parsed.get(key, "")
                    st.markdown(content)
                    fb_col1, fb_col2, _ = st.columns([1, 1, 6])
                    with fb_col1:
                        if st.button("👍", key=f"up_{key}_{topic}"):
                            st.toast("Thanks for the feedback!")
                    with fb_col2:
                        if st.button(
                            "👎 Regenerate", key=f"down_{key}_{topic}"
                        ):
                            with st.spinner("Regenerating explanation..."):
                                regen_prompt = build_regenerate_prompt(
                                    st.session_state.last_topic, difficulty
                                )
                                regen_raw = call_gemini(regen_prompt)
                                regen_parsed = parse_response(regen_raw)
                                if regen_parsed.get(key):
                                    st.session_state.last_parsed[key] = (
                                        regen_parsed[key]
                                    )
                                    st.rerun()

            st.markdown("---")
            st.subheader("✅ Prerequisites")
            prereq_content = parsed.get("prerequisites", "")
            st.markdown(prereq_content)

            st.markdown("---")

            # Action buttons row
            action_col1, action_col2, action_col3 = st.columns(3)
            with action_col1:
                save_button(username, topic, parsed)
            with action_col2:
                if st.button(
                    "📋 Add to Study Plan",
                    key=f"add_plan_{topic}",
                    type="primary"
                ):
                    st.session_state._add_to_plan = True
                    st.session_state._plan_input = st.session_state.get(
                        "last_full_input", final_input
                    )
            with action_col3:
                pdf_bytes = generate_learning_pdf(topic, parsed)
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=(
                        f"educlarify_{topic[:30].replace(' ', '_')}.pdf"
                    ),
                    mime="application/pdf"
                )

            # Handle study plan addition
            if st.session_state.get("_add_to_plan"):
                with st.spinner("🧠 Parsing syllabus into modules..."):
                    try:
                        from modules.syllabus_parser import parse_syllabus
                        from modules.database import save_study_plan
                        import json
                        from datetime import date, timedelta

                        plan_input = st.session_state.get("_plan_input", "")
                        result = parse_syllabus(plan_input)
                        if result.get("modules"):
                            # Auto-assign deadlines
                            today = date.today()
                            for i, mod in enumerate(result["modules"]):
                                mod["deadline"] = (
                                    today + timedelta(days=(i + 1) * 3)
                                ).isoformat()

                            plan_data = {
                                "plan_name": topic[:50],
                                "modules_json": json.dumps(result["modules"]),
                                "strategy": result.get("strategy", ""),
                                "syllabus_text": plan_input[:5000]
                            }
                            save_study_plan(username, plan_data)
                            st.success(
                                f"✅ Added {len(result['modules'])} modules "
                                f"to your Study Plan! "
                                f"Check the 📋 Study Planner tab."
                            )
                        else:
                            st.warning(
                                "Could not parse modules from the input. "
                                "Try providing more structured text."
                            )
                    except Exception as e:
                        st.error(f"Error adding to plan: {e}")
                    finally:
                        st.session_state._add_to_plan = False

        # ── Concept Map Tab ───────────────────────────────────────
        with t2:
            st.subheader("🗺️ Learning Roadmap")
            st.caption(
                "Follow the steps below to trace concept dependencies. "
                "Start from Step 1."
            )
            concept_content = parsed.get("concept_graph", "")
            st.markdown(concept_content)

        # ── Quiz Tab ──────────────────────────────────────────────
        with t3:
            st.subheader("📝 Quick Quiz")
            st.caption(
                "Test your understanding on the entire topic. "
                "For topic-specific quizzes, use the Study Planner tab."
            )

            if "_active_quiz" not in st.session_state:
                num_questions = st.slider(
                    "Number of questions",
                    min_value=3, max_value=20, value=5,
                    key="quiz_num_slider"
                )

                if st.button(
                    "🎯 Generate Quiz", key="gen_quiz_btn",
                    type="primary", use_container_width=True
                ):
                    with st.spinner("Generating quiz questions..."):
                        quiz_prompt = build_prompt(
                            topic,
                            st.session_state.difficulty,
                            num_questions=num_questions,
                            avoid_repetition=True
                        )
                        quiz_raw = call_gemini(quiz_prompt)
                        if not quiz_raw.startswith("ERROR:"):
                            quiz_parsed = parse_response(quiz_raw)
                            new_mcqs = quiz_parsed.get("mcqs", [])
                            if new_mcqs:
                                st.session_state._active_quiz = new_mcqs
                                st.rerun()
                            else:
                                st.warning(
                                    "Could not generate questions. Try again."
                                )
                        else:
                            st.error(f"API Error: {quiz_raw}")

            # Render active quiz
            if "_active_quiz" in st.session_state:
                st.markdown("---")
                render_quiz(
                    st.session_state._active_quiz,
                    topic, username, difficulty
                )

    else:
        # Landing feature cards
        st.markdown("### What EduClarify Does For You")
        st.markdown("")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📖</div>
                <div class="feature-title">3-Layer Explanations</div>
                <div class="feature-desc">
                    ELI5 → Conceptual → Expert, auto-calibrated to your level
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🗺️</div>
                <div class="feature-title">Concept Map</div>
                <div class="feature-desc">
                    Visual learning roadmap of all sub-concepts
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Smart Quiz</div>
                <div class="feature-desc">
                    Custom questions, topic filtering, non-repeating
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Study Planner</div>
                <div class="feature-desc">
                    Break syllabus into modules, track progress, master topics
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# STUDY PLANNER TAB
# ══════════════════════════════════════════════════════════════════════
with planner_tab:
    try:
        from modules.study_planner import render_study_planner
        render_study_planner(username)
    except ImportError:
        st.info("📋 Study Planner is being set up. Please refresh in a moment.")
    except Exception as e:
        st.error(f"Study Planner error: {e}")


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
