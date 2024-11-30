"use client";

import LoginFormLayout from "@/components/layouts/loginForm";

export default function Page() {
  return (
    <>
      <div className="flex h-screen justify-center items-center">
        <main className="flex flex-col justify-center items-center p-8 md:p-16 bg-white rounded-lg border border-gray-200">
          <LoginFormLayout />
        </main>
      </div>
    </>
  );
}
