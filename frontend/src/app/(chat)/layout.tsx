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
  const [isOpen, setIsOpen] = useState(true);

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
      <SidebarComponent
        threadID={threadId}
        isOpen={isOpen}
        setIsOpen={setIsOpen}
      />
      <div
        className={`duration-300 transition-all ${isOpen ? "pl-52" : "pl-0"}`}
      >
        <div className="w-full h-screen">{children}</div>
      </div>
    </>
  );
}
