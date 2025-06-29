"use client"
import { AppSidebar } from "@/components/app-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { HeroSection } from "@/components/hero-section"
import { ModuleCards } from "@/components/module-cards"
import { AntiCheatMonitor } from "@/components/anti-cheat-monitor"
import { SyntheticAnalytics } from "@/components/synthetic-analytics"
import { ReplayViewer } from "@/components/replay-viewer"
import { VoiceChatOverlay } from "@/components/voice-chat-overlay"
import { ConnectionTest } from "@/components/connection-test"

export default function Home() {
  return (
    <main className="relative min-h-screen bg-background">
      <div className="fixed inset-0 z-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5" />
        <div className="grid-bg opacity-30" />
      </div>

      <div className="flex h-screen relative z-10">
        <AppSidebar />
        <div className="flex-1 flex flex-col overflow-hidden">
          <DashboardHeader />

          <div className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 md:px-6 lg:px-8 py-6 space-y-8">
              <HeroSection />
              
              {/* Connection Test - Temporary for verification */}
              <ConnectionTest />
              
              <ModuleCards />

              <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                <AntiCheatMonitor />
                <SyntheticAnalytics />
              </div>

              <ReplayViewer />
            </div>
          </div>
        </div>

        <VoiceChatOverlay />
      </div>
    </main>
  )
}
