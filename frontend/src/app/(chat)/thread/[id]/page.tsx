"use client";

import { ContinueConversation, FetchMessagesList } from "@/api/messages";
import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/hooks/useSidebar";
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

  /*
    handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
  */
  const handleSubmit = async (value: string) => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // FIXME: idはwebsocket通信よりidが帰ってきたらmessagesに追加するようにする
    const userMessage = CreateUserMessage(value);
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // "generating..." メッセージを追加
    const generatingMessage = CreateGeneratingMessage();
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    // 画面を一番下にスクロール
    scrollToBottom();

    try {
      const threadID = params.id;
      const response = await ContinueConversation(threadID, value);

      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages.pop(); // "generating..." メッセージを削除
        return [...updatedMessages, response];
      });
    } catch (error) {
      console.error(error);
      // エラーメッセージを会話に追加
      const errorMessage = CreateErrorMessage();
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

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
