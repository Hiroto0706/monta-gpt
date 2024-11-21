"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import SidebarComponent from "@/components/sidebar";
import { SidebarProvider } from "@/contexts/SidebarContext";
import { VerifyToken } from "@/api/auth";
import { useSidebar } from "@/hooks/useSidebar";

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [threadId, setThreadId] = useState<number | null>(null);

  useEffect(() => {
    VerifyToken(router);
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
      <SidebarProvider>
        <ChatLayoutContent threadId={threadId}>{children}</ChatLayoutContent>
      </SidebarProvider>
    </>
  );
}

function ChatLayoutContent({
  children,
  threadId,
}: {
  children: React.ReactNode;
  threadId: number | null;
}) {
  const { isOpen, toggleSidebar } = useSidebar();

  // TODO: サイドバーはPC版とスマホ版で分けたほうがよい
  useEffect(() => {
    const breakPoint = 768;
    if (window.innerWidth >= breakPoint) {
      toggleSidebar(true);
    }
  }, []);

  return (
    <>
      <SidebarComponent threadID={threadId} />
      <div
        className={`duration-300 transition-all ${
          isOpen ? "pl-0 md:pl-52" : "pl-0"
        }`}
      >
        <div className="w-full h-screen">{children}</div>
      </div>
    </>
  );
}
