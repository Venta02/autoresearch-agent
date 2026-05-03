"""Web Search Tool using Tavily API."""

from typing import List, Dict
from langchain_core.tools import tool
from tavily import TavilyClient

from core.config import TAVILY_API_KEY, MAX_SEARCH_RESULTS


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str, max_results: int = 5) -> dict:
    """
    Search the web for information using Tavily AI search.
    
    Args:
        query: Search query (be specific)
        max_results: Number of results (1-10, default 5)
    
    Returns:
        Dict with results and metadata
    """
    try:
        response = tavily_client.search(
            query=query,
            max_results=min(max_results, MAX_SEARCH_RESULTS),
            search_depth="advanced",
            include_answer=True,
        )
        
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:1500],
                "score": item.get("score", 0.0),
            })
        
        return {
            "query": query,
            "answer": response.get("answer", ""),
            "results": results,
            "total": len(results),
        }
    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "query": query, "results": []}


if __name__ == "__main__":
    result = web_search.invoke({"query": "AI agents 2026"})
    print(f"Found {result.get('total', 0)} results")
