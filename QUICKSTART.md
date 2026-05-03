# Quickstart Guide / 快速入門指南

Get the AutoResearch Agent running in 15 minutes.

15 分鐘內讓 AutoResearch Agent 運作。

---

## Step 1: Get Free API Keys / 取得免費 API 金鑰 (5 minutes)

### Gemini API

1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API key"
4. Copy the key (starts with `AIzaSy...`)

### Tavily Search API

1. Visit https://app.tavily.com
2. Sign up (free, no credit card)
3. Dashboard → API Keys → Copy
4. Key starts with `tvly-...`

**Free tier: 1,000 searches/month** / **免費方案：每月 1,000 次搜尋**

---

## Step 2: Setup Project / 設定專案 (5 minutes)

```powershell
cd autoresearch-agent

# For VS Code with Anaconda env
C:/Users/luqman_Arif/anaconda3/envs/env/python.exe -m pip install -r requirements.txt
```

---

## Step 3: Configure Environment / 設定環境 (2 minutes)

```powershell
# Windows
copy .env.example .env
notepad .env
```

Edit `.env`:

```env
GEMINI_API_KEY=AIzaSy...your_actual_key
TAVILY_API_KEY=tvly-...your_actual_key
```

---

## Step 4: Test Setup / 測試設定 (2 minutes)

```powershell
C:/Users/luqman_Arif/anaconda3/envs/env/python.exe -m tests.test_setup
```

Expected output / 預期輸出:

```
[PASS] Imports
[PASS] Config
[PASS] Gemini API
[PASS] Tavily Search
[PASS] Agent Init

5/5 tests passed
```

---

## Step 5: Run with Chainlit (Recommended) / 啟動 Chainlit (推薦)

```powershell
C:/Users/luqman_Arif/anaconda3/envs/env/Scripts/chainlit.exe run ui/chainlit_app.py -w
```

Browser opens at: **http://localhost:8000**

**Features:**
- Beautiful chat interface (purple theme)
- 4 starter questions to try
- Action buttons (PDF, follow-up, new research)
- 3 chat profiles (Quick, Deep, Academic)
- Live tool execution visualization

---

## Step 6: Try Streamlit (Alternative) / 嘗試 Streamlit (替代方案)

```powershell
C:/Users/luqman_Arif/anaconda3/envs/env/python.exe -m streamlit run ui/streamlit_app.py
```

Opens at: **http://localhost:8501**

---

## Try These Queries / 試試這些查詢

- "Latest developments in AI agents 2026"
- "Best vector databases for RAG applications"
- "Quantum computing breakthroughs"
- "Renewable energy storage technologies"
- "Best practices for fine-tuning LLMs"

---

## Troubleshooting / 疑難排解

### "GEMINI_API_KEY not found"

Check `.env` exists in **root folder** (not in subfolders).

### "TAVILY_API_KEY not found"

Get free key at https://app.tavily.com

### "ModuleNotFoundError"

Run from project root using module syntax:
```bash
python -m tests.test_setup     # Correct
python -m scripts.run_cli "..."  # Correct
```

### Chainlit not starting

```powershell
# Ensure Chainlit is installed
C:/Users/luqman_Arif/anaconda3/envs/env/python.exe -m pip install chainlit

# Use full path to chainlit.exe
C:/Users/luqman_Arif/anaconda3/envs/env/Scripts/chainlit.exe run ui/chainlit_app.py -w
```

### Quota exceeded

- Gemini: 250 requests/day (free)
- Tavily: 1,000 searches/month (free)

---

## Next Steps / 後續步驟

1. **Customize prompts** in `core/prompts.py` / 自訂提示
2. **Add new tools** in `tools/` directory / 新增工具
3. **Modify Chainlit theme** in `.chainlit/config.toml` / 修改主題
4. **Deploy to HF Spaces** / 部署至 HF Spaces
5. **Update README** with your info / 更新 README

---

## Need Help? / 需要協助？

- See `README.md` for full documentation / 完整文件
- See `docs/` for detailed guides / 詳細指南
