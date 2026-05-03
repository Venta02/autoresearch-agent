"""State management for research agent."""

from typing import TypedDict, List, Optional, Annotated
from operator import add
from langchain_core.messages import BaseMessage


class ResearchState(TypedDict):
    """LangGraph state for the research agent."""
    query: str
    plan: Optional[str]
    search_results: Annotated[List[dict], add]
    documents: Annotated[List[dict], add]
    insights: Annotated[List[str], add]
    messages: Annotated[List[BaseMessage], add]
    current_iteration: int
    final_report: Optional[str]
    sources: Annotated[List[dict], add]
