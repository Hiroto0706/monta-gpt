"use client";

import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/hooks/useSidebar";
import { useWebSocket } from "@/hooks/useWebSocket";
import { CreateGeneratingMessage, CreateUserMessage } from "@/lib/utils";
import { Message } from "@/types/messages";
import { useCallback, useEffect, useRef, useState } from "react";

export default function NewThreadPage() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const hasChatStartRef = useRef(false);
  const hasNavigatedRef = useRef(false); // URL画面遷移済みかどうかを管理する
  const sessionIDRef = useRef<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const { isOpen } = useSidebar();

  /**
   * handleWebSocketMessage はWebサーバから受け取ったメッセージを処理する関数
   * @param newMessage
   */
  const handleWebSocketMessage = useCallback((newMessage: Message) => {
    const newUrl = `/thread/${newMessage.session_id}`;

    if (
      !hasNavigatedRef.current &&
      newMessage.session_id !== 0 &&
      window.location.pathname !== newUrl
    ) {
      sessionIDRef.current = newMessage.session_id;
      window.history.pushState(null, "", newUrl);
      hasNavigatedRef.current = true;
    }

    setMessages((prevMessages) => {
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
    });
  }, []);

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

  // FIXME: これはカスタムフックしたい
  /**
   * scrollToBottom は一番下部に要素をスクロールする関数
   */
  const scrollToBottom = (): void => {
    if (messagesEndRef != undefined) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages.length]);

  return (
    <>
      {hasChatStartRef.current ? (
        <>
          <ChatHistoryComponent
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
            <p className="text-2xl font-bold mb-8">なんでも聞いてや〜</p>
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
