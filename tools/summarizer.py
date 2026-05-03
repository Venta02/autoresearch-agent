"""Summarizer Tool using Gemini."""

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import GEMINI_API_KEY, GEMINI_MODEL
from core.prompts import SUMMARIZER_PROMPT


_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)


@tool
def summarize_content(content: str, query: str) -> dict:
    """
    Summarize long content into key insights.
    
    Args:
        content: Full text to summarize
        query: Research query (for relevance scoring)
    
    Returns:
        Dict with summary
    """
    try:
        if len(content) > 8000:
            content = content[:8000] + "..."
        
        prompt = SUMMARIZER_PROMPT.format(content=content, query=query)
        response = _llm.invoke(prompt)
        
        return {
            "summary": response.content,
            "original_length": len(content),
        }
    except Exception as e:
        return {"error": f"Summarization failed: {str(e)}"}
