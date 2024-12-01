import { AIMessage, GeneratingMessage } from "@/types/messages";
import React from "react";
import ReactMarkDown from "react-markdown";
import remarkGfm from "remark-gfm";
import GeneratingMessageComponent from "@/components/ui/message/generatingMessage";

interface Props {
  index: number;
  message: AIMessage | GeneratingMessage;
  isLastMessage: boolean;
}

const SystemMessage: React.FC<Props> = ({ index, message, isLastMessage }) => {
  return (
    <>
      <div
        key={index}
        className={`mt-4 p-4 max-w-2xl mx-auto text-left break-words ${
          isLastMessage ? "pb-8" : "pb-8 border-b border-gray-300"
        }`}
      >
        <div className="flex items-center mb-4">
          <div className="rounded-full bg-gray-300 w-8 h-8 flex items-center justify-center mr-2">
            A
          </div>
          <p className="ml-2">Monta</p>
        </div>
        <div className="break-words prose max-w-none">
          <ReactMarkDown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ ...props }) => <h1 className="text-2xl my-4" {...props} />,
              h2: ({ ...props }) => <h2 className="text-xl my-3" {...props} />,
              h3: ({ ...props }) => <h3 className="text-lg my-2" {...props} />,
            }}
          >
            {message.content}
          </ReactMarkDown>
          {message.isGenerating && <GeneratingMessageComponent />}
        </div>
      </div>
    </>
  );
};

export default SystemMessage;
