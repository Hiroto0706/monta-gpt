"use client";

import { Message } from "@/types/messages";
import axios from "axios";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

// TODO: getServerSidePropsを使ってリダイレクト処理を実装する

const fetchMessages = async (): Promise<Message[]> => {
  try {
    const response = await axios.get("http://monta-gpt.com/api/messages/4");
    return response.data;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export default function Chat() {
  const searchParams = useSearchParams();
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const fetchedMessages = await fetchMessages();
      setMessages(fetchedMessages);
    };

    fetchData();
  }, []);

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      sessionStorage.setItem("access_token", token);
    }
  }, [searchParams]);

  return (
    <>
      <p>This is Chat Page</p>
      {messages.map((message) => (
        <div key={message.id}>{message.content}</div>
      ))}
    </>
  );
}
