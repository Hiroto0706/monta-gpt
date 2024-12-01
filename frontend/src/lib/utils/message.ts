import { AIMessage, GeneratingMessage, HumanMessage } from "@/types/messages";

export const isGeneratingMessage = (
  message: HumanMessage | AIMessage | GeneratingMessage
): message is GeneratingMessage => {
  return !message.isUser && message.isGenerating === true;
};

export const isAIMessage = (
  message: HumanMessage | AIMessage | GeneratingMessage
): message is AIMessage => {
  return !message.isUser && message.isGenerating === false;
};

export const isHumanMessage = (
  message: HumanMessage | AIMessage | GeneratingMessage
): message is HumanMessage => {
  return message.isUser;
};

export const CreateUserMessage = (
  value: string,
  threadID: number = 0
): HumanMessage => {
  return {
    id: 9999, // TODO: この時点ではUserIDはわからないので9999とする。
    content: value,
    isUser: true,
    sessionID: threadID,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
};

export const CreateGeneratingMessage = (): GeneratingMessage => {
  return {
    id: 9999, // TODO: この時点ではUserIDはわからないので9999とする。
    content: "",
    isUser: false,
    sessionID: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    isGenerating: true,
  };
};

export const CreateAgentMessage = (
  content: string = "",
  threadID: number
): AIMessage => {
  return {
    id: 9999, // TODO: この時点ではUserIDはわからないので9999とする。
    content: content,
    isUser: false,
    sessionID: threadID,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    isGenerating: false,
  };
};

export const CreateErrorMessage = (
  content: string = "An unexpected error occurred. Please try again.",
  threadID: number = 0
): AIMessage => {
  return {
    id: 9999, // TODO: この時点ではUserIDはわからないので9999とする。
    content: content,
    isUser: false,
    sessionID: threadID,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    isGenerating: false,
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

/**
 * GeneratingMessageをAIMessageに変換する関数
 */
export const addNewMessageToPreviousMessages = (
  prevMessages: (HumanMessage | AIMessage | GeneratingMessage)[],
  newMessage: AIMessage
): (HumanMessage | AIMessage)[] => {
  const updatedMessages = [...prevMessages];

  for (let i = updatedMessages.length - 1; i >= 0; i--) {
    const currentMessage = updatedMessages[i];

    if (isGeneratingMessage(currentMessage) || isAIMessage(currentMessage)) {
      const existingContent = currentMessage.content ?? "";

      updatedMessages[i] = {
        ...currentMessage,
        content: existingContent + newMessage.content,
        isGenerating: false, // 常に AIMessage に変換
      };

      break;
    }
  }

  // GeneratingMessage を含まない配列を返す
  return updatedMessages.filter(
    (message): message is HumanMessage | AIMessage =>
      message.isUser || (message.isUser === false && !message.isGenerating)
  );
};
