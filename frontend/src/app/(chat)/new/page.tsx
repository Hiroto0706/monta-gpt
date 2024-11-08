"use client";

import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/contexts/SidebarContext";
import { Message } from "@/types/messages";
import { Thread } from "@/types/threads";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function NewThreadPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatStarted, setChatStarted] = useState(false);
  const [threadID, setThreadID] = useState<number>();
  const { isOpen } = useSidebar();

  {
    /*
    handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
    */
  }
  const handleSubmit = async (value: string) => {
    // Add user's message to messages
    const userMessage: Message = {
      content: value,
      is_user: true,
      session_id: threadID || 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Add 'generating...' message
    const generatingMessage: Message = {
      content: "",
      is_user: false,
      session_id: threadID || 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_generating: true,
    };
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    // Set chatStarted to true to display ChatHistoryComponent
    setChatStarted(true);

    const formData = {
      prompt: value,
    };
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}chat_sessions/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );
      if (response.ok) {
        const payload = await response.json();
        setThreadID(payload.id);

        // Assume the API returns the assistant's message
        const newThread: Thread = payload;
        const assistantMessage: Message = {
          content: newThread?.content,
          is_user: false,
          session_id: payload.id,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };

        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          updatedMessages.pop(); // Remove 'generating...' message
          return [...updatedMessages, assistantMessage];
        });

        // Update URL without redirecting
        router.push(`/thread/${payload.id}`);
      } else {
        console.error("Failed to create new chat session");
        // Handle error by removing 'generating...' message and adding error message
        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          updatedMessages.pop(); // Remove 'generating...' message
          const errorMessage: Message = {
            content: "スレッドの作成に失敗しました。再度実行してください。",
            is_user: false,
            session_id: threadID || 0,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          };
          return [...updatedMessages, errorMessage];
        });
      }
    } catch (error) {
      console.error(error);
      // Handle error by removing 'generating...' message and adding error message
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages.pop(); // Remove 'generating...' message
        const errorMessage: Message = {
          content: "An unexpected error occurred. Please try again.",
          is_user: false,
          session_id: threadID || 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        return [...updatedMessages, errorMessage];
      });
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
            <p className="text-2xl font-bold mb-8">
              なんでも聞いてや〜
            </p>
            <ChatBoxComponent handleSubmit={handleSubmit} />
          </div>
        </div>
      )}
    </>
  );
}
