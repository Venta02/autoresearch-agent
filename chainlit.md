# Welcome to AutoResearch Agent

> AI-powered research assistant with autonomous multi-tool reasoning, built with **LangGraph** and **Google Gemini**.

## What This Agent Can Do

This isn't a simple chatbot — it's an **autonomous AI agent** that:

- **Plans** research strategies for any topic
- **Searches** the web with Tavily AI
- **Reads** full content from web pages
- **Synthesizes** findings into comprehensive reports
- **Cites** every source for verification
- **Generates** professional PDF reports

## How It Works

The agent uses **ReAct pattern** (Reason → Act → Observe → Repeat):

1. **Planner Node** — Creates research strategy
2. **Researcher Node** — Decides which tools to call
3. **Tool Execution** — Runs web search, fetch, summarize
4. **Writer Node** — Generates final report

All orchestrated with **LangGraph** for production-grade reliability.

## Getting Started

1. Click a starter question above, or
2. Type your own research question in the chat
3. Watch the agent work in real-time
4. Review the report and sources
5. Generate PDF or ask follow-up questions

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | LangGraph |
| LLM | Google Gemini 2.5 Flash |
| Search | Tavily AI |
| UI | Chainlit |
| PDF | ReportLab |

## Sample Queries

Try asking:
- "What are the latest trends in AI agents in 2026?"
- "Compare the best vector databases for RAG applications"
- "What are the breakthroughs in renewable energy storage?"
- "How does quantum computing differ from classical computing?"

---

**Built by:** [Your Name](https://github.com/your-username)
**Source:** [GitHub Repository](https://github.com/your-username/autoresearch-agent)

Ready? Start researching!
