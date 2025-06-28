"use client"

import { Play, Zap, Shield } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function HeroSection() {
  return (
    <section className="relative">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Hero Content */}
        <div className="space-y-6">
          <div className="space-y-4">
            <Badge variant="outline" className="border-primary/30 text-primary">
              <Zap className="mr-1 h-3 w-3" />
              eSports Platform
            </Badge>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight">
              <span className="text-primary">GhostLAN</span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-lg">
              Advanced offline eSports anti-cheat testing platform for competitive gaming environments.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Button size="lg" className="gap-2 bg-primary hover:bg-primary/90">
              <Play className="h-5 w-5" />
              Start Session
            </Button>
            <Button variant="outline" size="lg" className="gap-2 bg-transparent">
              <Shield className="h-5 w-5" />
              View Documentation
            </Button>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-3 gap-4 pt-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">99.9%</div>
              <div className="text-xs text-muted-foreground">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-secondary">1,247</div>
              <div className="text-xs text-muted-foreground">Tests Run</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">Active</div>
              <div className="text-xs text-muted-foreground">Status</div>
            </div>
          </div>
        </div>

        {/* Hero Visual */}
        <div className="relative">
          <Card className="cyberpunk-card overflow-hidden">
            <CardContent className="p-0">
              <div className="aspect-video bg-gradient-to-br from-primary/20 via-background to-secondary/20 flex items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 grid-bg opacity-20" />
                <div className="relative z-10 text-center space-y-4">
                  <div className="w-16 h-16 mx-auto bg-primary/20 rounded-full flex items-center justify-center">
                    <Shield className="h-8 w-8 text-primary" />
                  </div>
                  <div className="space-y-2">
                    <div className="text-lg font-medium">System Ready</div>
                    <div className="text-sm text-muted-foreground">All systems operational</div>
                  </div>
                </div>

                {/* Animated elements */}
                <div className="absolute top-4 left-4 w-2 h-2 bg-primary rounded-full animate-pulse" />
                <div
                  className="absolute top-8 right-8 w-1 h-1 bg-secondary rounded-full animate-pulse"
                  style={{ animationDelay: "0.5s" }}
                />
                <div
                  className="absolute bottom-6 left-8 w-1.5 h-1.5 bg-primary rounded-full animate-pulse"
                  style={{ animationDelay: "1s" }}
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
