"use client";

import { logout } from "@/lib/utils";
import { Thread } from "@/types/threads";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

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

const SidebarComponent = () => {
  const [threads, setThreads] = useState<Thread[]>([]);

  useEffect(() => {
    const loadThreads = async () => {
      const fetchedThreads = await fetchThreadList();
      setThreads(fetchedThreads);
    };

    loadThreads();
  }, []);

  return (
    <>
      <div className="w-48 h-screen bg-gray-200 fixed">
        <div className="h-screen p-2 flex flex-col justify-between">
          <div>
            <Link
              href="/new"
              className="text-2xl my-4 flex justify-center hover:opacity-70 duration-300"
            >
              もんたGPT
            </Link>
            <Link
              className="mb-4 px-2 py-1 w-full bg-white border rounded-xl border-gray-300 text-sm block shadow hover:bg-gray-200 duration-300"
              href="/new"
            >
              New chat
            </Link>

            <div className="max-h-[580px] overflow-y-auto flex flex-col">
              {threads.length >= 0 && (
                <>
                  {threads.map((thread) => (
                    <Link
                      key={thread.id}
                      href={`/thread/${thread.id}`}
                      className="block px-2 py-1 mb-1 rounded cursor-pointer hover:bg-gray-300 duration-300 overflow-hidden whitespace-nowrap text-ellipsis"
                    >
                      {thread.summary}
                    </Link>
                  ))}
                </>
              )}
            </div>
          </div>

          <div
            className="mb-2 py-1 px-4 bg-gray-600 border border-gray-600 rounded-xl text-white hover:bg-white hover:text-gray-600 duration-300 cursor-pointer text-center"
            onClick={logout}
          >
            ログアウト
          </div>
        </div>
      </div>
    </>
  );
};

export default SidebarComponent;
