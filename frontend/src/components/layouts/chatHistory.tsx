"use client";

import React, { useEffect } from "react";
import { Message } from "@/types/messages";
import SystemMessage from "@/components/ui/message/systemMessage";
import UserMessage from "@/components/ui/message/userMessage";
import { ScrollToBottom } from "@/lib/utils/message";

interface Props {
  messages: Message[];
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
              {messages.map((message, index) => (
                <>
                  {message.is_user ? (
                    <UserMessage index={index} message={message} />
                  ) : (
                    <SystemMessage
                      index={index}
                      message={message}
                      isLastMessage={index === messages.length - 1}
                    />
                  )}
                </>
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

export default ChatHistoryLayout;
