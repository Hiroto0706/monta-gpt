import "@/styles/globals.css";
import { metadata } from "@/components/layouts/head";
export { metadata };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="text-gray-600 bg-gray-50">{children}</body>
    </html>
  );
}
