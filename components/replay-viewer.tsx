"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Slider } from "@/components/ui/slider"
import { Play, Pause, SkipBack, SkipForward, Download, Flag, Eye } from "lucide-react"

// Mock replay data
const FLAGGED_EVENTS = [
  { time: 45, type: "aimbot", player: "ShadowByte", severity: "high" },
  { time: 127, type: "wallhack", player: "NeonSniper", severity: "medium" },
  { time: 203, type: "speed", player: "QuantumFrag", severity: "high" },
  { time: 289, type: "macro", player: "CyberNinja", severity: "low" },
  { time: 367, type: "esp", player: "VirtualPhantom", severity: "medium" },
]

const MATCH_INFO = {
  id: "MATCH_1247",
  duration: 420, // 7 minutes in seconds
  map: "de_cyberpunk",
  mode: "5v5 Competitive",
  date: "2024-01-15 14:30:00",
}

export function ReplayViewer() {
  const [currentTime, setCurrentTime] = useState([0])
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  const getEventColor = (type: string) => {
    switch (type) {
      case "aimbot":
        return "bg-red-500"
      case "wallhack":
        return "bg-orange-500"
      case "speed":
        return "bg-yellow-500"
      case "macro":
        return "bg-blue-500"
      case "esp":
        return "bg-purple-500"
      default:
        return "bg-gray-500"
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "border-red-500/30 text-red-400"
      case "medium":
        return "border-yellow-500/30 text-yellow-400"
      case "low":
        return "border-blue-500/30 text-blue-400"
      default:
        return "border-gray-500/30 text-gray-400"
    }
  }

  return (
    <Card className="cyberpunk-card w-full max-w-none">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Eye className="h-5 w-5 text-primary" />
            <CardTitle className="text-xl">Replay Viewer Preview</CardTitle>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="px-3 py-1">
              {MATCH_INFO.id}
            </Badge>
            <Button variant="outline" size="sm" className="gap-2 bg-transparent">
              <Download className="h-4 w-4" />
              Export Replay
            </Button>
          </div>
        </div>
        <CardDescription>
          Match timeline analysis with flagged events - {MATCH_INFO.map} • {MATCH_INFO.mode}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Match Info */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4 w-full">
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Duration</div>
            <div className="text-lg font-bold">{formatTime(MATCH_INFO.duration)}</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Events</div>
            <div className="text-lg font-bold text-red-400">{FLAGGED_EVENTS.length}</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Map</div>
            <div className="text-lg font-bold">{MATCH_INFO.map}</div>
          </div>
          <div className="bg-muted/30 p-3 rounded-lg">
            <div className="text-sm text-muted-foreground">Date</div>
            <div className="text-lg font-bold">Jan 15, 2024</div>
          </div>
        </div>

        {/* Timeline Visualization */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-medium">Match Timeline</h3>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Flag className="h-4 w-4" />
              Flagged Events
            </div>
          </div>

          {/* Timeline Bar */}
          <div className="relative">
            <div className="h-16 bg-muted/20 rounded-lg border border-border/40 relative overflow-hidden">
              {/* Progress indicator */}
              <div
                className="absolute top-0 left-0 h-full bg-primary/20 transition-all duration-300"
                style={{ width: `${(currentTime[0] / MATCH_INFO.duration) * 100}%` }}
              />

              {/* Event markers */}
              {FLAGGED_EVENTS.map((event, index) => (
                <div
                  key={index}
                  className="absolute top-1 bottom-1 w-2 rounded-sm cursor-pointer hover:scale-110 transition-transform"
                  style={{
                    left: `${(event.time / MATCH_INFO.duration) * 100}%`,
                  }}
                  title={`${event.type} - ${event.player} at ${formatTime(event.time)}`}
                >
                  <div className={`w-full h-full ${getEventColor(event.type)} rounded-sm`} />
                </div>
              ))}

              {/* Current time indicator */}
              <div
                className="absolute top-0 bottom-0 w-0.5 bg-primary shadow-lg"
                style={{ left: `${(currentTime[0] / MATCH_INFO.duration) * 100}%` }}
              />
            </div>

            {/* Time labels */}
            <div className="flex justify-between text-xs text-muted-foreground mt-2">
              <span>0:00</span>
              <span>{formatTime(MATCH_INFO.duration)}</span>
            </div>
          </div>

          {/* Timeline Slider */}
          <Slider
            value={currentTime}
            onValueChange={setCurrentTime}
            max={MATCH_INFO.duration}
            step={1}
            className="w-full"
          />
        </div>

        {/* Playback Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <SkipBack className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsPlaying(!isPlaying)}
              className={isPlaying ? "text-primary" : ""}
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <Button variant="outline" size="sm">
              <SkipForward className="h-4 w-4" />
            </Button>
            <div className="text-sm font-mono bg-muted/30 px-3 py-1 rounded">
              {formatTime(currentTime[0])} / {formatTime(MATCH_INFO.duration)}
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">Speed:</span>
              <select
                value={playbackSpeed}
                onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
                className="bg-muted/30 border border-border rounded px-2 py-1 text-sm"
              >
                <option value={0.25}>0.25x</option>
                <option value={0.5}>0.5x</option>
                <option value={1}>1x</option>
                <option value={2}>2x</option>
                <option value={4}>4x</option>
              </select>
            </div>
          </div>
        </div>

        {/* Flagged Events List */}
        <div className="space-y-3">
          <h3 className="font-medium">Flagged Events</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {FLAGGED_EVENTS.map((event, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 rounded-lg bg-muted/20 hover:bg-muted/40 transition-colors cursor-pointer"
                onClick={() => setCurrentTime([event.time])}
              >
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${getEventColor(event.type)}`} />
                  <span className="font-medium capitalize">{event.type}</span>
                  <span className="text-muted-foreground">by {event.player}</span>
                  <span className="text-sm text-muted-foreground">at {formatTime(event.time)}</span>
                </div>
                <Badge variant="outline" className={`${getSeverityColor(event.severity)} text-xs`}>
                  {event.severity.toUpperCase()}
                </Badge>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
