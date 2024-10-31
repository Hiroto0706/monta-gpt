"use client";

import ChatHistoryComponent from "@/components/chatHistory";
import { Message } from "@/types/messages";
import { useEffect, useState } from "react";

const fetchThreadDetail = async (threadId: number): Promise<Message[]> => {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}messages/${threadId}`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return await response.json();
  } catch (error) {
    console.error(error);
    return [];
  }
};

export default function ThreadPage({ params }: { params: { id: number } }) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const loadThreadDetail = async () => {
      const response = await fetchThreadDetail(params.id);
      setMessages(response);
    };
    loadThreadDetail();
  }, [params.id]);

  return (
    <>
      <ChatHistoryComponent
        threadID={params.id}
        messages={messages}
        setMessages={setMessages}
      />
    </>
  );
}
