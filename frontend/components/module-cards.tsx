"use client"

import { Shield, Network, BarChart3, Play, ArrowRight, Activity, AlertTriangle, CheckCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

const modules = [
  {
    id: 1,
    title: "Anti-Cheat Status",
    description: "Real-time monitoring of cheat detection systems and security protocols",
    icon: Shield,
    status: "active",
    statusText: "Active",
    metrics: "3 alerts",
    color: "text-green-400",
    bgColor: "bg-green-400/10",
    borderColor: "border-green-400/30",
  },
  {
    id: 2,
    title: "Network Stress Test",
    description: "Simulate high-load network conditions and packet loss scenarios",
    icon: Network,
    status: "running",
    statusText: "Running",
    metrics: "12ms avg",
    color: "text-blue-400",
    bgColor: "bg-blue-400/10",
    borderColor: "border-blue-400/30",
  },
  {
    id: 3,
    title: "Match Analytics",
    description: "Generate realistic player behavior patterns and performance metrics",
    icon: BarChart3,
    status: "ready",
    statusText: "Ready",
    metrics: "1.2k samples",
    color: "text-purple-400",
    bgColor: "bg-purple-400/10",
    borderColor: "border-purple-400/30",
  },
  {
    id: 4,
    title: "Replay Viewer",
    description: "Analyze recorded gameplay sessions and detect anomalous behavior",
    icon: Play,
    status: "idle",
    statusText: "Idle",
    metrics: "47 replays",
    color: "text-yellow-400",
    bgColor: "bg-yellow-400/10",
    borderColor: "border-yellow-400/30",
  },
]

const getStatusIcon = (status: string) => {
  switch (status) {
    case "active":
      return <CheckCircle className="h-4 w-4 text-green-400" />
    case "running":
      return <Activity className="h-4 w-4 text-blue-400 animate-pulse" />
    case "ready":
      return <CheckCircle className="h-4 w-4 text-purple-400" />
    case "idle":
      return <AlertTriangle className="h-4 w-4 text-yellow-400" />
    default:
      return <CheckCircle className="h-4 w-4" />
  }
}

export function ModuleCards() {
  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Core Modules</h2>
          <p className="text-muted-foreground">Essential eSports and testing components</p>
        </div>
        <Button variant="outline" size="sm">
          View All
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {modules.map((module) => (
          <Card key={module.id} className={`cyberpunk-card hover-lift cursor-pointer group ${module.borderColor}`}>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg ${module.bgColor}`}>
                  <module.icon className={`h-5 w-5 ${module.color}`} />
                </div>
                <Badge variant="outline" className="gap-1">
                  {getStatusIcon(module.status)}
                  {module.statusText}
                </Badge>
              </div>
              <CardTitle className="text-lg">{module.title}</CardTitle>
              <CardDescription className="text-sm leading-relaxed">{module.description}</CardDescription>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">{module.metrics}</div>
                <Button size="sm" variant="ghost" className="opacity-0 group-hover:opacity-100 transition-opacity">
                  View
                  <ArrowRight className="ml-1 h-3 w-3" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
