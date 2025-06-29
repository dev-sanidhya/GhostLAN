"use client"

import { useState, useEffect } from "react"
import { useSystemStatus, useHealthStatus, useWebSocket } from "@/hooks/use-api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { 
  CheckCircle, 
  XCircle, 
  RefreshCw, 
  Wifi, 
  WifiOff,
  Activity
} from "lucide-react"
import { cn } from "@/lib/utils"

export function ConnectionTest() {
  const { status, loading: statusLoading, error: statusError, refetch: refetchStatus } = useSystemStatus()
  const { health, loading: healthLoading, error: healthError, refetch: refetchHealth } = useHealthStatus()
  const { connected, connecting, error: wsError, reconnect } = useWebSocket()
  const [testResults, setTestResults] = useState<{
    health: boolean
    status: boolean
    websocket: boolean
  }>({
    health: false,
    status: false,
    websocket: false
  })

  useEffect(() => {
    setTestResults({
      health: !healthError && health !== null,
      status: !statusError && status !== null,
      websocket: connected
    })
  }, [health, status, connected, healthError, statusError])

  const runAllTests = () => {
    refetchStatus()
    refetchHealth()
    if (!connected && !connecting) {
      reconnect()
    }
  }

  const allTestsPassed = testResults.health && testResults.status && testResults.websocket
  const anyTestFailed = !testResults.health || !testResults.status || !testResults.websocket

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="h-5 w-5 text-primary" />
            <CardTitle>Backend Connection Test</CardTitle>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={runAllTests}
            disabled={statusLoading || healthLoading || connecting}
          >
            <RefreshCw className={cn("h-4 w-4", (statusLoading || healthLoading || connecting) && "animate-spin")} />
            <span className="ml-2">Run Tests</span>
          </Button>
        </div>
        <CardDescription>
          Test the connection between frontend and GhostLAN backend
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Overall Status */}
        <div className="flex items-center justify-center p-4 rounded-lg border-2 border-dashed">
          {allTestsPassed ? (
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="h-6 w-6" />
              <span className="text-lg font-semibold">All Tests Passed!</span>
            </div>
          ) : anyTestFailed ? (
            <div className="flex items-center space-x-2 text-red-600">
              <XCircle className="h-6 w-6" />
              <span className="text-lg font-semibold">Some Tests Failed</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2 text-gray-600">
              <RefreshCw className="h-6 w-6 animate-spin" />
              <span className="text-lg font-semibold">Running Tests...</span>
            </div>
          )}
        </div>

        {/* Individual Test Results */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Health Check Test */}
          <div className="p-4 rounded-lg border">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium">Health Check</span>
              {healthLoading ? (
                <RefreshCw className="h-4 w-4 animate-spin text-blue-500" />
              ) : testResults.health ? (
                <CheckCircle className="h-4 w-4 text-green-500" />
              ) : (
                <XCircle className="h-4 w-4 text-red-500" />
              )}
            </div>
            <div className="text-sm text-muted-foreground">
              {healthLoading ? "Testing..." : 
               healthError ? `Error: ${healthError}` :
               health ? `Status: ${health.status}` : "No data"}
            </div>
          </div>

          {/* API Status Test */}
          <div className="p-4 rounded-lg border">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium">API Status</span>
              {statusLoading ? (
                <RefreshCw className="h-4 w-4 animate-spin text-blue-500" />
              ) : testResults.status ? (
                <CheckCircle className="h-4 w-4 text-green-500" />
              ) : (
                <XCircle className="h-4 w-4 text-red-500" />
              )}
            </div>
            <div className="text-sm text-muted-foreground">
              {statusLoading ? "Testing..." : 
               statusError ? `Error: ${statusError}` :
               status ? `Status: ${status.status}` : "No data"}
            </div>
          </div>

          {/* WebSocket Test */}
          <div className="p-4 rounded-lg border">
            <div className="flex items-center justify-between mb-2">
              <span className="font-medium">WebSocket</span>
              {connecting ? (
                <RefreshCw className="h-4 w-4 animate-spin text-blue-500" />
              ) : testResults.websocket ? (
                <Wifi className="h-4 w-4 text-green-500" />
              ) : (
                <WifiOff className="h-4 w-4 text-red-500" />
              )}
            </div>
            <div className="text-sm text-muted-foreground">
              {connecting ? "Connecting..." : 
               wsError ? `Error: ${wsError}` :
               connected ? "Connected" : "Disconnected"}
            </div>
          </div>
        </div>

        {/* Error Details */}
        {(healthError || statusError || wsError) && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="text-sm font-medium text-red-800 mb-2">Connection Issues:</div>
            <div className="space-y-1 text-sm text-red-700">
              {healthError && <div>• Health Check: {healthError}</div>}
              {statusError && <div>• API Status: {statusError}</div>}
              {wsError && <div>• WebSocket: {wsError}</div>}
            </div>
          </div>
        )}

        {/* Success Details */}
        {allTestsPassed && (
          <div className="p-3 bg-green-50 border border-green-200 rounded-md">
            <div className="text-sm font-medium text-green-800 mb-2">Connection Successful!</div>
            <div className="space-y-1 text-sm text-green-700">
              <div>• Backend API is responding correctly</div>
              <div>• All services are operational</div>
              <div>• Real-time WebSocket connection established</div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
} 