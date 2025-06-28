"use client"

import { useState } from "react"
import { Menu, Home, Play, FileText, Settings, Bell, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function DashboardHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navItems = [
    { icon: Home, label: "Home", active: true },
    { icon: Play, label: "Simulations", active: false },
    { icon: FileText, label: "Logs", active: false },
    { icon: Settings, label: "Settings", active: false },
  ]

  return (
    <header className="border-b border-border/40 bg-background/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="container mx-auto px-4 md:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <img src="/images/logo.png" alt="GhostLAN Logo" className="w-8 h-8" />
            <div className="flex flex-col">
              <h1 className="text-xl font-bold text-primary">GhostLAN</h1>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Button
                key={item.label}
                variant={item.active ? "default" : "ghost"}
                size="sm"
                className={`gap-2 ${
                  item.active ? "bg-primary/10 text-primary hover:bg-primary/20" : "hover:bg-muted/50"
                }`}
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Button>
            ))}
          </nav>

          {/* Right Section */}
          <div className="flex items-center gap-3">
            <ShadowSyncBanner />

            {/* Notifications */}
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-4 w-4" />
              <Badge className="absolute -top-1 -right-1 h-5 w-5 text-xs bg-secondary">3</Badge>
            </Button>

            {/* User Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="gap-2 px-2">
                  <Avatar className="h-7 w-7 border border-primary/30">
                    <AvatarImage src="/placeholder.svg?height=32&width=32" />
                    <AvatarFallback className="bg-primary/10 text-primary text-xs">GP</AvatarFallback>
                  </Avatar>
                  <span className="hidden sm:block text-sm">GhostPlayer</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem>
                  <User className="mr-2 h-4 w-4" />
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Sign out</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Menu className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border/40 py-4">
            <nav className="flex flex-col gap-2">
              {navItems.map((item) => (
                <Button
                  key={item.label}
                  variant={item.active ? "default" : "ghost"}
                  size="sm"
                  className={`justify-start gap-2 ${item.active ? "bg-primary/10 text-primary" : ""}`}
                >
                  <item.icon className="h-4 w-4" />
                  {item.label}
                </Button>
              ))}
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
