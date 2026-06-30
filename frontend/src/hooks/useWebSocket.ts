import { useEffect, useRef, useCallback, useState } from "react";
import { AgentEvent, ConnectionStatus } from "../types";

const WS_BASE = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

export function useWebSocket(sessionId: string) {
  const ws = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>("idle");
  const [activeAgent, setActiveAgent] = useState<string>("");
  const onEventRef = useRef<((event: AgentEvent) => void) | null>(null);

  const connect = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) return;

    ws.current = new WebSocket(`${WS_BASE}/${sessionId}`);

    ws.current.onopen = () => setStatus("idle");

    ws.current.onmessage = (e) => {
      const event: AgentEvent = JSON.parse(e.data);

      if (event.type === "agent_start" || event.type === "agent_update") {
        setStatus("working");
        setActiveAgent(event.agent ?? "");
      } else if (event.type === "final_response") {
        setStatus("done");
        setActiveAgent("");
      } else if (event.type === "error") {
        setStatus("error");
        setActiveAgent("");
      }

      onEventRef.current?.(event);
    };

    ws.current.onclose = () => setStatus("idle");
    ws.current.onerror = () => setStatus("error");
  }, [sessionId]);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);

  const sendPrompt = useCallback((prompt: string) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      setStatus("thinking");
      ws.current.send(JSON.stringify({ prompt }));
    }
  }, []);

  const onEvent = useCallback((handler: (event: AgentEvent) => void) => {
    onEventRef.current = handler;
  }, []);

  return { sendPrompt, onEvent, status, activeAgent };
}
