"use client";

import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/hooks/useSidebar";
import { useWebSocket } from "@/hooks/useWebSocket";
import {
  CreateErrorMessage,
  CreateGeneratingMessage,
  CreateUserMessage,
} from "@/lib/utils";
import { Message } from "@/types/messages";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function NewThreadPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatStarted, setChatStarted] = useState(false);
  const { isOpen } = useSidebar();

  /**
   * handleWebSocketMessage はWebサーバから受け取ったメッセージを処理する関数
   * @param data
   */
  const handleWebSocketMessage = (newMessage: Message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages];
      updatedMessages.pop();
      return [...updatedMessages, newMessage];
    });

    if (newMessage.session_id !== 0) {
      router.push(`/thread/${newMessage.id}`);
    }
  };

  const baseUrl: string = process.env.NEXT_PUBLIC_BASE_URL_WS + "chat_sessions";
  const { sendMessage, isConnected } = useWebSocket(
    baseUrl,
    handleWebSocketMessage
  );

  /**
   * handleSubmit はユーザーからの質問を受け取りAIの回答を生成し、新しいスレッドを作成する関数
   * @param value {string} ユーザーからのプロンプト
   */
  const handleSubmit = async (value: string) => {
    const userMessage = CreateUserMessage(value);
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    const generatingMessage = CreateGeneratingMessage();
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    setChatStarted(true);

    // WebSocket経由でスレッド作成リクエストを送信
    if (isConnected) {
      sendMessage(value, 0); // スレッド新規作成時はthread_idは存在しないので0
    } else {
      console.error("WebSocket is not connected");
      const errorMessage = CreateErrorMessage();
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <>
      {chatStarted ? (
        <>
          <ChatHistoryComponent messages={messages} />
          <div
            className={`fixed bottom-0 w-full max-w-[640px] transform -translate-x-1/2 p-4 duration-300 left-[50%] ${
              !isOpen ? "" : "md:left-[calc(50%+6rem)]"
            }`}
          >
            <ChatBoxComponent handleSubmit={handleSubmit} />
          </div>
        </>
      ) : (
        <div className="flex items-center justify-center h-screen">
          <div className="text-center w-full max-w-[640px] mx-4">
            <p className="text-2xl font-bold mb-8">なんでも聞いてや〜</p>
            <ChatBoxComponent handleSubmit={handleSubmit} />
          </div>
        </div>
      )}
    </>
  );
}
