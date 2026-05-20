import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Groq model tiers
HEAVY_MODEL = "groq/llama-3.3-70b-versatile"   # for orchestrator + code agents
LIGHT_MODEL = "groq/llama-3.1-8b-instant"                    # fast, lightweight tasks
LONG_CTX_MODEL = "groq/mixtral-8x7b-32768"                   # large context

APP_NAME = "agentic-code-editor"
