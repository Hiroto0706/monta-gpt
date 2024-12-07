import { Timestamp } from ".";
import { UserID } from "./users";

type ChatSessionID = number;
type ChatSessionSummary = string;
type ChatSessionFirstContent = string;

interface BaseChatSession {
  id: ChatSessionID;
  userID: UserID;
  summary: ChatSessionSummary;
  startTime: Timestamp;
  endTime: Timestamp;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

export type ChatSession = BaseChatSession;
