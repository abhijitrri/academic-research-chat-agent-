"""Helper functions for research discovery."""
import json
import pandas as pd
import arxiv
from datetime import datetime, timedelta
from src.agent.engine import ResearchAgent
from src.config.settings import settings


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


def fetch_papers(research_topic: str, num_papers: int, years: int, researchers: list = None) -> pd.DataFrame:
    """Fetch papers from ArXiv by researchers or topic.

    Args:
        research_topic: Research topic to search
        num_papers: Number of papers to retrieve
        years: Number of years to look back
        researchers: Optional list of researcher names to search for their papers

    Returns:
        DataFrame with columns: Title, Authors, Year, Publication Link, ArXiv Link
    """
    papers_list = []
    cutoff_date = datetime.now() - timedelta(days=years*365)

    try:
        # Search ArXiv with flexible topic query
        # Using all fields to catch more relevant papers
        query = f'all:{research_topic}'

        client = arxiv.Client()
        search = client.results(
            arxiv.Search(
                query=query,
                max_results=num_papers * 3,  # Fetch more to filter by date
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
        )

        seen_ids = set()
        for paper in search:
            if len(papers_list) >= num_papers:
                break

            # Skip if already added (avoid duplicates)
            if paper.entry_id in seen_ids:
                continue
            seen_ids.add(paper.entry_id)

            # Check if within date range
            if paper.published.replace(tzinfo=None) < cutoff_date:
                continue

            # Skip papers with no authors
            if not paper.authors:
                continue

            paper_dict = {
                'title': paper.title.strip(),
                'authors': ', '.join([author.name for author in paper.authors]),
                'year': paper.published.year,
                'publication_link': None,
                'arxiv_link': paper.entry_id
            }
            papers_list.append(paper_dict)

    except Exception as e:
        print(f"Error searching ArXiv: {e}")
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Publication Link', 'ArXiv Link'])

    # Convert to DataFrame
    if papers_list:
        df = pd.DataFrame(papers_list)
        df.columns = ['Title', 'Authors', 'Year', 'Publication Link', 'ArXiv Link']
        return df
    else:
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Publication Link', 'ArXiv Link'])


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
