"use client";

import { FetchThreadList } from "@/api/threads";
import { ChatSession } from "@/types/chat_sessions";
import { useRouter } from "next/navigation";
import React, { useContext, useEffect, useState } from "react";
import LogOutButton from "@/components/ui/button/logoutButton";
import SidebarIcon, { IconMode } from "../ui/button/sidebarIcon";
import { SidebarContext } from "@/contexts/sidebarContext";
import ChatSessionList from "@/components/ui/sidebar/chatSessionList";
import SidebarHeader from "@/components/ui/sidebar/sidebarHeader";

interface Props {
  threadID: number | null;
}

const SidebarLayout: React.FC<Props> = ({ threadID }) => {
  const [threads, setThreads] = useState<ChatSession[]>([]);
  const { isOpen, toggleSidebar } = useContext(SidebarContext);
  const [isTransitionEnabled, setIsTransitionEnabled] = useState(true);
  const router = useRouter();

  /**
   * handleLinkClick はリンクをクリックしたときの処理を行う関数
   * @param target {string} 遷移先URL
   */
  const handleLinkClick = (target: string) => {
    if (window.innerWidth < 768) {
      toggleSidebar();
    }

    if (target === "/new") {
      window.location.href = target;
    } else {
      router.push(target);
    }
  };

  /**
   * ブレークポイントの変更時にアニメーションを無効化する
   */
  useEffect(() => {
    const handleResize = () => {
      setIsTransitionEnabled(false);
      setTimeout(() => setIsTransitionEnabled(true), 100);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  /**
   * sessionIDが変化した時、chatSessionを取得する
   */
  useEffect(() => {
    const loadThreads = async () => {
      const fetchedThreads = await FetchThreadList();

      if (fetchedThreads.length > 0) {
        setThreads(fetchedThreads);
      }
    };

    loadThreads();
  }, [threadID]);

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black opacity-20 z-10 md:hidden"
          onClick={() => toggleSidebar()}
        ></div>
      )}

      <div
        className={`h-screen fixed z-20 border-r bg-gray-200 overflow-hidden ${
          isTransitionEnabled ? "transition-all duration-300" : ""
        } ${
          isOpen
            ? "w-52 translate-x-0"
            : "md:w-0 w-52 md:translate-x-0 translate-x-[-100%]"
        }`}
      >
        <div className="h-screen w-52">
          <div className="h-full p-4 flex flex-col">
            <SidebarIcon
              mode={IconMode.Close}
              isOpen={isOpen}
              toggleSidebar={toggleSidebar}
            />

            <SidebarHeader onClick={handleLinkClick} />

            <ChatSessionList
              threads={threads}
              threadID={threadID}
              onClick={handleLinkClick}
            />

            <LogOutButton />
          </div>
        </div>
      </div>

      <SidebarIcon
        mode={IconMode.Open}
        isOpen={isOpen}
        toggleSidebar={toggleSidebar}
      />
    </>
  );
};

export default SidebarLayout;
