import { useState, useCallback, useEffect } from "react";
import { ChatMessages } from "./components/ChatMessages";
import { FileUpload } from "./components/FileUpload";
import { useWebSocket } from "./hooks/useWebSocket";
import { ChatMessage, AgentEvent } from "./types";

const SESSION_ID = `session-${Date.now()}`;

function makeId() {
  return Math.random().toString(36).slice(2);
}

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

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: makeId(),
      role: "agent",
      agent: "orchestrator",
      text: "Hello! Describe what you want to build, paste code or attach a file to edit/debug/explain, or ask any coding question.",
      timestamp: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);

  const { sendPrompt, onEvent, status, activeAgent } = useWebSocket(SESSION_ID);
  const isDisabled = status === "thinking" || status === "working";

  useEffect(() => {
    onEvent((event: AgentEvent) => {
      if (event.type === "text_chunk" && event.text) {
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "agent" && last.agent === event.agent) {
            return [...prev.slice(0, -1), { ...last, text: last.text + event.text }];
          }
          return [
            ...prev,
            { id: makeId(), role: "agent", agent: event.agent, text: event.text!, timestamp: Date.now() },
          ];
        });
      }

      if (event.type === "final_response" && event.text) {
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "agent") return prev;
          return [
            ...prev,
            { id: makeId(), role: "agent", agent: "orchestrator", text: event.text!, timestamp: Date.now() },
          ];
        });
      }

      if (event.type === "error") {
        setMessages((prev) => [
          ...prev,
          { id: makeId(), role: "agent", agent: "system", text: `Error: ${event.message}`, timestamp: Date.now() },
        ]);
      }
    });
  }, [onEvent]);

  const handleSend = useCallback(() => {
    const trimmed = input.trim();
    if (!trimmed || isDisabled) return;

    let fullPrompt = trimmed;
    let displayText = trimmed;

    if (fileName && fileContent) {
      const ext = fileName.split(".").pop() || "";
      fullPrompt = `File: \`${fileName}\`\n\`\`\`${ext}\n${fileContent}\n\`\`\`\n\n${trimmed}`;
      displayText = `📎 \`${fileName}\`\n\n${trimmed}`;
    }

    setMessages((prev) => [
      ...prev,
      { id: makeId(), role: "user", text: displayText, timestamp: Date.now() },
    ]);
    sendPrompt(fullPrompt);
    setInput("");
    setFileName(null);
    setFileContent(null);
  }, [input, isDisabled, sendPrompt, fileName, fileContent]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      <div className="px-6 py-3 border-b border-gray-700 bg-gray-800 flex items-center gap-3">
        <span className="font-semibold text-white">🤖 Agentic Code Editor</span>
        {isDisabled && (
          <span className="flex items-center gap-1.5 text-sm text-blue-400">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
            {AGENT_LABELS[activeAgent] ?? "Thinking"}...
          </span>
        )}
      </div>

      <ChatMessages messages={messages} />

      <div className="px-4 py-3 border-t border-gray-700 bg-gray-800">
        <div className="max-w-4xl mx-auto space-y-2">
          {fileName && (
            <FileUpload
              fileName={fileName}
              onFileSelect={() => {}}
              onClear={() => {
                setFileName(null);
                setFileContent(null);
              }}
            />
          )}
          <div className="flex gap-3 items-end">
            {!fileName && (
              <FileUpload
                fileName={null}
                onFileSelect={(name, content) => {
                  setFileName(name);
                  setFileContent(content);
                }}
                onClear={() => {}}
              />
            )}
            <textarea
              className="flex-1 bg-gray-900 text-gray-100 rounded-xl px-4 py-3 text-sm resize-none outline-none border border-gray-700 focus:border-blue-500 transition-colors"
              rows={3}
              placeholder="Describe what you want, or paste code... (Enter to send, Shift+Enter for new line)"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isDisabled}
            />
            <button
              onClick={handleSend}
              disabled={isDisabled || !input.trim()}
              className="px-5 py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl text-sm font-medium transition-colors"
            >
              {isDisabled ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
