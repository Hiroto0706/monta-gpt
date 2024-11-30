"use client";

import { FetchThreadList } from "@/api/threads";
import { useSidebar } from "@/hooks/useSidebar";
import { Thread } from "@/types/chat_sessions";
import Link from "next/link";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import LogOutButton from "@/components/ui/button/logoutButton";
import SidebarIcon, { IconMode } from "./ui/button/sidebarIcon";

interface Props {
  threadID: number | null;
}

const SidebarComponent: React.FC<Props> = ({ threadID }) => {
  const [threads, setThreads] = useState<Thread[]>([]);
  const { isOpen, toggleSidebar } = useSidebar();
  const [isTransitionEnabled, setIsTransitionEnabled] = useState(true);
  const router = useRouter();

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

  useEffect(() => {
    const loadThreads = async () => {
      const fetchedThreads = await FetchThreadList();

      if (fetchedThreads.length > 0) {
        setThreads(fetchedThreads);
      }
    };

    loadThreads();
  }, []);

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black opacity-20 z-10 md:hidden"
          onClick={() => toggleSidebar()}
        ></div>
      )}

      {/* サイドバー本体 */}
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

            {/* ヘッダー部分 */}
            <div>
              <Link
                href="/new"
                className="text-2xl my-4 flex justify-center hover:opacity-70 duration-300"
                onClick={() => handleLinkClick("/new")}
              >
                MontaGPT
              </Link>
              <Link
                className="mb-2 px-2 py-1 w-full bg-white border rounded-xl border-gray-300 text-sm block shadow hover:bg-gray-100 duration-300"
                href="/new"
                onClick={() => handleLinkClick("/new")}
              >
                New chat
              </Link>
            </div>

            {/* スレッドリスト */}
            <div className="flex-grow overflow-y-auto mt-2">
              {threads.length >= 0 && (
                <>
                  {threads.map((thread) => {
                    const isActive = threadID === thread.id;
                    return (
                      <Link
                        key={thread.id}
                        href={`/thread/${thread.id}`}
                        className={`block p-2 mb-1 rounded cursor-pointer hover:bg-gray-300 duration-300 overflow-hidden whitespace-nowrap text-ellipsis text-xs ${
                          isActive ? "bg-gray-300" : ""
                        }`}
                        onClick={() => handleLinkClick(`/thread/${thread.id}`)}
                      >
                        {thread.summary}
                      </Link>
                    );
                  })}
                </>
              )}
            </div>

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

export default SidebarComponent;
