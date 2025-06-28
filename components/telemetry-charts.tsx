"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, TrendingDown, Activity, AlertTriangle } from "lucide-react"

// Mock chart data
const packetLossData = [
  { time: "14:00", loss: 0.2, jitter: 12 },
  { time: "14:05", loss: 0.1, jitter: 8 },
  { time: "14:10", loss: 0.3, jitter: 15 },
  { time: "14:15", loss: 0.8, jitter: 22 },
  { time: "14:20", loss: 0.4, jitter: 18 },
  { time: "14:25", loss: 0.2, jitter: 10 },
  { time: "14:30", loss: 0.1, jitter: 7 },
]

const cheatEvents = [
  { category: "Aimbot", count: 3, severity: "high" },
  { category: "Wallhack", count: 1, severity: "medium" },
  { category: "Speed Hack", count: 2, severity: "high" },
  { category: "ESP", count: 0, severity: "low" },
  { category: "Macro", count: 4, severity: "medium" },
]

export function TelemetryCharts() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Match Telemetry</h2>
        <p className="text-muted-foreground">Real-time performance metrics and security analytics</p>
      </div>

      <Tabs defaultValue="network" className="space-y-4">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="network" className="data-[state=active]:text-primary">
            Network Performance
          </TabsTrigger>
          <TabsTrigger value="security" className="data-[state=active]:text-primary">
            Security Events
          </TabsTrigger>
        </TabsList>

        <TabsContent value="network" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Activity className="h-4 w-4 text-blue-400" />
                  <span className="text-sm font-medium">Avg Latency</span>
                </div>
                <div className="mt-2">
                  <div className="text-2xl font-bold">12ms</div>
                  <div className="flex items-center gap-1 text-xs text-green-400">
                    <TrendingDown className="h-3 w-3" />
                    -2ms from last hour
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-400" />
                  <span className="text-sm font-medium">Packet Loss</span>
                </div>
                <div className="mt-2">
                  <div className="text-2xl font-bold">0.2%</div>
                  <div className="flex items-center gap-1 text-xs text-yellow-400">
                    <TrendingUp className="h-3 w-3" />
                    +0.1% from baseline
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="flex items-center gap-2">
                  <Activity className="h-4 w-4 text-purple-400" />
                  <span className="text-sm font-medium">Jitter</span>
                </div>
                <div className="mt-2">
                  <div className="text-2xl font-bold">8ms</div>
                  <div className="flex items-center gap-1 text-xs text-green-400">
                    <TrendingDown className="h-3 w-3" />
                    Stable
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="cyberpunk-card">
            <CardHeader>
              <CardTitle className="text-lg">Network Performance Over Time</CardTitle>
              <CardDescription>Packet loss and jitter measurements</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 flex items-center justify-center border border-primary/20 rounded-lg bg-primary/5">
                <div className="text-center space-y-2">
                  <Activity className="h-8 w-8 text-primary mx-auto" />
                  <div className="text-sm font-medium">Network Chart</div>
                  <div className="text-xs text-muted-foreground">Real-time packet loss and jitter visualization</div>
                  <Badge variant="outline" className="text-xs">
                    Chart Component Placeholder
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-400">10</div>
                  <div className="text-xs text-muted-foreground">Total Events</div>
                </div>
              </CardContent>
            </Card>

            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-400">5</div>
                  <div className="text-xs text-muted-foreground">High Severity</div>
                </div>
              </CardContent>
            </Card>

            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">3</div>
                  <div className="text-xs text-muted-foreground">Medium</div>
                </div>
              </CardContent>
            </Card>

            <Card className="cyberpunk-card">
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">2</div>
                  <div className="text-xs text-muted-foreground">Players Banned</div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="cyberpunk-card">
            <CardHeader>
              <CardTitle className="text-lg">Cheat Detection Events</CardTitle>
              <CardDescription>Flagged activities by category and severity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {cheatEvents.map((event, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/20">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded bg-primary/10 flex items-center justify-center">
                        <span className="text-sm font-bold text-primary">{event.count}</span>
                      </div>
                      <div>
                        <div className="font-medium">{event.category}</div>
                        <div className="text-xs text-muted-foreground">Detection events</div>
                      </div>
                    </div>
                    <Badge
                      variant="outline"
                      className={
                        event.severity === "high"
                          ? "border-red-400/30 text-red-400"
                          : event.severity === "medium"
                            ? "border-yellow-400/30 text-yellow-400"
                            : "border-green-400/30 text-green-400"
                      }
                    >
                      {event.severity}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
