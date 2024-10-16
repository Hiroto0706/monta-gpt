"use client";

import Head from "next/head";
import Image from "next/image";

export default function Home() {
  // const router = useRouter();

  const handleGoogleLogin = async () => {
    // Google OAuth認証の処理を書く場所
    console.log("Googleでログイン");
    try {
      const response = await fetch(
        "http://monta-gpt.com/api/auth/google/login"
      );
      const data = await response.json();

      window.location.href = data.auth_url;
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Head>
        <title>もんたGPT</title>
        <meta name="description" content="Googleでログインするページ" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="flex h-screen justify-center items-center bg-white">
        <main className="flex flex-col justify-center items-center p-16 bg-white rounded-lg border border-gray-200">
          <h1 className="text-3xl font-bold my-16">もんたGPT</h1>
          <button
            onClick={() => handleGoogleLogin()}
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
