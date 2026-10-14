
import streamlit as st
from graph import app

st.set_page_config(
    page_title=" AI Meeting Notes Analyzer",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f7f8fc;
    color: #20243a;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu, footer {
    visibility: hidden;
}
.hero {
    background: linear-gradient(115deg, #6c63ff, #9b6dff);
    padding: 34px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
}
.hero h1 {
    font-size: 38px;
    font-weight: 750;
    color: white;
    margin: 8px 0;
}
.hero p {
    color: #f0edff;
    font-size: 16px;
}
.eyebrow {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #e5deff;
}
.section-title {
    font-size: 23px;
    font-weight: 700;
    color: #272747;
    margin-top: 18px;
    margin-bottom: 8px;
}
.section-card {
    background: white;
    border: 1px solid #e8eaf3;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 4px 16px rgba(40, 40, 90, 0.04);
}
.section-card h3 {
    color: #5146c8;
    margin-top: 0;
    font-size: 19px;
}
.stTextArea textarea {
    background: white !important;
    color: #24243a !important;
    border: 1px solid #dfe2ef !important;
    border-radius: 13px !important;
    font-size: 15px !important;
}
.stButton button {
    border-radius: 11px;
    min-height: 46px;
    font-weight: 650;
    border: 1px solid #dedbff;
}
div.stButton > button[kind="primary"] {
    background: #6c63ff;
    color: white;
    border: none;
}
div.stButton > button[kind="primary"]:hover {
    background: #5548e8;
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e8eaf3;
    border-radius: 15px;
    padding: 18px;
}
div[data-testid="stMetricLabel"] {
    color: #777b93;
}
div[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #ececf5;
}
hr {
    border-color: #e8eaf3;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✨ MeetMind AI")
    st.caption("Your intelligent meeting assistant")
    st.divider()
    st.markdown("### How it works")
    st.write("**01** · Paste your transcript")
    st.write("**02** · Let AI analyze it")
    st.write("**03** · Review your meeting report")
    st.divider()
    st.caption("Powered by LangGraph + OpenAI")

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR AI MEETING ASSISTANT</div>
    <h1>Make every meeting count.</h1>
    <p>Get the key points, clear action items and task priorities — all in one place.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">📝 Meeting Transcript</div>',
            unsafe_allow_html=True)
st.write("Paste your meeting conversation below to generate an AI-powered report.")

transcript = st.text_area(
    "Meeting transcript",
    placeholder="Paste your transcript here...\n\nExample:\nJohn: We need to launch the website by Friday.\nSarah: I will finish the homepage tomorrow.\nDavid: I will test the website this week.",
    height=230,
    label_visibility="collapsed",
    key="meeting_transcript"
)

left, right = st.columns([3, 1])

with left:
    analyze = st.button(
        "✨  Analyze Meeting",
        type="primary",
        use_container_width=True
    )

with right:
    st.button(
        "↻  Clear",
        use_container_width=True,
        on_click=lambda: st.session_state.update(
            meeting_transcript=""
        )
    )

if analyze:
    if not transcript.strip():
        st.warning("Please paste a meeting transcript first.")
    else:
        try:
            with st.spinner("Analyzing your meeting..."):
                result = app.invoke({"transcript": transcript})

            st.session_state["meeting_result"] = result

        except Exception as e:
            st.error(f"Something went wrong: {e}")

if "meeting_result" in st.session_state:
    result = st.session_state["meeting_result"]
    no_actions = "NO ACTION ITEMS" in result["actions"].upper()

    st.divider()
    st.markdown("## 📊 Your Meeting Report")
    st.caption("Here is the breakdown of your meeting.")

    a, b, c = st.columns(3)

    with a:
        st.metric("Key Topics", "Ready")

    with b:
        st.metric("Action Items", "None" if no_actions else "Found")

    with c:
        st.metric(
            "Priority Level",
            "N/A" if no_actions else result["priority"]
        )

    st.markdown("""
    <div class="section-card">
        <h3>📄 Meeting Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    st.write(result["summary"])

    st.markdown("""
    <div class="section-card">
        <h3>🎯 Key Topics</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(result["topics"])

    st.markdown("""
    <div class="section-card">
        <h3>✅ Action Items</h3>
    </div>
    """, unsafe_allow_html=True)

    if no_actions:
        st.info("No action items identified in this meeting.")
        st.write("No task owners identified.")
    else:
        st.markdown(result["actions"])

        st.markdown("""
        <div class="section-card">
            <h3>👥 Task Owners</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(result["actions"])

        st.markdown("""
        <div class="section-card">
            <h3>⚡ Priority Level</h3>
        </div>
        """, unsafe_allow_html=True)
        st.write(result["priority"])

    st.divider()
    st.caption("MeetMind AI · Smarter meetings, simpler work.")