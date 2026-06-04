# 🤖 Agentic Code Editor

A chat-based AI coding assistant built with **Google ADK**, **Groq API**, and **Streamlit**, where users simply describe what they want in plain English or upload a file and a team of 8 specialized agents handles the rest — an **Orchestrator** routes each request to the right agent, the **Planner** breaks complex tasks into steps, **Code Generation** writes new code, **Code Edit** refactors existing code, **Debugger** finds and fixes bugs, **Test Writer** generates tests, **Reviewer** checks for quality and security issues, and **Documentation** adds docstrings and comments — with responses rendered in real-time with syntax-highlighted, copyable code blocks, all powered by **LLaMA 3.3 70B** on Groq's free tier at zero infrastructure cost.

---

## 🏗️ Architecture

```
User Input (Streamlit UI)
        │
        ▼
  Orchestrator Agent         ← routes to the right specialist
        │
   ┌────┴─────────────────────────────────────┐
   ▼        ▼         ▼        ▼       ▼      ▼       ▼
Planner  Code Gen  Code Edit  Debug  Tests  Review  Docs
```

---

## 🧠 Agents

| Agent | Responsibility |
|---|---|
| **Orchestrator** | Understands user intent, delegates to specialist agents, handles explain/clarify directly |
| **Planner** | Breaks complex requests into ordered steps |
| **Code Generation** | Writes new code from natural language descriptions |
| **Code Edit** | Modifies and refactors pasted or uploaded code |
| **Debugger** | Finds root causes of bugs and returns fixed code |
| **Test Writer** | Generates unit and integration tests (pytest / Jest) |
| **Reviewer** | Reviews code for quality, security, and performance |
| **Documentation** | Adds docstrings, inline comments, and README sections |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Agent Framework** | Google ADK (Agent Development Kit) |
| **LLM Provider** | Groq API (free tier) |
| **Models** | `llama-3.3-70b-versatile` · `llama-3.1-8b-instant` · `mixtral-8x7b-32768` |
| **Language** | Python 3.11+ |

---

## 📁 Project Structure

```
agentic-code-editor/
├── .env                    ← API keys
├── .env.example
├── requirements.txt
├── README.md
│
├── frontend/
│   └── app.py              ← Streamlit UI (entry point)
│
└── backend/
    ├── config.py           ← Model configuration
    └── agents/
        ├── __init__.py
        ├── orchestrator.py
        ├── planner.py
        ├── code_generation.py
        ├── code_edit.py
        ├── debugger.py
        ├── test_writer.py
        ├── reviewer.py
        └── documentation.py
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/agentic-code-editor.git
cd agentic-code-editor
```

### 2. Create a virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
cd ..
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at → [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
# Windows
.\backend\venv\Scripts\streamlit run frontend\app.py

# macOS / Linux
backend/venv/bin/streamlit run frontend/app.py
```

Open **http://localhost:8501** in your browser.

---

## ✨ Features

- 💬 **Chat interface** — describe what you want in plain English
- 📁 **File upload** — upload `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.txt` files directly into the chat
- 🎨 **Syntax highlighting** — all code responses rendered with proper language highlighting
- 📋 **Copy button** — one-click copy on every code block
- ⚡ **Real-time streaming** — see agent responses token-by-token as they generate
- 🔀 **Agent routing** — orchestrator automatically picks the right specialist agent

---

## 💬 Example Usage

| What you type | What happens |
|---|---|
| `Write a Python function to sort a list of dicts by a key` | Code Generation agent writes the function |
| `Refactor this to use async/await` + paste code | Code Edit agent rewrites it |
| `My app crashes with KeyError: 'name'` + paste code | Debugger finds and fixes the bug |
| `Write tests for this` + paste code | Test Writer generates pytest tests |
| `Review this for security issues` + paste code | Reviewer checks and reports findings |
| `Add docstrings to this` + paste code | Documentation agent adds docstrings |
| `Explain what this code does` + paste code | Orchestrator explains it directly |
| Upload a `.py` file + `refactor this` | File contents sent automatically to the agent |

---

## ⚙️ Model Routing

| Task | Model |
|---|---|
| Orchestration, code gen, debug, review | `llama-3.3-70b-versatile` |
| Tests, docs, lightweight tasks | `llama-3.1-8b-instant` |
| Long context tasks | `mixtral-8x7b-32768` |

All models run on **Groq's free tier** — no cost, no local GPU required.

---

## 📌 Notes

- Input and output are **text only** — paste or upload code directly into the chat
- All agents run on Groq's free API — no paid subscription needed
- The orchestrator handles explain, clarify, and conversational messages directly without delegating
- Groq enforces a 10-enum tool schema limit — sub-agents are capped at 7 to stay within bounds

---
