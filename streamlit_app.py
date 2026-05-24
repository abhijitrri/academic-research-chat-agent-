"""Main Streamlit dashboard for AI Research Collaborator Agent."""
import streamlit as st
import pandas as pd
from src.config.settings import settings

# Page configuration
st.set_page_config(
    page_title="AI Research Collaborator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background
st.markdown("""
    <style>
        .main {
            background-image: url('file:///Users/abhijitghosh/projects/academic-research-chat-agent-/SNB.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            opacity: 0.95;
        }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📚 AI Research Collaborator Agent")
st.markdown("---")
st.write("Discover research papers, researchers, and insights in your field of interest.")

# Sidebar for input parameters
with st.sidebar:
    st.header("🔍 Research Parameters")

    # Research topic input
    research_topic = st.text_input(
        label="Research Topic",
        placeholder="e.g., Information Theory in Biology",
        help="Enter the research topic you want to explore"
    )

    # Number of references slider
    num_papers = st.slider(
        label="Number of References to Explore",
        min_value=1,
        max_value=10,
        value=5,
        help="How many top papers would you like to discover?"
    )

    # Years to explore slider
    years_to_explore = st.slider(
        label="Prior Years to Explore",
        min_value=1,
        max_value=50,
        value=5,
        help="How many years back should we search?"
    )

    # Submit button
    search_button = st.button(
        label="🚀 Search",
        use_container_width=True,
        type="primary"
    )

# Main content area
if search_button:
    if not research_topic:
        st.error("Please enter a research topic to proceed.")
    else:
        st.success(f"Searching for papers in: **{research_topic}**")
        st.info(f"Parameters: {num_papers} papers from last {years_to_explore} years")

        # Placeholder for results
        st.markdown("### 📖 Top Research Papers")
        st.markdown("*(Results will appear here)*")

        st.markdown("### 👥 Top Researchers")
        st.markdown("*(Results will appear here)*")

        st.markdown("### 💬 Chat with AI")
        st.markdown("*(Chat interface will appear here)*")

        st.markdown("### 🔮 Future Research Directions")
        st.markdown("*(Research directions will appear here)*")
else:
    st.markdown("""
        ### Welcome to the AI Research Collaborator Agent

        This platform helps you discover research papers, identify key researchers,
        and explore new research directions in your field of interest.

        **How to use:**
        1. Enter your research topic in the sidebar
        2. Select how many papers you want to explore (1-10)
        3. Choose the time period (last 1-50 years)
        4. Click **Search** to begin your research journey

        **Features:**
        - 📰 Discover top papers with direct links
        - 👨‍🔬 Identify leading researchers in your field
        - 💬 Chat with AI for paper summaries
        - 🚀 Get suggestions for new research directions
    """)

# Footer
st.markdown("---")
st.markdown(f"⚙️ LLM Provider: **{settings.llm_provider.upper()}** | Model: **{settings.get_active_model()}**")
