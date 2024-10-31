"use client";

import React, { Dispatch, SetStateAction, useEffect, useRef } from "react";
import ChatBoxComponent from "./chatBox";
import GeneratingAnimation from "./generatingAnimation";
import { Message } from "@/types/messages";

interface Props {
  threadID: number;
  messages: Message[];
  setMessages: Dispatch<SetStateAction<Message[]>>;
}

const ChatHistoryComponent: React.FC<Props> = ({
  threadID,
  messages,
  setMessages,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  {
    /*
    scrollToBottom は一番下部に要素をスクロールする関数
    */
  }
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

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
      session_id: threadID,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // "generating..." メッセージを追加
    const generatingMessage: Message = {
      content: "generating...",
      is_user: false,
      session_id: threadID,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_generating: true,
    };
    setMessages((prevMessages) => [...prevMessages, generatingMessage]);

    // 画面を一番下にスクロール
    scrollToBottom();

    const formData = {
      session_id: threadID,
      prompt: value,
    };
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
        session_id: threadID,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMessages((prevMessages) => [...prevMessages, generatingMessage]);
    }
  };

  {
    /*
    adjustFontSize はユーザーの質問の長さより文字のサイズを変化させる関数
    */
  }
  const adjustFontSize = (content: string) => {
    return content.length > 100 ? "" : "text-3xl";
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <>
      <div className="flex flex-col">
        <div className="flex-grow overflow-y-auto p-16">
          {messages.length >= 0 && (
            <>
              {messages.map((message, index) => (
                <div
                  key={message.id}
                  className={`p-4 max-w-2xl mx-auto text-left break-words ${
                    message.is_user
                      ? `${adjustFontSize(message.content)} mt-4`
                      : index === messages.length - 1
                      ? "pb-8"
                      : "pb-8 border-b border-gray-300"
                  }`}
                >
                  {!message.is_user && (
                    <div className="flex items-center mb-8">
                      <>
                        <div className="rounded-full bg-gray-300 w-8 h-8 flex items-center justify-center mr-2">
                          A
                        </div>
                        <p className="ml-2">もんた</p>
                      </>
                    </div>
                  )}
                  <p
                    className={`${
                      message.is_user
                        ? ""
                        : "p-4 border-xl bg-gray-100 rounded-xl break-words"
                    } `}
                  >
                    {message.content}
                    {message.is_generating && (
                      <>
                        <GeneratingAnimation />
                      </>
                    )}
                  </p>
                </div>
              ))}
              {/* 一番下へのスクロール用のダミー要素 */}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        <div className="fixed bottom-0 w-full max-w-[640px] left-[calc(50%+6rem)] transform -translate-x-1/2 p-4 z-10">
          <ChatBoxComponent handleSubmit={handleSubmit} />
        </div>
      </div>
    </>
  );
};

export default ChatHistoryComponent;
