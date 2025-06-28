"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Terminal, Pause, Play, Download } from "lucide-react"

// Mock log data
const LOG_TYPES = {
  info: { color: "text-blue-400", bg: "bg-blue-400/10" },
  warning: { color: "text-yellow-400", bg: "bg-yellow-400/10" },
  error: { color: "text-red-400", bg: "bg-red-400/10" },
  success: { color: "text-green-400", bg: "bg-green-400/10" },
}

const INITIAL_LOGS = [
  {
    id: 1,
    timestamp: "14:32:15",
    type: "info",
    event: "SYSTEM_START",
    message: "GhostLAN SimWorld initialized successfully",
  },
  {
    id: 2,
    timestamp: "14:32:16",
    type: "success",
    event: "ANTICHEAT_LOAD",
    message: "Anti-cheat engine loaded and active",
  },
  {
    id: 3,
    timestamp: "14:32:18",
    type: "info",
    event: "NETWORK_TEST",
    message: "Network stress test module ready",
  },
  {
    id: 4,
    timestamp: "14:32:22",
    type: "warning",
    event: "PLAYER_CONNECT",
    message: "Player CyberNinja connected with high ping (245ms)",
  },
  {
    id: 5,
    timestamp: "14:32:25",
    type: "error",
    event: "CHEAT_DETECT",
    message: "Suspicious activity detected from player ShadowByte",
  },
  {
    id: 6,
    timestamp: "14:32:28",
    type: "info",
    event: "REPLAY_SAVE",
    message: "Match replay saved to storage (ID: 1247)",
  },
]

export function LiveLogs() {
  const [logs, setLogs] = useState(INITIAL_LOGS)
  const [isPaused, setIsPaused] = useState(false)
  const [autoScroll, setAutoScroll] = useState(true)

  // Simulate real-time logs
  useEffect(() => {
    if (isPaused) return

    const interval = setInterval(() => {
      const newLog = {
        id: logs.length + Math.random(),
        timestamp: new Date().toLocaleTimeString([], { hour12: false }),
        type: ["info", "warning", "error", "success"][Math.floor(Math.random() * 4)] as keyof typeof LOG_TYPES,
        event: ["PLAYER_ACTION", "NETWORK_EVENT", "SYSTEM_CHECK", "DATA_SYNC"][Math.floor(Math.random() * 4)],
        message: [
          "Player QuantumFrag performed headshot",
          "Network latency spike detected (156ms)",
          "System health check completed",
          "Analytics data synchronized",
          "New player joined the simulation",
          "Packet loss detected on connection #4",
        ][Math.floor(Math.random() * 6)],
      }

      setLogs((prev) => [...prev.slice(-19), newLog])
    }, 2000)

    return () => clearInterval(interval)
  }, [isPaused, logs.length])

  return (
    <Card className="cyberpunk-card h-[500px] flex flex-col">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="h-5 w-5 text-primary" />
            <CardTitle className="text-lg">Live Logs</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => setIsPaused(!isPaused)}>
              {isPaused ? <Play className="h-4 w-4" /> : <Pause className="h-4 w-4" />}
            </Button>
            <Button variant="ghost" size="sm">
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <CardDescription>Real-time system events and monitoring data</CardDescription>
      </CardHeader>

      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full px-6 pb-6">
          <div className="space-y-2 font-mono text-sm">
            {logs.map((log) => (
              <div key={log.id} className="flex items-start gap-3 p-2 rounded-md hover:bg-muted/30 transition-colors">
                <span className="text-muted-foreground text-xs mt-0.5 min-w-[60px]">{log.timestamp}</span>
                <Badge
                  variant="outline"
                  className={`${LOG_TYPES[log.type].color} ${LOG_TYPES[log.type].bg} border-current/30 text-xs`}
                >
                  {log.event}
                </Badge>
                <span className="text-foreground flex-1 leading-relaxed">{log.message}</span>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
