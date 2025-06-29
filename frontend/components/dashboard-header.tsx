"use client"

import { useSystemStatus, useHealthStatus, useWebSocket } from "@/hooks/use-api"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { 
  Activity, 
  Wifi, 
  WifiOff, 
  RefreshCw, 
  AlertTriangle,
  CheckCircle,
  XCircle
} from "lucide-react"
import { cn } from "@/lib/utils"

export function DashboardHeader() {
  const { status, loading: statusLoading, error: statusError, refetch: refetchStatus } = useSystemStatus()
  const { health, loading: healthLoading, error: healthError, refetch: refetchHealth } = useHealthStatus()
  const { connected, connecting, error: wsError, reconnect } = useWebSocket()

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational':
      case 'healthy':
        return 'bg-green-500'
      case 'degraded':
        return 'bg-yellow-500'
      case 'error':
      case 'unhealthy':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational':
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'degraded':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'error':
      case 'unhealthy':
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <Activity className="h-4 w-4 text-gray-500" />
    }
  }

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 md:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Activity className="h-6 w-6 text-primary" />
              <h1 className="text-xl font-bold">GhostLAN SimWorld</h1>
            </div>
            
            {/* System Status */}
            <div className="flex items-center space-x-2">
              {statusLoading ? (
                <Badge variant="secondary" className="flex items-center space-x-1">
                  <RefreshCw className="h-3 w-3 animate-spin" />
                  <span>Loading...</span>
                </Badge>
              ) : status ? (
                <Badge 
                  variant="secondary" 
                  className={cn(
                    "flex items-center space-x-1",
                    status.status === 'operational' && "bg-green-100 text-green-800",
                    status.status === 'degraded' && "bg-yellow-100 text-yellow-800",
                    status.status === 'error' && "bg-red-100 text-red-800"
                  )}
                >
                  {getStatusIcon(status.status)}
                  <span className="capitalize">{status.status}</span>
                </Badge>
              ) : (
                <Badge variant="destructive" className="flex items-center space-x-1">
                  <XCircle className="h-3 w-3" />
                  <span>Error</span>
                </Badge>
              )}
            </div>

            {/* Health Status */}
            <div className="flex items-center space-x-2">
              {healthLoading ? (
                <Badge variant="secondary" className="flex items-center space-x-1">
                  <RefreshCw className="h-3 w-3 animate-spin" />
                  <span>Health...</span>
                </Badge>
              ) : health ? (
                <Badge 
                  variant="secondary" 
                  className={cn(
                    "flex items-center space-x-1",
                    health.status === 'healthy' && "bg-green-100 text-green-800",
                    health.status === 'degraded' && "bg-yellow-100 text-yellow-800",
                    health.status === 'unhealthy' && "bg-red-100 text-red-800"
                  )}
                >
                  {getStatusIcon(health.status)}
                  <span className="capitalize">{health.status}</span>
                </Badge>
              ) : (
                <Badge variant="destructive" className="flex items-center space-x-1">
                  <XCircle className="h-3 w-3" />
                  <span>Health Error</span>
                </Badge>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* WebSocket Status */}
            <div className="flex items-center space-x-2">
              {connecting ? (
                <Badge variant="secondary" className="flex items-center space-x-1">
                  <RefreshCw className="h-3 w-3 animate-spin" />
                  <span>Connecting...</span>
                </Badge>
              ) : connected ? (
                <Badge variant="secondary" className="flex items-center space-x-1 bg-green-100 text-green-800">
                  <Wifi className="h-3 w-3" />
                  <span>Connected</span>
                </Badge>
              ) : (
                <Badge variant="destructive" className="flex items-center space-x-1">
                  <WifiOff className="h-3 w-3" />
                  <span>Disconnected</span>
                </Badge>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  refetchStatus()
                  refetchHealth()
                }}
                disabled={statusLoading || healthLoading}
              >
                <RefreshCw className={cn("h-4 w-4", (statusLoading || healthLoading) && "animate-spin")} />
                <span className="ml-2">Refresh</span>
              </Button>

              {!connected && !connecting && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={reconnect}
                >
                  <Wifi className="h-4 w-4" />
                  <span className="ml-2">Reconnect</span>
                </Button>
              )}
            </div>
          </div>
        </div>

        {/* Error Messages */}
        {(statusError || healthError || wsError) && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center space-x-2 text-red-800">
              <AlertTriangle className="h-4 w-4" />
              <span className="text-sm font-medium">Connection Issues:</span>
            </div>
            <div className="mt-1 text-sm text-red-700 space-y-1">
              {statusError && <div>• System Status: {statusError}</div>}
              {healthError && <div>• Health Check: {healthError}</div>}
              {wsError && <div>• WebSocket: {wsError}</div>}
            </div>
          </div>
        )}

        {/* System Details */}
        {status && (
          <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Duality AI</span>
                  <Badge 
                    variant="outline" 
                    className={cn(
                      status.services.duality_simulation.initialized 
                        ? "border-green-500 text-green-700" 
                        : "border-red-500 text-red-700"
                    )}
                  >
                    {status.services.duality_simulation.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Anti-Cheat</span>
                  <Badge 
                    variant="outline" 
                    className={cn(
                      status.services.anticheat_engine.initialized 
                        ? "border-green-500 text-green-700" 
                        : "border-red-500 text-red-700"
                    )}
                  >
                    {status.services.anticheat_engine.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Analytics</span>
                  <Badge 
                    variant="outline" 
                    className={cn(
                      status.services.analytics_pipeline.initialized 
                        ? "border-green-500 text-green-700" 
                        : "border-red-500 text-red-700"
                    )}
                  >
                    {status.services.analytics_pipeline.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Match Recorder</span>
                  <Badge 
                    variant="outline" 
                    className={cn(
                      status.services.match_recorder.initialized 
                        ? "border-green-500 text-green-700" 
                        : "border-red-500 text-red-700"
                    )}
                  >
                    {status.services.match_recorder.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </header>
  )
}
