"""
AutoResearch Agent - Streamlit UI (Alternative)

For users who prefer Streamlit over Chainlit.

Run:
    streamlit run ui/streamlit_app.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from agents import ResearchAgent


st.set_page_config(
    page_title="AutoResearch Agent",
    page_icon="🔬",
    layout="wide",
)


# Custom CSS for polished look
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        background: linear-gradient(135deg, #7B61FF 0%, #9D87FF 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .source-card {
        background: rgba(123, 97, 255, 0.05);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #7B61FF;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">AutoResearch Agent</h1>
    <p style="color: white; opacity: 0.9; margin: 0.5rem 0 0 0;">
        AI-powered research with autonomous multi-tool reasoning
    </p>
</div>
""", unsafe_allow_html=True)

st.info("**Note:** For the best experience, try the Chainlit UI: `chainlit run ui/chainlit_app.py -w`")


@st.cache_resource
def load_agent():
    return ResearchAgent()


with st.sidebar:
    st.title("Settings")
    
    show_plan = st.checkbox("Show research plan", value=True)
    show_steps = st.checkbox("Show research steps", value=False)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    AutoResearch Agent uses:
    - LangGraph (agent framework)
    - Google Gemini 2.5 Flash
    - Tavily AI Search
    
    [GitHub](https://github.com/your-username/autoresearch-agent)
    """)


if "agent" not in st.session_state:
    with st.spinner("Loading agent..."):
        try:
            st.session_state.agent = load_agent()
        except Exception as e:
            st.error(f"Failed: {e}")
            st.info("Setup .env file with API keys. See QUICKSTART.md.")
            st.stop()


st.markdown("### Sample Queries")
col1, col2, col3 = st.columns(3)

samples = [
    "Latest AI agent trends 2026",
    "Quantum computing breakthroughs",
    "LLM fine-tuning best practices",
]

for col, query in zip([col1, col2, col3], samples):
    if col.button(query, use_container_width=True):
        st.session_state.pending_query = query


st.markdown("### Research Query")
user_query = st.text_input("What would you like to research?", placeholder="e.g., AI agent frameworks 2026")

if "pending_query" in st.session_state:
    user_query = st.session_state.pending_query
    del st.session_state.pending_query


if st.button("Start Research", type="primary", use_container_width=True) and user_query:
    
    with st.spinner("Researching..."):
        try:
            result = st.session_state.agent.research(user_query)
            
            st.success("Research complete!")
            
            if show_plan and result.get("plan"):
                with st.expander("Research Plan"):
                    st.markdown(result["plan"])
            
            st.markdown("---")
            st.markdown("## Research Report")
            st.markdown(result["report"])
            
            if result.get("sources"):
                st.markdown("---")
                st.markdown("### Sources")
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>[{i}] {source.get('title', 'Untitled')}</strong><br/>
                        <a href="{source.get('url', '#')}">{source.get('url', '')}</a>
                    </div>
                    """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Iterations", result.get("iterations", 0))
            col2.metric("Sources", len(result.get("sources", [])))
            col3.metric("Status", "Complete")
            
        except Exception as e:
            st.error(f"Research failed: {e}")
