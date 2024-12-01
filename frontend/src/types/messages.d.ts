import { Timestamp } from ".";
import { ChatSessionID } from "./chat_sessions";

export interface ContinueConversationRequest {
  sessionID: number;
  prompt: string;
}

type MessageID = number;
type MessageContent = string;

interface BaseMessage {
  id: MessageID;
  content: MessageContent;
  sessionID: ChatSessionID;
  createdAt: Timestamp;
  updatedAt: Timestamp;
  isUser: boolean;
}

export interface HumanMessage extends BaseMessage {
  isUser: true;
}

export interface AIMessage extends BaseMessage {
  isUser: false;
  isGenerating: false;
}

export interface GeneratingMessage extends BaseMessage {
  isUser: false;
  isGenerating: true;
}
