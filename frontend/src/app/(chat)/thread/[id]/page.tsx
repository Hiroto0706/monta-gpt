"use client";

import { FetchMessagesList } from "@/api/messages";
import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/hooks/useSidebar";
import { useWebSocket } from "@/hooks/useWebSocket";
import { CreateGeneratingMessage, CreateUserMessage } from "@/lib/utils";
import { Message } from "@/types/messages";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

export default function ThreadPage({ params }: { params: { id: number } }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isOpen } = useSidebar();

  /**
   * handleWebSocketMessage はWebサーバから受け取ったmessageを処理する関数
   * @param newContent {Message} WebSocketサーバから受け取ったメッセージ
   */
  const handleWebSocketMessage = useCallback((newContent: Message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages];
      for (let i = updatedMessages.length - 1; i >= 0; i--) {
        if (!updatedMessages[i].is_user) {
          const existingContent = updatedMessages[i].content ?? "";
          updatedMessages[i] = {
            ...updatedMessages[i],
            content: existingContent + newContent.content,
            is_generating: false,
          };
          break;
        }
      }
      return updatedMessages;
    });
  }, []);

  const baseUrl = useMemo(() => {
    return `${process.env.NEXT_PUBLIC_BASE_URL_WS}messages/conversation?session_id=${params.id}`;
  }, [params.id]);

  const { sendMessage, isConnected } = useWebSocket(
    baseUrl,
    handleWebSocketMessage
  );

  /**
   * handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
   * @param value {string} ユーザーからのプロンプト
   */
  const handleSubmit = async (value: string) => {
    if (!isConnected) {
      // FIXME: idはwebsocket通信よりidが帰ってきたらmessagesに追加するようにする
      const userMessage = CreateUserMessage(value);
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      const generatingMessage = CreateGeneratingMessage();
      setMessages((prevMessages) => [...prevMessages, generatingMessage]);

      const threadID = params.id;
      sendMessage(value, threadID);
    }
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
        <ChatBoxComponent
          handleSubmit={handleSubmit}
          isConnected={isConnected}
        />
      </div>
    </>
  );
}
