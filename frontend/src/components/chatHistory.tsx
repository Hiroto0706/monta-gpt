"use client";

import React, { useEffect } from "react";
import GeneratingAnimation from "./generatingAnimation";
import { Message } from "@/types/messages";

interface Props {
  messages: Message[];
  messagesEndRef?: React.RefObject<HTMLDivElement>;
}

const ChatHistoryComponent: React.FC<Props> = ({
  messages,
  messagesEndRef,
}) => {
  {
    /*
    scrollToBottom は一番下部に要素をスクロールする関数
    */
  }
  const scrollToBottom = () => {
    if (messagesEndRef != undefined) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  {
    /*
    adjustFontSize はユーザーの質問の長さより文字のサイズを変化させる関数
    */
  }
  const adjustFontSize = (content: string = "") => {
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
                  <p className={`${message.is_user ? "" : "break-words"} `}>
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
      </div>
    </>
  );
};

export default ChatHistoryComponent;
