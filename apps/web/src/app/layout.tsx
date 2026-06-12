import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Resume Screener",
  description: "Recruiter dashboard for AI resume screening",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
