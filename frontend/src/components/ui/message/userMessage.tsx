import { Message } from "@/types/messages";
import React from "react";

interface Props {
  index: number;
  message: Message;
}

const UserMessage: React.FC<Props> = ({ index, message }) => {
  /**
   * adjustFontSize はユーザーの質問の長さより文字のサイズを変化させる関数
   * @param content {string} textareaに入力されている内容
   * @returns {string} contentが100文字以下の場合は"text-3xl"（大きいフォントサイズクラス）、100文字を超える場合は空文字（デフォルトフォントサイズクラス）を返す
   */
  const adjustFontSize = (content: string = ""): string => {
    return content.length > 100 ? "" : "text-lg";
  };

  return (
    <>
      <div
        key={index}
        className={`mt-4 p-4 max-w-2xl mx-auto text-left break-words rounded-lg bg-gray-100 shadow ${adjustFontSize(
          message.content
        )}`}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>
      </div>
    </>
  );
};

export default UserMessage;
