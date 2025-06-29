"""
Voice Simulation Module
Simulates voice chat activity for anti-cheat testing
"""

import asyncio
import logging
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)

class VoiceActivityType(Enum):
    SPEECH = "speech"
    BACKGROUND_NOISE = "background_noise"
    ECHO = "echo"
    FEEDBACK = "feedback"
    SILENCE = "silence"

class VoiceQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    POOR = "poor"
    BAD = "bad"

@dataclass
class VoiceEvent:
    """Voice chat event"""
    speaker_id: str
    activity_type: VoiceActivityType
    duration: float  # seconds
    quality: VoiceQuality
    volume: float  # 0.0 to 1.0
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class VoiceSimulation:
    """Simulates voice chat activity and quality"""
    
    def __init__(self):
        self.active_speakers: Dict[str, Dict[str, Any]] = {}
        self.voice_events: List[VoiceEvent] = []
        self.voice_quality = VoiceQuality.GOOD
        self.is_initialized = False
        
        # Voice chat parameters
        self.max_simultaneous_speakers = 3
        self.average_speech_duration = 2.0  # seconds
        self.speech_probability = 0.1  # 10% chance per second
        self.background_noise_level = 0.1
        
    async def initialize(self):
        """Initialize the voice simulation"""
        logger.info("Initializing Voice Simulation...")
        
        # Start voice monitoring
        asyncio.create_task(self._monitor_voice_activity())
        
        self.is_initialized = True
        logger.info("Voice Simulation initialized")
    
    async def _monitor_voice_activity(self):
        """Monitor and generate voice activity"""
        while self.is_initialized:
            try:
                # Generate random voice events
                await self._generate_voice_events()
                
                # Update voice quality
                await self._update_voice_quality()
                
                # Clean up old events
                await self._cleanup_old_events()
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in voice monitoring: {e}")
                await asyncio.sleep(5)
    
    async def _generate_voice_events(self):
        """Generate random voice events"""
        # Check for new speech events
        for speaker_id in list(self.active_speakers.keys()):
            if random.random() < self.speech_probability:
                await self._generate_speech_event(speaker_id)
        
        # Generate background noise
        if random.random() < 0.05:  # 5% chance of background noise
            await self._generate_background_noise()
        
        # Generate voice issues
        if random.random() < 0.02:  # 2% chance of voice issues
            await self._generate_voice_issue()
    
    async def _generate_speech_event(self, speaker_id: str):
        """Generate a speech event for a speaker"""
        duration = random.uniform(0.5, self.average_speech_duration * 2)
        
        # Determine voice quality
        quality = self._determine_voice_quality()
        
        # Determine volume
        volume = random.uniform(0.3, 1.0)
        
        # Generate speech content
        speech_content = self._generate_speech_content()
        
        event = VoiceEvent(
            speaker_id=speaker_id,
            activity_type=VoiceActivityType.SPEECH,
            duration=duration,
            quality=quality,
            volume=volume,
            timestamp=datetime.now(),
            metadata={
                "content": speech_content,
                "language": "en",
                "emotion": random.choice(["neutral", "excited", "frustrated", "calm"]),
                "clarity": random.uniform(0.7, 1.0)
            }
        )
        
        self.voice_events.append(event)
        logger.debug(f"Speech event generated for {speaker_id}: {speech_content[:50]}...")
    
    async def _generate_background_noise(self):
        """Generate background noise event"""
        duration = random.uniform(1, 5)
        
        event = VoiceEvent(
            speaker_id="BACKGROUND",
            activity_type=VoiceActivityType.BACKGROUND_NOISE,
            duration=duration,
            quality=VoiceQuality.POOR,
            volume=random.uniform(0.1, 0.3),
            timestamp=datetime.now(),
            metadata={
                "noise_type": random.choice(["keyboard", "mouse_clicks", "ambient", "music"]),
                "intensity": random.uniform(0.1, 0.5)
            }
        )
        
        self.voice_events.append(event)
        logger.debug("Background noise event generated")
    
    async def _generate_voice_issue(self):
        """Generate voice quality issues"""
        issue_types = [VoiceActivityType.ECHO, VoiceActivityType.FEEDBACK]
        issue_type = random.choice(issue_types)
        
        duration = random.uniform(0.5, 2.0)
        
        event = VoiceEvent(
            speaker_id="SYSTEM",
            activity_type=issue_type,
            duration=duration,
            quality=VoiceQuality.BAD,
            volume=random.uniform(0.2, 0.8),
            timestamp=datetime.now(),
            metadata={
                "issue_severity": random.choice(["mild", "moderate", "severe"]),
                "affected_speakers": random.sample(list(self.active_speakers.keys()), 
                                                 min(2, len(self.active_speakers)))
            }
        )
        
        self.voice_events.append(event)
        logger.warning(f"Voice issue generated: {issue_type.value}")
    
    def _determine_voice_quality(self) -> VoiceQuality:
        """Determine voice quality based on current conditions"""
        # Base quality on current voice quality setting
        base_quality = self.voice_quality
        
        # Add some randomness
        quality_chance = random.random()
        
        if quality_chance < 0.7:
            return base_quality
        elif quality_chance < 0.85:
            # Slightly worse
            if base_quality == VoiceQuality.EXCELLENT:
                return VoiceQuality.GOOD
            elif base_quality == VoiceQuality.GOOD:
                return VoiceQuality.POOR
            else:
                return VoiceQuality.BAD
        else:
            # Slightly better
            if base_quality == VoiceQuality.BAD:
                return VoiceQuality.POOR
            elif base_quality == VoiceQuality.POOR:
                return VoiceQuality.GOOD
            else:
                return VoiceQuality.EXCELLENT
    
    def _generate_speech_content(self) -> str:
        """Generate realistic speech content"""
        speech_templates = [
            "Enemy spotted at {location}!",
            "Need backup at {location}!",
            "Bomb planted at {location}!",
            "Clear! Moving to {location}!",
            "Rush {location}!",
            "Hold position at {location}!",
            "Cover me while I {action}!",
            "Good shot!",
            "Nice play!",
            "Watch out for {enemy}!",
            "I'm reloading!",
            "Defusing the bomb!",
            "Planting the bomb!",
            "Enemy down!",
            "Team wipe!",
            "Round won!",
            "Round lost!",
            "Good game!",
            "Well played!",
            "Let's go!"
        ]
        
        locations = ["A", "B", "mid", "long", "short", "catwalk", "tunnel", "site"]
        actions = ["reload", "heal", "defuse", "plant", "flank"]
        enemies = ["sniper", "rusher", "camper", "lurker"]
        
        template = random.choice(speech_templates)
        
        # Replace placeholders
        content = template.format(
            location=random.choice(locations),
            action=random.choice(actions),
            enemy=random.choice(enemies)
        )
        
        return content
    
    async def _update_voice_quality(self):
        """Update overall voice quality"""
        # Simulate quality changes based on network conditions
        if random.random() < 0.01:  # 1% chance of quality change
            quality_levels = list(VoiceQuality)
            current_index = quality_levels.index(self.voice_quality)
            
            # Move one level up or down
            if random.random() < 0.5 and current_index > 0:
                self.voice_quality = quality_levels[current_index - 1]
            elif current_index < len(quality_levels) - 1:
                self.voice_quality = quality_levels[current_index + 1]
            
            logger.info(f"Voice quality changed to: {self.voice_quality.value}")
    
    async def _cleanup_old_events(self):
        """Remove old voice events"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=5)  # Keep last 5 minutes
        
        self.voice_events = [
            event for event in self.voice_events
            if event.timestamp > cutoff_time
        ]
    
    async def add_speaker(self, speaker_id: str, speaker_info: Optional[Dict[str, Any]] = None):
        """Add a speaker to the voice chat"""
        if speaker_id not in self.active_speakers:
            self.active_speakers[speaker_id] = {
                "info": speaker_info or {},
                "join_time": datetime.now(),
                "total_speech_time": 0.0,
                "last_speech": None
            }
            logger.info(f"Speaker {speaker_id} joined voice chat")
    
    async def remove_speaker(self, speaker_id: str):
        """Remove a speaker from the voice chat"""
        if speaker_id in self.active_speakers:
            del self.active_speakers[speaker_id]
            logger.info(f"Speaker {speaker_id} left voice chat")
    
    async def simulate_voice_activity(self) -> Dict[str, Any]:
        """Simulate voice activity and return event data"""
        if not self.active_speakers:
            return {
                "speaker_id": "SYSTEM",
                "type": "silence",
                "duration": 1.0,
                "message": "No active speakers"
            }
        
        # Select a random speaker
        speaker_id = random.choice(list(self.active_speakers.keys()))
        
        # Generate activity type
        activity_type = random.choice([
            VoiceActivityType.SPEECH,
            VoiceActivityType.BACKGROUND_NOISE,
            VoiceActivityType.SILENCE
        ])
        
        if activity_type == VoiceActivityType.SPEECH:
            content = self._generate_speech_content()
            duration = random.uniform(0.5, 3.0)
            
            return {
                "speaker_id": speaker_id,
                "type": "speech",
                "duration": duration,
                "content": content,
                "quality": self.voice_quality.value,
                "volume": random.uniform(0.3, 1.0)
            }
        
        elif activity_type == VoiceActivityType.BACKGROUND_NOISE:
            return {
                "speaker_id": speaker_id,
                "type": "background_noise",
                "duration": random.uniform(1, 3),
                "noise_type": random.choice(["keyboard", "mouse_clicks", "ambient"]),
                "volume": random.uniform(0.1, 0.3)
            }
        
        else:  # SILENCE
            return {
                "speaker_id": speaker_id,
                "type": "silence",
                "duration": random.uniform(1, 5),
                "message": "No voice activity"
            }
    
    def get_voice_stats(self) -> Dict[str, Any]:
        """Get voice chat statistics"""
        recent_events = [
            event for event in self.voice_events
            if event.timestamp > datetime.now() - timedelta(minutes=1)
        ]
        
        speech_events = [e for e in recent_events if e.activity_type == VoiceActivityType.SPEECH]
        issue_events = [e for e in recent_events if e.activity_type in [VoiceActivityType.ECHO, VoiceActivityType.FEEDBACK]]
        
        return {
            "active_speakers": len(self.active_speakers),
            "total_events": len(recent_events),
            "speech_events": len(speech_events),
            "issue_events": len(issue_events),
            "voice_quality": self.voice_quality.value,
            "average_speech_duration": (
                sum(e.duration for e in speech_events) / len(speech_events)
                if speech_events else 0
            )
        }
    
    def get_recent_events(self, minutes: int = 5) -> List[Dict[str, Any]]:
        """Get recent voice events"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        return [
            {
                "speaker_id": event.speaker_id,
                "type": event.activity_type.value,
                "duration": event.duration,
                "quality": event.quality.value,
                "volume": event.volume,
                "timestamp": event.timestamp.isoformat(),
                "metadata": event.metadata
            }
            for event in self.voice_events
            if event.timestamp > cutoff_time
        ]
    
    async def set_voice_quality(self, quality: VoiceQuality):
        """Set the voice quality level"""
        self.voice_quality = quality
        logger.info(f"Voice quality set to: {quality.value}")
    
    async def shutdown(self):
        """Shutdown the voice simulation"""
        logger.info("Shutting down Voice Simulation...")
        self.is_initialized = False
        
        # Clear all data
        self.active_speakers.clear()
        self.voice_events.clear()
        
        logger.info("Voice Simulation shutdown complete") 