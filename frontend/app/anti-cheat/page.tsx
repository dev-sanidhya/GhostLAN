"use client"

import { AppSidebar } from "@/components/app-sidebar"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import { AntiCheatMonitor } from "@/components/anti-cheat-monitor"

export default function AntiCheatPage() {
  return (
    <main className="relative min-h-screen bg-background overflow-hidden">
      <div className="fixed inset-0 z-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent z-10" />
        <div
          className="w-full h-full bg-cover bg-center"
          style={{ backgroundImage: "url('/images/background.png')" }}
        />
      </div>

      <div className="flex h-screen relative z-10">
        <AppSidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <header className="border-b border-border/40 bg-background/60 backdrop-blur-xl p-4 md:p-6 flex flex-wrap md:flex-nowrap items-center justify-between gap-4 flex-shrink-0">
            <div className="flex items-center gap-3">
              <img src="/images/logo.png" alt="GhostLAN Logo" className="w-8 h-8" />
              <h1 className="text-xl md:text-2xl font-bold text-primary">GhostLAN</h1>
            </div>
            <ShadowSyncBanner />
            <div className="hidden md:block text-sm">Status: Online</div>
          </header>

          <div className="flex-1 p-4 md:p-8 flex flex-col min-h-0" style={{ height: 'calc(100vh - 120px)' }}>
            <AntiCheatMonitor />
          </div>
        </div>
      </div>
    </main>
  )
}
