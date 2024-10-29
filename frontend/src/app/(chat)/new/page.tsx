"use client";

import ChatBoxComponent from "@/components/chatBox";
import { useRouter } from "next/navigation";

export default function NewThreadPage() {
  const router = useRouter();

  const handleSubmit = async (value: string) => {
    const formData = {
      content: value,
    };
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}chat_sessions/`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );
      if (response.ok) {
        const data = await response.json();
        const threadId = data.id;
        // 新しいスレッドページにリダイレクト
        router.push(`/thread/${threadId}`);
      } else {
        console.error("Failed to create new chat session");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <div className="flex items-center justify-center w-full min-h-screen bg-gray-50">
        <div className="text-center w-full max-w-[640px] mx-4">
          <p className="text-2xl font-bold mb-8">
            今日は何をお手伝いしましょうか？
          </p>
          <ChatBoxComponent handleSubmit={handleSubmit} />
        </div>
      </div>
    </>
  );
}
