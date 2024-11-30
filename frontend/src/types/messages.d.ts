import { Timestamp } from ".";
import { ChatSessionID } from "./chat_sessions";

export interface Message {
  content?: string;
  is_user: boolean;
  id?: number;
  session_id: number;
  created_at: string;
  updated_at: string;
  is_generating?: boolean;
}

export interface ContinueConversationRequest {
  session_id: number;
  prompt: string;
}

// ---

type MessageID = number;
type MessageContent = string;

interface BaseMessage {
  id: MessageID;
  content: MessageContent;
  session_id: ChatSessionID;
  created_at: Timestamp;
  updated_at: Timestamp;
  is_user: boolean;
}

export interface HumanMessage extends BaseMessage {
  is_user: true;
}

export interface AIMessage extends BaseMessage {
  is_user: false;
}

export interface GeneratingMessage extends BaseMessage {
  is_user: false;
  is_generating: true;
}
