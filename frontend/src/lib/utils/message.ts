import { Message } from "@/types/messages";

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

/**
 * scrollToBottom はtargetRefに要素をスクロールする関数
 */
export const ScrollToBottom = (
  targetRef: React.RefObject<HTMLDivElement> | undefined
): void => {
  if (targetRef != undefined) {
    targetRef.current?.scrollIntoView({ behavior: "smooth" });
  }
};

export const addNewMessageToPreviousMessages = (
  prevMessages: Message[],
  newMessage: Message
): Message[] => {
  const updatedMessages = [...prevMessages];
  for (let i = updatedMessages.length - 1; i >= 0; i--) {
    if (!updatedMessages[i].is_user) {
      const existingContent = updatedMessages[i].content ?? "";
      updatedMessages[i] = {
        ...updatedMessages[i],
        content: existingContent + newMessage.content,
        is_generating: false,
      };
      break;
    }
  }
  return updatedMessages;
};
