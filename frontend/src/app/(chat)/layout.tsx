"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import SidebarComponent from "@/components/sidebar";

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [threadId, setThreadId] = useState<number | null>(null);

  // 認証処理
  useEffect(() => {
    const verifyToken = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BASE_URL}auth/verify`,
          {
            method: "GET",
            credentials: "include",
          }
        );

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

  useEffect(() => {
    const pathParts = pathname.split("/");
    const lastPart = pathParts[pathParts.length - 1];
    if (lastPart) {
      setThreadId(Number(lastPart));
    }
  }, [pathname]);

  return (
    <>
      <SidebarComponent threadID={threadId} />
      <div className="pl-52">
        <div className="w-full h-screen">{children}</div>
      </div>
    </>
  );
}
