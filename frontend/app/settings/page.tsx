"use client"

import { AppSidebar } from "@/components/app-sidebar"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Settings, Shield, Bell, Monitor, Database, Network } from "lucide-react"

export default function SettingsPage() {
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

          <div className="flex-1 p-4 md:p-8 overflow-auto">
            <div className="max-w-4xl mx-auto space-y-6">
              <div className="flex items-center gap-3">
                <Settings className="h-8 w-8 text-primary" />
                <h1 className="text-3xl font-bold">Settings</h1>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Shield className="h-5 w-5" />
                      Anti-Cheat Settings
                    </CardTitle>
                    <CardDescription>
                      Configure anti-cheat detection sensitivity and rules
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="sensitivity">Detection Sensitivity</Label>
                      <Select defaultValue="medium">
                        <SelectTrigger className="w-32">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="low">Low</SelectItem>
                          <SelectItem value="medium">Medium</SelectItem>
                          <SelectItem value="high">High</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="auto-ban">Auto-ban detected cheaters</Label>
                      <Switch id="auto-ban" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="real-time">Real-time monitoring</Label>
                      <Switch id="real-time" defaultChecked />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Bell className="h-5 w-5" />
                      Notification Settings
                    </CardTitle>
                    <CardDescription>
                      Manage notification preferences and alerts
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="email-notifications">Email notifications</Label>
                      <Switch id="email-notifications" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="push-notifications">Push notifications</Label>
                      <Switch id="push-notifications" defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="sound-alerts">Sound alerts</Label>
                      <Switch id="sound-alerts" defaultChecked />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Monitor className="h-5 w-5" />
                      Display Settings
                    </CardTitle>
                    <CardDescription>
                      Customize the user interface and display options
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="dark-mode">Dark mode</Label>
                      <Switch id="dark-mode" defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="animations">Enable animations</Label>
                      <Switch id="animations" defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="compact-mode">Compact mode</Label>
                      <Switch id="compact-mode" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Database className="h-5 w-5" />
                      Data Settings
                    </CardTitle>
                    <CardDescription>
                      Configure data retention and storage options
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="retention">Data retention period</Label>
                      <Select defaultValue="30">
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="7">7 days</SelectItem>
                          <SelectItem value="30">30 days</SelectItem>
                          <SelectItem value="90">90 days</SelectItem>
                          <SelectItem value="365">1 year</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="auto-backup">Auto backup</Label>
                      <Switch id="auto-backup" defaultChecked />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="analytics">Enable analytics</Label>
                      <Switch id="analytics" defaultChecked />
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Network className="h-5 w-5" />
                    Network Configuration
                  </CardTitle>
                  <CardDescription>
                    Configure network settings and connection preferences
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="server-url">Server URL</Label>
                      <Input id="server-url" defaultValue="http://localhost:8000" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="timeout">Connection timeout (ms)</Label>
                      <Input id="timeout" type="number" defaultValue="5000" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="auto-reconnect">Auto-reconnect on disconnect</Label>
                    <Switch id="auto-reconnect" defaultChecked />
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end gap-4">
                <Button variant="outline">Reset to Defaults</Button>
                <Button>Save Settings</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
} 