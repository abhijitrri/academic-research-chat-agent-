"""Helper functions for research discovery."""
import json
import pandas as pd
from datetime import datetime, timedelta
from src.agent.engine import ResearchAgent
from src.config.settings import settings
from src.rag_search import MultiSourceRAG


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
    """Fetch papers using GPT recommendations + RAG search across multiple sources.

    Args:
        research_topic: Research topic to search
        num_papers: Number of papers to retrieve
        years: Number of years to look back
        researchers: Optional list of researcher names

    Returns:
        DataFrame with columns: Title, Authors, Year, Source, Link
    """
    agent = ResearchAgent()
    rag = MultiSourceRAG()
    papers_list = []

    # Step 1: Ask GPT to recommend important papers/books in the field
    prompt = f"""You are an expert in "{research_topic}".

List the {num_papers} most important, influential, and seminal papers, books, or review articles in this field
published or written in the last {years} years.

For each resource, provide EXACTLY in this JSON format:
{{
    "resources": [
        {{
            "title": "Exact title",
            "authors": ["Author One", "Author Two"],
            "year": 2024,
            "type": "paper"
        }}
    ]
}}

CRITICAL RULES:
- Only include real resources you have reliable knowledge about
- Include papers, books, AND review articles
- Type should be: "paper", "book", or "review"
- Sort by importance and influence in the field
- Return ONLY valid JSON with no other text"""

    try:
        response = agent.chat(prompt)

        # Parse JSON response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        json_str = response[json_start:json_end]
        data = json.loads(json_str)

        resources = data.get('resources', [])

        # Step 2: For each resource, search across sources using RAG
        for resource in resources:
            if len(papers_list) >= num_papers:
                break

            title = resource.get('title')
            authors = resource.get('authors', [])
            year = resource.get('year')
            res_type = resource.get('type', 'paper')

            # Search across multiple sources
            result = rag.multi_search(title, authors, year)

            if result:
                papers_list.append({
                    'Title': title,
                    'Authors': ', '.join(authors) if isinstance(authors, list) else authors,
                    'Year': year,
                    'Type': res_type.capitalize(),
                    'Source': result.get('source', 'Unknown'),
                    'Link': result.get('link', '')
                })
            else:
                # Add anyway with note that resource wasn't found online
                papers_list.append({
                    'Title': title,
                    'Authors': ', '.join(authors) if isinstance(authors, list) else authors,
                    'Year': year,
                    'Type': res_type.capitalize(),
                    'Source': 'Not found online',
                    'Link': ''
                })

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Type', 'Source', 'Link'])
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Type', 'Source', 'Link'])

    # Convert to DataFrame
    if papers_list:
        df = pd.DataFrame(papers_list)
        return df
    else:
        return pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Type', 'Source', 'Link'])


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
