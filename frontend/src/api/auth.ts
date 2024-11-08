import apiClient from "@/lib/apiClient";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

/*
  VerifyToken はcookieの情報を元に認証処理を行う
*/
export const VerifyToken = async (router: AppRouterInstance): Promise<void> => {
  try {
    const response = await apiClient.get("/auth/verify", {
      withCredentials: true,
    });
    if (response.status !== 200) {
      router.push("/");
    }
  } catch (error) {
    console.error("Unexpected error: ", error);
    router.push("/");
  }
};

/*
  RedirectGoogleLoginPage はGoogle認証用のURLを返し、リダイレクトする関数
*/
export const RedirectGoogleLoginPage = async () => {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_BASE_URL}auth/google/login`
    );
    const { auth_url } = response.data;
    if (auth_url) {
      window.location.href = auth_url;
    } else {
      console.error("No auth_url provided in the response.");
    }
  } catch (error) {
    console.error("Unexpected error:", error);
  }
};
