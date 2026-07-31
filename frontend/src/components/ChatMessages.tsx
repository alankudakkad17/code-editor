import { useEffect, useRef } from "react";
import { ChatMessage } from "../types";
import { MessageContent } from "./MessageContent";

const AGENT_LABELS: Record<string, string> = {
  orchestrator: "Orchestrator",
  planner: "Planner",
  code_generation: "Code Generation",
  code_edit: "Code Edit",
  debugger: "Debugger",
  test_writer: "Test Writer",
  reviewer: "Reviewer",
  documentation: "Documentation",
};

export function ChatMessages({ messages }: { messages: ChatMessage[] }) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
      {messages.map((msg) => (
        <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
          <div
            className={`max-w-3xl rounded-xl px-4 py-3 text-sm ${
              msg.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-100 border border-gray-700"
            }`}
          >
            {msg.role === "agent" && msg.agent && msg.agent !== "orchestrator" && (
              <div className="text-xs text-blue-400 mb-1.5 font-medium">
                {AGENT_LABELS[msg.agent] ?? msg.agent}
              </div>
            )}
            <MessageContent text={msg.text} />
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
