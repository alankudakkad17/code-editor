export type MessageRole = "user" | "agent";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  text: string;
  agent?: string;
  timestamp: number;
}

export type ConnectionStatus = "idle" | "thinking" | "working" | "done" | "error";

export interface AgentEvent {
  type: "agent_start" | "agent_update" | "text_chunk" | "final_response" | "error";
  agent?: string;
  text?: string;
  message?: string;
}
