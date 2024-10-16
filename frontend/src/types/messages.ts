export interface Message {
  content: string;
  is_user: boolean;
  id: number;
  session_id: number;
  created_at: string;
  updated_at: string;
}
