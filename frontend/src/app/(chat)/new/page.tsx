"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef } from "react";

// TODO: getServerSidePropsを使ってリダイレクト処理を実装する

export default function New() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      sessionStorage.setItem("access_token", token);

      const newSearchParams = new URLSearchParams(searchParams.toString());
      newSearchParams.delete("token");
      const newPathname =
        window.location.pathname +
        (newSearchParams.toString() ? `?${newSearchParams.toString()}` : "");
      router.replace(newPathname);
    }
  }, [searchParams, router]);

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  };

  return (
    <>
      <div className="flex items-center justify-center w-full min-h-screen bg-gray-50">
        <div className="text-center w-full max-w-[640px] mx-4">
          <p className="text-2xl font-bold mb-8">
            今日は何をお手伝いしましょうか？
          </p>
          <div className="flex relative items-center bg-white border rounded-lg py-2 px-2 w-full">
            <textarea
              ref={textareaRef}
              placeholder="Prompt type here..."
              className="rounded-lg w-full pl-2 pr-9 py-1 text-gray-700 focus:outline-none resize-none overflow-y-auto"
              rows={1}
              onInput={handleInput}
            />
            <button className="absolute bottom-2 right-1 bg-black text-white rounded-full p-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M5 12h14M12 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
