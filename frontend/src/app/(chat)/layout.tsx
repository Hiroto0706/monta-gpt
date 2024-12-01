"use client";

import { useContext, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import SidebarLayout from "@/components/layouts/sidebar";
import { VerifyToken } from "@/api/auth";
import { SidebarContext } from "@/contexts/sidebarContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [threadId, setThreadId] = useState<number | null>(null);
  const { isOpen, toggleSidebar } = useContext(SidebarContext);

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

  // FIXME: サイドバーはPC版とスマホ版で分けたほうがよい
  useEffect(() => {
    const breakPoint = 768;
    if (window.innerWidth >= breakPoint) {
      toggleSidebar(true);
    }
  }, []);

  return (
    <>
      <SidebarLayout threadID={threadId} />
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
