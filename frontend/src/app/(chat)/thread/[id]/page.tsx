"use client";

import { FetchMessagesList } from "@/api/messages";
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
import { useEffect, useRef, useState } from "react";

export default function ThreadPage({ params }: { params: { id: number } }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isOpen } = useSidebar();

  /**
   * handleWebSocketMessage はWebサーバから受け取ったmessageを処理する関数
   * @param message {string} WebSocketサーバから受け取ったテキスト
   */
  const handleWebSocketMessage = (message: Message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const baseUrl: string =
    process.env.NEXT_PUBLIC_BASE_URL_WS + "messages/conversation";
  const { sendMessage, isConnected } = useWebSocket(
    baseUrl,
    handleWebSocketMessage
  );

  /**
   * handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
   * @param value {string} ユーザーからのプロンプト
   */
  const handleSubmit = async (value: string) => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // FIXME: idはwebsocket通信よりidが帰ってきたらmessagesに追加するようにする
    const userMessage = CreateUserMessage(value);
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    const generatingMessage = CreateGeneratingMessage();
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    const threadID = params.id;
    if (isConnected) {
      sendMessage(value, threadID);
    } else {
      const errorText = "WebSocket is not connected";
      console.error(errorText);
      const errorMessage = CreateErrorMessage(errorText);
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }

    scrollToBottom();
  };

  /**
   * 初回レンダリング時に会話履歴を取得する
   */
  useEffect(() => {
    if (params.id) {
      const loadThreadDetail = async () => {
        const response = await FetchMessagesList(params.id);
        setMessages(response);
      };
      loadThreadDetail();
    }
  }, [params.id]);

  return (
    <>
      <ChatHistoryComponent
        messages={messages}
        messagesEndRef={messagesEndRef}
      />

      <div
        className={`fixed bottom-0 w-full max-w-[640px] transform -translate-x-1/2 p-4 duration-300 left-[50%] ${
          !isOpen ? "" : "md:left-[calc(50%+6rem)]"
        }`}
      >
        <ChatBoxComponent handleSubmit={handleSubmit} />
      </div>
    </>
  );
}
