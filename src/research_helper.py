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

    prompt = f"""Find the {num_papers} most important and influential papers in the field of "{research_topic}"
published or appeared on arxiv in the last {years} years.

For each paper, provide EXACTLY in this JSON format:
{{
    "papers": [
        {{
            "title": "Paper Title",
            "authors": ["Author One", "Author Two", "Author Three"],
            "year": 2024,
            "publication_link": "https://doi.org/...",
            "arxiv_link": "https://arxiv.org/abs/..."
        }}
    ]
}}

Rules:
- Sort authors alphabetically by last name
- Include DOI/publication links if available
- Include ArXiv links if available
- If a link is not available, use null
- Return ONLY valid JSON, no other text
- Papers should be seminal works, highly cited, or recent breakthroughs in the field"""

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

    prompt = f"""Find the 10 most authoritative and influential contemporary researchers in the field of "{research_topic}"
who have published at least one paper or article in this field in the last 2 years.

For each researcher, provide EXACTLY in this JSON format:
{{
    "researchers": [
        {{
            "name": "Full Name",
            "affiliation": "University/Institution Name",
            "homepage": "https://..."
        }}
    ]
}}

Rules:
- Include only researchers with recent publications (last 2 years)
- Include their current institution/affiliation
- Include homepage link if available, otherwise use null
- Sort by influence/citation count
- Return ONLY valid JSON, no other text"""

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

    prompt = f"""Based on current trends in "{research_topic}", suggest 5 promising future research directions.

For each direction, provide in this JSON format:
{{
    "directions": [
        {{
            "title": "Direction Title",
            "description": "Description up to 200 words..."
        }}
    ]
}}

Return ONLY valid JSON."""

    response = agent.chat(prompt)

    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)
        return data.get('directions', [])
    except json.JSONDecodeError:
        return []
