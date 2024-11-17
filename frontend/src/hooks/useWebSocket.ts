import { CreateAgentMessage, CreateErrorMessage } from "@/lib/utils";
import { Message } from "@/types/messages";
import { useEffect, useRef, useState } from "react";

type MessageHandler = (message: Message) => void;

export const useWebSocket = (
  url: string,
  onMessage: MessageHandler,
  query: Record<string, string | number | boolean> = {}
): {
  sendMessage: (message: string, threadID?: number) => void;
  isConnected: boolean;
} => {
  const socketRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const accessTokenRef = useRef<string | null>(null);

  useEffect(() => {
    // クッキーを解析してaccess_tokenを取得
    const cookies = document.cookie
      .split("; ")
      .find((row) => row.startsWith("access_token="));
    if (cookies) {
      accessTokenRef.current = cookies.split("=")[1];
    }
  }, []);

  /**
   * クエリオブジェクトをクエリ文字列に変換するユーティリティ関数
   * @param query {Record<string, string | number | boolean>} クエリパラメータのオブジェクト
   * @returns {string} クエリ文字列
   */
  const buildQueryString = (
    query: Record<string, string | number | boolean>
  ): string => {
    const params = new URLSearchParams(query as Record<string, string>);
    return params.toString();
  };

  /**
   * connectWebSocket はWebSocketの接続を開始する関数
   */
  const connectWebSocket = () => {
    if (socketRef.current) return;

    const accessToken = accessTokenRef.current;
    if (accessToken) {
      query["access_token"] = accessToken;
    }

    const queryString = buildQueryString(query);
    const fullUrl = queryString ? `${url}?${queryString}` : url;

    const socket = new WebSocket(fullUrl);
    socketRef.current = socket;

    socket.onopen = () => {
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
   * @param threadID {number} ThreadID (optional)
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
