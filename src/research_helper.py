"""Helper functions for research discovery."""
import json
import pandas as pd
from src.agent.engine import ResearchAgent
from src.config.settings import settings


def fetch_papers(research_topic: str, num_papers: int, years: int) -> pd.DataFrame:
    """Fetch top papers in a research area using GPT.

    Args:
        research_topic: Research topic to search
        num_papers: Number of papers to retrieve
        years: Number of years to look back

    Returns:
        DataFrame with columns: Title, Authors, Year, Publication Link, ArXiv Link
    """
    agent = ResearchAgent()

    prompt = f"""Based on your knowledge, recommend the {num_papers} most important, influential, and impactful papers/review articles/books
in the field of "{research_topic}" published in the last {years} years.

These should be papers you actually know about from your training data. Include papers from:
- Top-tier journals (Nature, Science, PNAS, Cell, Lancet, etc.)
- High-quality conference proceedings (NeurIPS, ICML, ICCV, ECCV, MICCAI, etc.)
- ArXiv preprints that gained significant attention
- Important review articles and books in the field

For each paper, provide EXACTLY in this JSON format:
{{
    "papers": [
        {{
            "title": "Exact paper title you know about",
            "authors": ["Author One", "Author Two", "Author Three"],
            "year": 2024,
            "publication_link": "https://doi.org/10.xxxx/xxxxx or https://actual-journal-url.com/paper",
            "arxiv_link": "https://arxiv.org/abs/XXXX.XXXXX or null if not applicable"
        }}
    ]
}}

CRITICAL RULES:
- Only include papers/articles/books you have reliable knowledge about
- Sort authors alphabetically by last name
- Use realistic DOI links or journal URLs if you know them, otherwise use null
- Use real arxiv links if the paper is on arxiv, otherwise null
- Year must be between {2024 - years} and 2024
- Return ONLY valid JSON with no other text
- Papers should be seminal works, highly cited papers, or important recent breakthroughs
- Include diverse perspectives and methodologies in the field"""

    response = agent.chat(prompt)

    try:
        # Parse JSON response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)

        # Convert to DataFrame
        papers_list = data.get('papers', [])
        df = pd.DataFrame(papers_list)

        # Format authors column
        if 'authors' in df.columns:
            df['authors'] = df['authors'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))

        # Rename columns for display
        df.columns = ['Title', 'Authors', 'Year', 'Publication Link', 'ArXiv Link']

        return df

    except json.JSONDecodeError:
        # If JSON parsing fails, return empty DataFrame
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Publication Link', 'ArXiv Link'])


def fetch_researchers(research_topic: str) -> pd.DataFrame:
    """Fetch top researchers in a research area using GPT.

    Args:
        research_topic: Research topic to search

    Returns:
        DataFrame with columns: Name, Affiliation, Homepage
    """
    agent = ResearchAgent()

    prompt = f"""Based on your knowledge, list the 10 most authoritative, influential, and active contemporary researchers
in the field of "{research_topic}" who have published papers or articles in this field in the last 2 years.

Focus on researchers who are:
- Leaders in their subfields
- Have high citation counts
- Published in top-tier venues recently
- Known for significant contributions to the field

For each researcher, provide EXACTLY in this JSON format:
{{
    "researchers": [
        {{
            "name": "Full Name (First Last)",
            "affiliation": "Current University/Institution Name",
            "homepage": "https://researcher-website.edu or null"
        }}
    ]
}}

CRITICAL RULES:
- Only include researchers you have reliable knowledge about
- Use their current/recent affiliations
- Include full names in (First Last) format
- Include university homepage links if you know them, otherwise use null
- Sort by research influence and recent activity
- Return ONLY valid JSON with no other text
- Include researchers from different countries and institutions"""

    response = agent.chat(prompt)

    try:
        # Parse JSON response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)

        # Convert to DataFrame
        researchers_list = data.get('researchers', [])
        df = pd.DataFrame(researchers_list)

        # Rename columns for display
        df.columns = ['Name', 'Affiliation', 'Homepage']

        return df

    except json.JSONDecodeError:
        return pd.DataFrame(columns=['Name', 'Affiliation', 'Homepage'])


def get_paper_summaries(selected_papers: list) -> dict:
    """Get summaries of selected papers using GPT.

    Args:
        selected_papers: List of paper titles

    Returns:
        Dictionary with paper titles as keys and summaries as values
    """
    agent = ResearchAgent()

    papers_str = '\n'.join([f"- {paper}" for paper in selected_papers])

    prompt = f"""Provide concise summaries (max 300 words each) for the following papers:

{papers_str}

For each paper, provide in this JSON format:
{{
    "summaries": {{
        "Paper Title": "Summary text here..."
    }}
}}

Return ONLY valid JSON."""

    response = agent.chat(prompt)

    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)
        return data.get('summaries', {})
    except json.JSONDecodeError:
        return {}


def get_research_directions(research_topic: str) -> list:
    """Get future research directions in a field using GPT.

    Args:
        research_topic: Research topic

    Returns:
        List of research directions (max 200 words each)
    """
    agent = ResearchAgent()

    prompt = f"""Based on current trends, open challenges, and emerging opportunities in "{research_topic}",
propose 5 promising and innovative future research directions that are:
- Feasible and actionable
- Address gaps in current knowledge
- Have significant potential impact
- Build on recent advances in the field

For each direction, provide in this JSON format:
{{
    "directions": [
        {{
            "title": "Concise research direction title",
            "description": "A detailed description (max 200 words) explaining: (1) what the direction is about,
            (2) why it's important, (3) potential approaches or methodologies, (4) expected impact or applications"
        }}
    ]
}}

CRITICAL RULES:
- Each title should be specific and actionable
- Descriptions should be based on real gaps and opportunities in the field
- Avoid vague or overly general suggestions
- Include diverse perspectives (theoretical, applied, methodological, etc.)
- Return ONLY valid JSON with no other text"""

    response = agent.chat(prompt)

    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)
        return data.get('directions', [])
    except json.JSONDecodeError:
        return []
