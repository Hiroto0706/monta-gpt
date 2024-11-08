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
