"""
Anti-Cheat Engine
Multi-layer cheat detection system for GhostLAN
"""

import asyncio
import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import numpy as np
import time

logger = logging.getLogger(__name__)

class CheatType(Enum):
    AIMBOT = "aimbot"
    WALLHACK = "wallhack"
    SPEEDHACK = "speedhack"
    ESP = "esp"  # Extra Sensory Perception
    MACRO = "macro"
    TRIGGERBOT = "triggerbot"
    BUNNYHOP = "bunnyhop"
    AUTOSTRAFE = "autostrafe"
    INJECTION = "injection"
    UNKNOWN = "unknown"

class DetectionSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class DetectionRule:
    """Anti-cheat detection rule"""
    rule_id: str
    name: str
    cheat_type: CheatType
    severity: DetectionSeverity
    threshold: float
    description: str
    enabled: bool = True
    weight: float = 1.0

@dataclass
class CheatDetection:
    """Cheat detection result"""
    detection_id: str
    player_id: str
    player_name: str
    cheat_type: CheatType
    severity: DetectionSeverity
    confidence: float
    timestamp: datetime
    evidence: Dict[str, Any]
    rule_triggered: str
    description: str
    detection_level: DetectionSeverity
    location: Optional[Tuple[float, float, float]] = None
    match_id: Optional[str] = None

@dataclass
class PlayerProfile:
    """Player behavior profile for analysis"""
    player_id: str
    player_name: str
    join_time: datetime
    total_actions: int = 0
    suspicious_actions: int = 0
    detections: List[CheatDetection] = field(default_factory=list)
    behavior_patterns: Dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0

@dataclass
class PlayerStats:
    """Player statistics for analysis"""
    player_id: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    accuracy: float = 0.0
    headshot_ratio: float = 0.0
    reaction_time: float = 0.0
    movement_speed: float = 0.0
    suspicious_actions: int = 0
    last_updated: float = 0.0

class AntiCheatEngine:
    """Multi-layer anti-cheat detection engine"""
    
    def __init__(self, sensitivity: float = 0.8):
        self.sensitivity = max(0.1, min(1.0, sensitivity))
        self.detection_rules: List[DetectionRule] = []
        self.player_profiles: Dict[str, PlayerProfile] = {}
        self.detections: List[CheatDetection] = []
        self.player_stats: Dict[str, PlayerStats] = {}
        self.suspicious_players: Dict[str, float] = {}
        self.is_initialized = False
        self.detection_callbacks: List[Callable] = []
        
        # Detection thresholds
        self.global_thresholds = {
            "aimbot_accuracy_threshold": 0.95,
            "wallhack_detection_threshold": 0.8,
            "speedhack_velocity_threshold": 1.5,
            "macro_pattern_threshold": 0.7,
            "esp_detection_threshold": 0.85
        }
        
        # Initialize detection rules
        self._initialize_detection_rules()
        
        logger.info(f"Anti-Cheat Engine initialized with sensitivity: {self.sensitivity}")
    
    def _initialize_detection_rules(self):
        """Initialize default detection rules"""
        rules = [
            DetectionRule(
                rule_id="AIMBOT_001",
                name="High Accuracy Detection",
                cheat_type=CheatType.AIMBOT,
                severity=DetectionSeverity.HIGH,
                threshold=0.95,
                description="Detects unusually high accuracy over time"
            ),
            DetectionRule(
                rule_id="AIMBOT_002",
                name="Instant Aim Detection",
                cheat_type=CheatType.AIMBOT,
                severity=DetectionSeverity.CRITICAL,
                threshold=0.1,
                description="Detects instant aim adjustments"
            ),
            DetectionRule(
                rule_id="WALLHACK_001",
                name="Wall Penetration Detection",
                cheat_type=CheatType.WALLHACK,
                severity=DetectionSeverity.HIGH,
                threshold=0.8,
                description="Detects shooting through walls"
            ),
            DetectionRule(
                rule_id="WALLHACK_002",
                name="Enemy Tracking Detection",
                cheat_type=CheatType.WALLHACK,
                severity=DetectionSeverity.MEDIUM,
                threshold=0.7,
                description="Detects tracking enemies through walls"
            ),
            DetectionRule(
                rule_id="SPEEDHACK_001",
                name="Movement Speed Detection",
                cheat_type=CheatType.SPEEDHACK,
                severity=DetectionSeverity.HIGH,
                threshold=1.5,
                description="Detects movement speed exceeding limits"
            ),
            DetectionRule(
                rule_id="ESP_001",
                name="Information Leak Detection",
                cheat_type=CheatType.ESP,
                severity=DetectionSeverity.HIGH,
                threshold=0.85,
                description="Detects access to hidden information"
            ),
            DetectionRule(
                rule_id="MACRO_001",
                name="Pattern Repetition Detection",
                cheat_type=CheatType.MACRO,
                severity=DetectionSeverity.MEDIUM,
                threshold=0.7,
                description="Detects repetitive input patterns"
            ),
            DetectionRule(
                rule_id="TRIGGERBOT_001",
                name="Instant Reaction Detection",
                cheat_type=CheatType.TRIGGERBOT,
                severity=DetectionSeverity.HIGH,
                threshold=0.05,
                description="Detects instant reactions to targets"
            )
        ]
        
        self.detection_rules.extend(rules)
        logger.info(f"Initialized {len(rules)} detection rules")
    
    async def initialize(self):
        """Initialize the anti-cheat engine"""
        logger.info("Initializing Anti-Cheat Engine...")
        
        # Start monitoring tasks
        asyncio.create_task(self._monitor_players())
        asyncio.create_task(self._analyze_patterns())
        
        self.is_initialized = True
        logger.info("Anti-Cheat Engine initialized successfully")
    
    async def _monitor_players(self):
        """Monitor player activities for suspicious behavior"""
        while self.is_initialized:
            try:
                # Analyze all player profiles
                for player_id, profile in self.player_profiles.items():
                    await self._analyze_player_behavior(player_id)
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in player monitoring: {e}")
                await asyncio.sleep(5)
    
    async def _analyze_patterns(self):
        """Analyze behavior patterns across all players"""
        while self.is_initialized:
            try:
                # Perform pattern analysis
                await self._detect_global_patterns()
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in pattern analysis: {e}")
                await asyncio.sleep(10)
    
    async def _analyze_player_behavior(self, player_id: str):
        """Analyze behavior of a specific player"""
        profile = self.player_profiles.get(player_id)
        if not profile:
            return
        
        # Calculate risk score
        risk_score = await self._calculate_risk_score(profile)
        profile.risk_score = risk_score
        
        # Check for suspicious patterns
        suspicious_count = 0
        
        # Check action frequency
        if profile.total_actions > 100:
            action_rate = profile.total_actions / (datetime.now() - profile.join_time).total_seconds()
            if action_rate > 10:  # More than 10 actions per second
                suspicious_count += 1
        
        # Check detection history
        recent_detections = [
            d for d in profile.detections
            if d.timestamp > datetime.now() - timedelta(minutes=5)
        ]
        
        if len(recent_detections) > 3:
            suspicious_count += 2
        
        profile.suspicious_actions = suspicious_count
    
    async def _calculate_risk_score(self, profile: PlayerProfile) -> float:
        """Calculate risk score for a player"""
        risk_score = 0.0
        
        # Base risk from detections
        risk_score += len(profile.detections) * 10.0
        
        # Risk from recent detections
        recent_detections = [
            d for d in profile.detections
            if d.timestamp > datetime.now() - timedelta(minutes=10)
        ]
        risk_score += len(recent_detections) * 20.0
        
        # Risk from high severity detections
        high_severity = [
            d for d in profile.detections
            if d.severity in [DetectionSeverity.HIGH, DetectionSeverity.CRITICAL]
        ]
        risk_score += len(high_severity) * 30.0
        
        # Risk from suspicious actions
        risk_score += profile.suspicious_actions * 5.0
        
        return min(100.0, risk_score)
    
    async def _detect_global_patterns(self):
        """Detect patterns across all players"""
        # Analyze aim patterns
        await self._detect_aim_patterns()
        
        # Analyze movement patterns
        await self._detect_movement_patterns()
        
        # Analyze communication patterns
        await self._detect_communication_patterns()
    
    async def _detect_aim_patterns(self):
        """Detect aim-related cheating patterns"""
        for profile in self.player_profiles.values():
            if profile.behavior_patterns.get("aim_accuracy", 0) > self.global_thresholds["aimbot_accuracy_threshold"]:
                await self._create_detection(
                    profile.player_id,
                    profile.player_name,
                    CheatType.AIMBOT,
                    DetectionSeverity.HIGH,
                    0.9,
                    "Unusually high aim accuracy detected",
                    {"accuracy": profile.behavior_patterns["aim_accuracy"]},
                    "AIMBOT_001"
                )
    
    async def _detect_movement_patterns(self):
        """Detect movement-related cheating patterns"""
        for profile in self.player_profiles.values():
            if profile.behavior_patterns.get("movement_speed", 0) > self.global_thresholds["speedhack_velocity_threshold"]:
                await self._create_detection(
                    profile.player_id,
                    profile.player_name,
                    CheatType.SPEEDHACK,
                    DetectionSeverity.HIGH,
                    0.85,
                    "Movement speed exceeds normal limits",
                    {"speed": profile.behavior_patterns["movement_speed"]},
                    "SPEEDHACK_001"
                )
    
    async def _detect_communication_patterns(self):
        """Detect communication-related cheating patterns"""
        # This would analyze voice chat and text communication
        pass
    
    async def process_action(self, player_id: str, player_name: str, action_data: Dict[str, Any]) -> Optional[CheatDetection]:
        """Process a player action for cheat detection"""
        # Ensure player profile exists
        if player_id not in self.player_profiles:
            await self.add_player(player_id, player_name)
        
        profile = self.player_profiles[player_id]
        profile.total_actions += 1
        
        # Analyze the action
        detection = await self._analyze_action(player_id, player_name, action_data)
        
        if detection:
            profile.detections.append(detection)
            self.detections.append(detection)
            
            # Notify callbacks
            for callback in self.detection_callbacks:
                try:
                    await callback(detection)
                except Exception as e:
                    logger.error(f"Error in detection callback: {e}")
        
        return detection
    
    async def _analyze_action(self, player_id: str, player_name: str, action_data: Dict[str, Any]) -> Optional[CheatDetection]:
        """Analyze a specific action for cheating"""
        action_type = action_data.get("type")
        
        if action_type == "shoot":
            return await self._analyze_shoot_action(player_id, player_name, action_data)
        elif action_type == "move":
            return await self._analyze_move_action(player_id, player_name, action_data)
        elif action_type == "communicate":
            return await self._analyze_communication_action(player_id, player_name, action_data)
        
        return None
    
    async def _analyze_shoot_action(self, player_id: str, player_name: str, action_data: Dict[str, Any]) -> Optional[CheatDetection]:
        """Analyze shooting actions for aimbot and triggerbot"""
        accuracy = action_data.get("accuracy", 0.0)
        headshot = action_data.get("headshot", False)
        reaction_time = action_data.get("reaction_time", 1.0)
        
        # Check for aimbot
        if accuracy > self.global_thresholds["aimbot_accuracy_threshold"]:
            return await self._create_detection(
                player_id, player_name, CheatType.AIMBOT, DetectionSeverity.HIGH,
                0.9, "High accuracy shooting detected",
                {"accuracy": accuracy, "headshot": headshot}, "AIMBOT_001"
            )
        
        # Check for triggerbot (instant reaction)
        if reaction_time < 0.1:  # Less than 100ms reaction time
            return await self._create_detection(
                player_id, player_name, CheatType.TRIGGERBOT, DetectionSeverity.HIGH,
                0.85, "Instant reaction detected",
                {"reaction_time": reaction_time}, "TRIGGERBOT_001"
            )
        
        return None
    
    async def _analyze_move_action(self, player_id: str, player_name: str, action_data: Dict[str, Any]) -> Optional[CheatDetection]:
        """Analyze movement actions for speedhack and bunnyhop"""
        speed = action_data.get("speed", 1.0)
        distance = action_data.get("distance", 0.0)
        
        # Check for speedhack
        if speed > self.global_thresholds["speedhack_velocity_threshold"]:
            return await self._create_detection(
                player_id, player_name, CheatType.SPEEDHACK, DetectionSeverity.HIGH,
                0.8, "Movement speed exceeds limits",
                {"speed": speed, "distance": distance}, "SPEEDHACK_001"
            )
        
        return None
    
    async def _analyze_communication_action(self, player_id: str, player_name: str, action_data: Dict[str, Any]) -> Optional[CheatDetection]:
        """Analyze communication actions for information leaks"""
        message = action_data.get("message", "")
        channel = action_data.get("channel", "team")
        
        # Check for information leaks (ESP indicators)
        esp_keywords = ["behind wall", "through wall", "hidden enemy", "invisible"]
        if any(keyword in message.lower() for keyword in esp_keywords):
            return await self._create_detection(
                player_id, player_name, CheatType.ESP, DetectionSeverity.MEDIUM,
                0.7, "Potential ESP information leak",
                {"message": message, "channel": channel}, "ESP_001"
            )
        
        return None
    
    async def _create_detection(
        self,
        player_id: str,
        player_name: str,
        cheat_type: CheatType,
        severity: DetectionSeverity,
        confidence: float,
        description: str,
        evidence: Dict[str, Any],
        rule_id: str
    ) -> CheatDetection:
        """Create a new cheat detection"""
        detection = CheatDetection(
            detection_id=f"DET_{len(self.detections) + 1:06d}",
            player_id=player_id,
            player_name=player_name,
            cheat_type=cheat_type,
            severity=severity,
            confidence=confidence,
            timestamp=datetime.now(),
            evidence=evidence,
            rule_triggered=rule_id,
            description=description,
            detection_level=self._get_detection_level(confidence)
        )
        
        logger.warning(f"Cheat detection: {player_name} - {cheat_type.value} (Confidence: {confidence:.2f})")
        return detection
    
    async def add_player(self, player_id: str, player_name: str):
        """Add a new player to monitoring"""
        if player_id not in self.player_profiles:
            profile = PlayerProfile(
                player_id=player_id,
                player_name=player_name,
                join_time=datetime.now()
            )
            self.player_profiles[player_id] = profile
            logger.info(f"Added player to monitoring: {player_name} ({player_id})")
    
    async def remove_player(self, player_id: str):
        """Remove a player from monitoring"""
        if player_id in self.player_profiles:
            del self.player_profiles[player_id]
            logger.info(f"Removed player from monitoring: {player_id}")
    
    def get_detections(self, player_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get cheat detections"""
        detections = self.detections
        
        if player_id:
            detections = [d for d in detections if d.player_id == player_id]
        
        # Convert to dict format
        return [
            {
                "detection_id": d.detection_id,
                "player_id": d.player_id,
                "player_name": d.player_name,
                "cheat_type": d.cheat_type.value,
                "severity": d.severity.value,
                "confidence": d.confidence,
                "timestamp": d.timestamp.isoformat(),
                "evidence": d.evidence,
                "rule_triggered": d.rule_triggered,
                "description": d.description,
                "detection_level": d.detection_level.value
            }
            for d in detections[-limit:]
        ]
    
    def get_player_profiles(self) -> List[Dict[str, Any]]:
        """Get all player profiles"""
        return [
            {
                "player_id": p.player_id,
                "player_name": p.player_name,
                "join_time": p.join_time.isoformat(),
                "total_actions": p.total_actions,
                "suspicious_actions": p.suspicious_actions,
                "detection_count": len(p.detections),
                "risk_score": p.risk_score,
                "behavior_patterns": p.behavior_patterns
            }
            for p in self.player_profiles.values()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get anti-cheat statistics"""
        total_detections = len(self.detections)
        recent_detections = [
            d for d in self.detections
            if d.timestamp > datetime.now() - timedelta(hours=1)
        ]
        
        detection_by_type = {}
        for detection in self.detections:
            cheat_type = detection.cheat_type.value
            detection_by_type[cheat_type] = detection_by_type.get(cheat_type, 0) + 1
        
        return {
            "total_detections": total_detections,
            "recent_detections": len(recent_detections),
            "active_players": len(self.player_profiles),
            "detection_by_type": detection_by_type,
            "high_risk_players": len([p for p in self.player_profiles.values() if p.risk_score > 50])
        }
    
    def add_detection_callback(self, callback: Callable):
        """Add a callback for new detections"""
        self.detection_callbacks.append(callback)
    
    async def shutdown(self):
        """Shutdown the anti-cheat engine"""
        logger.info("Shutting down Anti-Cheat Engine...")
        self.is_initialized = False
        
        # Clear all data
        self.player_profiles.clear()
        self.detections.clear()
        self.player_stats.clear()
        self.suspicious_players.clear()
        self.detection_callbacks.clear()
        
        logger.info("Anti-Cheat Engine shutdown complete")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the anti-cheat engine"""
        return {
            "is_running": self.is_initialized,
            "sensitivity": self.sensitivity,
            "total_detections": len(self.detections),
            "suspicious_players": len(self.suspicious_players),
            "monitored_players": len(self.player_stats),
            "last_detection": self.detections[-1].timestamp if self.detections else None,
            "uptime": time.time() - getattr(self, '_start_time', time.time())
        }
    
    def _get_detection_level(self, confidence: float) -> DetectionSeverity:
        """Get detection level based on confidence"""
        if confidence >= 0.95:
            return DetectionSeverity.CRITICAL
        elif confidence >= 0.8:
            return DetectionSeverity.HIGH
        elif confidence >= 0.6:
            return DetectionSeverity.MEDIUM
        else:
            return DetectionSeverity.LOW
    
    def _update_player_stats(self, player_id: str, action_type: str, data: Dict[str, Any]):
        """Update player statistics"""
        if player_id not in self.player_stats:
            self.player_stats[player_id] = PlayerStats(player_id=player_id)
        
        stats = self.player_stats[player_id]
        current_time = time.time()
        
        if action_type == "shoot":
            if data.get("hit"):
                stats.kills += 1
                if data.get("headshot"):
                    stats.headshot_ratio = (stats.headshot_ratio * 0.9 + 1.0 * 0.1)
                else:
                    stats.headshot_ratio = stats.headshot_ratio * 0.9
            else:
                stats.deaths += 1
            
            # Update accuracy
            total_shots = stats.kills + stats.deaths
            if total_shots > 0:
                stats.accuracy = stats.kills / total_shots
        
        elif action_type == "reaction":
            reaction_time = data.get("reaction_time", 0.0)
            if reaction_time > 0:
                stats.reaction_time = (stats.reaction_time * 0.9 + reaction_time * 0.1)
        
        elif action_type == "move":
            speed = data.get("speed", 0.0)
            if speed > 0:
                stats.movement_speed = (stats.movement_speed * 0.9 + speed * 0.1)
        
        stats.last_updated = current_time
    
    def _update_suspicious_players(self, player_id: str, confidence: float):
        """Update suspicious players list"""
        if confidence > 0.6:
            self.suspicious_players[player_id] = confidence
        elif player_id in self.suspicious_players:
            del self.suspicious_players[player_id]
    
    def get_player_risk_score(self, player_id: str) -> float:
        """Get risk score for a player (0.0 to 1.0)"""
        if player_id in self.suspicious_players:
            return self.suspicious_players[player_id]
        
        stats = self.player_stats.get(player_id)
        if not stats:
            return 0.0
        
        # Calculate risk based on statistics
        risk_factors = []
        
        if stats.accuracy > 0.9:
            risk_factors.append(0.3)
        if stats.headshot_ratio > 0.7:
            risk_factors.append(0.25)
        if stats.reaction_time < 0.15:
            risk_factors.append(0.2)
        if stats.movement_speed > 1.2:
            risk_factors.append(0.15)
        if stats.suspicious_actions > 5:
            risk_factors.append(0.1)
        
        return min(1.0, sum(risk_factors))
    
    def get_recent_detections(self, minutes: int = 10) -> List[CheatDetection]:
        """Get recent detections within specified minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [d for d in self.detections if d.timestamp > cutoff_time]
    
    def export_detection_report(self, filepath: str) -> bool:
        """Export detection report to JSON file"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "engine_status": self.get_status(),
                "detections": [asdict(d) for d in self.detections],
                "suspicious_players": self.suspicious_players,
                "player_stats": {pid: asdict(stats) for pid, stats in self.player_stats.items()}
            }
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Detection report exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export detection report: {e}")
            return False
    
    def reset(self):
        """Reset the anti-cheat engine"""
        self.detections.clear()
        self.player_stats.clear()
        self.suspicious_players.clear()
        logger.info("Anti-Cheat Engine reset")
    
    def cleanup(self):
        """Clean up resources"""
        # Use synchronous shutdown for cleanup
        logger.info("Shutting down Anti-Cheat Engine...")
        self.is_initialized = False
        
        # Clear all data
        self.player_profiles.clear()
        self.detections.clear()
        self.player_stats.clear()
        self.suspicious_players.clear()
        self.detection_callbacks.clear()
        
        logger.info("Anti-Cheat Engine cleaned up") 