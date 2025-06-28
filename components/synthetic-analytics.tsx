"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { BarChart3, Download, Filter, TrendingUp, Users } from "lucide-react"

// Mock analytics data
const NETWORK_DATA = [
  { time: "14:00", packetLoss: 0.2, jitter: 12 },
  { time: "14:05", packetLoss: 0.1, jitter: 8 },
  { time: "14:10", packetLoss: 0.3, jitter: 15 },
  { time: "14:15", packetLoss: 0.8, jitter: 22 },
  { time: "14:20", packetLoss: 0.4, jitter: 18 },
  { time: "14:25", packetLoss: 0.2, jitter: 10 },
  { time: "14:30", packetLoss: 0.1, jitter: 7 },
]

const CHEAT_ATTEMPTS = [
  { match: "Match #1247", aimbot: 3, wallhack: 1, speedhack: 2, other: 1 },
  { match: "Match #1248", aimbot: 1, wallhack: 2, speedhack: 0, other: 3 },
  { match: "Match #1249", aimbot: 4, wallhack: 0, speedhack: 1, other: 2 },
  { match: "Match #1250", aimbot: 2, wallhack: 3, speedhack: 1, other: 0 },
  { match: "Match #1251", aimbot: 0, wallhack: 1, speedhack: 3, other: 1 },
]

const PLAYER_STATS = [
  {
    id: 1,
    name: "CyberNinja",
    kills: 24,
    deaths: 8,
    accuracy: 68.4,
    kdr: 3.0,
    suspicionScore: 12,
    status: "clean",
  },
  {
    id: 2,
    name: "ShadowByte",
    kills: 31,
    deaths: 5,
    accuracy: 94.2,
    kdr: 6.2,
    suspicionScore: 87,
    status: "flagged",
  },
  {
    id: 3,
    name: "QuantumFrag",
    kills: 18,
    deaths: 12,
    accuracy: 72.1,
    kdr: 1.5,
    suspicionScore: 23,
    status: "clean",
  },
  {
    id: 4,
    name: "NeonSniper",
    kills: 22,
    deaths: 9,
    accuracy: 81.7,
    kdr: 2.4,
    suspicionScore: 45,
    status: "monitoring",
  },
  {
    id: 5,
    name: "VirtualPhantom",
    kills: 16,
    deaths: 14,
    accuracy: 65.3,
    kdr: 1.1,
    suspicionScore: 8,
    status: "clean",
  },
]

export function SyntheticAnalytics() {
  const [sortBy, setSortBy] = useState("kdr")
  const [filterStatus, setFilterStatus] = useState("all")

  const filteredPlayers = PLAYER_STATS.filter(
    (player) => filterStatus === "all" || player.status === filterStatus,
  ).sort((a, b) => {
    switch (sortBy) {
      case "kdr":
        return b.kdr - a.kdr
      case "accuracy":
        return b.accuracy - a.accuracy
      case "suspicion":
        return b.suspicionScore - a.suspicionScore
      default:
        return 0
    }
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "clean":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "flagged":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "monitoring":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getSuspicionColor = (score: number) => {
    if (score >= 70) return "text-red-400"
    if (score >= 40) return "text-yellow-400"
    return "text-green-400"
  }

  return (
    <Card className="cyberpunk-card w-full max-w-none">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-primary" />
            <CardTitle className="text-xl">Match Analytics</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-2 bg-transparent">
              <Download className="h-4 w-4" />
              Download CSV
            </Button>
            <Button variant="outline" size="sm">
              View Full Report
            </Button>
          </div>
        </div>
        <CardDescription>Comprehensive match performance and behavioral analysis</CardDescription>
      </CardHeader>

      <CardContent>
        <Tabs defaultValue="network" className="space-y-4">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="network" className="data-[state=active]:text-primary">
              Network
            </TabsTrigger>
            <TabsTrigger value="security" className="data-[state=active]:text-primary">
              Security
            </TabsTrigger>
            <TabsTrigger value="players" className="data-[state=active]:text-primary">
              Players
            </TabsTrigger>
          </TabsList>

          <TabsContent value="network" className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 w-full">
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Avg Latency</div>
                <div className="text-xl font-bold text-blue-400">12.4ms</div>
                <div className="text-xs text-green-400 flex items-center gap-1">
                  <TrendingUp className="h-3 w-3 rotate-180" />
                  -2ms
                </div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Packet Loss</div>
                <div className="text-xl font-bold text-yellow-400">0.3%</div>
                <div className="text-xs text-yellow-400">Stable</div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Jitter</div>
                <div className="text-xl font-bold text-purple-400">13.2ms</div>
                <div className="text-xs text-green-400">Normal</div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Bandwidth</div>
                <div className="text-xl font-bold text-cyan-400">45.2MB/s</div>
                <div className="text-xs text-green-400">Optimal</div>
              </div>
            </div>

            <div className="h-64 border border-primary/20 rounded-lg bg-primary/5 flex items-center justify-center">
              <div className="text-center space-y-2">
                <TrendingUp className="h-8 w-8 text-primary mx-auto" />
                <div className="text-sm font-medium">Network Performance Chart</div>
                <div className="text-xs text-muted-foreground">Packet loss and jitter over time</div>
                <Badge variant="outline" className="text-xs">
                  Chart Visualization
                </Badge>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="security" className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 w-full">
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Total Attempts</div>
                <div className="text-xl font-bold text-red-400">37</div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Blocked</div>
                <div className="text-xl font-bold text-green-400">35</div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">Success Rate</div>
                <div className="text-xl font-bold text-primary">94.6%</div>
              </div>
              <div className="bg-muted/30 p-3 rounded-lg">
                <div className="text-sm text-muted-foreground">False Positives</div>
                <div className="text-xl font-bold text-yellow-400">2</div>
              </div>
            </div>

            <div className="space-y-3">
              <h3 className="font-medium">Cheat Attempts by Match</h3>
              <div className="space-y-2">
                {CHEAT_ATTEMPTS.map((match, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/20">
                    <span className="font-medium">{match.match}</span>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-red-400">Aimbot: {match.aimbot}</span>
                      <span className="text-yellow-400">Wallhack: {match.wallhack}</span>
                      <span className="text-blue-400">Speed: {match.speedhack}</span>
                      <span className="text-purple-400">Other: {match.other}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="players" className="space-y-4">
            <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-primary" />
                <span className="font-medium">Player Statistics</span>
              </div>
              <div className="flex flex-col sm:flex-row gap-2">
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-[140px]">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="kdr">K/D Ratio</SelectItem>
                    <SelectItem value="accuracy">Accuracy</SelectItem>
                    <SelectItem value="suspicion">Suspicion Score</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-[120px]">
                    <Filter className="mr-2 h-4 w-4" />
                    <SelectValue placeholder="Filter" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Players</SelectItem>
                    <SelectItem value="clean">Clean</SelectItem>
                    <SelectItem value="monitoring">Monitoring</SelectItem>
                    <SelectItem value="flagged">Flagged</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border/40">
                    <th className="text-left p-3 font-medium">Player</th>
                    <th className="text-left p-3 font-medium">K/D</th>
                    <th className="text-left p-3 font-medium">Accuracy</th>
                    <th className="text-left p-3 font-medium">Suspicion</th>
                    <th className="text-left p-3 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="[&_tr:last-child]:border-0">
                  {filteredPlayers.map((player) => (
                    <tr key={player.id} className="border-b border-border/20 hover:bg-muted/20">
                      <td className="p-3 font-medium">{player.name}</td>
                      <td className="p-3">{player.kdr.toFixed(1)}</td>
                      <td className="p-3">{player.accuracy.toFixed(1)}%</td>
                      <td className="p-3">
                        <span className={`font-medium ${getSuspicionColor(player.suspicionScore)}`}>
                          {player.suspicionScore}
                        </span>
                      </td>
                      <td className="p-3">
                        <Badge variant="outline" className={`${getStatusColor(player.status)} text-xs`}>
                          {player.status.toUpperCase()}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
