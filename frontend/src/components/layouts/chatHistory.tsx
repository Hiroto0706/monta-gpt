"use client";

import React, { useEffect } from "react";
import { AIMessage, GeneratingMessage, HumanMessage } from "@/types/messages";
import SystemMessage from "@/components/ui/message/systemMessage";
import UserMessage from "@/components/ui/message/userMessage";
import { ScrollToBottom } from "@/lib/utils/message";

interface Props {
  messages: (HumanMessage | AIMessage | GeneratingMessage)[];
  messagesEndRef?: React.RefObject<HTMLDivElement>;
}

const ChatHistoryLayout: React.FC<Props> = ({ messages, messagesEndRef }) => {
  useEffect(() => {
    ScrollToBottom(messagesEndRef);
  }, [messages.length]);

  return (
    <>
      <div className="flex flex-col">
        <div className="flex-grow overflow-y-auto p-4 md:p-16 mb-8">
          {messages.length >= 0 && (
            <>
              {messages.map((message, index) =>
                !message.isUser || !message.isUser ? (
                  <SystemMessage
                    key={index}
                    index={index}
                    message={message}
                    isLastMessage={index === messages.length - 1}
                  />
                ) : (
                  <UserMessage key={index} index={index} message={message} />
                )
              )}
              {/* 一番下へのスクロール用のダミー要素 */}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ChatHistoryLayout;
