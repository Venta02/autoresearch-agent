# AutoResearch Agent
# 自動研究助理

> Production-grade AI research assistant with autonomous multi-tool reasoning. Built with **LangGraph**, **Google Gemini**, and **Chainlit**.
>
> 生產級 AI 研究助理，具備自主多工具推理能力。基於 **LangGraph**、**Google Gemini** 與 **Chainlit** 構建。

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://www.langchain.com/langgraph)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-blue.svg)](https://ai.google.dev/)
[![Chainlit](https://img.shields.io/badge/Chainlit-1.3-purple.svg)](https://chainlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Demo / 演示

<p align="center">
  <img src="docs/demo.gif" alt="Demo" width="800"/>
</p>

> **Live demo:** Coming soon at Hugging Face Spaces / 即將上線

---

## Overview / 概覽

AutoResearch Agent autonomously researches any topic by combining:

- **Strategic Planning** — Creates research strategy
- **Web Search** — Tavily AI-optimized search
- **Content Reading** — Full-page extraction
- **Synthesis** — Multi-source insights
- **Citation Tracking** — Verifiable sources
- **PDF Reports** — Professional output

AutoResearch Agent 能夠自主研究任何主題：

- **策略規劃** — 制定研究策略
- **網路搜尋** — Tavily AI 優化搜尋
- **內容讀取** — 完整頁面擷取
- **資訊整合** — 多來源洞察
- **引用追蹤** — 可驗證來源
- **PDF 報告** — 專業輸出

## Key Features / 主要功能

- **Multi-tool Agent** — 4 specialized tools / 4 個專業工具
- **ReAct Pattern** — Think-Act-Observe-Repeat / ReAct 推理模式
- **LangGraph Workflow** — Production-grade framework / 生產級框架
- **Beautiful Chainlit UI** — Modern AI chat interface / 現代化聊天介面
- **Streaming Responses** — Real-time updates / 即時更新
- **Citation Tracking** — Every claim sourced / 完整來源引用
- **Free APIs** — Generous free tiers / 慷慨的免費 API

## Architecture / 系統架構

```
┌─────────────────────────────────────────────────┐
│                  USER QUERY                     │
└────────────────────┬────────────────────────────┘
                     ▼
              ┌─────────────┐
              │   Planner   │ Research strategy
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │ Researcher  │ ←──────────┐
              │   (LLM)     │            │
              └──────┬──────┘            │
                     │ Tool Call?        │
                     ▼                   │
              ┌──────────────┐           │
              │    Tools     │           │
              │              │           │
              │ web_search   │───────────┘
              │ web_fetch    │
              │ summarize    │
              │ pdf_gen      │
              └──────────────┘
                     │
              ┌──────▼──────┐
              │   Writer    │ Final report
              └──────┬──────┘
                     ▼
              ┌─────────────┐
              │   REPORT    │ With citations
              └─────────────┘
```

## Tech Stack / 技術堆疊

| Component / 元件 | Technology / 技術 |
|------------------|-------------------|
| Agent Framework | LangGraph |
| LLM | Google Gemini 2.5 Flash |
| UI Framework | Chainlit (modern AI-native) |
| Web Search | Tavily AI Search |
| Web Scraping | BeautifulSoup4 |
| Vector DB | ChromaDB |
| PDF Generation | ReportLab |

## Quick Start / 快速開始

### Prerequisites / 前置需求

- Python 3.10+
- Google account (for Gemini API)
- Tavily account (for search API)

### Installation / 安裝

```bash
# Clone repo
git clone https://github.com/your-username/autoresearch-agent.git
cd autoresearch-agent

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys
```

### Get API Keys (Free) / 取得免費 API 金鑰

1. **Gemini API**: https://aistudio.google.com/app/apikey
2. **Tavily Search**: https://app.tavily.com (1,000 searches/month free)

### Run / 執行

```bash
# Test setup
python -m tests.test_setup

# Run with Chainlit (recommended) / 啟動 Chainlit (推薦)
chainlit run ui/chainlit_app.py -w

# Or run with Streamlit
streamlit run ui/streamlit_app.py
```

Browser opens at: http://localhost:8000 (Chainlit) or http://localhost:8501 (Streamlit)

## UI Comparison / 介面比較

This project includes **two UI implementations**:

本專案包含**兩種介面實作**：

### Chainlit (Recommended) / 推薦

- Modern AI-native chat interface / 現代化 AI 聊天介面
- Built-in streaming and tool visualization / 內建串流與工具視覺化
- Beautiful animations and theming / 精美動畫與主題
- ChatGPT-like UX / 類 ChatGPT 體驗

### Streamlit (Alternative)

- Simpler dashboard layout / 較簡潔的儀表板佈局
- Familiar to ML practitioners / ML 從業者熟悉
- Quick deployment / 快速部署

## Usage / 使用方法

### Chainlit UI (Recommended)

```bash
chainlit run ui/chainlit_app.py -w
```

Features:
- 4 starter questions
- 3 chat profiles (Quick, Deep, Academic)
- Action buttons (PDF export, follow-up)
- Live tool execution visualization
- Custom purple/violet theme

### Python API

```python
from agents import ResearchAgent

agent = ResearchAgent()
result = agent.research("Latest AI agent trends 2026")

print(result["report"])
for source in result["sources"]:
    print(f"- {source['title']}: {source['url']}")
```

### CLI

```bash
python -m scripts.run_cli "Your research query here"
```

## Project Structure / 專案結構

```
autoresearch-agent/
├── agents/
│   └── research_agent.py    # LangGraph agent
├── core/
│   ├── config.py            # Configuration
│   ├── state.py             # Agent state
│   └── prompts.py           # System prompts
├── tools/
│   ├── web_search.py        # Tavily search
│   ├── web_fetch.py         # URL reader
│   ├── summarizer.py        # Summarizer
│   └── pdf_generator.py     # PDF builder
├── ui/
│   ├── chainlit_app.py      # Chainlit UI (recommended)
│   └── streamlit_app.py     # Streamlit UI (alternative)
├── public/
│   ├── style.css            # Custom Chainlit CSS
│   ├── logo_dark.svg
│   ├── logo_light.svg
│   └── icons/               # Starter icons
├── .chainlit/
│   └── config.toml          # Chainlit configuration
├── chainlit.md              # Chainlit welcome page
├── tests/
├── scripts/
├── notebooks/
├── docs/
├── .env.example
├── requirements.txt
└── README.md
```

## Key Design Decisions / 關鍵設計決策

1. **Why LangGraph? / 為何選擇 LangGraph？**
   - Modern, graph-based architecture
   - Production-grade with checkpointing
   - 現代化圖形架構，具備檢查點機制

2. **Why Chainlit over Streamlit? / 為何選擇 Chainlit？**
   - Designed for AI/LLM apps specifically
   - Built-in streaming and tool visualization
   - More professional appearance
   - 專為 AI/LLM 應用設計，外觀更專業

3. **Why Tavily for search? / 為何選擇 Tavily？**
   - AI-optimized results
   - Generous free tier (1K/month)
   - Better than Google Custom Search for agents

4. **Why Gemini 2.5 Flash? / 為何選擇 Gemini？**
   - Fast and free
   - 1M token context window
   - Strong reasoning capabilities

## Future Improvements / 未來改進

- [ ] Multi-agent orchestration (researcher + fact-checker + writer)
- [ ] Long-term memory with ChromaDB
- [ ] Email integration (Gmail API)
- [ ] Voice input/output
- [ ] Citation verification agent
- [ ] Custom domain RAG (upload PDFs)
- [ ] Hugging Face Spaces deployment
- [ ] Mobile-friendly UI

## License / 授權

MIT License — see [LICENSE](LICENSE) for details.

## Author / 作者

**[Embun Ventani]**

- GitHub: [@Venta02](https://github.com/Venta02)
- LinkedIn: [embun ventani](https://linkedin.com/in/embun-ventani-34ba50206)
- Email: embunventa02@gmail.com

---

<p align="center">
  <strong>If this project helped you, please consider starring the repository.</strong><br/>
  <strong>若本專案對您有所幫助，歡迎為儲存庫加上星標。</strong>
</p>
