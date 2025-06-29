"use client"

import { useState, useEffect } from "react"
import { Mic, MicOff, Volume2, VolumeX, UserX, MoreVertical } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Mock voice chat participants
const VOICE_PARTICIPANTS = [
  {
    id: 1,
    name: "CyberNinja",
    speaking: true,
    muted: false,
    team: "alpha",
    avatar: "/placeholder.svg?height=40&width=40",
  },
  {
    id: 2,
    name: "QuantumFrag",
    speaking: false,
    muted: false,
    team: "alpha",
    avatar: "/placeholder.svg?height=40&width=40",
  },
  {
    id: 3,
    name: "NeonSniper",
    speaking: false,
    muted: true,
    team: "beta",
    avatar: "/placeholder.svg?height=40&width=40",
  },
  {
    id: 4,
    name: "ShadowByte",
    speaking: true,
    muted: false,
    team: "beta",
    avatar: "/placeholder.svg?height=40&width=40",
  },
]

export function VoiceChatOverlay({ fullPage = false }) {
  const [participants, setParticipants] = useState(VOICE_PARTICIPANTS)
  const [selfMuted, setSelfMuted] = useState(false)
  const [expanded, setExpanded] = useState(true)

  // Simulate random speaking patterns
  useEffect(() => {
    const interval = setInterval(() => {
      setParticipants((prev) =>
        prev.map((p) => ({
          ...p,
          speaking: p.muted ? false : Math.random() > 0.7,
        })),
      )
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  const toggleMute = (id: number) => {
    setParticipants((prev) => prev.map((p) => (p.id === id ? { ...p, muted: !p.muted, speaking: false } : p)))
  }

  const toggleSelfMute = () => {
    setSelfMuted(!selfMuted)
  }

  if (fullPage) {
    return (
      <div className="h-full w-full p-8 overflow-auto">
        <div className="h-full w-full space-y-8 max-w-none">
          <div className="flex items-center justify-between">
            <h2 className="text-3xl font-bold text-primary">Voice Chat</h2>
            <Button
              variant="ghost"
              size="icon"
              className={`h-12 w-12 rounded-full ${selfMuted ? "bg-destructive/20 text-destructive hover:bg-destructive/30" : "hover:bg-primary/20"}`}
              onClick={toggleSelfMute}
            >
              {selfMuted ? <MicOff className="h-6 w-6" /> : <Mic className="h-6 w-6" />}
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-8 w-full">
            {participants.map((participant) => (
              <Card
                key={participant.id}
                className={`
                  cyberpunk-card p-8 flex flex-col items-center gap-6 transition-all hover-lift cursor-pointer h-80
                  ${participant.speaking && !participant.muted ? "bg-primary/5 hover:bg-primary/10 border-primary/30" : "hover:bg-muted/30"}
                `}
              >
                <div className="relative">
                  <Avatar
                    className={`
                      h-24 w-24 border-4
                      ${participant.team === "alpha" ? "border-primary/50" : "border-secondary/50"}
                      ${participant.speaking && !participant.muted ? "animate-pulse-glow" : ""}
                    `}
                  >
                    <AvatarImage src={participant.avatar || "/placeholder.svg"} />
                    <AvatarFallback className="bg-muted text-lg">{participant.name.substring(0, 2)}</AvatarFallback>
                  </Avatar>
                  {participant.speaking && !participant.muted && (
                    <span className="absolute -bottom-2 -right-2 h-6 w-6 bg-green-500 rounded-full border-4 border-background"></span>
                  )}
                </div>

                <div className="text-center flex-1">
                  <p className="text-xl font-medium mb-2">{participant.name}</p>
                  <div className="flex items-center justify-center gap-2 mb-4">
                    {!participant.muted ? (
                      <div className="flex items-center gap-2">
                        <Volume2 className="h-5 w-5 text-muted-foreground" />
                        <div className="flex items-center gap-1">
                          {[1, 2, 3, 4, 5].map((i) => (
                            <div
                              key={i}
                              className={`
                                h-3 w-2 rounded-sm transition-all
                                ${
                                  participant.speaking
                                    ? i <= Math.floor(Math.random() * 5) + 1
                                      ? "bg-primary"
                                      : "bg-primary/30"
                                    : "bg-muted-foreground/30"
                                }
                              `}
                              style={{
                                height: participant.speaking
                                  ? `${Math.max(8, Math.floor(Math.random() * 20))}px`
                                  : "8px",
                              }}
                            ></div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                        <MicOff className="h-5 w-5 text-destructive" />
                        <span className="text-sm text-destructive">Muted</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-10 w-10 rounded-full hover:bg-muted">
                        <MoreVertical className="h-5 w-5" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-40">
                      <DropdownMenuItem onClick={() => toggleMute(participant.id)}>
                        {participant.muted ? (
                          <>
                            <Volume2 className="mr-2 h-4 w-4" />
                            <span>Unmute</span>
                          </>
                        ) : (
                          <>
                            <VolumeX className="mr-2 h-4 w-4" />
                            <span>Mute</span>
                          </>
                        )}
                      </DropdownMenuItem>
                      <DropdownMenuItem>
                        <UserX className="mr-2 h-4 w-4" />
                        <span>Kick</span>
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </Card>
            ))}
          </div>

          <Card className="cyberpunk-card">
            <CardContent className="p-8">
              <h3 className="text-2xl font-medium mb-6">Voice Settings</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-6 w-full">
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">Input Device</p>
                  <select className="w-full bg-muted/50 border border-border rounded-md p-3 text-base">
                    <option>Default Microphone</option>
                    <option>Headset Microphone</option>
                    <option>External Microphone</option>
                  </select>
                </div>
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">Output Device</p>
                  <select className="w-full bg-muted/50 border border-border rounded-md p-3 text-base">
                    <option>Default Speakers</option>
                    <option>Headset</option>
                    <option>External Speakers</option>
                  </select>
                </div>
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">Voice Activation</p>
                  <select className="w-full bg-muted/50 border border-border rounded-md p-3 text-base">
                    <option>Push to Talk</option>
                    <option>Voice Activity</option>
                    <option>Always On</option>
                  </select>
                </div>
                <div className="space-y-3">
                  <p className="text-sm text-muted-foreground">Noise Suppression</p>
                  <select className="w-full bg-muted/50 border border-border rounded-md p-3 text-base">
                    <option>High</option>
                    <option>Medium</option>
                    <option>Low</option>
                    <option>Off</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${expanded ? "w-80" : "w-16"}`}>
      <Card className="cyberpunk-card border-primary/30 shadow-lg">
        <CardContent className="p-1">
          <div className="p-3 border-b border-border flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setExpanded(!expanded)}>
                {expanded ? <MoreVertical className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
              </Button>
              {expanded && <span className="text-sm font-medium">Voice Chat</span>}
            </div>
            {expanded && (
              <div className="flex items-center gap-1">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className={`h-7 w-7 rounded-full ${selfMuted ? "bg-destructive/20 text-destructive hover:bg-destructive/30" : "hover:bg-primary/20"}`}
                        onClick={toggleSelfMute}
                      >
                        {selfMuted ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent side="left">{selfMuted ? "Unmute Microphone" : "Mute Microphone"}</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
            )}
          </div>

          {expanded && (
            <div className="max-h-80 overflow-y-auto">
              {participants.map((participant) => (
                <div
                  key={participant.id}
                  className={`
                    p-4 flex items-center gap-4 border-b border-border/50 transition-all hover-glow
                    ${participant.speaking && !participant.muted ? "bg-primary/5 hover:bg-primary/10" : "hover:bg-muted/30"}
                  `}
                >
                  <div className="relative">
                    <Avatar
                      className={`
                      h-8 w-8 border-2
                      ${participant.team === "alpha" ? "border-primary/50" : "border-secondary/50"}
                      ${participant.speaking && !participant.muted ? "animate-pulse-glow" : ""}
                    `}
                    >
                      <AvatarImage src={participant.avatar || "/placeholder.svg"} />
                      <AvatarFallback className="bg-muted text-xs">{participant.name.substring(0, 2)}</AvatarFallback>
                    </Avatar>
                    {participant.speaking && !participant.muted && (
                      <span className="absolute -bottom-1 -right-1 h-3 w-3 bg-green-500 rounded-full border-2 border-background"></span>
                    )}
                  </div>

                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{participant.name}</p>
                    <div className="flex items-center gap-1.5">
                      {!participant.muted ? (
                        <div className="flex items-center gap-1">
                          <Volume2 className="h-3 w-3 text-muted-foreground" />
                          <div className="flex items-center gap-0.5">
                            {[1, 2, 3, 4, 5].map((i) => (
                              <div
                                key={i}
                                className={`
                                  h-1.5 w-1 rounded-sm transition-all
                                  ${
                                    participant.speaking
                                      ? i <= Math.floor(Math.random() * 5) + 1
                                        ? "bg-primary"
                                        : "bg-primary/30"
                                      : "bg-muted-foreground/30"
                                  }
                                `}
                                style={{
                                  height: participant.speaking
                                    ? `${Math.max(4, Math.floor(Math.random() * 12))}px`
                                    : "4px",
                                }}
                              ></div>
                            ))}
                          </div>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1">
                          <MicOff className="h-3 w-3 text-destructive" />
                          <span className="text-xs text-destructive">Muted</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-7 w-7 rounded-full hover:bg-muted">
                          <MoreVertical className="h-3.5 w-3.5" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-40">
                        <DropdownMenuItem onClick={() => toggleMute(participant.id)}>
                          {participant.muted ? (
                            <>
                              <Volume2 className="mr-2 h-4 w-4" />
                              <span>Unmute</span>
                            </>
                          ) : (
                            <>
                              <VolumeX className="mr-2 h-4 w-4" />
                              <span>Mute</span>
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <UserX className="mr-2 h-4 w-4" />
                          <span>Kick</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!expanded && (
            <div className="p-2 flex flex-col items-center gap-2">
              {participants
                .filter((p) => p.speaking && !p.muted)
                .slice(0, 3)
                .map((participant) => (
                  <Tooltip key={participant.id}>
                    <TooltipTrigger asChild>
                      <Avatar className="h-8 w-8 animate-pulse-glow">
                        <AvatarImage src={participant.avatar || "/placeholder.svg"} />
                        <AvatarFallback className="bg-muted text-xs">{participant.name.substring(0, 2)}</AvatarFallback>
                      </Avatar>
                    </TooltipTrigger>
                    <TooltipContent side="left">{participant.name} is speaking</TooltipContent>
                  </Tooltip>
                ))}

              <Button
                variant="ghost"
                size="icon"
                className={`h-8 w-8 rounded-full mt-1 ${selfMuted ? "bg-destructive/20 text-destructive" : ""}`}
                onClick={toggleSelfMute}
              >
                {selfMuted ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
