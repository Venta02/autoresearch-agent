"""Web Fetcher Tool."""

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

from core.config import MAX_CONTENT_LENGTH


@tool
def web_fetch(url: str) -> dict:
    """
    Fetch and extract clean text from a URL.
    
    Args:
        url: Full URL to fetch (must include https://)
    
    Returns:
        Dict with title, content, and metadata
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        title = soup.title.string if soup.title else "No title"
        title = title.strip() if title else "No title"
        
        for element in soup(["script", "style", "nav", "footer", "iframe", "header"]):
            element.decompose()
        
        main_content = (
            soup.find("article") or
            soup.find("main") or
            soup.find(class_="content") or
            soup.find(id="content") or
            soup.body
        )
        
        if main_content:
            text = main_content.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        clean_text = "\n".join(lines)
        
        truncated = False
        if len(clean_text) > MAX_CONTENT_LENGTH:
            clean_text = clean_text[:MAX_CONTENT_LENGTH] + "..."
            truncated = True
        
        return {
            "url": url,
            "title": title,
            "content": clean_text,
            "length": len(clean_text),
            "truncated": truncated,
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timed out", "url": url}
    except Exception as e:
        return {"error": f"Failed to fetch: {str(e)}", "url": url}


if __name__ == "__main__":
    result = web_fetch.invoke({"url": "https://example.com"})
    print(result.get("title"), result.get("length"))
