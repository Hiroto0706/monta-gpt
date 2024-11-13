import { CreateAgentMessage, CreateErrorMessage } from "@/lib/utils";
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

  /**
   * connectWebSocket はWebSocketの接続を開始する関数
   */
  const connectWebSocket = () => {
    if (socketRef.current) return;

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
          const newMessage = CreateAgentMessage(data.content, data.session_id);
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
      socketRef.current = null;
    };
  };

  useEffect(() => {
    return () => {
      if (
        socketRef.current &&
        socketRef.current.readyState === WebSocket.OPEN
      ) {
        socketRef.current.close();
      }
    };
  }, [url]);

  /**
   * sendMessage はWebサーバにmessageを送信する関数です
   * @param message {string} Webサーバに送信するメッセージ
   */
  const sendMessage = (message: string, threadID: number = 0) => {
    if (!socketRef.current) {
      // sendMessageが初めて呼ばれたときにWebSocketを接続
      connectWebSocket();
    }

    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(
        JSON.stringify({ message: message, thread_id: threadID })
      );
    }
  };

  return { sendMessage, isConnected };
};
