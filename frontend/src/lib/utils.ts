import { Message } from "@/types/messages";

export const logout = () => {
  // sessionStorage.removeItem("access_token");
  window.location.href = "/";
};

export const CreateUserMessage = (
  value: string,
  threadID: number = 0
): Message => {
  return {
    content: value,
    is_user: true,
    session_id: threadID,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
};

export const CreateGeneratingMessage = (): Message => {
  return {
    content: "",
    is_user: false,
    session_id: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    is_generating: true,
  };
};

export const CreateAgentMessage = (
  content: string = "",
  threadID: number
): Message => {
  return {
    content: content,
    is_user: false,
    session_id: threadID,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
};

export const CreateErrorMessage = (
  content: string = "An unexpected error occurred. Please try again.",
  threadID: number = 0
): Message => {
  return {
    content: content,
    is_user: false,
    session_id: threadID,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
};
