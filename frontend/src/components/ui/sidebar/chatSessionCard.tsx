'use client';

import { Thread } from "@/types/chat_sessions";
import Link from "next/link";
import React from "react";

interface Props {
  isActive: boolean;
  thread: Thread;
  onClick: (target: string) => void;
}

const ChatSessionCard: React.FC<Props> = ({ isActive, thread, onClick }) => {
  return (
    <Link
      key={thread.id}
      href={`/thread/${thread.id}`}
      className={`block p-2 mb-1 rounded cursor-pointer hover:bg-gray-300 duration-300 overflow-hidden whitespace-nowrap text-ellipsis text-xs ${
        isActive ? "bg-gray-300" : ""
      }`}
      onClick={() => onClick(`/thread/${thread.id}`)}
    >
      {thread.summary}
    </Link>
  );
};

export default ChatSessionCard;
