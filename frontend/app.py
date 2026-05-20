import asyncio
import os
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

# Persist session service and runner across Streamlit reruns
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
            "content": "Hello! Describe what you want to build, paste code to edit/debug/explain, or ask any coding question.",
            "agent": "orchestrator",
        }
    ]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and msg.get("agent") and msg["agent"] != "orchestrator":
            st.caption(msg["agent"].replace("_", " ").title())
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Describe what you want, or paste code..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        agent_label = st.empty()
        response_container = st.empty()

        # Use a dict so the async function can mutate it without nonlocal
        state = {"full_response": "", "current_agent": ""}

        async def stream_response():
            async for event in st.session_state.runner.run_async(
                user_id="user",
                session_id=st.session_state.session_id,
                new_message=Content(role="user", parts=[Part(text=prompt)]),
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
                            response_container.markdown(state["full_response"] + "▌")

        asyncio.run(stream_response())
        agent_label.empty()
        response_container.markdown(state["full_response"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": state["full_response"],
        "agent": state["current_agent"],
    })
