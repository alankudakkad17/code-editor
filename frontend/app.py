import asyncio
import os
import re
import sys
import uuid

# Add backend to path so agents and config can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

from agents.orchestrator import orchestrator
from config import APP_NAME

st.set_page_config(page_title="Agentic Code Editor", page_icon="🤖", layout="wide")
st.title("🤖 Agentic Code Editor")


def render_message(text: str):
    """Render a message — plain text as markdown, code blocks with syntax highlighting + copy button."""
    parts = re.split(r"(```[\w]*\n[\s\S]*?```)", text)
    for part in parts:
        code_match = re.match(r"```(\w+)?\n([\s\S]*?)```", part)
        if code_match:
            lang = code_match.group(1) or "plaintext"
            code = code_match.group(2).rstrip()
            st.code(code, language=lang)
        elif part.strip():
            st.markdown(part)


# ── Sidebar: File Upload ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload File")
    uploaded_file = st.file_uploader(
        "Upload a .py, .js, .ts, or .txt file",
        type=["py", "js", "ts", "tsx", "jsx", "txt"],
        help="File contents will be attached to your next message automatically.",
    )

    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state["uploaded_file_name"] = uploaded_file.name
        st.session_state["uploaded_file_content"] = file_content
        st.success(f"✅ {uploaded_file.name} ready to use")
        with st.expander("Preview file"):
            ext = uploaded_file.name.rsplit(".", 1)[-1]
            st.code(file_content, language=ext)

    # Clear uploaded file button
    if st.session_state.get("uploaded_file_content"):
        if st.button("🗑 Clear file"):
            st.session_state.pop("uploaded_file_name", None)
            st.session_state.pop("uploaded_file_content", None)
            st.rerun()

    st.divider()
    st.caption("Supported: .py · .js · .ts · .tsx · .jsx · .txt")


# ── Session setup ────────────────────────────────────────────────────────────
if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if "runner" not in st.session_state:
    st.session_state.runner = Runner(
        agent=orchestrator,
        app_name=APP_NAME,
        session_service=st.session_state.session_service,
    )

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    asyncio.run(
        st.session_state.session_service.create_session(
            app_name=APP_NAME,
            user_id="user",
            session_id=st.session_state.session_id,
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Describe what you want to build, paste code or upload a file to edit/debug/explain, or ask any coding question.",
            "agent": "orchestrator",
        }
    ]

# ── Chat history ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("agent") and msg["agent"] != "orchestrator":
            st.caption(msg["agent"].replace("_", " ").title())
        render_message(msg["content"])

# ── Chat input ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Describe what you want, or paste code..."):

    # If a file is uploaded, prepend its contents to the prompt
    if st.session_state.get("uploaded_file_content"):
        fname = st.session_state["uploaded_file_name"]
        fcontent = st.session_state["uploaded_file_content"]
        ext = fname.rsplit(".", 1)[-1]
        full_prompt = (
            f"File: `{fname}`\n"
            f"```{ext}\n{fcontent}\n```\n\n"
            f"{prompt}"
        )
        display_prompt = f"📎 `{fname}`\n\n{prompt}"
        # Clear file after sending
        st.session_state.pop("uploaded_file_name", None)
        st.session_state.pop("uploaded_file_content", None)
    else:
        full_prompt = prompt
        display_prompt = prompt

    st.session_state.messages.append({"role": "user", "content": display_prompt})
    with st.chat_message("user"):
        render_message(display_prompt)

    with st.chat_message("assistant"):
        agent_label = st.empty()
        stream_container = st.empty()
        state = {"full_response": "", "current_agent": ""}

        async def stream_response():
            async for event in st.session_state.runner.run_async(
                user_id="user",
                session_id=st.session_state.session_id,
                new_message=Content(role="user", parts=[Part(text=full_prompt)]),
            ):
                if hasattr(event, "author") and event.author:
                    if event.author != state["current_agent"]:
                        state["current_agent"] = event.author
                        label = event.author.replace("_", " ").title()
                        agent_label.caption(f"⚙ {label}...")

                if hasattr(event, "content") and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            state["full_response"] += part.text
                            stream_container.markdown(state["full_response"] + "▌")

        asyncio.run(stream_response())
        agent_label.empty()
        stream_container.empty()
        render_message(state["full_response"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": state["full_response"],
        "agent": state["current_agent"],
    })
