"use client";

import { Message } from "@/types/messages";
import axios from "axios";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

// TODO: getServerSidePropsを使ってリダイレクト処理を実装する

const fetchMessages = async (): Promise<Message[]> => {
  try {
    const token = sessionStorage.getItem("access_token");

    // ヘッダーに access_token を含めて API を呼び出す
    const response = await axios.get("http://monta-gpt.com/api/messages/4", {
      headers: {
        Authorization: `Bearer ${token}`, // Authorization ヘッダーにトークンをセット
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      if (error.response.status === 401) {
        window.location.href = "http://monta-gpt.com";
      } else {
        console.error(`Error ${error.response.status}:`, error.response.data);
      }
    } else {
      console.error("Unexpected error:", error);
    }
    return [];
  }
};

export default function Chat() {
  const searchParams = useSearchParams();
  const router = useRouter();
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

      const newSearchParams = new URLSearchParams(searchParams.toString());
      newSearchParams.delete("token");
      const newPathname =
        window.location.pathname +
        (newSearchParams.toString() ? `?${newSearchParams.toString()}` : "");
      router.replace(newPathname);
    }
  }, [searchParams, router]);

  return (
    <>
      <p>This is Chat Page</p>
      {messages.map((message) => (
        <div key={message.id}>{message.content}</div>
      ))}
    </>
  );
}
