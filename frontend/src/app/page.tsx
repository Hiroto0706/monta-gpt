"use client";

import { RedirectGoogleLoginPage } from "@/api/auth";
import Image from "next/image";

export default function Home() {
  return (
    <>
      <div className="flex h-screen justify-center items-center">
        <main className="flex flex-col justify-center items-center p-8 md:p-16 bg-white rounded-lg border border-gray-200">
          <h1 className="text-3xl font-bold my-16">もんたGPT</h1>
          <button
            onClick={() => RedirectGoogleLoginPage()}
            className="flex items-center justify-center w-64 bg-white border border-gray-200 font-medium py-2 px-4 shadow rounded-lg hover:bg-gray-100"
          >
            <Image
              src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/google/google-original.svg"
              alt="Google Logo"
              className="w-6 h-6 mr-3"
              width={64}
              height={64}
            />
            Googleでログイン
          </button>
        </main>
      </div>
    </>
  );
}
