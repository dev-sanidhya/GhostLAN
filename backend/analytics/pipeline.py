"""
Analytics Pipeline
Data processing and analysis pipeline for GhostLAN
"""

import asyncio
import logging
import json
import sqlite3
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class AnalyticsEvent:
    """Analytics event data"""
    event_id: str
    event_type: str
    timestamp: datetime
    player_id: str
    match_id: str
    data: Dict[str, Any]

class AnalyticsPipeline:
    """Data processing and analytics pipeline"""
    
    def __init__(self):
        self.db_path = "analytics.db"
        self.events: List[AnalyticsEvent] = []
        self.is_initialized = False
        self.processors = {}
        
        # Initialize database
        self._init_database()
        
        # Register event processors
        self._register_processors()
    
    def _init_database(self):
        """Initialize the analytics database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    player_id TEXT,
                    match_id TEXT,
                    data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    match_id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    map_name TEXT,
                    game_mode TEXT,
                    player_count INTEGER,
                    duration INTEGER,
                    status TEXT DEFAULT 'active',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create player_stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id TEXT NOT NULL,
                    match_id TEXT NOT NULL,
                    kills INTEGER DEFAULT 0,
                    deaths INTEGER DEFAULT 0,
                    assists INTEGER DEFAULT 0,
                    accuracy REAL DEFAULT 0.0,
                    headshots INTEGER DEFAULT 0,
                    damage_dealt INTEGER DEFAULT 0,
                    damage_taken INTEGER DEFAULT 0,
                    movement_distance REAL DEFAULT 0.0,
                    suspicious_actions INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(player_id, match_id)
                )
            ''')
            
            # Create network_stats table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    latency REAL,
                    packet_loss REAL,
                    jitter REAL,
                    bandwidth_usage REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Analytics database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _register_processors(self):
        """Register event processors"""
        self.processors = {
            "agent_action": self._process_agent_action,
            "network_issue": self._process_network_issue,
            "voice_activity": self._process_voice_activity,
            "match_start": self._process_match_start,
            "match_end": self._process_match_end,
            "suspicious_behavior": self._process_suspicious_behavior,
            "player_join": self._process_player_join,
            "player_leave": self._process_player_leave
        }
    
    async def initialize(self):
        """Initialize the analytics pipeline"""
        logger.info("Initializing Analytics Pipeline...")
        
        # Start data processing tasks
        asyncio.create_task(self._process_events())
        asyncio.create_task(self._cleanup_old_data())
        
        self.is_initialized = True
        logger.info("Analytics Pipeline initialized successfully")
    
    async def _process_events(self):
        """Process events in the pipeline"""
        while self.is_initialized:
            try:
                if self.events:
                    event = self.events.pop(0)
                    await self._process_event(event)
                
                await asyncio.sleep(0.1)  # Process events quickly
                
            except Exception as e:
                logger.error(f"Error processing events: {e}")
                await asyncio.sleep(1)
    
    async def _process_event(self, event: AnalyticsEvent):
        """Process a single event"""
        try:
            # Store event in database
            await self._store_event(event)
            
            # Process with appropriate processor
            processor = self.processors.get(event.event_type)
            if processor:
                await processor(event)
            
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {e}")
    
    async def _store_event(self, event: AnalyticsEvent):
        """Store event in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (event_id, event_type, timestamp, player_id, match_id, data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event.event_id,
                event.event_type,
                event.timestamp.isoformat(),
                event.player_id,
                event.match_id,
                json.dumps(event.data)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
    
    async def _process_agent_action(self, event: AnalyticsEvent):
        """Process agent action events"""
        data = event.data
        action_type = data.get("action_type")
        
        if action_type == "shoot":
            await self._update_shooting_stats(event)
        elif action_type == "move":
            await self._update_movement_stats(event)
        elif action_type == "communicate":
            await self._update_communication_stats(event)
    
    async def _process_network_issue(self, event: AnalyticsEvent):
        """Process network issue events"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO network_stats (match_id, timestamp, latency, packet_loss, jitter, bandwidth_usage)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event.match_id,
                event.timestamp.isoformat(),
                data.get("latency", 0),
                data.get("packet_loss", 0),
                data.get("jitter", 0),
                data.get("bandwidth_usage", 0)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store network stats: {e}")
    
    async def _process_voice_activity(self, event: AnalyticsEvent):
        """Process voice activity events"""
        # Store voice activity data
        data = event.data
        
        # This could be extended to analyze voice patterns
        # for potential voice-based cheating detection
        
        logger.debug(f"Voice activity processed: {data.get('activity_type')}")
    
    async def _process_match_start(self, event: AnalyticsEvent):
        """Process match start events"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO matches (match_id, start_time, map_name, game_mode, player_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                event.match_id,
                event.timestamp.isoformat(),
                data.get("map_name", "unknown"),
                data.get("game_mode", "5v5"),
                data.get("player_count", 10)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store match start: {e}")
    
    async def _process_match_end(self, event: AnalyticsEvent):
        """Process match end events"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE matches 
                SET end_time = ?, duration = ?, status = 'completed'
                WHERE match_id = ?
            ''', (
                event.timestamp.isoformat(),
                data.get("duration", 0),
                event.match_id
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update match end: {e}")
    
    async def _process_suspicious_behavior(self, event: AnalyticsEvent):
        """Process suspicious behavior events"""
        data = event.data
        
        # Update player suspicious actions count
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE player_stats 
                SET suspicious_actions = suspicious_actions + 1
                WHERE player_id = ? AND match_id = ?
            ''', (event.player_id, event.match_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update suspicious behavior: {e}")
    
    async def _process_player_join(self, event: AnalyticsEvent):
        """Process player join events"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO player_stats 
                (player_id, match_id, kills, deaths, assists, accuracy, headshots, 
                 damage_dealt, damage_taken, movement_distance, suspicious_actions)
                VALUES (?, ?, 0, 0, 0, 0.0, 0, 0, 0, 0.0, 0)
            ''', (event.player_id, event.match_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store player join: {e}")
    
    async def _process_player_leave(self, event: AnalyticsEvent):
        """Process player leave events"""
        # Could be used to finalize player statistics
        logger.debug(f"Player {event.player_id} left match {event.match_id}")
    
    async def _update_shooting_stats(self, event: AnalyticsEvent):
        """Update shooting statistics"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current stats
            cursor.execute('''
                SELECT kills, headshots, damage_dealt, accuracy
                FROM player_stats 
                WHERE player_id = ? AND match_id = ?
            ''', (event.player_id, event.match_id))
            
            result = cursor.fetchone()
            if result:
                kills, headshots, damage_dealt, accuracy = result
                
                # Update stats
                new_kills = kills + (1 if data.get("kill", False) else 0)
                new_headshots = headshots + (1 if data.get("headshot", False) else 0)
                new_damage = damage_dealt + data.get("damage", 0)
                
                # Calculate new accuracy (simplified)
                shots_fired = data.get("shots_fired", 1)
                shots_hit = data.get("shots_hit", 0)
                new_accuracy = ((accuracy * (kills + headshots)) + shots_hit) / (kills + headshots + shots_fired)
                
                cursor.execute('''
                    UPDATE player_stats 
                    SET kills = ?, headshots = ?, damage_dealt = ?, accuracy = ?
                    WHERE player_id = ? AND match_id = ?
                ''', (new_kills, new_headshots, new_damage, new_accuracy, event.player_id, event.match_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update shooting stats: {e}")
    
    async def _update_movement_stats(self, event: AnalyticsEvent):
        """Update movement statistics"""
        data = event.data
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            distance = data.get("distance", 0)
            
            cursor.execute('''
                UPDATE player_stats 
                SET movement_distance = movement_distance + ?
                WHERE player_id = ? AND match_id = ?
            ''', (distance, event.player_id, event.match_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to update movement stats: {e}")
    
    async def _update_communication_stats(self, event: AnalyticsEvent):
        """Update communication statistics"""
        # Could track communication patterns
        # for potential voice-based cheating detection
        pass
    
    async def _cleanup_old_data(self):
        """Clean up old data"""
        while self.is_initialized:
            try:
                # Keep only last 30 days of data
                cutoff_date = datetime.now() - timedelta(days=30)
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM events 
                    WHERE timestamp < ?
                ''', (cutoff_date.isoformat(),))
                
                conn.commit()
                conn.close()
                
                await asyncio.sleep(3600)  # Clean up every hour
                
            except Exception as e:
                logger.error(f"Error in data cleanup: {e}")
                await asyncio.sleep(3600)
    
    async def add_event(self, event_type: str, player_id: str, match_id: str, data: Dict[str, Any]):
        """Add an event to the pipeline"""
        event = AnalyticsEvent(
            event_id=f"EVT_{len(self.events) + 1:06d}",
            event_type=event_type,
            timestamp=datetime.now(),
            player_id=player_id,
            match_id=match_id,
            data=data
        )
        
        self.events.append(event)
    
    def get_match_statistics(self, match_id: str) -> Dict[str, Any]:
        """Get statistics for a specific match"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get match info
            match_df = pd.read_sql_query('''
                SELECT * FROM matches WHERE match_id = ?
            ''', conn, params=[match_id])
            
            # Get player stats
            player_df = pd.read_sql_query('''
                SELECT * FROM player_stats WHERE match_id = ?
            ''', conn, params=[match_id])
            
            # Get network stats
            network_df = pd.read_sql_query('''
                SELECT * FROM network_stats WHERE match_id = ?
            ''', conn, params=[match_id])
            
            conn.close()
            
            if match_df.empty:
                return {}
            
            match_info = match_df.iloc[0].to_dict()
            
            return {
                "match_info": match_info,
                "player_stats": player_df.to_dict('records'),
                "network_stats": network_df.to_dict('records'),
                "summary": {
                    "total_players": len(player_df),
                    "total_kills": player_df['kills'].sum(),
                    "total_deaths": player_df['deaths'].sum(),
                    "average_accuracy": player_df['accuracy'].mean(),
                    "suspicious_actions": player_df['suspicious_actions'].sum()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get match statistics: {e}")
            return {}
    
    def get_player_statistics(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get statistics for a specific player"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            df = pd.read_sql_query('''
                SELECT * FROM player_stats 
                WHERE player_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', conn, params=[player_id, limit])
            
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Failed to get player statistics: {e}")
            return []
    
    def get_network_statistics(self, match_id: str) -> List[Dict[str, Any]]:
        """Get network statistics for a match"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            df = pd.read_sql_query('''
                SELECT * FROM network_stats 
                WHERE match_id = ? 
                ORDER BY timestamp
            ''', conn, params=[match_id])
            
            conn.close()
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Failed to get network statistics: {e}")
            return []
    
    async def shutdown(self):
        """Shutdown the analytics pipeline"""
        logger.info("Shutting down Analytics Pipeline...")
        self.is_initialized = False
        
        # Process remaining events
        while self.events:
            event = self.events.pop(0)
            await self._process_event(event)
        
        logger.info("Analytics Pipeline shutdown complete") 