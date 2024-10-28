"use client";

import { useState, useEffect, useRef } from "react";
import { Message } from "@/types/messages";
import ChatBoxComponent from "@/components/chatBox";

export default function ThreadPage({ params }: { params: { id: string } }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const mockMessages: Message[] = [
      {
        content: `ユーザーのプロンプトがここに表示されます -> ${params.id}`,
        is_user: true,
        id: 0,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: `生成AIからの回答がここに表示される -> ${params.id}`,
        is_user: false,
        id: 1,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "ユーザーのプロンプトがここに表示されます",
        is_user: true,
        id: 2,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "生成AIからの回答がここに表示される",
        is_user: false,
        id: 3,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "ユーザーのプロンプトがここに表示されます",
        is_user: true,
        id: 4,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "生成AIからの回答がここに表示される",
        is_user: false,
        id: 5,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "ユーザーのプロンプトがここに表示されます",
        is_user: true,
        id: 6,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "生成AIからの回答がここに表示される",
        is_user: false,
        id: 7,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "ユーザーのプロンプトがここに表示されます",
        is_user: true,
        id: 8,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "生成AIからの回答がここに表示される",
        is_user: false,
        id: 9,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content: "ユーザーのプロンプトがここに表示されます",
        is_user: true,
        id: 10,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        content:
          "生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される生成AIからの回答がここに表示される",
        is_user: false,
        id: 11,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];
    setMessages(mockMessages);
  }, [params.id]);

  const handleSubmit = () => {
    if (textareaRef.current && textareaRef.current.value) {
      const newMessage: Message = {
        content: textareaRef.current.value,
        is_user: true,
        id: messages.length + 1,
        session_id: Number(params.id),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMessages([...messages, newMessage]);
      textareaRef.current.value = "";
      textareaRef.current.style.height = "auto";
    }
  };

  const adjustFontSize = (content: string) => {
    return content.length > 100 ? "" : "text-3xl font-bold";
  };

  return (
    <>
      <div className="w-full h-screen flex flex-col bg-gray-50">
        <div className="flex-grow overflow-y-auto p-16">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`mb-6 p-4 max-w-2xl mx-auto text-left ${
                message.is_user
                  ? `${adjustFontSize(message.content)}`
                  : "border-b border-gray-300"
              }`}
            >
              {!message.is_user && (
                <div className="flex items-center mb-8">
                  <>
                    <div className="rounded-full bg-gray-300 w-8 h-8 flex items-center justify-center mr-2">
                      A
                    </div>
                    <p className="font-bold ml-2">もんた</p>
                  </>
                </div>
              )}
              <p
                className={`mb-4 ${
                  message.is_user ? "" : "p-4 border-xl bg-gray-100 rounded-xl"
                } `}
              >
                {message.content}
              </p>
            </div>
          ))}
        </div>

        <div className="fixed bottom-0 w-full max-w-[640px] left-[calc(50%+6rem)] transform -translate-x-1/2 p-4 z-10">
          <ChatBoxComponent />
        </div>
      </div>
    </>
  );
}
