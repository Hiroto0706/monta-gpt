import { useEffect, useRef, useState } from "react";

type MessageHandler = (message: string) => void;

export const useWebSocket = (
  url: string,
  onMessage: MessageHandler
): { sendMessage: (message: string) => void; isConnected: boolean } => {
  const socketRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
      setIsConnected(true);
    };

    socket.onmessage = (event: MessageEvent) => {
      onMessage(event.data);
    };

    socket.onclose = () => {
      console.log("Disconnected from WebSocket server");
      setIsConnected(false);
    };

    return () => {
      socket.close();
    };
  }, [url, onMessage]);

  const sendMessage = (message: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(message);
    } else {
      console.error("WebSocket is not connected");
    }
  };
  return { sendMessage, isConnected };
};
