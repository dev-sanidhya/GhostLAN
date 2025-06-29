"""
AI Agents Module
Defines AI agents with different behaviors and cheat types for simulation
"""

import asyncio
import logging
import random
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class AgentBehavior(Enum):
    NORMAL = "normal"
    CHEAT = "cheat"

class CheatBehavior(Enum):
    AIMBOT = "aimbot"
    WALLHACK = "wallhack"
    SPEEDHACK = "speedhack"
    ESP = "esp"  # Extra Sensory Perception
    MACRO = "macro"

@dataclass
class AgentStats:
    """Statistics for an AI agent"""
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    accuracy: float = 0.0
    headshots: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    movement_distance: float = 0.0
    suspicious_actions: int = 0
    last_action_time: Optional[datetime] = None

@dataclass
class AgentPosition:
    """Position and movement data for an agent"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rotation: float = 0.0
    velocity: float = 0.0
    is_moving: bool = False

class AIAgent:
    """AI Agent with configurable behavior and cheat patterns"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        behavior: AgentBehavior = AgentBehavior.NORMAL,
        cheat_type: Optional[CheatBehavior] = None,
        skill_level: int = 5
    ):
        self.agent_id = agent_id
        self.name = name
        self.behavior = behavior
        self.cheat_type = cheat_type
        self.skill_level = skill_level
        self.is_active = False
        self.stats = AgentStats()
        self.position = AgentPosition()
        self.team = random.choice(["T", "CT"])  # Terrorist or Counter-Terrorist
        self.health = 100
        self.armor = 100
        self.weapon = "AK47"
        self.last_action = None
        self.action_cooldown = 0
        
        # Cheat-specific parameters
        self.cheat_activation_time = None
        self.cheat_detection_probability = 0.1  # Base detection probability
        
        # Behavior patterns
        self.action_patterns = self._generate_action_patterns()
        
    def _generate_action_patterns(self) -> Dict[str, Any]:
        """Generate action patterns based on behavior and skill level"""
        base_patterns = {
            "action_frequency": random.uniform(0.5, 2.0),  # Actions per second
            "accuracy_modifier": random.uniform(0.7, 1.3),
            "reaction_time": random.uniform(0.1, 0.5),  # seconds
            "movement_style": random.choice(["aggressive", "defensive", "balanced"]),
            "target_priority": random.choice(["closest", "weakest", "strongest", "random"])
        }
        
        # Modify patterns based on cheat type
        if self.cheat_type:
            if self.cheat_type == CheatBehavior.AIMBOT:
                base_patterns["accuracy_modifier"] *= 2.0
                base_patterns["reaction_time"] *= 0.3
            elif self.cheat_type == CheatBehavior.SPEEDHACK:
                base_patterns["action_frequency"] *= 1.5
            elif self.cheat_type == CheatBehavior.WALLHACK:
                base_patterns["target_priority"] = "closest"  # Always know where enemies are
        
        return base_patterns
    
    async def initialize(self):
        """Initialize the agent"""
        logger.info(f"Initializing agent {self.name} ({self.agent_id})")
        self.is_active = True
        
        # Set initial position
        self.position.x = random.uniform(-100, 100)
        self.position.y = random.uniform(-100, 100)
        self.position.z = 0
        
        # Activate cheat if applicable
        if self.cheat_type:
            await self._activate_cheat()
    
    async def _activate_cheat(self):
        """Activate cheat behavior"""
        self.cheat_activation_time = datetime.now()
        if self.cheat_type:
            logger.info(f"Agent {self.name} activated {self.cheat_type.value} cheat")
        
        # Modify behavior based on cheat type
        if self.cheat_type == CheatBehavior.AIMBOT:
            self.action_patterns["accuracy_modifier"] *= 2.0
            self.action_patterns["reaction_time"] *= 0.3
        elif self.cheat_type == CheatBehavior.WALLHACK:
            self.action_patterns["target_priority"] = "closest"
        elif self.cheat_type == CheatBehavior.SPEEDHACK:
            self.action_patterns["action_frequency"] *= 1.5
        elif self.cheat_type == CheatBehavior.ESP:
            self.action_patterns["target_priority"] = "weakest"
        elif self.cheat_type == CheatBehavior.MACRO:
            self.action_patterns["action_frequency"] *= 1.2
    
    async def generate_action(self, elapsed: int) -> Optional[Dict[str, Any]]:
        """Generate an action for the agent"""
        if not self.is_active or self.health <= 0:
            return None
        
        # Check action cooldown
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            return None
        
        # Determine action type based on behavior and patterns
        action_type = await self._determine_action_type()
        
        if not action_type:
            return None
        
        # Generate action data
        action_data = await self._generate_action_data(action_type)
        
        # Apply cheat modifications
        if self.cheat_type:
            action_data = await self._apply_cheat_modifications(action_data)
        
        # Update agent state
        await self._update_agent_state(action_type, action_data)
        
        # Set cooldown
        self.action_cooldown = int(1.0 / self.action_patterns["action_frequency"])
        
        return {
            "type": action_type,
            "data": action_data,
            "timestamp": elapsed
        }
    
    async def _determine_action_type(self) -> Optional[str]:
        """Determine what type of action to perform"""
        action_weights = {
            "move": 0.4,
            "shoot": 0.3,
            "reload": 0.1,
            "switch_weapon": 0.05,
            "use_ability": 0.05,
            "communicate": 0.1
        }
        
        # Modify weights based on current state
        if self.health < 30:
            action_weights["move"] *= 1.5  # More defensive when low health
        if self.stats.kills > 10:
            action_weights["shoot"] *= 1.2  # More aggressive when doing well
        
        # Choose action based on weights
        total_weight = sum(action_weights.values())
        rand_val = random.uniform(0, total_weight)
        
        current_weight = 0
        for action, weight in action_weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                return action
        
        return None
    
    async def _generate_action_data(self, action_type: str) -> Dict[str, Any]:
        """Generate data for the specified action type"""
        if action_type == "move":
            return {
                "direction": random.choice(["forward", "backward", "left", "right"]),
                "speed": random.uniform(0.5, 1.0),
                "distance": random.uniform(5, 20),
                "target_position": {
                    "x": self.position.x + random.uniform(-20, 20),
                    "y": self.position.y + random.uniform(-20, 20),
                    "z": self.position.z
                }
            }
        
        elif action_type == "shoot":
            return {
                "target_id": f"TARGET_{random.randint(1, 10)}",
                "weapon": self.weapon,
                "accuracy": min(1.0, random.uniform(0.3, 1.0) * self.action_patterns["accuracy_modifier"]),
                "damage": random.randint(20, 100),
                "headshot": random.random() < 0.2,
                "position": {
                    "x": self.position.x,
                    "y": self.position.y,
                    "z": self.position.z
                }
            }
        
        elif action_type == "reload":
            return {
                "weapon": self.weapon,
                "duration": random.uniform(1.5, 3.0)
            }
        
        elif action_type == "switch_weapon":
            weapons = ["AK47", "M4A1", "AWP", "Desert Eagle", "USP"]
            return {
                "from_weapon": self.weapon,
                "to_weapon": random.choice([w for w in weapons if w != self.weapon]),
                "duration": random.uniform(0.5, 1.5)
            }
        
        elif action_type == "use_ability":
            abilities = ["flash", "smoke", "grenade", "defuse", "plant"]
            return {
                "ability": random.choice(abilities),
                "target_position": {
                    "x": self.position.x + random.uniform(-10, 10),
                    "y": self.position.y + random.uniform(-10, 10),
                    "z": self.position.z
                }
            }
        
        elif action_type == "communicate":
            messages = [
                "Enemy spotted!",
                "Need backup!",
                "Bomb planted!",
                "Clear!",
                "Rush B!",
                "Hold position!"
            ]
            return {
                "message": random.choice(messages),
                "channel": random.choice(["team", "global"]),
                "duration": random.uniform(1, 3)
            }
        
        return {}
    
    async def _apply_cheat_modifications(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply cheat-specific modifications to action data"""
        if not self.cheat_type:
            return action_data
        
        modified_data = action_data.copy()
        
        if self.cheat_type == CheatBehavior.AIMBOT:
            if action_data.get("type") == "shoot":
                modified_data["accuracy"] = min(1.0, modified_data["accuracy"] * 2.0)
                modified_data["headshot"] = random.random() < 0.8  # High headshot rate
        
        elif self.cheat_type == CheatBehavior.WALLHACK:
            if action_data.get("type") == "shoot":
                # Simulate shooting through walls
                modified_data["through_wall"] = random.random() < 0.3
        
        elif self.cheat_type == CheatBehavior.SPEEDHACK:
            if action_data.get("type") == "move":
                modified_data["speed"] *= 1.5
                modified_data["distance"] *= 1.3
        
        elif self.cheat_type == CheatBehavior.ESP:
            if action_data.get("type") == "shoot":
                # Always know enemy positions
                modified_data["target_visible"] = True
                modified_data["target_distance"] = random.uniform(10, 50)
        
        elif self.cheat_type == CheatBehavior.MACRO:
            # Simulate macro usage (repetitive actions)
            if random.random() < 0.1:  # 10% chance of macro pattern
                modified_data["macro_pattern"] = True
                modified_data["repetition_count"] = random.randint(3, 8)
        
        return modified_data
    
    async def _update_agent_state(self, action_type: str, action_data: Dict[str, Any]):
        """Update agent state based on the action performed"""
        self.last_action = {
            "type": action_type,
            "data": action_data,
            "timestamp": datetime.now()
        }
        
        # Update position if moving
        if action_type == "move":
            target_pos = action_data.get("target_position", {})
            self.position.x = target_pos.get("x", self.position.x)
            self.position.y = target_pos.get("y", self.position.y)
            self.position.z = target_pos.get("z", self.position.z)
            self.position.is_moving = True
        
        # Update stats if shooting
        if action_type == "shoot":
            if action_data.get("headshot"):
                self.stats.headshots += 1
            self.stats.damage_dealt += action_data.get("damage", 0)
            
            # Simulate kill
            if random.random() < 0.3:  # 30% chance of kill
                self.stats.kills += 1
        
        # Update last action time
        self.stats.last_action_time = datetime.now()
    
    def take_damage(self, damage: int, attacker_id: Optional[str] = None):
        """Take damage from another agent"""
        self.health = max(0, self.health - damage)
        self.stats.damage_taken += damage
        
        if self.health <= 0:
            self.stats.deaths += 1
            self.is_active = False
            logger.info(f"Agent {self.name} was eliminated by {attacker_id or 'unknown'}")
    
    def get_suspicion_score(self) -> float:
        """Calculate suspicion score based on behavior patterns"""
        score = 0.0
        
        # Base suspicion from cheat type
        if self.cheat_type:
            score += 50.0
        
        # Suspicion from stats
        if self.stats.kills > 20:
            score += 20.0
        if self.stats.accuracy > 0.9:
            score += 15.0
        if self.stats.headshots / max(self.stats.kills, 1) > 0.8:
            score += 10.0
        
        # Suspicion from recent actions
        if self.stats.suspicious_actions > 5:
            score += 25.0
        
        return min(100.0, score)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "team": self.team,
            "behavior": self.behavior.value,
            "cheat_type": self.cheat_type.value if self.cheat_type else None,
            "skill_level": self.skill_level,
            "is_active": self.is_active,
            "health": self.health,
            "armor": self.armor,
            "weapon": self.weapon,
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z
            },
            "stats": {
                "kills": self.stats.kills,
                "deaths": self.stats.deaths,
                "assists": self.stats.assists,
                "accuracy": self.stats.accuracy,
                "headshots": self.stats.headshots,
                "damage_dealt": self.stats.damage_dealt,
                "damage_taken": self.stats.damage_taken,
                "suspicious_actions": self.stats.suspicious_actions
            },
            "suspicion_score": self.get_suspicion_score()
        }
    
    async def shutdown(self):
        """Shutdown the agent"""
        logger.info(f"Shutting down agent {self.name}")
        self.is_active = False 