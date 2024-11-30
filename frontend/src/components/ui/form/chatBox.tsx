import { useChatBox } from "@/hooks/useChatBox";
import React from "react";

interface Props {
  handleSubmit: (value: string) => Promise<void>;
  isConnected?: boolean;
}

const ChatBoxComponent: React.FC<Props> = ({
  handleSubmit,
  isConnected = false,
}) => {
  const {
    query,
    setQuery,
    textareaRef,
    onSubmit,
    handleKeyDown,
    handleCompositionStart,
    handleCompositionEnd,
  } = useChatBox(handleSubmit, isConnected);

  return (
    <>
      <div className="flex relative items-center bg-white border rounded-3xl py-2 px-2 w-full">
        <textarea
          ref={textareaRef}
          placeholder="Prompt type here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="rounded-3xl w-full pl-4 pr-9 py-1 text-gray-700 focus:outline-none resize-none overflow-y-auto"
          rows={1}
          onKeyDown={handleKeyDown}
          onCompositionStart={handleCompositionStart}
          onCompositionEnd={handleCompositionEnd}
        />
        <button
          className={`absolute bottom-2 right-2 rounded-full p-2 ${
            isConnected
              ? "bg-gray-200 cursor-not-allowed"
              : "bg-black text-white"
          }`}
          onClick={onSubmit}
          disabled={isConnected}
        >
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
    </>
  );
};

export default ChatBoxComponent;
