"""Knowledge graph for managing citations, topics, and author networks."""
from typing import Set, Dict, List, Tuple
import networkx as nx


class ResearchKnowledgeGraph:
    """Graph-based knowledge representation for research."""

    def __init__(self):
        """Initialize knowledge graph."""
        self.graph = nx.DiGraph()

    def add_paper(self, paper_id: str, title: str, authors: List[str], year: int):
        """Add paper node to graph.

        Args:
            paper_id: Unique paper identifier
            title: Paper title
            authors: List of author names
            year: Publication year
        """
        self.graph.add_node(paper_id, type="paper", title=title, authors=authors, year=year)

    def add_topic(self, topic_id: str, name: str):
        """Add topic node to graph.

        Args:
            topic_id: Unique topic identifier
            name: Topic name
        """
        self.graph.add_node(topic_id, type="topic", name=name)

    def add_author(self, author_id: str, name: str):
        """Add author node to graph.

        Args:
            author_id: Unique author identifier
            name: Author name
        """
        self.graph.add_node(author_id, type="author", name=name)

    def add_citation(self, citing_paper: str, cited_paper: str):
        """Add citation relationship.

        Args:
            citing_paper: Paper that cites
            cited_paper: Paper being cited
        """
        self.graph.add_edge(citing_paper, cited_paper, relation="cites")

    def add_authorship(self, author_id: str, paper_id: str):
        """Add authorship relationship.

        Args:
            author_id: Author identifier
            paper_id: Paper identifier
        """
        self.graph.add_edge(author_id, paper_id, relation="authored")

    def add_topic_association(self, paper_id: str, topic_id: str):
        """Associate paper with topic.

        Args:
            paper_id: Paper identifier
            topic_id: Topic identifier
        """
        self.graph.add_edge(paper_id, topic_id, relation="covers_topic")

    def find_related_papers(self, paper_id: str, depth: int = 2) -> Set[str]:
        """Find papers related through citations.

        Args:
            paper_id: Starting paper
            depth: Citation depth to explore

        Returns:
            Set of related paper IDs
        """
        related = set()
        for _ in range(depth):
            related.update(self.graph.successors(paper_id))
            related.update(self.graph.predecessors(paper_id))
        return related

    def get_topic_hierarchy(self) -> Dict:
        """Get hierarchical structure of topics.

        Returns:
            Dictionary representing topic relationships
        """
        topics = [n for n, d in self.graph.nodes(data=True) if d.get("type") == "topic"]
        return {"topics": topics}

    def get_author_network(self, author_id: str) -> List[str]:
        """Get collaborators of an author.

        Args:
            author_id: Author identifier

        Returns:
            List of collaborating author IDs
        """
        papers = list(self.graph.successors(author_id))
        collaborators = set()
        for paper in papers:
            collaborators.update(self.graph.predecessors(paper))
        return list(collaborators)
