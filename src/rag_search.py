"""RAG-based search across multiple sources: ArXiv, Books, Journals."""
import arxiv
import requests
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd


class MultiSourceRAG:
    """Search and retrieve papers/books across multiple sources."""

    def __init__(self):
        """Initialize RAG search with multiple sources."""
        self.arxiv_client = arxiv.Client()

    def search_arxiv(self, title: str, authors: List[str], year: int) -> Optional[Dict]:
        """Search ArXiv for a specific paper.

        Args:
            title: Paper title
            authors: List of author names
            year: Publication year

        Returns:
            Dict with paper details or None if not found
        """
        try:
            # Search by title
            query = f'ti:"{title}"'
            results = list(self.arxiv_client.results(
                arxiv.Search(query=query, max_results=5)
            ))

            for paper in results:
                # Check if year matches (within 1 year)
                if abs(paper.published.year - year) <= 1:
                    return {
                        'source': 'ArXiv',
                        'title': paper.title,
                        'authors': ', '.join([a.name for a in paper.authors]),
                        'year': paper.published.year,
                        'link': paper.entry_id,
                        'type': 'Paper',
                        'found': True
                    }

            # If no exact match, return best match anyway
            if results:
                paper = results[0]
                return {
                    'source': 'ArXiv',
                    'title': paper.title,
                    'authors': ', '.join([a.name for a in paper.authors]),
                    'year': paper.published.year,
                    'link': paper.entry_id,
                    'type': 'Paper',
                    'found': True
                }

        except Exception as e:
            print(f"ArXiv search error for '{title}': {e}")

        return None

    def search_google_books(self, title: str, authors: List[str]) -> Optional[Dict]:
        """Search Google Books for a book.

        Args:
            title: Book title
            authors: List of author names

        Returns:
            Dict with book details or None if not found
        """
        try:
            author_str = ' '.join(authors[:2]) if authors else ''
            query = f'{title} {author_str}'

            # Google Books API - free tier
            url = 'https://www.googleapis.com/books/v1/volumes'
            params = {
                'q': query,
                'maxResults': 5,
                'printType': 'books'
            }

            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and len(data['items']) > 0:
                    book = data['items'][0]['volumeInfo']
                    return {
                        'source': 'Google Books',
                        'title': book.get('title', title),
                        'authors': ', '.join(book.get('authors', authors)),
                        'year': book.get('publishedDate', '')[:4],
                        'link': book.get('previewLink', ''),
                        'type': 'Book',
                        'found': True
                    }

        except Exception as e:
            print(f"Google Books search error for '{title}': {e}")

        return None

    def search_major_journals(self, title: str, authors: List[str], year: int) -> Optional[Dict]:
        """Search major journals (Nature, Science, PNAS, JMLR, etc.).

        Args:
            title: Paper title
            authors: List of author names
            year: Publication year

        Returns:
            Dict with paper details or None if not found
        """
        try:
            # CrossRef API for journal search (free, no key required)
            url = 'https://api.crossref.org/works'
            params = {
                'query': title,
                'rows': 5,
                'sort': 'score',
                'order': 'desc'
            }

            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'items' in data['message']:
                    for item in data['message']['items']:
                        # Check if year matches
                        item_year = item.get('issued', {}).get('date-parts', [[None]])[0][0]
                        if item_year and abs(int(item_year) - year) <= 1:
                            return {
                                'source': f"Journal ({item.get('container-title', ['Unknown'])[0]})",
                                'title': item.get('title', [title])[0],
                                'authors': ', '.join([f"{a.get('given', '')} {a.get('family', '')}"
                                                     for a in item.get('author', [])[:3]]),
                                'year': int(item_year),
                                'link': item.get('URL', ''),
                                'type': 'Paper',
                                'found': True
                            }

        except Exception as e:
            print(f"Journal search error for '{title}': {e}")

        return None

    def multi_search(self, title: str, authors: List[str], year: int,
                     search_type: str = 'auto') -> Optional[Dict]:
        """Search across all sources in parallel for a paper/book.

        Args:
            title: Title to search
            authors: List of author names
            year: Publication year
            search_type: 'paper', 'book', or 'auto'

        Returns:
            Dict with best match or None
        """
        # Use ThreadPoolExecutor for parallel searches
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.search_arxiv, title, authors, year): 'arxiv',
                executor.submit(self.search_google_books, title, authors): 'books',
                executor.submit(self.search_major_journals, title, authors, year): 'journals'
            }

            results = []
            # Collect results as they complete (no waiting for slowest)
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=5)
                    if result and result.get('found'):
                        # Return immediately on first found result
                        return result
                    elif result:
                        results.append(result)
                except Exception as e:
                    print(f"Search error: {e}")

        # Return best attempt if nothing marked as found
        return results[0] if results else None

    def batch_search(self, resources: List[Dict]) -> List[Optional[Dict]]:
        """Search for multiple resources in parallel.

        Args:
            resources: List of dicts with 'title', 'authors', 'year'

        Returns:
            List of search results
        """
        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(
                    self.multi_search,
                    r.get('title'),
                    r.get('authors', []),
                    r.get('year')
                ): i
                for i, r in enumerate(resources)
            }

            # Maintain order while processing in parallel
            ordered_results = [None] * len(resources)
            for future in as_completed(futures):
                try:
                    idx = futures[future]
                    ordered_results[idx] = future.result(timeout=10)
                except Exception as e:
                    print(f"Batch search error: {e}")

            return ordered_results
