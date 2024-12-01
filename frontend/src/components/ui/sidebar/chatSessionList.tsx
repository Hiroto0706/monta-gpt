"use client";

import { ChatSession } from "@/types/chat_sessions";
import ChatSessionCard from "@/components/ui/sidebar/chatSessionCard";
import React from "react";

interface Props {
  threads: ChatSession[];
  threadID: number | null;
  onClick: (target: string) => void;
}

const ChatSessionList: React.FC<Props> = ({ threads, threadID, onClick }) => {
  return (
    <>
      <div className="flex-grow overflow-y-auto mt-2">
        {threads.length > 0 && (
          <>
            {threads.map((thread) => (
              <ChatSessionCard
                key={thread.id}
                isActive={threadID == thread.id}
                thread={thread}
                onClick={onClick}
              />
            ))}
          </>
        )}
      </div>
    </>
  );
};

export default ChatSessionList;
