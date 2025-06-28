"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Shield, Download, AlertTriangle, Activity, TrendingUp } from "lucide-react"

// Mock anti-cheat detection data
const DETECTION_EVENTS = [
  {
    id: 1,
    timestamp: "14:32:47",
    playerId: "PLR_4829",
    playerName: "ShadowByte",
    eventType: "AIMBOT_DETECTED",
    confidence: 94.2,
    severity: "high",
    details: "Abnormal mouse movement patterns detected",
  },
  {
    id: 2,
    timestamp: "14:31:23",
    playerId: "PLR_7391",
    playerName: "NeonSniper",
    eventType: "WALLHACK_SUSPECTED",
    confidence: 78.5,
    severity: "medium",
    details: "Player tracking through solid objects",
  },
  {
    id: 3,
    timestamp: "14:30:15",
    playerId: "PLR_2847",
    playerName: "QuantumFrag",
    eventType: "SPEED_HACK",
    confidence: 89.7,
    severity: "high",
    details: "Movement speed exceeds game limits",
  },
  {
    id: 4,
    timestamp: "14:29:08",
    playerId: "PLR_5632",
    playerName: "CyberNinja",
    eventType: "MACRO_USAGE",
    confidence: 67.3,
    severity: "low",
    details: "Repetitive input patterns detected",
  },
  {
    id: 5,
    timestamp: "14:28:42",
    playerId: "PLR_9184",
    playerName: "VirtualPhantom",
    eventType: "ESP_DETECTED",
    confidence: 91.8,
    severity: "high",
    details: "Extra sensory perception indicators",
  },
]

const HEATMAP_DATA = [
  { hour: "12:00", incidents: 2 },
  { hour: "13:00", incidents: 5 },
  { hour: "14:00", incidents: 12 },
  { hour: "15:00", incidents: 8 },
  { hour: "16:00", incidents: 3 },
  { hour: "17:00", incidents: 7 },
]

export function AntiCheatMonitor() {
  const [events, setEvents] = useState(DETECTION_EVENTS)
  const [isLive, setIsLive] = useState(true)

  // Simulate real-time detection events
  useEffect(() => {
    if (!isLive) return

    const interval = setInterval(() => {
      const newEvent = {
        id: events.length + Math.random(),
        timestamp: new Date().toLocaleTimeString([], { hour12: false }),
        playerId: `PLR_${Math.floor(Math.random() * 9999)}`,
        playerName: ["GhostHunter", "PixelWarrior", "DataMiner", "CodeBreaker"][Math.floor(Math.random() * 4)],
        eventType: ["AIMBOT_DETECTED", "WALLHACK_SUSPECTED", "SPEED_HACK", "MACRO_USAGE", "ESP_DETECTED"][
          Math.floor(Math.random() * 5)
        ],
        confidence: Math.floor(Math.random() * 40) + 60,
        severity: ["high", "medium", "low"][Math.floor(Math.random() * 3)] as "high" | "medium" | "low",
        details: [
          "Suspicious behavior pattern identified",
          "Anomalous game state manipulation",
          "Irregular network packet timing",
          "Unauthorized memory access detected",
        ][Math.floor(Math.random() * 4)],
      }

      setEvents((prev) => [newEvent, ...prev.slice(0, 9)])
    }, 3000)

    return () => clearInterval(interval)
  }, [isLive, events.length])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "low":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return "text-red-400"
    if (confidence >= 75) return "text-yellow-400"
    return "text-blue-400"
  }

  const totalIncidents = HEATMAP_DATA.reduce((sum, data) => sum + data.incidents, 0)
  const highSeverityCount = events.filter((e) => e.severity === "high").length

  return (
    <Card className="cyberpunk-card w-full h-full max-w-none">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-primary" />
            <CardTitle className="text-xl">Live Anti-Cheat Monitor</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="border-green-500/30 text-green-400">
              <Activity className="mr-1 h-3 w-3" />
              {isLive ? "LIVE" : "PAUSED"}
            </Badge>
            <Button variant="outline" size="sm" className="gap-2 bg-transparent">
              <Download className="h-4 w-4" />
              Export Report
            </Button>
          </div>
        </div>
        <CardDescription>Real-time cheat detection and behavioral analysis</CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 w-full">
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Total Incidents</div>
            <div className="text-2xl font-bold text-primary">{totalIncidents}</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">High Severity</div>
            <div className="text-2xl font-bold text-red-400">{highSeverityCount}</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Active Players</div>
            <div className="text-2xl font-bold text-green-400">24</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Detection Rate</div>
            <div className="text-2xl font-bold text-yellow-400">97.3%</div>
          </div>
        </div>

        {/* Behavior Heatmap */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-primary" />
            <h3 className="font-medium">Suspicious Activity Heatmap</h3>
          </div>
          <div className="grid grid-cols-6 md:grid-cols-8 lg:grid-cols-12 xl:grid-cols-16 gap-4 px-2 py-3 w-full">
            {HEATMAP_DATA.map((data, index) => (
              <div key={index} className="text-center">
                <div
                  className={`h-8 rounded-md flex items-center justify-center text-xs font-medium transition-all hover:scale-105 ${
                    data.incidents > 10
                      ? "bg-red-500/30 text-red-400"
                      : data.incidents > 5
                        ? "bg-yellow-500/30 text-yellow-400"
                        : "bg-blue-500/30 text-blue-400"
                  }`}
                >
                  {data.incidents}
                </div>
                <div className="text-xs text-muted-foreground mt-1">{data.hour}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Detection Log Feed */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-medium">Detection Log Feed</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsLive(!isLive)}
              className={isLive ? "text-green-400" : "text-yellow-400"}
            >
              {isLive ? "Pause" : "Resume"}
            </Button>
          </div>

          <ScrollArea className="h-80 border border-border/40 rounded-lg">
            <div className="p-4 space-y-3 font-mono text-sm">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="flex flex-col sm:flex-row sm:items-center gap-2 p-3 rounded-md bg-muted/20 hover:bg-muted/40 transition-colors"
                >
                  <div className="flex items-center gap-3 flex-1">
                    <span className="text-muted-foreground text-xs min-w-[60px]">{event.timestamp}</span>
                    <Badge variant="outline" className={`text-xs ${getSeverityColor(event.severity)}`}>
                      {event.eventType}
                    </Badge>
                    <span className="font-medium">{event.playerName}</span>
                    <span className="text-muted-foreground text-xs">({event.playerId})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-sm font-bold ${getConfidenceColor(event.confidence)}`}>
                      {event.confidence.toFixed(1)}%
                    </span>
                    <AlertTriangle className="h-4 w-4 text-yellow-400" />
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
      </CardContent>
    </Card>
  )
}
