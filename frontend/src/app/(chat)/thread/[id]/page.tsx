"use client";

import { FetchMessagesList } from "@/api/messages";
import ChatBoxComponent from "@/components/ui/form/chatBox";
import ChatHistoryLayout from "@/components/layouts/chatHistory";
import { useWebSocket } from "@/hooks/useWebSocket";
import {
  addNewMessageToPreviousMessages,
  CreateGeneratingMessage,
  CreateUserMessage,
} from "@/lib/utils/message";
import { AIMessage, GeneratingMessage, HumanMessage } from "@/types/messages";
import { useRouter } from "next/navigation";
import { useContext, useEffect, useRef, useState } from "react";
import { SidebarContext } from "@/contexts/sidebarContext";

export default function Page({ params }: { params: { id: number } }) {
  const [messages, setMessages] = useState<
    (HumanMessage | AIMessage | GeneratingMessage)[]
  >([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isOpen } = useContext(SidebarContext);
  const router = useRouter();

  /**
   * handleWebSocketMessage はWebサーバから受け取ったmessageを処理する関数
   * @param newContent {Message} WebSocketサーバから受け取ったメッセージ
   */
  const handleWebSocketMessage = (newMessage: AIMessage) => {
    setMessages((prevMessages) =>
      addNewMessageToPreviousMessages(prevMessages, newMessage)
    );
  };

  const { sendMessage, isConnected } = useWebSocket(handleWebSocketMessage, {
    session_id: params.id,
  });

  /**
   * handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
   * @param value {string} ユーザーからのプロンプト
   */
  const handleSubmit = async (value: string) => {
    if (!isConnected) {
      const userMessage = CreateUserMessage(value);
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      const generatingMessage = CreateGeneratingMessage();
      setMessages((prevMessages) => [...prevMessages, generatingMessage]);

      const threadID = params.id;
      const baseUrl = `${process.env.NEXT_PUBLIC_BASE_URL_WS}messages/conversation`;
      sendMessage(value, baseUrl, threadID);
    }
  };

  /**
   * 初回レンダリング時に会話履歴を取得する
   */
  useEffect(() => {
    if (params.id) {
      const loadThreadDetail = async () => {
        const response = await FetchMessagesList(params.id);

        if (response.length > 0) {
          setMessages(response);
        } else {
          router.push("/new");
        }
      };

      loadThreadDetail();
    }
  }, [params.id]);

  return (
    <>
      <ChatHistoryLayout messages={messages} messagesEndRef={messagesEndRef} />
      <div
        className={`fixed bottom-0 w-full max-w-[580px] lg:max-w-[640px] transform -translate-x-1/2 p-4 duration-300 left-[50%] ${
          !isOpen ? "" : "md:left-[calc(50%+6.5rem)]"
        }`}
      >
        <ChatBoxComponent
          handleSubmit={handleSubmit}
          isConnected={isConnected}
        />
      </div>
    </>
  );
}
