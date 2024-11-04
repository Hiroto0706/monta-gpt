"use client";

import { logout } from "@/lib/utils";
import { Thread } from "@/types/threads";
import Image from "next/image";
import Link from "next/link";
import React, { Dispatch, SetStateAction, useEffect, useState } from "react";

interface Props {
  threadID: number | null;
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
}

const fetchThreadList = async (): Promise<Thread[]> => {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}chat_sessions/`,
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

const SidebarComponent: React.FC<Props> = ({ threadID, isOpen, setIsOpen }) => {
  const [threads, setThreads] = useState<Thread[]>([]);
  // const [isOpen, setIsOpen] = useState(true);

  useEffect(() => {
    const loadThreads = async () => {
      const fetchedThreads = await fetchThreadList();
      setThreads(fetchedThreads);
    };

    loadThreads();
  }, []);

  return (
    <>
      {/* サイドバー本体 */}
      <div
        className={`h-screen fixed border-r transition-all duration-300 overflow-hidden bg-gray-200 ${
          isOpen ? "w-52" : "w-0 border-r-0"
        }`}
      >
        <div className="h-screen w-52">
          <div className="h-full p-4 flex flex-col">
            {/* 閉じるアイコン */}
            <div
              className="absolute top-1 left-1 p-1 hover:bg-gray-300 duration-300 rounded-lg cursor-pointer"
              onClick={() => setIsOpen(false)}
            >
              <Image
                src="/icons/sidebar-close.png"
                width={20}
                height={20}
                alt="sidebar close button"
              />
            </div>

            {/* ヘッダー部分 */}
            <div>
              <Link
                href="/new"
                className="text-2xl my-4 flex justify-center hover:opacity-70 duration-300"
              >
                もんたGPT
              </Link>
              <Link
                className="mb-2 px-2 py-1 w-full bg-white border rounded-xl border-gray-300 text-sm block shadow hover:bg-gray-100 duration-300"
                href="/new"
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
                        className={`block px-2 py-1 mb-1 rounded cursor-pointer hover:bg-gray-300 duration-300 overflow-hidden whitespace-nowrap text-ellipsis text-xs ${
                          isActive ? "bg-gray-300" : ""
                        }`}
                      >
                        {thread.summary}
                      </Link>
                    );
                  })}
                </>
              )}
            </div>

            {/* ログアウトボタン */}
            <div
              className="mt-4 py-1 px-4 bg-gray-600 border border-gray-600 rounded-xl text-white hover:bg-white hover:text-gray-600 duration-300 cursor-pointer text-center"
              onClick={logout}
            >
              ログアウト
            </div>
          </div>
        </div>
      </div>

      {/* 開くアイコン（サイドバーが閉じているときに表示） */}
      <div
        className={`fixed top-1 left-1 p-1 hover:bg-gray-300 duration-300 rounded-lg cursor-pointer ${
          isOpen ? "hidden" : ""
        }`}
        onClick={() => setIsOpen(true)}
      >
        <Image
          src="/icons/sidebar-open.png"
          width={20}
          height={20}
          alt="sidebar open button"
        />
      </div>
    </>
  );
};

export default SidebarComponent;
