import { Timestamp } from ".";
import { UserID } from "./users";

export interface Thread {
  id: number;
  user_id: number;
  summary: string;
  start_time: string;
  end_time: string;
  created_at: string;
  updated_at: string;
  content?: string;
}

// ---

type ChatSessionID = number;
type ChatSessionSummary = string;
type ChatSessionFirstContent = string;

interface BaseChatSession {
  id: ChatSessionID;
  user_id: UserID;
  summary: ChatSessionSummary;
  start_time: Timestamp;
  end_time: Timestamp;
  created_at: Timestamp;
  updated_at: Timestamp;
}

export interface ChatSession extends BaseChatSession {}

export interface InitialChatSession extends BaseChatSession {
  content: ChatSessionFirstContent;
}
