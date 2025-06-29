/**
 * GhostLAN API Client
 * Handles all communication with the backend API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

export interface SystemStatus {
  status: 'operational' | 'degraded' | 'error';
  timestamp: string;
  version: string;
  services: {
    duality_simulation: { status: string; initialized: boolean };
    anticheat_engine: { status: string; initialized: boolean };
    analytics_pipeline: { status: string; initialized: boolean };
    match_recorder: { status: string; initialized: boolean };
  };
  websocket_connections: number;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  systems: {
    duality_simulation: boolean;
    anticheat_engine: boolean;
    analytics_pipeline: boolean;
    match_recorder: boolean;
  };
  version: string;
}

export interface MatchData {
  id: string;
  timestamp: string;
  players: string[];
  duration: number;
  map: string;
  result: 'win' | 'loss' | 'draw';
  events: MatchEvent[];
}

export interface MatchEvent {
  id: string;
  timestamp: string;
  type: 'kill' | 'death' | 'assist' | 'objective' | 'chat';
  player: string;
  target?: string;
  location?: [number, number];
  data?: any;
}

export interface AnalyticsData {
  player_performance: any;
  team_dynamics: any;
  anomalies: any[];
  heatmap_data: any;
}

export interface AntiCheatAlert {
  id: string;
  timestamp: string;
  player: string;
  type: 'suspicious_behavior' | 'cheat_detected' | 'anomaly';
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  evidence: any;
}

class ApiClient {
  private ws: WebSocket | null = null;
  private wsListeners: Map<string, (data: any) => void> = new Map();

  // HTTP API Methods
  async getHealth(): Promise<HealthStatus> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  async getStatus(): Promise<SystemStatus> {
    const response = await fetch(`${API_BASE_URL}/api/v1/status`);
    if (!response.ok) {
      throw new Error(`Status check failed: ${response.statusText}`);
    }
    return response.json();
  }

  async getMatchHistory(limit: number = 10): Promise<MatchData[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/export/matches?limit=${limit}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch match history: ${response.statusText}`);
    }
    return response.json();
  }

  async getAnalytics(matchId?: string): Promise<AnalyticsData> {
    const url = matchId 
      ? `${API_BASE_URL}/api/v1/export/analytics/${matchId}`
      : `${API_BASE_URL}/api/v1/export/analytics`;
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch analytics: ${response.statusText}`);
    }
    return response.json();
  }

  async getAntiCheatAlerts(limit: number = 50): Promise<AntiCheatAlert[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/export/anticheat?limit=${limit}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch anti-cheat alerts: ${response.statusText}`);
    }
    return response.json();
  }

  async startMatch(config: any): Promise<{ match_id: string }> {
    const response = await fetch(`${API_BASE_URL}/api/v1/match/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ config }),
    });
    if (!response.ok) {
      throw new Error(`Failed to start match: ${response.statusText}`);
    }
    return response.json();
  }

  async stopMatch(matchId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/match/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ match_id: matchId }),
    });
    if (!response.ok) {
      throw new Error(`Failed to stop match: ${response.statusText}`);
    }
  }

  // WebSocket Methods
  connectWebSocket(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(`${WS_URL}/ws`);
        
        this.ws.onopen = () => {
          console.log('WebSocket connected to GhostLAN backend');
          resolve();
        };
        
        this.ws.onmessage = (event) => {
          console.log('WebSocket message:', event.data);
          try {
            if (event.data === "ping") return;
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
          } catch (error) {
            if (event.data !== "ping") {
              console.error('Failed to parse WebSocket message:', error, event.data);
            }
          }
        };
        
        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
        
        this.ws.onclose = (event) => {
          console.log('WebSocket disconnected from GhostLAN backend', event);
          this.ws = null;
        };
        
      } catch (error) {
        reject(error);
      }
    });
  }

  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private handleWebSocketMessage(data: any): void {
    const { type, payload } = data;
    
    // Handle different message types
    switch (type) {
      case 'match_event':
        this.notifyListeners('match_event', payload);
        break;
      case 'anticheat_alert':
        this.notifyListeners('anticheat_alert', payload);
        break;
      case 'system_status':
        this.notifyListeners('system_status', payload);
        break;
      case 'analytics_update':
        this.notifyListeners('analytics_update', payload);
        break;
      default:
        console.log('Unknown WebSocket message type:', type);
    }
  }

  // Event listeners for WebSocket messages
  on(event: string, callback: (data: any) => void): void {
    this.wsListeners.set(event, callback);
  }

  off(event: string): void {
    this.wsListeners.delete(event);
  }

  private notifyListeners(event: string, data: any): void {
    const callback = this.wsListeners.get(event);
    if (callback) {
      callback(data);
    }
  }

  // Utility methods
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  sendMessage(message: any): void {
    if (this.isConnected() && this.ws) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected');
    }
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Export types for use in components
export type { ApiClient }; 