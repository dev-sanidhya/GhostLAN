"""
Match API Endpoints
Match control and management endpoints for GhostLAN SimWorld
"""

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/match", tags=["match"])

# Pydantic models
class MatchConfig(BaseModel):
    map: str
    players: list
    duration: int
    game_mode: str

class MatchStartRequest(BaseModel):
    config: MatchConfig

class MatchStopRequest(BaseModel):
    match_id: str

# Mock match storage
active_matches: Dict[str, Dict[str, Any]] = {}

@router.post("/start")
async def start_match(request: MatchStartRequest):
    """Start a new match"""
    try:
        import uuid
        match_id = f"match_{uuid.uuid4().hex[:8]}"
        
        # Store match configuration
        active_matches[match_id] = {
            "id": match_id,
            "config": request.config.dict(),
            "status": "running",
            "start_time": "2025-06-28T21:00:00Z",
            "players": request.config.players
        }
        
        logger.info(f"Started match {match_id} with {len(request.config.players)} players")
        
        return {
            "match_id": match_id,
            "status": "started",
            "message": f"Match {match_id} started successfully"
        }
    except Exception as e:
        logger.error(f"Failed to start match: {e}")
        raise HTTPException(status_code=500, detail="Failed to start match")

@router.post("/stop")
async def stop_match(request: MatchStopRequest):
    """Stop an active match"""
    try:
        match_id = request.match_id
        
        if match_id not in active_matches:
            raise HTTPException(status_code=404, detail="Match not found")
        
        # Update match status
        active_matches[match_id]["status"] = "completed"
        active_matches[match_id]["end_time"] = "2025-06-28T21:30:00Z"
        
        logger.info(f"Stopped match {match_id}")
        
        return {
            "match_id": match_id,
            "status": "stopped",
            "message": f"Match {match_id} stopped successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop match: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop match")

@router.get("/list")
async def get_active_matches():
    """Get all active matches"""
    try:
        return {
            "active_matches": list(active_matches.values()),
            "count": len(active_matches)
        }
    except Exception as e:
        logger.error(f"Failed to get active matches: {e}")
        raise HTTPException(status_code=500, detail="Failed to get active matches")

@router.get("/{match_id}")
async def get_match_status(match_id: str):
    """Get status of a specific match"""
    try:
        if match_id not in active_matches:
            raise HTTPException(status_code=404, detail="Match not found")
        
        return active_matches[match_id]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get match status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get match status") 