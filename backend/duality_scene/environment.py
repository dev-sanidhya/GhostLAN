"""
LAN Environment Module
Simulates network conditions and LAN environment for testing
"""

import asyncio
import logging
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class NetworkIssueType(Enum):
    PACKET_LOSS = "packet_loss"
    HIGH_LATENCY = "high_latency"
    BANDWIDTH_THROTTLE = "bandwidth_throttle"
    CONNECTION_DROP = "connection_drop"
    JITTER = "jitter"

@dataclass
class NetworkConditions:
    """Network conditions configuration"""
    base_latency: float = 5.0  # ms
    packet_loss_rate: float = 0.001  # 0.1%
    bandwidth_limit: float = 100.0  # Mbps
    jitter: float = 2.0  # ms
    connection_stability: float = 0.99  # 99% stable

@dataclass
class NetworkIssue:
    """Network issue event"""
    issue_type: NetworkIssueType
    severity: str  # low, medium, high, critical
    duration: float  # seconds
    affected_agents: List[str]
    description: str
    timestamp: datetime

class LANEnvironment:
    """Simulates a LAN environment with network conditions and issues"""
    
    def __init__(self):
        self.network_conditions = NetworkConditions()
        self.active_issues: List[NetworkIssue] = []
        self.connected_agents: List[str] = []
        self.network_stats = {
            "total_packets": 0,
            "dropped_packets": 0,
            "average_latency": 0.0,
            "peak_latency": 0.0,
            "bandwidth_usage": 0.0
        }
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the LAN environment"""
        logger.info("Initializing LAN Environment...")
        
        # Set up network monitoring
        asyncio.create_task(self._monitor_network_conditions())
        
        self.is_initialized = True
        logger.info("LAN Environment initialized")
    
    async def _monitor_network_conditions(self):
        """Monitor and update network conditions"""
        while self.is_initialized:
            try:
                # Update network statistics
                await self._update_network_stats()
                
                # Check for new network issues
                await self._check_for_network_issues()
                
                # Clean up expired issues
                await self._cleanup_expired_issues()
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in network monitoring: {e}")
                await asyncio.sleep(5)
    
    async def _update_network_stats(self):
        """Update network statistics"""
        # Simulate packet traffic
        new_packets = random.randint(100, 1000)
        self.network_stats["total_packets"] += new_packets
        
        # Simulate packet loss
        lost_packets = int(new_packets * self.network_conditions.packet_loss_rate)
        self.network_stats["dropped_packets"] += lost_packets
        
        # Update latency
        current_latency = self.network_conditions.base_latency + random.uniform(-2, 2)
        self.network_stats["average_latency"] = (
            (self.network_stats["average_latency"] * 0.9) + (current_latency * 0.1)
        )
        
        if current_latency > self.network_stats["peak_latency"]:
            self.network_stats["peak_latency"] = current_latency
        
        # Update bandwidth usage
        self.network_stats["bandwidth_usage"] = random.uniform(
            self.network_conditions.bandwidth_limit * 0.3,
            self.network_conditions.bandwidth_limit * 0.8
        )
    
    async def _check_for_network_issues(self):
        """Check for new network issues"""
        # Random chance of network issues based on stability
        if random.random() > self.network_conditions.connection_stability:
            await self._generate_network_issue()
    
    async def _generate_network_issue(self):
        """Generate a random network issue"""
        issue_types = list(NetworkIssueType)
        issue_type = random.choice(issue_types)
        
        # Determine severity based on issue type
        severity_weights = {
            "low": 0.4,
            "medium": 0.3,
            "high": 0.2,
            "critical": 0.1
        }
        
        severity = random.choices(
            list(severity_weights.keys()),
            weights=list(severity_weights.values())
        )[0]
        
        # Determine duration based on severity
        duration_ranges = {
            "low": (5, 30),
            "medium": (30, 120),
            "high": (120, 300),
            "critical": (300, 600)
        }
        
        duration = random.uniform(*duration_ranges[severity])
        
        # Select affected agents
        if self.connected_agents:
            max_agents = min(5, len(self.connected_agents))
            num_affected = random.randint(1, max_agents) if max_agents >= 1 else 0
            affected_agents = random.sample(self.connected_agents, num_affected) if num_affected > 0 else []
        else:
            num_affected = 0
            affected_agents = []
        
        # Generate description
        descriptions = {
            NetworkIssueType.PACKET_LOSS: f"Packet loss detected affecting {len(affected_agents)} agents",
            NetworkIssueType.HIGH_LATENCY: f"High latency spike affecting {len(affected_agents)} agents",
            NetworkIssueType.BANDWIDTH_THROTTLE: f"Bandwidth throttling affecting {len(affected_agents)} agents",
            NetworkIssueType.CONNECTION_DROP: f"Connection drop affecting {len(affected_agents)} agents",
            NetworkIssueType.JITTER: f"Network jitter affecting {len(affected_agents)} agents"
        }
        
        issue = NetworkIssue(
            issue_type=issue_type,
            severity=severity,
            duration=duration,
            affected_agents=affected_agents,
            description=descriptions[issue_type],
            timestamp=datetime.now()
        )
        
        self.active_issues.append(issue)
        logger.warning(f"Network issue generated: {issue.description} (Severity: {severity})")
    
    async def _cleanup_expired_issues(self):
        """Remove expired network issues"""
        current_time = datetime.now()
        expired_issues = []
        
        for issue in self.active_issues:
            if current_time - issue.timestamp > timedelta(seconds=issue.duration):
                expired_issues.append(issue)
        
        for issue in expired_issues:
            self.active_issues.remove(issue)
            logger.info(f"Network issue resolved: {issue.description}")
    
    async def get_network_conditions(self) -> Dict[str, Any]:
        """Get current network conditions"""
        current_latency = self.network_conditions.base_latency
        
        # Apply active issues
        for issue in self.active_issues:
            if issue.issue_type == NetworkIssueType.HIGH_LATENCY:
                current_latency *= 3.0
            elif issue.issue_type == NetworkIssueType.JITTER:
                current_latency += random.uniform(5, 15)
        
        return {
            "latency": current_latency,
            "packet_loss": self.network_conditions.packet_loss_rate,
            "bandwidth": self.network_conditions.bandwidth_limit,
            "jitter": self.network_conditions.jitter,
            "stability": self.network_conditions.connection_stability,
            "active_issues": len(self.active_issues)
        }
    
    async def simulate_network_issue(self) -> Dict[str, Any]:
        """Manually trigger a network issue"""
        await self._generate_network_issue()
        
        if self.active_issues:
            latest_issue = self.active_issues[-1]
            return {
                "type": latest_issue.issue_type.value,
                "severity": latest_issue.severity,
                "affected_agents": latest_issue.affected_agents,
                "description": latest_issue.description,
                "duration": latest_issue.duration
            }
        
        return {}
    
    async def connect_agent(self, agent_id: str) -> bool:
        """Connect an agent to the LAN"""
        if agent_id not in self.connected_agents:
            self.connected_agents.append(agent_id)
            logger.info(f"Agent {agent_id} connected to LAN")
            return True
        return False
    
    async def disconnect_agent(self, agent_id: str) -> bool:
        """Disconnect an agent from the LAN"""
        if agent_id in self.connected_agents:
            self.connected_agents.remove(agent_id)
            logger.info(f"Agent {agent_id} disconnected from LAN")
            return True
        return False
    
    async def send_packet(self, from_agent: str, to_agent: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate sending a packet between agents"""
        # Check if agents are connected
        if from_agent not in self.connected_agents or to_agent not in self.connected_agents:
            return {"success": False, "error": "Agent not connected"}
        
        # Check for packet loss
        if random.random() < self.network_conditions.packet_loss_rate:
            return {"success": False, "error": "Packet lost"}
        
        # Calculate latency
        latency = self.network_conditions.base_latency
        
        # Apply network issues
        for issue in self.active_issues:
            if from_agent in issue.affected_agents or to_agent in issue.affected_agents:
                if issue.issue_type == NetworkIssueType.HIGH_LATENCY:
                    latency *= 3.0
                elif issue.issue_type == NetworkIssueType.JITTER:
                    latency += random.uniform(5, 15)
                elif issue.issue_type == NetworkIssueType.CONNECTION_DROP:
                    return {"success": False, "error": "Connection dropped"}
        
        # Simulate transmission delay
        await asyncio.sleep(latency / 1000)  # Convert ms to seconds
        
        return {
            "success": True,
            "latency": latency,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        return {
            "total_packets": self.network_stats["total_packets"],
            "dropped_packets": self.network_stats["dropped_packets"],
            "packet_loss_rate": (
                self.network_stats["dropped_packets"] / 
                max(self.network_stats["total_packets"], 1)
            ),
            "average_latency": self.network_stats["average_latency"],
            "peak_latency": self.network_stats["peak_latency"],
            "bandwidth_usage": self.network_stats["bandwidth_usage"],
            "connected_agents": len(self.connected_agents),
            "active_issues": len(self.active_issues)
        }
    
    def get_active_issues(self) -> List[Dict[str, Any]]:
        """Get list of active network issues"""
        return [
            {
                "type": issue.issue_type.value,
                "severity": issue.severity,
                "duration": issue.duration,
                "affected_agents": issue.affected_agents,
                "description": issue.description,
                "timestamp": issue.timestamp.isoformat(),
                "remaining_time": max(0, issue.duration - (datetime.now() - issue.timestamp).total_seconds())
            }
            for issue in self.active_issues
        ]
    
    async def shutdown(self):
        """Shutdown the LAN environment"""
        logger.info("Shutting down LAN Environment...")
        self.is_initialized = False
        
        # Disconnect all agents
        self.connected_agents.clear()
        
        # Clear active issues
        self.active_issues.clear()
        
        logger.info("LAN Environment shutdown complete") 