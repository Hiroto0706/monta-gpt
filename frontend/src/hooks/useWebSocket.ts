import { CreateErrorMessage, CreateUserMessage } from "@/lib/utils";
import { Message } from "@/types/messages";
import { useEffect, useRef, useState } from "react";

type MessageHandler = (message: Message) => void;

export const useWebSocket = (
  url: string,
  onMessage: MessageHandler
): {
  sendMessage: (message: string, threadID: number) => void;
  isConnected: boolean;
} => {
  const socketRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      setIsConnected(true);
    };

    // TODO: eventはMessage型とthreadID型で分ける
    socket.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data);

        if ("session_id" in data && "content" in data) {
          const newMessage = CreateUserMessage(data.content, data.session_id);
          onMessage(newMessage);
        } else {
          const errorMessage = CreateErrorMessage();
          onMessage(errorMessage);
        }
      } catch (error) {
        const errorText = "Failed to parse message: " + error;
        console.error(errorText);
        const errorMessage = CreateErrorMessage(errorText);
        onMessage(errorMessage);
      }
    };

    socket.onerror = (error: Event) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("Disconnected from WebSocket server");
      setIsConnected(false);
    };

    return () => {
      socket.close();
    };
  }, [url, onMessage]);

  /**
   * sendMessage はWebサーバにmessageを送信する関数です
   * @param message {string} Webサーバに送信するメッセージ
   */
  const sendMessage = (message: string, threadID: number = 0) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(
        JSON.stringify({ message: message, thread_id: threadID })
      );
    } else {
      console.error("WebSocket is not connected");
    }
  };
  return { sendMessage, isConnected };
};
