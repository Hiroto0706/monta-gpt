import apiClient from "@/lib/apiClient";
import {
  AIMessage,
  ContinueConversationRequest,
  HumanMessage,
} from "@/types/messages";

/*
  FetchMessagesList はsessionIDに紐づいたメッセージを取得する関数
*/
export const FetchMessagesList = async (
  sessionID: number
): Promise<HumanMessage[] | AIMessage[]> => {
  try {
    const response = await apiClient.get(`messages/${sessionID}`, {
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching messages list.Please try again: ", error);
    return [];
  }
};

/*
  ContinueConversation はsessionIDでAgentとの会話を行う関数
*/
export const ContinueConversation = async (
  sessionID: number,
  prompt: string
): Promise<AIMessage> => {
  const formData: ContinueConversationRequest = {
    sessionID,
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
