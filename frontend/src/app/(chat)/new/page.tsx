"use client";

import ChatBoxComponent from "@/components/chatBox";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef } from "react";
// import Cookies from "js-cookie";

export default function New() {
  // const searchParams = useSearchParams();
  // const router = useRouter();
  // const textareaRef = useRef<HTMLTextAreaElement>(null);

  // useEffect(() => {
  //   const token = searchParams.get("token");
  //   if (token) {
  //     // トークンをクッキーに保存
  //     Cookies.set("access_token", token, { expires: 7 });

  //     // URLからトークンを削除
  //     const newSearchParams = new URLSearchParams(searchParams.toString());
  //     newSearchParams.delete("token");
  //     const newPathname =
  //       window.location.pathname +
  //       (newSearchParams.toString() ? `?${newSearchParams.toString()}` : "");
  //     router.replace(newPathname);
  //   }
  // }, [searchParams, router]);

  return (
    <>
      <div className="flex items-center justify-center w-full min-h-screen bg-gray-50">
        <div className="text-center w-full max-w-[640px] mx-4">
          <p className="text-2xl font-bold mb-8">
            今日は何をお手伝いしましょうか？
          </p>
          <ChatBoxComponent />
        </div>
      </div>
    </>
  );
}
