# 🤖 Agentic Code Editor

A chat-based AI coding assistant built with **Google ADK**, **Groq API**, **React**, and **FastAPI**, where users simply describe what they want in plain English or upload a file and a team of 8 specialized agents handles the rest — an **Orchestrator** routes each request to the right agent, the **Planner** breaks complex tasks into steps, **Code Generation** writes new code, **Code Edit** refactors existing code, **Debugger** finds and fixes bugs, **Test Writer** generates tests, **Reviewer** checks for quality and security issues, and **Documentation** adds docstrings and comments — with responses streamed in real-time over WebSockets and rendered with syntax-highlighted, copyable code blocks, all powered by **LLaMA 3.3 70B** on Groq's free tier at zero infrastructure cost, and fully containerized with **Docker**.

---

## 🏗️ Architecture

```
React Frontend (Vite + TS)
        │ WebSocket
        ▼
FastAPI Backend (Uvicorn)
        │
  Orchestrator Agent (Google ADK)   ← routes to the right specialist
        │
   ┌────┴─────────────────────────────────────┐
   ▼        ▼         ▼        ▼       ▼      ▼       ▼
Planner  Code Gen  Code Edit  Debug  Tests  Review  Docs
        │
        ▼
   Groq API (LLaMA 3.3 70B / 3.1 8B)
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
| **Frontend** | React 18 + TypeScript + Vite + Tailwind CSS |
| **API / Streaming** | FastAPI + WebSockets |
| **Agent Framework** | Google ADK (Agent Development Kit) |
| **LLM Provider** | Groq API (free tier) |
| **Models** | `llama-3.3-70b-versatile` · `llama-3.1-8b-instant` · `mixtral-8x7b-32768` |
| **Containerization** | Docker + Docker Compose |
| **Frontend serving** | Nginx (production build) |

---

## 📁 Project Structure

```
agentic-code-editor/
├── docker-compose.yml
├── .env                     ← API keys (used by docker-compose)
├── .env.example
├── requirements.txt
├── README.md
│
├── frontend/
│   ├── Dockerfile           ← multi-stage build (Vite → Nginx)
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── index.css
│       ├── types/index.ts
│       ├── hooks/useWebSocket.ts
│       └── components/
│           ├── ChatMessages.tsx
│           ├── MessageContent.tsx   ← syntax highlighting + copy button
│           └── FileUpload.tsx
│
└── backend/
    ├── Dockerfile
    ├── main.py              ← FastAPI + WebSocket server
    ├── config.py             ← Model configuration
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

### Option A — Run with Docker (recommended)

**1. Install Docker Desktop**

Download from [docker.com](https://www.docker.com/products/docker-desktop/) (requires WSL2 on Windows).

**2. Set up your API key**

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

**3. Build and run**

```bash
docker compose up --build
```

- Frontend → **http://localhost:5173**
- Backend API → **http://localhost:8000**

**4. Stop**

```bash
docker compose down
```

---

### Option B — Run locally without Docker

**Backend:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

cd ..
pip install -r requirements.txt
uvicorn main:app --reload --app-dir backend
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

---

## ✨ Features

- 💬 **Real-time chat interface** — describe what you want in plain English
- 📁 **File upload** — attach `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.txt` files directly into the chat
- 🎨 **Syntax highlighting** — all code responses rendered with `react-syntax-highlighter`
- 📋 **Copy button** — one-click copy on every code block
- ⚡ **WebSocket streaming** — see agent responses token-by-token as they generate
- 🔀 **Agent routing** — orchestrator automatically picks the right specialist agent
- 🐳 **Fully containerized** — one command spins up the whole stack

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
| Attach a `.py` file + `refactor this` | File contents sent automatically to the agent |

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
- WebSocket URL is configurable at build time via `VITE_WS_URL` (set in `docker-compose.yml`)

---
