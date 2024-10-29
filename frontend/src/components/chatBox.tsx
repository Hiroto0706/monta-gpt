import React, { useRef } from "react";

interface Props {
  handleSubmit: (value: string) => void;
}

const ChatBoxComponent: React.FC<Props> = ({ handleSubmit }) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  };

  const onSubmit = () => {
    if (textareaRef.current) {
      const value = textareaRef.current.value.trim();
      if (value) {
        handleSubmit(value);
        textareaRef.current.value = ""; // テキストエリアをクリア
        textareaRef.current.style.height = "auto"; // テキストエリアの高さをリセット
      }
    }
  };

  return (
    <>
      <div className="flex relative items-center bg-white border rounded-3xl py-2 px-2 w-full">
        <textarea
          ref={textareaRef}
          placeholder="Prompt type here..."
          className="rounded-3xl w-full pl-4 pr-9 py-1 text-gray-700 focus:outline-none resize-none overflow-y-auto"
          rows={1}
          onInput={handleInput}
        />
        <button
          className="absolute bottom-2 right-2 bg-black text-white rounded-full p-2"
          onClick={onSubmit}
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
