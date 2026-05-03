"""Test setup script."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    print("Test 1: Imports")
    try:
        import langgraph
        import langchain_google_genai
        import tavily
        import chromadb
        import chainlit
        import streamlit
        print("All imports OK\n")
        return True
    except ImportError as e:
        print(f"Import failed: {e}\n")
        return False


def test_config():
    print("Test 2: Configuration")
    try:
        from core.config import GEMINI_API_KEY, TAVILY_API_KEY, GEMINI_MODEL
        assert GEMINI_API_KEY, "GEMINI_API_KEY missing"
        assert TAVILY_API_KEY, "TAVILY_API_KEY missing"
        print(f"Gemini key: {GEMINI_API_KEY[:10]}...")
        print(f"Tavily key: {TAVILY_API_KEY[:10]}...")
        print(f"Model: {GEMINI_MODEL}\n")
        return True
    except Exception as e:
        print(f"Config failed: {e}\n")
        return False


def test_gemini():
    print("Test 3: Gemini API")
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from core.config import GEMINI_API_KEY, GEMINI_MODEL
        
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
        )
        response = llm.invoke("Say 'OK' in one word.")
        print(f"Response: {response.content[:100]}")
        print("Gemini API working!\n")
        return True
    except Exception as e:
        print(f"Gemini failed: {e}\n")
        return False


def test_tavily():
    print("Test 4: Tavily Search")
    try:
        from tools.web_search import web_search
        result = web_search.invoke({"query": "Python", "max_results": 2})
        print(f"Found {result.get('total', 0)} results")
        print("Tavily working!\n")
        return True
    except Exception as e:
        print(f"Tavily failed: {e}\n")
        return False


def test_agent():
    print("Test 5: Agent Initialization")
    try:
        from agents import ResearchAgent
        agent = ResearchAgent()
        print("Agent initialized!\n")
        return True
    except Exception as e:
        print(f"Agent failed: {e}\n")
        return False


def main():
    print("=" * 60)
    print("AutoResearch Agent - Setup Tests")
    print("=" * 60 + "\n")
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    
    if results[1][1]:
        results.append(("Gemini API", test_gemini()))
        results.append(("Tavily Search", test_tavily()))
        results.append(("Agent Init", test_agent()))
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! Now run:")
        print("  chainlit run ui/chainlit_app.py -w")
        print("  (or: streamlit run ui/streamlit_app.py)")
    else:
        print("\nSome tests failed. Check errors above.")


if __name__ == "__main__":
    main()
