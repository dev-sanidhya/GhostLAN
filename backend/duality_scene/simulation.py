"""
Duality AI Simulation Manager
Manages the digital twin LAN environment with AI agents
"""

import asyncio
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .agents import AIAgent, AgentBehavior, CheatBehavior
from .environment import LANEnvironment, NetworkConditions
from .voice_simulation import VoiceSimulation

logger = logging.getLogger(__name__)

class SimulationState(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

@dataclass
class SimulationConfig:
    """Configuration for the simulation"""
    num_agents: int = 10  # 5v5 setup
    match_duration: int = 420  # 7 minutes in seconds
    network_conditions: Optional[NetworkConditions] = None
    cheat_probability: float = 0.3  # 30% chance of cheat behavior
    voice_enabled: bool = True
    recording_enabled: bool = True

class SimulationManager:
    """Manages the Duality AI simulation environment"""
    
    def __init__(self):
        self.state = SimulationState.IDLE
        self.config = SimulationConfig()
        self.agents: List[AIAgent] = []
        self.environment: Optional[LANEnvironment] = None
        self.voice_simulation: Optional[VoiceSimulation] = None
        self.current_match_id: Optional[str] = None
        self.match_start_time: Optional[datetime] = None
        self.events: List[Dict[str, Any]] = []
        self.callbacks = []
        
    async def initialize(self):
        """Initialize the simulation environment"""
        logger.info("Initializing Duality AI Simulation...")
        self.state = SimulationState.INITIALIZING
        
        try:
            # Initialize LAN environment
            self.environment = LANEnvironment()
            if self.environment is not None:
                await self.environment.initialize()
            
            # Initialize voice simulation
            if self.config.voice_enabled:
                self.voice_simulation = VoiceSimulation()
                if self.voice_simulation is not None:
                    await self.voice_simulation.initialize()
            
            # Create AI agents
            await self._create_agents()
            
            self.state = SimulationState.IDLE
            logger.info("Duality AI Simulation initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize simulation: {e}")
            self.state = SimulationState.STOPPED
            raise
    
    async def _create_agents(self):
        """Create AI agents with mixed behaviors"""
        logger.info(f"Creating {self.config.num_agents} AI agents...")
        
        agent_names = [
            "ShadowByte", "NeonSniper", "QuantumFrag", "CyberNinja", "VirtualPhantom",
            "DataMiner", "CodeBreaker", "PixelWarrior", "GhostHunter", "NetRunner"
        ]
        
        for i in range(self.config.num_agents):
            # Determine if agent should have cheat behavior
            has_cheat = random.random() < self.config.cheat_probability
            
            if has_cheat:
                cheat_type = random.choice([
                    CheatBehavior.AIMBOT,
                    CheatBehavior.WALLHACK,
                    CheatBehavior.SPEEDHACK,
                    CheatBehavior.ESP,
                    CheatBehavior.MACRO
                ])
                behavior = AgentBehavior.CHEAT
            else:
                cheat_type = None
                behavior = AgentBehavior.NORMAL
            
            agent = AIAgent(
                agent_id=f"AGENT_{i+1:04d}",
                name=agent_names[i % len(agent_names)],
                behavior=behavior,
                cheat_type=cheat_type,
                skill_level=random.randint(1, 10)
            )
            
            self.agents.append(agent)
        
        logger.info(f"Created {len(self.agents)} agents ({sum(1 for a in self.agents if a.behavior == AgentBehavior.CHEAT)} with cheat behavior)")
    
    async def start_match(self, match_id: Optional[str] = None) -> str:
        """Start a new match simulation"""
        if self.state != SimulationState.IDLE:
            raise RuntimeError("Simulation must be in IDLE state to start match")
        
        self.current_match_id = match_id or f"MATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.match_start_time = datetime.now()
        self.events = []
        
        logger.info(f"Starting match: {self.current_match_id}")
        self.state = SimulationState.RUNNING
        
        # Start the match simulation
        asyncio.create_task(self._run_match())
        
        return self.current_match_id
    
    async def _run_match(self):
        """Run the match simulation"""
        try:
            match_duration = self.config.match_duration
            start_time = datetime.now()
            
            logger.info(f"Match {self.current_match_id} started, duration: {match_duration}s")
            
            # Initialize all agents
            for agent in self.agents:
                await agent.initialize()
                await self._record_event("agent_joined", {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "behavior": agent.behavior.value,
                    "cheat_type": agent.cheat_type.value if agent.cheat_type else None
                })
            
            # Main match loop
            elapsed = 0
            while elapsed < match_duration and self.state == SimulationState.RUNNING:
                await asyncio.sleep(1)  # 1-second tick
                elapsed += 1
                
                # Simulate agent actions
                await self._simulate_agent_actions(elapsed)
                
                # Simulate network conditions
                await self._simulate_network_conditions(elapsed)
                
                # Simulate voice chat
                if self.voice_simulation:
                    await self._simulate_voice_chat(elapsed)
                
                # Record periodic events
                if elapsed % 30 == 0:  # Every 30 seconds
                    await self._record_periodic_events(elapsed)
            
            # End match
            await self._end_match()
            
        except Exception as e:
            logger.error(f"Error during match simulation: {e}")
            self.state = SimulationState.STOPPED
    
    async def _simulate_agent_actions(self, elapsed: int):
        """Simulate agent actions during the match"""
        for agent in self.agents:
            # Generate random actions based on agent behavior
            action = await agent.generate_action(elapsed)
            
            if action:
                await self._record_event("agent_action", {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "action_type": action["type"],
                    "timestamp": elapsed,
                    "data": action["data"]
                })
    
    async def _simulate_network_conditions(self, elapsed: int):
        """Simulate network conditions and events"""
        if self.environment:
            conditions = await self.environment.get_network_conditions()
            
            # Simulate network issues
            if random.random() < 0.05:  # 5% chance of network issue
                issue = await self.environment.simulate_network_issue()
                await self._record_event("network_issue", {
                    "timestamp": elapsed,
                    "issue_type": issue["type"],
                    "severity": issue["severity"],
                    "affected_agents": issue["affected_agents"]
                })
    
    async def _simulate_voice_chat(self, elapsed: int):
        """Simulate voice chat activity"""
        if self.voice_simulation and random.random() < 0.1:  # 10% chance of voice activity
            voice_event = await self.voice_simulation.simulate_voice_activity()
            await self._record_event("voice_activity", {
                "timestamp": elapsed,
                "speaker_id": voice_event["speaker_id"],
                "activity_type": voice_event["type"],
                "duration": voice_event["duration"]
            })
    
    async def _record_periodic_events(self, elapsed: int):
        """Record periodic match events"""
        # Record match statistics
        stats = await self._calculate_match_stats()
        await self._record_event("match_stats", {
            "timestamp": elapsed,
            "stats": stats
        })
    
    async def _calculate_match_stats(self) -> Dict[str, Any]:
        """Calculate current match statistics"""
        return {
            "total_kills": sum(agent.stats.kills for agent in self.agents),
            "total_deaths": sum(agent.stats.deaths for agent in self.agents),
            "active_players": len([a for a in self.agents if a.is_active]),
            "suspicious_events": len([e for e in self.events if e.get("type") == "suspicious_behavior"])
        }
    
    async def _record_event(self, event_type: str, data: Dict[str, Any]):
        """Record an event in the simulation"""
        event = {
            "id": len(self.events) + 1,
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "match_id": self.current_match_id,
            "data": data
        }
        
        self.events.append(event)
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                await callback(event)
            except Exception as e:
                logger.error(f"Error in event callback: {e}")
    
    async def _end_match(self):
        """End the current match"""
        logger.info(f"Ending match: {self.current_match_id}")
        
        # Record final statistics
        final_stats = await self._calculate_match_stats()
        await self._record_event("match_end", {
            "match_id": self.current_match_id,
            "duration": self.config.match_duration,
            "final_stats": final_stats,
            "total_events": len(self.events)
        })
        
        self.state = SimulationState.IDLE
        logger.info(f"Match {self.current_match_id} completed")
    
    async def pause_match(self):
        """Pause the current match"""
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
            logger.info("Match paused")
    
    async def resume_match(self):
        """Resume the current match"""
        if self.state == SimulationState.PAUSED:
            self.state = SimulationState.RUNNING
            logger.info("Match resumed")
    
    async def stop_match(self):
        """Stop the current match"""
        if self.state in [SimulationState.RUNNING, SimulationState.PAUSED]:
            self.state = SimulationState.STOPPED
            await self._end_match()
            logger.info("Match stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current simulation status"""
        return {
            "state": self.state.value,
            "current_match_id": self.current_match_id,
            "match_start_time": self.match_start_time.isoformat() if self.match_start_time else None,
            "num_agents": len(self.agents),
            "total_events": len(self.events),
            "config": {
                "num_agents": self.config.num_agents,
                "match_duration": self.config.match_duration,
                "cheat_probability": self.config.cheat_probability,
                "voice_enabled": self.config.voice_enabled
            }
        }
    
    def get_events(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get simulation events"""
        events = self.events
        
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        
        return events[-limit:] if limit else events
    
    def add_event_callback(self, callback):
        """Add an event callback function"""
        self.callbacks.append(callback)
    
    async def shutdown(self):
        """Shutdown the simulation"""
        logger.info("Shutting down Duality AI Simulation...")
        
        if self.state in [SimulationState.RUNNING, SimulationState.PAUSED]:
            await self.stop_match()
        
        if self.environment:
            await self.environment.shutdown()
        
        if self.voice_simulation:
            await self.voice_simulation.shutdown()
        
        for agent in self.agents:
            await agent.shutdown()
        
        self.state = SimulationState.STOPPED
        logger.info("Duality AI Simulation shutdown complete") 