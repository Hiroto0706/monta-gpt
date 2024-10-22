"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ChatLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();

  const logout = () => {
    sessionStorage.removeItem("access_token");
    router.push("/");
  };

  return (
    <>
      <div className="w-48 h-screen bg-gray-200 fixed">
        <div className="h-screen p-2 flex flex-col justify-between">
          <div>
            <div className="text-2xl my-4 flex justify-center">もんたGPT</div>
            <Link
              className="mb-4 px-2 py-1 w-full bg-white border rounded-xl border-gray-300 text-sm block shadow"
              href="/new"
            >
              New chat
            </Link>

            <div className="max-h-[600px] overflow-y-auto">
              {Array(50)
                .fill(null)
                .map((_, i) => (
                  <div
                    key={i}
                    className="p-1 mb-1 rounded cursor-pointer hover:bg-gray-300"
                  >
                    Thread{i + 1}
                  </div>
                ))}
            </div>
          </div>

          <div
            className="mb-2 py-1 px-4 bg-red-600 rounded-xl text-white hover:bg-red-700 cursor-pointer"
            onClick={logout}
          >
            ログアウト
          </div>
        </div>
      </div>
      <div className="pl-48">{children}</div>
    </>
  );
}
