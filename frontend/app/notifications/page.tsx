"use client"

import { AppSidebar } from "@/components/app-sidebar"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Bell, AlertTriangle, CheckCircle, Info, X, Clock, User } from "lucide-react"

export default function NotificationsPage() {
  const notifications = [
    {
      id: 1,
      type: 'alert',
      title: 'Anti-Cheat Alert',
      message: 'Suspicious activity detected from player GhostPlayer123',
      timestamp: '2 minutes ago',
      read: false,
      severity: 'high'
    },
    {
      id: 2,
      type: 'info',
      title: 'System Update',
      message: 'New patch v2.1.0 has been applied successfully',
      timestamp: '1 hour ago',
      read: false,
      severity: 'low'
    },
    {
      id: 3,
      type: 'success',
      title: 'Match Completed',
      message: 'Match #12345 has been recorded and analyzed',
      timestamp: '3 hours ago',
      read: true,
      severity: 'low'
    },
    {
      id: 4,
      type: 'alert',
      title: 'Connection Issue',
      message: 'Temporary connection loss detected, reconnected automatically',
      timestamp: '5 hours ago',
      read: true,
      severity: 'medium'
    }
  ]

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'alert':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'info':
        return <Info className="h-4 w-4 text-blue-500" />
      default:
        return <Bell className="h-4 w-4 text-gray-500" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-500 text-white'
      case 'medium':
        return 'bg-yellow-500 text-black'
      case 'low':
        return 'bg-blue-500 text-white'
      default:
        return 'bg-gray-500 text-white'
    }
  }

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
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Bell className="h-8 w-8 text-primary" />
                  <h1 className="text-3xl font-bold">Notifications</h1>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">
                    {notifications.filter(n => !n.read).length} unread
                  </Badge>
                  <Button variant="outline" size="sm">
                    Mark all as read
                  </Button>
                </div>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Notifications</CardTitle>
                  <CardDescription>
                    Stay updated with system alerts and important information
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className={`p-4 rounded-lg border transition-colors ${
                          notification.read 
                            ? 'bg-muted/30 border-muted' 
                            : 'bg-background border-border hover:bg-muted/20'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3 flex-1">
                            <div className="flex-shrink-0 mt-1">
                              {getNotificationIcon(notification.type)}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="font-medium text-sm">
                                  {notification.title}
                                </span>
                                {!notification.read && (
                                  <Badge className="text-xs bg-primary">New</Badge>
                                )}
                                <Badge className={`text-xs ${getSeverityColor(notification.severity)}`}>
                                  {notification.severity}
                                </Badge>
                              </div>
                              <p className="text-sm text-muted-foreground mb-2">
                                {notification.message}
                              </p>
                              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                                <div className="flex items-center gap-1">
                                  <Clock className="h-3 w-3" />
                                  <span>{notification.timestamp}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="flex-shrink-0"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
} 