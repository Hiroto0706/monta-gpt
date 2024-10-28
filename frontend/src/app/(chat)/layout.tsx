"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Cookies from "js-cookie";
import SidebarComponent from "@/components/sidebar";

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  // 認証処理
  useEffect(() => {
    const verifyToken = async () => {
      try {
        const response = await fetch("http://monta-gpt.com/api/auth/verify", {
          method: "GET",
          credentials: "include",
        });

        if (response.status !== 200) {
          router.push("/");
        }
      } catch (error) {
        console.error("Error verifying access token:", error);
        router.push("/");
      }
    };

    verifyToken();
  }, [router]);

  return (
    <>
      <SidebarComponent />
      <div className="pl-48">{children}</div>
    </>
  );
}
