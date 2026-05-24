"""Persistent memory management for user research context."""
from typing import Dict, List, Any
from datetime import datetime
import json


class MemoryManager:
    """Manages persistent user research memory and context."""

    def __init__(self, user_id: str):
        """Initialize memory manager for a user.

        Args:
            user_id: Unique user identifier
        """
        self.user_id = user_id
        self.research_interests: List[str] = []
        self.explored_topics: Dict[str, datetime] = {}
        self.ongoing_questions: List[Dict[str, Any]] = []
        self.session_history: List[Dict] = []

    def add_research_interest(self, interest: str):
        """Add research interest to memory.

        Args:
            interest: Research topic of interest
        """
        if interest not in self.research_interests:
            self.research_interests.append(interest)

    def record_topic_exploration(self, topic: str):
        """Record explored topic with timestamp.

        Args:
            topic: Topic that was explored
        """
        self.explored_topics[topic] = datetime.now()

    def add_question(self, question: str, context: Dict[str, Any] = None):
        """Add ongoing research question.

        Args:
            question: Research question
            context: Optional context about the question
        """
        self.ongoing_questions.append({
            "question": question,
            "context": context or {},
            "created_at": datetime.now().isoformat()
        })

    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of research context.

        Returns:
            Dictionary with interests, explored topics, and questions
        """
        return {
            "user_id": self.user_id,
            "research_interests": self.research_interests,
            "explored_topics": {k: v.isoformat() for k, v in self.explored_topics.items()},
            "ongoing_questions": self.ongoing_questions
        }

    def clear(self):
        """Clear all memory."""
        self.research_interests = []
        self.explored_topics = {}
        self.ongoing_questions = []
        self.session_history = []
