"""Main Streamlit dashboard for AI Research Collaborator Agent."""
import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config.settings import settings
from src.research_helper import fetch_papers, fetch_researchers, get_research_directions

# Page configuration
st.set_page_config(
    page_title="AI Research Collaborator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
        /* Pistachio green background with SNB.jpg transparent overlay */
        body, .stApp {
            background-image:
                linear-gradient(135deg, rgba(147, 197, 114, 0.75) 0%, rgba(122, 181, 74, 0.75) 100%),
                url('file:///Users/abhijitghosh/Pictures/SNB.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: #93C572;
        }

        /* Main content area */
        .main {
            background-color: rgba(255, 255, 255, 0.92);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(147, 197, 114, 0.2);
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: rgba(147, 197, 114, 0.95);
            border-radius: 10px;
        }

        /* Header styling */
        h1 {
            color: #2D5016;
            font-weight: 700;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(147, 197, 114, 0.2);
            margin-bottom: 10px;
        }

        h2, h3 {
            color: #4A7C2C;
            font-weight: 600;
            border-left: 5px solid #93C572;
            padding-left: 15px;
            margin-top: 20px;
        }

        /* Sidebar text */
        .sidebar .sidebar-content {
            color: #ffffff;
        }

        .sidebar h2, .sidebar h3 {
            color: #ffffff;
            border-left-color: #ffffff;
        }

        /* Input fields styling */
        .stTextInput input {
            border-radius: 8px;
            border: 2px solid #93C572;
            padding: 10px;
            color: #2D5016;
        }

        .stSlider {
            color: #4A7C2C;
        }

        /* Button styling */
        .stButton > button {
            background-color: #93C572;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(147, 197, 114, 0.3);
        }

        .stButton > button:hover {
            background-color: #7AB54A;
            box-shadow: 0 6px 20px rgba(147, 197, 114, 0.4);
            transform: translateY(-2px);
        }

        /* Dataframe styling */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(147, 197, 114, 0.15);
        }

        /* Success, info, warning messages */
        .stSuccess {
            background-color: rgba(147, 197, 114, 0.2);
            border-left: 5px solid #93C572;
            border-radius: 8px;
            padding: 15px;
        }

        .stInfo {
            background-color: rgba(74, 124, 44, 0.1);
            border-left: 5px solid #4A7C2C;
            border-radius: 8px;
            padding: 15px;
        }

        .stWarning {
            background-color: rgba(255, 193, 7, 0.1);
            border-left: 5px solid #FFC107;
            border-radius: 8px;
            padding: 15px;
        }

        /* Spinner text */
        .stSpinner {
            color: #93C572;
        }

        /* Divider styling */
        hr {
            border-color: #93C572;
            border-style: solid;
            opacity: 0.3;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            color: #4A7C2C;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #93C572;
        }

        /* Card-like containers */
        .metric-card {
            background: linear-gradient(135deg, rgba(147, 197, 114, 0.1) 0%, rgba(147, 197, 114, 0.05) 100%);
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #93C572;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.markdown("""
    <div style="padding: 20px; background: linear-gradient(135deg, rgba(147, 197, 114, 0.15) 0%, rgba(45, 80, 22, 0.1) 100%); border-radius: 15px; margin-bottom: 10px;">
        <h1 style="font-size: 2.5em; margin: 0; color: #2D5016;">📚 AI Research Collaborator</h1>
        <p style="font-size: 1em; color: #4A7C2C; margin: 5px 0 0 0; font-style: italic;">
            Discover papers • Find researchers • Explore directions
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for input parameters
with st.sidebar:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #93C572 0%, #7AB54A 100%); border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h2 style="color: white; text-align: center; margin: 0;">🔍 Research Parameters</h2>
        </div>
        """, unsafe_allow_html=True)

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

        # Parallel fetch: researchers, papers, and directions simultaneously
        st.markdown("### 🔄 Searching across all sources in parallel...")

        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all tasks simultaneously
            researcher_future = executor.submit(fetch_researchers, research_topic)
            papers_future = executor.submit(fetch_papers, research_topic, num_papers, years_to_explore, None)
            directions_future = executor.submit(get_research_directions, research_topic)

            # Collect results as they complete
            results = {
                researcher_future: 'researchers',
                papers_future: 'papers',
                directions_future: 'directions'
            }

            researchers_df = None
            papers_df = None
            directions = None

            for future in as_completed(results):
                task_name = results[future]
                try:
                    result = future.result(timeout=60)
                    if task_name == 'researchers':
                        researchers_df = result
                    elif task_name == 'papers':
                        papers_df = result
                    elif task_name == 'directions':
                        directions = result
                except Exception as e:
                    st.error(f"Error fetching {task_name}: {e}")

        # Display results
        st.markdown("### 👥 Top Researchers")
        researcher_names = []
        if researchers_df is not None and not researchers_df.empty:
            researcher_names = researchers_df['Name'].tolist()
            st.info("⚠️ **Note:** Homepage links may be outdated. Please verify current affiliations and contact information directly.")
            st.dataframe(
                researchers_df,
                use_container_width=True,
                column_config={
                    "Homepage": st.column_config.LinkColumn(),
                }
            )
        else:
            st.warning("No researchers found.")

        st.markdown("### 📖 Top Research Papers, Books & Reviews")
        if papers_df is not None and not papers_df.empty:
            st.dataframe(
                papers_df,
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn(display_text="🔗 Open"),
                }
            )
            st.caption("📌 **Sources:** Papers from ArXiv, Books from Google Books, Journals via CrossRef")
        else:
            st.warning("No resources found. Try a different topic.")

        st.markdown("### 🔮 Future Research Directions")
        if directions:
            for i, direction in enumerate(directions, 1):
                st.markdown(f"**{i}. {direction.get('title', 'Untitled')}**")
                st.write(direction.get('description', 'No description available.'))
        else:
            st.info("No research directions generated.")

        st.markdown("### 💬 Chat with AI")
        st.markdown("*(Chat interface coming soon)*")
else:
    st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <p style="color: #4A7C2C; font-size: 1.3em; margin: 20px 0;">
                👈 Enter a research topic in the sidebar and click <strong>Search</strong>
            </p>
            <p style="color: #7AB54A; font-size: 0.95em;">
                Discover papers • Find researchers • Explore directions
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="margin-top: 50px; padding-top: 20px; border-top: 2px solid #93C572; text-align: center;">
        <p style="color: #4A7C2C; font-size: 0.9em;">
            ⚙️ LLM Provider: <strong>{}</strong> | Model: <strong>{}</strong>
        </p>
        <p style="color: #7AB54A; font-size: 0.85em; margin-top: 10px;">
            🌿 Powered by AI Research Collaborator Agent
        </p>
    </div>
    """.format(settings.llm_provider.upper(), settings.get_active_model()), unsafe_allow_html=True)
