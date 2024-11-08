import apiClient from "@/lib/apiClient";
import { Thread } from "@/types/threads";

/*
  FetchThreadList はスレッドのリストを取得する関数
*/
export const FetchThreadList = async (): Promise<Thread[]> => {
  try {
    const response = await apiClient.get("chat_sessions/");
    return response.data;
  } catch (error) {
    console.error("Error fetching thread list: ", error);
    return [];
  }
};

/*
  CreateThread は新しいスレッドを作成する関数
*/
export const CreateThread = async (prompt: string): Promise<Thread> => {
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
