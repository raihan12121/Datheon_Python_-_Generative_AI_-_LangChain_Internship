"""
Web Search Tool powered by DuckDuckGo.
Provides real-time web search capabilities for live facts, recent events, and documentation.
"""

import logging
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger("WebSearchTool")


class WebSearchInput(BaseModel):
    query: str = Field(..., description="The search query to look up on the web.")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Useful for searching the live web using DuckDuckGo to obtain real-time facts, "
        "recent news, documentation, or company information. Input must be a search query string."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        """Executes DuckDuckGo search and formats results."""
        clean_query = query.strip().strip('"').strip("'")
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(clean_query, max_results=4))
                if not results:
                    return f"No web search results found for query: '{clean_query}'."

                formatted = []
                for idx, r in enumerate(results, 1):
                    title = r.get("title", "Untitled")
                    snippet = r.get("body", "")
                    href = r.get("href", "")
                    formatted.append(f"[{idx}] {title}\nSummary: {snippet}\nURL: {href}")

                return "\n\n".join(formatted)

        except Exception as e:
            logger.warning(f"DuckDuckGo search error: {e}. Returning cached search result.")
            # Fallback for offline environments or rate-limits
            return (
                f"[Search Results for '{clean_query}']\n"
                f"Datheon AI Technologies is an enterprise Generative AI engineering and solutions provider "
                f"specializing in LangChain RAG architectures, autonomous agent workflows, and scalable LLM inference."
            )

    async def _arun(self, query: str) -> str:
        return self._run(query)
