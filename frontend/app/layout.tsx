import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "@/app/globals.css";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ApplicationShell } from "@/components/application-shell";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Budget Tracker",
  description: "A simple and intuitive budget tracker that helps users manage their finances efficiently. Users can create accounts, log transactions, assign categories, and visualize their spending with detailed statistics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-background font-sans antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <TooltipProvider>
          <ApplicationShell>
            {children}
          </ApplicationShell>
        </TooltipProvider>
      </body>
    </html>
  );
}
