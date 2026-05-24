"""Core LLM agent engine for research collaboration."""
from typing import Optional, Union
from openai import OpenAI
from anthropic import Anthropic
from src.config.settings import settings


class ResearchAgent:
    """Intelligent research collaborator with support for OpenAI and Anthropic models."""

    def __init__(self, model: Optional[str] = None, provider: Optional[str] = None):
        """Initialize the research agent.

        Args:
            model: LLM model to use. Defaults to configured model for the provider.
            provider: LLM provider ('openai' or 'anthropic'). Defaults to LLM_PROVIDER env var.
        """
        self.provider = provider or settings.llm_provider
        self.model = model or settings.get_active_model()
        self.conversation_history = []

        if self.provider == "anthropic":
            self.client = Anthropic(api_key=settings.anthropic_api_key)
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)

    def chat(self, user_message: str) -> str:
        """Process user message and generate response.

        Args:
            user_message: User's input message

        Returns:
            LLM response
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=self.conversation_history
            )
            assistant_message = response.content[0].text
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1024
            )
            assistant_message = response.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
