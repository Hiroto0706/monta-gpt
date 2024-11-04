"use client";

import ChatBoxComponent from "@/components/chatBox";
import ChatHistoryComponent from "@/components/chatHistory";
import { Message } from "@/types/messages";
import { useEffect, useRef, useState } from "react";

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
  const messagesEndRef = useRef<HTMLDivElement>(null);

  {
    /*
    handleSubmit はユーザーからの質問を受け取りAIの回答を生成する関数
    */
  }
  const handleSubmit = async (value: string) => {
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    // FIXME: idはwebsocket通信よりidが帰ってきたらmessagesに追加するようにする
    const userMessage: Message = {
      content: value,
      is_user: true,
      session_id: params.id,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // "generating..." メッセージを追加
    const generatingMessage: Message = {
      content: "",
      is_user: false,
      session_id: params.id,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_generating: true,
    };
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    // 画面を一番下にスクロール
    scrollToBottom();

    const formData = {
      session_id: params.id,
      prompt: value,
    };
    console.log(formData);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}messages/conversation`,
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
        const newMessage = await response.json();

        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          updatedMessages.pop(); // "generating..." メッセージを削除
          return [...updatedMessages, newMessage];
        });
      } else {
        console.error("Failed to send message");
      }
    } catch (error) {
      console.error(error);
      // エラーメッセージを会話に追加
      const generatingMessage: Message = {
        content: "予期せぬエラーが発生しました。再度実行してください。",
        is_user: false,
        session_id: params.id,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMessages((prevMessages) => [...prevMessages, generatingMessage]);
    }
  };

  useEffect(() => {
    if (params.id) {
      const loadThreadDetail = async () => {
        const response = await fetchThreadDetail(params.id);
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

      <div className="fixed bottom-0 w-full max-w-[640px] left-[calc(50%+6rem)] transform -translate-x-1/2 p-4 z-10">
        <ChatBoxComponent handleSubmit={handleSubmit} />
      </div>
    </>
  );
}
