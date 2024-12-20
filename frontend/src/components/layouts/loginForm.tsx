import { RedirectGoogleLoginPage } from "@/api/auth";
import Image from "next/image";

const LoginFormLayout = () => {
  return (
    <>
      <h1 className="text-3xl font-bold my-16">MontaGPT</h1>
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
        Sign in with Google
      </button>
    </>
  );
};

export default LoginFormLayout;
