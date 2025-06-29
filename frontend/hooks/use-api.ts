/**
 * Custom hooks for GhostLAN API integration
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { apiClient, SystemStatus, HealthStatus, MatchData, AnalyticsData, AntiCheatAlert } from '@/lib/api';

// Hook for system status
export function useSystemStatus() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getStatus();
      setStatus(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch system status');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return { status, loading, error, refetch: fetchStatus };
}

// Hook for health status
export function useHealthStatus() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHealth = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getHealth();
      setHealth(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch health status');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, [fetchHealth]);

  return { health, loading, error, refetch: fetchHealth };
}

// Hook for match history
export function useMatchHistory(limit: number = 10) {
  const [matches, setMatches] = useState<MatchData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMatches = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getMatchHistory(limit);
      setMatches(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch match history');
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchMatches();
  }, [fetchMatches]);

  return { matches, loading, error, refetch: fetchMatches };
}

// Hook for analytics data
export function useAnalytics(matchId?: string) {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getAnalytics(matchId);
      setAnalytics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  }, [matchId]);

  useEffect(() => {
    fetchAnalytics();
  }, [fetchAnalytics]);

  return { analytics, loading, error, refetch: fetchAnalytics };
}

// Hook for anti-cheat alerts
export function useAntiCheatAlerts(limit: number = 50) {
  const [alerts, setAlerts] = useState<AntiCheatAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAlerts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiClient.getAntiCheatAlerts(limit);
      setAlerts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch anti-cheat alerts');
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [fetchAlerts]);

  return { alerts, loading, error, refetch: fetchAlerts };
}

// Hook for WebSocket connection and real-time updates
export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);

  const connect = useCallback(async () => {
    if (connected || connecting) return;
    
    try {
      setConnecting(true);
      setError(null);
      await apiClient.connectWebSocket();
      setConnected(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to WebSocket');
      setConnected(false);
    } finally {
      setConnecting(false);
    }
  }, [connected, connecting]);

  const disconnect = useCallback(() => {
    apiClient.disconnectWebSocket();
    setConnected(false);
    setError(null);
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
  }, []);

  const reconnect = useCallback(() => {
    disconnect();
    reconnectTimeoutRef.current = setTimeout(() => {
      connect().catch(console.error);
    }, 5000); // Reconnect after 5 seconds
  }, [connect, disconnect]);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    connected,
    connecting,
    error,
    connect,
    disconnect,
    reconnect,
  };
}

// Hook for real-time match events
export function useMatchEvents() {
  const [events, setEvents] = useState<any[]>([]);
  const { connected } = useWebSocket();

  useEffect(() => {
    if (!connected) return;

    const handleMatchEvent = (event: any) => {
      setEvents(prev => [...prev, event].slice(-100)); // Keep last 100 events
    };

    apiClient.on('match_event', handleMatchEvent);

    return () => {
      apiClient.off('match_event');
    };
  }, [connected]);

  return { events };
}

// Hook for real-time anti-cheat alerts
export function useRealTimeAlerts() {
  const [alerts, setAlerts] = useState<AntiCheatAlert[]>([]);
  const { connected } = useWebSocket();

  useEffect(() => {
    if (!connected) return;

    const handleAlert = (alert: AntiCheatAlert) => {
      setAlerts(prev => [alert, ...prev].slice(-50)); // Keep last 50 alerts
    };

    apiClient.on('anticheat_alert', handleAlert);

    return () => {
      apiClient.off('anticheat_alert');
    };
  }, [connected]);

  return { alerts };
}

// Hook for real-time system status updates
export function useRealTimeStatus() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const { connected } = useWebSocket();

  useEffect(() => {
    if (!connected) return;

    const handleStatusUpdate = (statusUpdate: SystemStatus) => {
      setStatus(statusUpdate);
    };

    apiClient.on('system_status', handleStatusUpdate);

    return () => {
      apiClient.off('system_status');
    };
  }, [connected]);

  return { status };
}

// Hook for match control
export function useMatchControl() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startMatch = useCallback(async (config: any) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.startMatch(config);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start match');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const stopMatch = useCallback(async (matchId: string) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.stopMatch(matchId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stop match');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    startMatch,
    stopMatch,
    loading,
    error,
  };
} 