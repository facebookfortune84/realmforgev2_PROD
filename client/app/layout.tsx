/**
 * REALM FORGE: TITAN LAYOUT v31.0
 * STYLE: CAFFEINE-MODERN (MILLION DOLLAR BUILD)
 * PATH: F:\RealmForge_PROD\client\app\layout.tsx
 */

import "./globals.css";
import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: 'REALM FORGE | Sovereign AIAAS',
  description: 'Industrial Agentic Software Engineering Platform',
  icons: { icon: '/favicon.ico' },
};

export const viewport: Viewport = {
  themeColor: "#080808",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable} dark`}>
      <body className="bg-[#080808] text-[#f0f0f0] antialiased selection:bg-[#ff007f] selection:text-white overflow-hidden">
        
        {/* THE INFINITE CANVAS BACKGROUND */}
        <div className="fixed inset-0 z-[-1] pointer-events-none">
          {/* Base Mesh Gradient */}
          <div className="absolute inset-0 bg-[#080808]" />
          <div className="absolute inset-0 bg-mesh opacity-20" />
          
          {/* Industrial Dot Grid */}
          <div className="absolute inset-0 bg-dot-grid opacity-10" />
          
          {/* Subtle Sector Vignette */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_#080808_100%)]" />
        </div>

        {/* HUD CHASSIS */}
        <div className="relative flex h-screen w-screen flex-col">
          {children}
        </div>

      </body>
    </html>
  );
}