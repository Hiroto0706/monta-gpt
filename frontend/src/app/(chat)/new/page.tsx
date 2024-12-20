"use client";

import ChatBoxComponent from "@/components/ui/form/chatBox";
import ChatHistoryLayout from "@/components/layouts/chatHistory";
import { useWebSocket } from "@/hooks/useWebSocket";
import {
  addNewMessageToPreviousMessages,
  CreateGeneratingMessage,
  CreateUserMessage,
  ScrollToBottom,
} from "@/lib/utils/message";
import { AIMessage, GeneratingMessage, HumanMessage } from "@/types/messages";
import { useContext, useEffect, useRef, useState } from "react";
import { SidebarContext } from "@/contexts/sidebarContext";

export default function Page() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const hasChatStartRef = useRef(false);
  const hasNavigatedRef = useRef(false); // URL画面遷移済みかどうかを管理する
  const sessionIDRef = useRef<number | null>(null);
  const [messages, setMessages] = useState<
    (HumanMessage | AIMessage | GeneratingMessage)[]
  >([]);
  const { isOpen } = useContext(SidebarContext);

  /**
   * handleWebSocketMessage はWebサーバから受け取ったメッセージを処理する関数
   * @param newMessage
   */
  const handleWebSocketMessage = (newMessage: AIMessage) => {
    // 画面遷移の条件定義 & ロジック
    const newUrl = `/thread/${newMessage.sessionID}`;
    const hasTransitionCondition =
      !hasNavigatedRef.current &&
      newMessage.sessionID !== 0 &&
      window.location.pathname !== newUrl;

    if (hasTransitionCondition) {
      sessionIDRef.current = newMessage.sessionID;
      window.history.pushState(null, "", newUrl);
      hasNavigatedRef.current = true;
    }

    setMessages((prevMessages) =>
      addNewMessageToPreviousMessages(prevMessages, newMessage)
    );
  };

  const { sendMessage, isConnected } = useWebSocket(handleWebSocketMessage);

  /**
   * handleSubmit はユーザーからの質問を受け取りAIの回答を生成し、新しいスレッドを作成する関数
   * @param value {string} ユーザーからのプロンプト
   */
  const handleSubmit = async (value: string) => {
    if (!isConnected) {
      const userMessage = CreateUserMessage(value);
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      const generatingMessage = CreateGeneratingMessage();
      setMessages((prevMessages) => [...prevMessages, generatingMessage]);

      const baseUrl = !hasChatStartRef.current
        ? process.env.NEXT_PUBLIC_BASE_URL_WS + "chat_sessions/create"
        : process.env.NEXT_PUBLIC_BASE_URL_WS + "messages/conversation";

      if (sessionIDRef.current !== null) {
        sendMessage(value, baseUrl, sessionIDRef.current);
      } else {
        sendMessage(value, baseUrl);
      }
      hasChatStartRef.current = true;
    }
  };

  // 会話履歴が取得できたら一番下にスクロールする
  useEffect(() => {
    ScrollToBottom(messagesEndRef);
  }, [messages.length]);

  return (
    <>
      {hasChatStartRef.current ? (
        <>
          <ChatHistoryLayout
            messages={messages}
            messagesEndRef={messagesEndRef}
          />
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
      ) : (
        <div className="flex items-center justify-center h-screen">
          <div className="text-center w-full max-w-[640px] mx-4">
            <p className="text-2xl font-bold mb-8">What Can I Help With?</p>
            <ChatBoxComponent
              handleSubmit={handleSubmit}
              isConnected={isConnected}
            />
          </div>
        </div>
      )}
    </>
  );
}
