import { useEffect, useRef, useState } from "react";

export const useChatBox = (
  handleSubmit: (value: string) => void,
  isConnected: boolean
) => {
  const [query, setQuery] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isComposing = useRef(false);

  const handleCompositionStart = () => {
    isComposing.current = true;
  };
  const handleCompositionEnd = () => {
    isComposing.current = false;
  };

  const onSubmit = () => {
    const trimmedQuery = query.trim();
    if (trimmedQuery) {
      setQuery("");
      try {
        handleSubmit(trimmedQuery);
      } catch (error) {
        console.error("Error submitting message: ", error);
      }
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !isConnected &&
      !isComposing.current
    ) {
      event.preventDefault();
      onSubmit();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        200
      )}px`;
    }
  }, [query]);

  return {
    query,
    setQuery,
    textareaRef,
    onSubmit,
    handleKeyDown,
    handleCompositionStart,
    handleCompositionEnd,
  };
};
