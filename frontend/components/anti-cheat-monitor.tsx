"use client"

import { useAntiCheatAlerts, useRealTimeAlerts } from "@/hooks/use-api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
  Shield, 
  AlertTriangle, 
  Eye, 
  RefreshCw,
  Clock,
  User,
  Zap
} from "lucide-react"
import { cn } from "@/lib/utils"

export function AntiCheatMonitor() {
  const { alerts, loading, error, refetch } = useAntiCheatAlerts(20)
  const { alerts: realTimeAlerts } = useRealTimeAlerts()

  // Combine static and real-time alerts
  const allAlerts = [...realTimeAlerts, ...alerts].slice(0, 20)

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-600 text-white font-semibold'
      case 'high':
        return 'bg-orange-600 text-white font-semibold'
      case 'medium':
        return 'bg-yellow-600 text-white font-semibold'
      case 'low':
        return 'bg-blue-600 text-white font-semibold'
      default:
        return 'bg-gray-600 text-white font-semibold'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'cheat_detected':
        return <Shield className="h-4 w-4 text-red-400" />
      case 'suspicious_behavior':
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
      case 'anomaly':
        return <Zap className="h-4 w-4 text-blue-400" />
      default:
        return <Eye className="h-4 w-4 text-gray-400" />
    }
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    return date.toLocaleDateString()
  }

  return (
    <Card className="h-full flex flex-col" style={{ height: 'calc(100vh - 200px)' }}>
      <CardHeader className="pb-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Shield className="h-5 w-5 text-primary" />
            <CardTitle className="text-lg text-foreground">Anti-Cheat Monitor</CardTitle>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={refetch}
            disabled={loading}
          >
            <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
            <span className="ml-2">Refresh</span>
          </Button>
        </div>
        <CardDescription className="text-foreground/80">
          Real-time monitoring of suspicious activities and cheat detection
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col min-h-0 p-6" style={{ height: 'calc(100% - 120px)' }}>
        {/* Status Summary */}
        <div className="grid grid-cols-3 gap-4 mb-4 flex-shrink-0">
          <div className="text-center">
            <div className="text-2xl font-bold text-red-400">
              {allAlerts.filter(a => a.severity === 'critical').length}
            </div>
            <div className="text-xs text-foreground/70 font-medium">Critical</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-400">
              {allAlerts.filter(a => a.severity === 'high').length}
            </div>
            <div className="text-xs text-foreground/70 font-medium">High</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">
              {allAlerts.filter(a => a.severity === 'medium').length}
            </div>
            <div className="text-xs text-foreground/70 font-medium">Medium</div>
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="p-3 bg-red-950/50 border border-red-500/30 rounded-md mb-4 flex-shrink-0">
            <div className="flex items-center space-x-2 text-red-300">
              <AlertTriangle className="h-4 w-4" />
              <span className="text-sm font-medium">Failed to load alerts: {error}</span>
            </div>
          </div>
        )}

        {/* Alerts List */}
        <ScrollArea className="flex-1 min-h-0" style={{ height: 'calc(100% - 200px)' }}>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin text-primary" />
              <span className="ml-2 text-foreground/80 font-medium">Loading alerts...</span>
            </div>
          ) : allAlerts.length === 0 ? (
            <div className="text-center py-8 text-foreground/70">
              <Shield className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-medium">No alerts detected</p>
              <p className="text-sm">System is running clean</p>
            </div>
          ) : (
            <div className="space-y-3">
              {allAlerts.map((alert, index) => (
                <div
                  key={`${alert.id}-${index}`}
                  className={cn(
                    "p-3 rounded-lg border transition-colors",
                    alert.severity === 'critical' && "bg-red-950/30 border-red-500/40",
                    alert.severity === 'high' && "bg-orange-950/30 border-orange-500/40",
                    alert.severity === 'medium' && "bg-yellow-950/30 border-yellow-500/40",
                    alert.severity === 'low' && "bg-blue-950/30 border-blue-500/40",
                    "hover:bg-muted/30"
                  )}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      <div className="flex-shrink-0 mt-1">
                        {getTypeIcon(alert.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-semibold text-sm truncate text-foreground">
                            {alert.player}
                          </span>
                          <Badge 
                            className={cn("text-xs font-medium", getSeverityColor(alert.severity))}
                          >
                            {alert.severity}
                          </Badge>
                        </div>
                        <p className="text-sm text-foreground/90 mb-2 leading-relaxed">
                          {alert.description}
                        </p>
                        <div className="flex items-center space-x-4 text-xs text-foreground/70">
                          <div className="flex items-center space-x-1">
                            <Clock className="h-3 w-3" />
                            <span className="font-medium">{formatTimestamp(alert.timestamp)}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <User className="h-3 w-3" />
                            <span className="font-medium">{alert.type.replace('_', ' ')}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="flex-shrink-0 text-foreground/70 hover:text-foreground"
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Footer Stats */}
        <div className="flex items-center justify-between text-xs text-foreground/70 pt-2 border-t border-border/50 mt-4 flex-shrink-0">
          <span className="font-medium">Total Alerts: {allAlerts.length}</span>
          <span className="font-medium">Real-time: {realTimeAlerts.length}</span>
        </div>
      </CardContent>
    </Card>
  )
}
