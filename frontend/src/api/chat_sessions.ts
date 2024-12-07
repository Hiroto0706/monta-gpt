import apiClient from "@/lib/apiClient";
import { ChatSession } from "@/types/chat_sessions";

/*
  FetchThreadList はスレッドのリストを取得する関数
*/
export const FetchThreadList = async (): Promise<ChatSession[]> => {
  try {
    const response = await apiClient.get("chat_sessions/", {
      withCredentials: true,
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching thread list: ", error);
    return [];
  }
};

/*
  CreateThread は新しいスレッドを作成する関数
*/
export const CreateThread = async (prompt: string): Promise<ChatSession> => {
  const formData = { prompt };

  try {
    const response = await apiClient.post("chat_sessions/", formData, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error("An unexpected error occurred. Please try again.:", error);
    throw new Error("An unexpected error occurred. Please try again.");
  }
};
