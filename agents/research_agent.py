"""
Main Research Agent using LangGraph.
Implements ReAct pattern with multi-tool support.
"""

from typing import Literal, AsyncGenerator
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from core.config import GEMINI_API_KEY, GEMINI_MODEL, MAX_RESEARCH_ITERATIONS
from core.state import ResearchState
from tools import ALL_TOOLS


# ============================================
# Initialize LLM
# ============================================
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
    streaming=True,
)

llm_with_tools = llm.bind_tools(ALL_TOOLS)


# ============================================
# Agent Nodes
# ============================================

def planner_node(state: ResearchState) -> dict:
    """Plans research strategy."""
    query = state["query"]
    
    plan_prompt = f"""You are a research planning expert. Create a detailed research plan.

Query: {query}

Provide:
1. 3-5 key sub-topics to investigate
2. Specific search queries to use
3. Types of sources needed

Be concise and actionable."""
    
    response = llm.invoke([SystemMessage(content=plan_prompt)])
    
    return {
        "plan": response.content,
        "messages": [
            SystemMessage(content=f"Research plan:\n{response.content}"),
            HumanMessage(content=query),
        ],
        "current_iteration": 0,
    }


def researcher_node(state: ResearchState) -> dict:
    """Main research loop with tool calling."""
    messages = state["messages"]
    iteration = state.get("current_iteration", 0)
    plan = state.get("plan", "")
    
    findings_summary = ""
    if state.get("documents"):
        findings_summary = f"\nDocuments gathered: {len(state['documents'])}\n"
    
    system_msg = SystemMessage(content=f"""You are a thorough research agent.

Research Plan:
{plan}

Iteration: {iteration + 1}/{MAX_RESEARCH_ITERATIONS}
{findings_summary}

Tasks:
1. Use web_search to find information
2. Use web_fetch to read full content
3. Use summarize_content to extract insights
4. Say "RESEARCH COMPLETE" when done

Be efficient: avoid duplicate searches. Use diverse credible sources.""")
    
    response = llm_with_tools.invoke([system_msg] + messages)
    
    return {
        "messages": [response],
        "current_iteration": iteration + 1,
    }


def writer_node(state: ResearchState) -> dict:
    """Generates final report."""
    query = state["query"]
    documents = state.get("documents", [])
    insights = state.get("insights", [])
    
    sources_text = "\n\n".join([
        f"[{i+1}] {doc.get('title', 'Untitled')}\n"
        f"URL: {doc.get('url', 'N/A')}\n"
        f"Content: {doc.get('content', '')[:500]}..."
        for i, doc in enumerate(documents[:10])
    ])
    
    insights_text = "\n".join([f"- {ins[:200]}" for ins in insights[:20]])
    
    writer_prompt = f"""Generate a comprehensive research report.

Query: {query}

Sources:
{sources_text if sources_text else "Use general knowledge"}

Insights:
{insights_text if insights_text else "Use general analysis"}

Write a well-structured Markdown report:

# [Report Title - based on query]

## Executive Summary
(2-3 sentences)

## Introduction
(Context and importance)

## Key Findings
(Organized by sub-topic, cite [1], [2], etc.)

## Analysis
(Insights and patterns)

## Conclusion
(Summary and implications)

## References
(Numbered list of sources)

Be objective, comprehensive, and accurate."""
    
    response = llm.invoke([SystemMessage(content=writer_prompt)])
    
    sources = [
        {"title": doc.get("title", "Untitled"), "url": doc.get("url", "")}
        for doc in documents[:10]
    ]
    
    return {
        "final_report": response.content,
        "sources": sources,
    }


def process_tool_results(state: ResearchState) -> dict:
    """Process tool results to update state."""
    messages = state["messages"]
    new_documents = []
    new_insights = []
    
    for msg in messages[-5:]:
        if isinstance(msg, ToolMessage):
            content = str(msg.content)
            
            if "title" in content.lower() and "content" in content.lower():
                new_documents.append({
                    "title": "Source from research",
                    "content": content[:1500],
                    "url": "",
                })
            
            if 100 < len(content) < 2000:
                new_insights.append(content[:500])
    
    return {
        "documents": new_documents,
        "insights": new_insights,
    }


# ============================================
# Routing
# ============================================

def should_continue_research(state: ResearchState) -> Literal["tools", "writer"]:
    """Decide next step."""
    messages = state["messages"]
    iteration = state.get("current_iteration", 0)
    
    if iteration >= MAX_RESEARCH_ITERATIONS:
        return "writer"
    
    last_message = messages[-1] if messages else None
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    if last_message and "RESEARCH COMPLETE" in str(last_message.content).upper():
        return "writer"
    
    return "writer"


# ============================================
# Build Graph
# ============================================

def build_research_graph():
    """Build LangGraph workflow."""
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("tools", ToolNode(ALL_TOOLS))
    workflow.add_node("processor", process_tool_results)
    workflow.add_node("writer", writer_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_conditional_edges(
        "researcher",
        should_continue_research,
        {"tools": "tools", "writer": "writer"}
    )
    workflow.add_edge("tools", "processor")
    workflow.add_edge("processor", "researcher")
    workflow.add_edge("writer", END)
    
    return workflow.compile()


# ============================================
# Public API
# ============================================

class ResearchAgent:
    """High-level research agent interface."""
    
    def __init__(self):
        print("Initializing AutoResearch Agent...")
        self.graph = build_research_graph()
        print("Agent ready!")
    
    def research(self, query: str, verbose: bool = False) -> dict:
        """Run research synchronously."""
        if verbose:
            print(f"\nResearching: {query}\n")
        
        initial_state: ResearchState = {
            "query": query,
            "plan": None,
            "search_results": [],
            "documents": [],
            "insights": [],
            "messages": [],
            "current_iteration": 0,
            "final_report": None,
            "sources": [],
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return {
            "query": query,
            "report": final_state.get("final_report", ""),
            "sources": final_state.get("sources", []),
            "iterations": final_state.get("current_iteration", 0),
            "plan": final_state.get("plan", ""),
        }
    
    async def research_async_stream(self, query: str) -> AsyncGenerator:
        """Stream research events asynchronously (for Chainlit)."""
        initial_state: ResearchState = {
            "query": query,
            "plan": None,
            "search_results": [],
            "documents": [],
            "insights": [],
            "messages": [],
            "current_iteration": 0,
            "final_report": None,
            "sources": [],
        }
        
        async for event in self.graph.astream(initial_state):
            yield event


if __name__ == "__main__":
    agent = ResearchAgent()
    result = agent.research(
        "Latest AI agent frameworks 2026",
        verbose=True,
    )
    print("\n" + "=" * 60)
    print("REPORT")
    print("=" * 60)
    print(result["report"])
    print(f"\nSources: {len(result['sources'])}")
    print(f"Iterations: {result['iterations']}")
