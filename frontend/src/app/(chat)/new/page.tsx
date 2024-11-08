"use client";

import { CreateThread } from "@/api/threads";
import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { useSidebar } from "@/hook/sidebar";
import {
  CreateAgentMessage,
  CreateErrorMessage,
  CreateGeneratingMessage,
  CreateUserMessage,
} from "@/lib/utils";
import { Message } from "@/types/messages";
import { Thread } from "@/types/threads";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function NewThreadPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatStarted, setChatStarted] = useState(false);
  const { isOpen } = useSidebar();

  /*
    handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
  */
  const handleSubmit = async (value: string) => {
    // Add user's message to messages
    const userMessage = CreateUserMessage(value);
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Add 'generating...' message
    const generatingMessage = CreateGeneratingMessage();
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    // Set chatStarted to true to display ChatHistoryComponent
    setChatStarted(true);

    try {
      const response = await CreateThread(value);
      // Assume the API returns the assistant's message
      const newThread: Thread = response;
      let assistantMessage: Message;
      if (newThread.content !== undefined) {
        assistantMessage = CreateAgentMessage(newThread?.content, newThread.id);
      }

      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages.pop(); // Remove 'generating...' message
        return [...updatedMessages, assistantMessage];
      });

      router.push(`/thread/${newThread.id}`);
    } catch (error) {
      console.error(error);
      // Handle error by removing 'generating...' message and adding error message
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        updatedMessages.pop(); // Remove 'generating...' message
        const errorMessage = CreateErrorMessage();
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
            <p className="text-2xl font-bold mb-8">なんでも聞いてや〜</p>
            <ChatBoxComponent handleSubmit={handleSubmit} />
          </div>
        </div>
      )}
    </>
  );
}
