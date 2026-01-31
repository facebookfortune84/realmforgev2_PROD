/**
 * REALM FORGE: TITAN LAYOUT v14.0 (INDUSTRIAL REDESIGN)
 * ARCHITECT: LEAD ENGINEER
 * PURPOSE: PERSISTENT SOVEREIGN SHELL
 * PATH: F:\RealmForge\client\app\layout.tsx
 */

import "./globals.css";
import type { Metadata, Viewport } from "next";

export const metadata: Metadata = {
  title: 'REALM FORGE OS',
  description: 'Industrial Agentic Ecosystem',
  icons: { icon: '/favicon.ico' },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#000000',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-black text-slate-300 antialiased overflow-hidden selection:bg-[#b5a642] selection:text-black font-sans">
        {/* THE TITAN GLASS OVERLAY - Persistent Background Layer */}
        <div className="fixed inset-0 z-[-1] bg-[radial-gradient(circle_at_50%_50%,_#1a1a1a_0%,_#000000_100%)]" />
        
        {/* SCANLINE EFFECT - Industrial Aesthetic */}
        <div className="pointer-events-none fixed inset-0 z-[9999] opacity-[0.03] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />
        
        <main className="relative flex h-screen w-screen flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}