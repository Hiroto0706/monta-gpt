import apiClient from "@/lib/apiClient";
import { ContinueConversationRequest, Message } from "@/types/messages";

/*
  FetchMessagesList はthreadIDに紐づいたメッセージを取得する関数
*/
export const FetchMessagesList = async (
  threadID: number
): Promise<Message[]> => {
  try {
    const response = await apiClient.get(`messages/${threadID}`, {
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching messages list.Please try again: ", error);
    return [];
  }
};

/*
  ContinueConversation はthreadIDでAgentとの会話を行う関数
*/
export const ContinueConversation = async (
  session_id: number,
  prompt: string
): Promise<Message> => {
  const formData: ContinueConversationRequest = {
    session_id,
    prompt,
  };

  try {
    const response = await apiClient.post("messages/conversation", formData, {
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.error("An unexpected error occurred. Please try again: ", error);
    throw new Error("An unexpected error occurred. Please try again.");
  }
};
