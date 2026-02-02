/**
 * REALM FORGE: TITAN LAYOUT v31.1
 * STYLE: CAFFEINE-NEON (PRODUCTION HARDENED)
 * ARCHITECT: LEAD SWARM ENGINEER
 * PATH: F:\RealmForge_PROD\client\app\layout.tsx
 */

import "./globals.css";
import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: 'REALM FORGE | SOVEREIGN COMMAND',
  description: 'Industrial Agentic Software Engineering Platform - v31.1',
  icons: { icon: '/favicon.ico' },
};

export const viewport: Viewport = {
  themeColor: "#050505",
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
      <body className="bg-[#050505] text-[#f0f0f0] antialiased selection:bg-[#00f2ff] selection:text-black font-sans overflow-hidden">
        
        {/* THE INFINITE CANVAS BACKGROUND (NEON-INDUSTRIAL) */}
        <div className="fixed inset-0 z-[-1] pointer-events-none select-none overflow-hidden">
          {/* Base Layer: Pure Abyss */}
          <div className="absolute inset-0 bg-[#050505]" />
          
          {/* Middle Layer: Ambient Mesh (Cyan/Pink Diffusion) */}
          <div className="absolute inset-0 bg-mesh opacity-10 blur-[100px]" />
          
          {/* Top Layer: Industrial Dot Grid */}
          <div className="absolute inset-0 bg-dot-grid opacity-[0.03]" />
          
          {/* Edge Layer: CRT Scanlines (Industrial Texture) */}
          <div className="absolute inset-0 pointer-events-none bg-scanlines opacity-[0.02]" />

          {/* Focal Layer: Central Vignette */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_20%,_#050505_100%)]" />
          
          {/* Ambient Glows: Cyan (Top Left), Pink (Bottom Right) */}
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#00f2ff] opacity-[0.05] blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#ff80bf] opacity-[0.05] blur-[120px] rounded-full" />
        </div>

        {/* TITAN HUD CHASSIS */}
        <div className="relative flex h-screen w-screen flex-col overflow-hidden">
          {/* Top Border Glow (High Visibility Rail) */}
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#00f2ff]/30 to-transparent z-[9999]" />
          
          {children}
        </div>

      </body>
    </html>
  );
}