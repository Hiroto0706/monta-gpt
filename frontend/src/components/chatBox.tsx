import React, { useRef, useState } from "react";

interface Props {
  handleSubmit: (value: string) => Promise<void>;
}

const ChatBoxComponent: React.FC<Props> = ({ handleSubmit }) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isComposing, setIsComposing] = useState(false);

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  };

  const onSubmit = async () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const value = textarea.value.trim();
    if (value) {
      setIsSubmitting(true);
      textarea.value = "";
      textarea.style.height = "auto";
      try {
        await handleSubmit(value);
      } catch (error) {
        console.error("Error submitting message:", error);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !isSubmitting &&
      !isComposing
    ) {
      event.preventDefault();
      onSubmit();
    }
  };

  const handleCompositionStart = () => {
    setIsComposing(true);
  };

  const handleCompositionEnd = () => {
    setIsComposing(false);
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
          onKeyDown={handleKeyDown}
          onCompositionStart={handleCompositionStart}
          onCompositionEnd={handleCompositionEnd}
        />
        <button
          className={`absolute bottom-2 right-2 rounded-full p-2 ${
            isSubmitting
              ? "bg-gray-200 cursor-not-allowed"
              : "bg-black text-white"
          }`}
          onClick={onSubmit}
          disabled={isSubmitting}
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
