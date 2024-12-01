import "@/styles/globals.css";
import { metadata } from "@/components/layouts/head";
import { SidebarProvider } from "@/contexts/sidebarContext";
export { metadata };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="text-gray-600 bg-gray-50">
        <SidebarProvider>{children}</SidebarProvider>
      </body>
    </html>
  );
}
