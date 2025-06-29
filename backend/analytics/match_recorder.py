"""
Match Recorder Module for GhostLAN SimWorld
Records and manages match data for analytics and replay
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import sqlite3
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class MatchEvent:
    """Represents a single match event"""
    timestamp: float
    event_type: str
    player_id: str
    data: Dict[str, Any]
    match_id: str

@dataclass
class MatchData:
    """Represents complete match data"""
    match_id: str
    start_time: datetime
    end_time: Optional[datetime]
    players: List[str]
    map_name: str
    game_mode: str
    events: List[MatchEvent]
    winner: Optional[str]
    duration: Optional[float]

class MatchRecorder:
    """Records and manages match data for analytics and replay"""
    
    def __init__(self, db_path: str = "match_data.db"):
        """Initialize the match recorder"""
        self.db_path = db_path
        self.current_match: Optional[MatchData] = None
        self.events: List[MatchEvent] = []
        self.db_conn: Optional[sqlite3.Connection] = None
        self._init_database()
        logger.info("Match Recorder initialized")
    
    def _init_database(self):
        """Initialize the SQLite database"""
        try:
            self.db_conn = sqlite3.connect(self.db_path)
            cursor = self.db_conn.cursor()
            
            # Create matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    match_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    map_name TEXT,
                    game_mode TEXT,
                    winner TEXT,
                    duration REAL,
                    player_count INTEGER
                )
            """)
            
            # Create events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    match_id TEXT,
                    timestamp REAL,
                    event_type TEXT,
                    player_id TEXT,
                    data TEXT,
                    FOREIGN KEY (match_id) REFERENCES matches (match_id)
                )
            """)
            
            # Create players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS match_players (
                    match_id TEXT,
                    player_id TEXT,
                    team TEXT,
                    final_score INTEGER DEFAULT 0,
                    kills INTEGER DEFAULT 0,
                    deaths INTEGER DEFAULT 0,
                    assists INTEGER DEFAULT 0,
                    PRIMARY KEY (match_id, player_id),
                    FOREIGN KEY (match_id) REFERENCES matches (match_id)
                )
            """)
            
            self.db_conn.commit()
            logger.info("Match database initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def start_match(self, match_id: str, players: List[str], map_name: str, game_mode: str) -> None:
        """Start recording a new match"""
        if self.current_match:
            logger.warning("Match already in progress, ending current match first")
            self.end_match()
        
        self.current_match = MatchData(
            match_id=match_id,
            start_time=datetime.now(),
            end_time=None,
            players=players,
            map_name=map_name,
            game_mode=game_mode,
            events=[],
            winner=None,
            duration=None
        )
        
        self.events = []
        logger.info(f"Started recording match {match_id}")
    
    def record_event(self, event_type: str, player_id: str, data: Dict[str, Any]) -> None:
        """Record a match event"""
        if not self.current_match:
            logger.warning("No match in progress, event ignored")
            return
        
        event = MatchEvent(
            timestamp=time.time(),
            event_type=event_type,
            player_id=player_id,
            data=data,
            match_id=self.current_match.match_id
        )
        
        self.events.append(event)
        self.current_match.events.append(event)
        
        # Store in database
        if self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("""
                    INSERT INTO events (match_id, timestamp, event_type, player_id, data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    event.match_id,
                    event.timestamp,
                    event.event_type,
                    event.player_id,
                    json.dumps(event.data)
                ))
                self.db_conn.commit()
            except Exception as e:
                logger.error(f"Failed to store event in database: {e}")
        
        logger.debug(f"Recorded event: {event_type} by {player_id}")
    
    def end_match(self, winner: Optional[str] = None) -> Optional[MatchData]:
        """End the current match and return the match data"""
        if not self.current_match:
            logger.warning("No match in progress")
            return None
        
        self.current_match.end_time = datetime.now()
        self.current_match.winner = winner
        self.current_match.duration = (
            self.current_match.end_time - self.current_match.start_time
        ).total_seconds()
        
        # Store match data in database
        if self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                
                # Insert match record
                cursor.execute("""
                    INSERT INTO matches (match_id, start_time, end_time, map_name, game_mode, winner, duration, player_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.current_match.match_id,
                    self.current_match.start_time.isoformat(),
                    self.current_match.end_time.isoformat(),
                    self.current_match.map_name,
                    self.current_match.game_mode,
                    winner,
                    self.current_match.duration,
                    len(self.current_match.players)
                ))
                
                # Insert player records
                for player_id in self.current_match.players:
                    cursor.execute("""
                        INSERT INTO match_players (match_id, player_id, team)
                        VALUES (?, ?, ?)
                    """, (self.current_match.match_id, player_id, "unknown"))
                
                self.db_conn.commit()
                logger.info(f"Match {self.current_match.match_id} data stored in database")
                
            except Exception as e:
                logger.error(f"Failed to store match data in database: {e}")
        
        match_data = self.current_match
        self.current_match = None
        self.events = []
        
        logger.info(f"Ended recording match {match_data.match_id}")
        return match_data
    
    def get_match_data(self, match_id: str) -> Optional[MatchData]:
        """Retrieve match data from database"""
        if not self.db_conn:
            return None
        
        try:
            cursor = self.db_conn.cursor()
            
            # Get match info
            cursor.execute("""
                SELECT start_time, end_time, map_name, game_mode, winner, duration
                FROM matches WHERE match_id = ?
            """, (match_id,))
            
            match_row = cursor.fetchone()
            if not match_row:
                return None
            
            # Get events
            cursor.execute("""
                SELECT timestamp, event_type, player_id, data
                FROM events WHERE match_id = ? ORDER BY timestamp
            """, (match_id,))
            
            events = []
            for row in cursor.fetchall():
                event = MatchEvent(
                    timestamp=row[0],
                    event_type=row[1],
                    player_id=row[2],
                    data=json.loads(row[3]),
                    match_id=match_id
                )
                events.append(event)
            
            # Get players
            cursor.execute("""
                SELECT player_id FROM match_players WHERE match_id = ?
            """, (match_id,))
            
            players = [row[0] for row in cursor.fetchall()]
            
            return MatchData(
                match_id=match_id,
                start_time=datetime.fromisoformat(match_row[0]),
                end_time=datetime.fromisoformat(match_row[1]) if match_row[1] else None,
                players=players,
                map_name=match_row[2],
                game_mode=match_row[3],
                events=events,
                winner=match_row[4],
                duration=match_row[5]
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve match data: {e}")
            return None
    
    def get_recent_matches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent matches summary"""
        if not self.db_conn:
            return []
        
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT match_id, start_time, end_time, map_name, game_mode, winner, duration, player_count
                FROM matches ORDER BY start_time DESC LIMIT ?
            """, (limit,))
            
            matches = []
            for row in cursor.fetchall():
                matches.append({
                    "match_id": row[0],
                    "start_time": row[1],
                    "end_time": row[2],
                    "map_name": row[3],
                    "game_mode": row[4],
                    "winner": row[5],
                    "duration": row[6],
                    "player_count": row[7]
                })
            
            return matches
            
        except Exception as e:
            logger.error(f"Failed to retrieve recent matches: {e}")
            return []
    
    def export_match_replay(self, match_id: str, filepath: str) -> bool:
        """Export match data as replay file"""
        match_data = self.get_match_data(match_id)
        if not match_data:
            return False
        
        try:
            replay_data = {
                "match_info": {
                    "match_id": match_data.match_id,
                    "start_time": match_data.start_time.isoformat(),
                    "end_time": match_data.end_time.isoformat() if match_data.end_time else None,
                    "map_name": match_data.map_name,
                    "game_mode": match_data.game_mode,
                    "winner": match_data.winner,
                    "duration": match_data.duration,
                    "players": match_data.players
                },
                "events": [
                    {
                        "timestamp": event.timestamp,
                        "event_type": event.event_type,
                        "player_id": event.player_id,
                        "data": event.data
                    }
                    for event in match_data.events
                ]
            }
            
            with open(filepath, 'w') as f:
                json.dump(replay_data, f, indent=2)
            
            logger.info(f"Exported replay to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export replay: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.db_conn:
            self.db_conn.close()
        logger.info("Match Recorder cleaned up") 