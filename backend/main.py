import json
import os
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

from agents.orchestrator import orchestrator
from config import APP_NAME

app = FastAPI(title="Agentic Code Editor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
runner = Runner(
    agent=orchestrator,
    app_name=APP_NAME,
    session_service=session_service,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    user_id = f"user-{session_id}"

    existing = await session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    if not existing:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            prompt = data.get("prompt", "").strip()

            if not prompt:
                continue

            await websocket.send_json({"type": "agent_start", "agent": "orchestrator"})

            try:
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=Content(role="user", parts=[Part(text=prompt)]),
                ):
                    if hasattr(event, "author") and event.author:
                        await websocket.send_json({
                            "type": "agent_update",
                            "agent": event.author,
                        })

                    if hasattr(event, "content") and event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, "text") and part.text:
                                await websocket.send_json({
                                    "type": "text_chunk",
                                    "agent": getattr(event, "author", "orchestrator"),
                                    "text": part.text,
                                })

                    if hasattr(event, "is_final_response") and event.is_final_response():
                        final_text = ""
                        if event.content and event.content.parts:
                            final_text = "".join(
                                p.text for p in event.content.parts if hasattr(p, "text")
                            )
                        await websocket.send_json({
                            "type": "final_response",
                            "text": final_text,
                        })

            except Exception as e:
                await websocket.send_json({"type": "error", "message": str(e)})

    except WebSocketDisconnect:
        pass
