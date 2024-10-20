import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import axios from "axios";

export async function middleware(request: NextRequest) {
  console.log(request);
  // const accessToken =
  //   request.cookies.get("access_token")?.value;
  // if (!accessToken) {
  //   return NextResponse.redirect(new URL("/", request.url));
  // }

  // try {
  //   const response = await axios.get("http://localhost:8080/verify", {
  //     headers: {
  //       Authorization: `Bearer ${accessToken}`,
  //     },
  //   });

  //   if (response.status === 200) {
  //     return NextResponse.next();
  //   }
  // } catch (error) {
  //   console.error(error);
  //   return NextResponse.redirect(new URL("/", request.url));
  // }

  // return NextResponse.redirect(new URL("/", request.url));
}

// ミドルウェアを適用するパス
export const config = {
  matcher: ["/chat"], // "/chat"ページにミドルウェアを適用
};
