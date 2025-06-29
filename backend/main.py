#!/usr/bin/env python3
"""
GhostLAN SimWorld - Main Application
Advanced eSports Anti-Cheat Testing Platform with Duality AI Integration
"""

import asyncio
import logging
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import json
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

# Import existing modules only
from duality_scene.simulation import SimulationManager
from ghostlan_core.anticheat import AntiCheatEngine
from analytics.pipeline import AnalyticsPipeline
from analytics.match_recorder import MatchRecorder
from api.server import start_api_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
duality_simulation = None
anticheat_engine = None
analytics_pipeline = None
match_recorder = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global duality_simulation, anticheat_engine, analytics_pipeline, match_recorder
    
    logger.info("🚀 Starting GhostLAN SimWorld...")
    
    try:
        # Initialize Duality AI simulation
        logger.info("🤖 Initializing Duality AI Simulation...")
        duality_simulation = SimulationManager()
        await duality_simulation.initialize()
        
        # Initialize anti-cheat engine
        logger.info("🛡️ Initializing Anti-Cheat Engine...")
        anticheat_engine = AntiCheatEngine()
        await anticheat_engine.initialize()
        
        # Initialize analytics pipeline
        logger.info("📊 Initializing Analytics Pipeline...")
        analytics_pipeline = AnalyticsPipeline()
        await analytics_pipeline.initialize()
        
        # Initialize match recorder
        logger.info("🎬 Initializing Match Recorder...")
        match_recorder = MatchRecorder()
        # Note: MatchRecorder doesn't have initialize method, so we skip it
        
        logger.info("✅ All systems initialized successfully!")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize systems: {e}")
        raise
    finally:
        # Cleanup
        logger.info("🛑 Shutting down GhostLAN SimWorld...")
        
        if duality_simulation:
            await duality_simulation.shutdown()
        if anticheat_engine:
            await anticheat_engine.shutdown()
        if analytics_pipeline:
            await analytics_pipeline.shutdown()
        # Note: MatchRecorder doesn't have shutdown method, so we skip it
            
        logger.info("✅ Shutdown complete")

# Create FastAPI app using the server function
app = start_api_server(lifespan=lifespan)

# WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    ping_task = None
    try:
        async def send_pings():
            while True:
                await asyncio.sleep(20)
                try:
                    await manager.send_personal_message("ping", websocket)
                except Exception as e:
                    logger.error(f"WebSocket ping error: {e}")
                    break
        ping_task = asyncio.create_task(send_pings())
        while True:
            try:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"Message text was: {data}", websocket)
            except WebSocketDisconnect:
                logger.info("WebSocket client disconnected.")
                break
            except Exception as e:
                logger.error(f"WebSocket receive error: {e}")
                break
    finally:
        if ping_task:
            ping_task.cancel()
        manager.disconnect(websocket)
        logger.info("WebSocket connection closed and cleaned up.")

@app.get("/")
async def root():
    """Root endpoint with project information"""
    return {
        "message": "GhostLAN SimWorld API",
        "version": "2.0.0",
        "description": "Advanced eSports Anti-Cheat Testing Platform with Duality AI Integration",
        "endpoints": {
            "health": "/health",
            "api_status": "/api/v1/status",
            "websocket": "/ws",
            "docs": "/docs"
        },
        "features": [
            "Duality AI Simulation",
            "Anti-Cheat Engine",
            "Analytics Pipeline",
            "Match Recording",
            "Real-time WebSocket Communication"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if core systems are available
        systems_status = {
            "duality_simulation": duality_simulation is not None,
            "anticheat_engine": anticheat_engine is not None,
            "analytics_pipeline": analytics_pipeline is not None,
            "match_recorder": match_recorder is not None
        }
        
        all_systems_healthy = all(systems_status.values())
        
        return {
            "status": "healthy" if all_systems_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "systems": systems_status,
            "version": "2.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/v1/status")
async def api_status():
    """Detailed API status endpoint"""
    try:
        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "services": {
                "duality_simulation": {
                    "status": "running" if duality_simulation else "stopped",
                    "initialized": duality_simulation is not None
                },
                "anticheat_engine": {
                    "status": "running" if anticheat_engine else "stopped",
                    "initialized": anticheat_engine is not None
                },
                "analytics_pipeline": {
                    "status": "running" if analytics_pipeline else "stopped",
                    "initialized": analytics_pipeline is not None
                },
                "match_recorder": {
                    "status": "running" if match_recorder else "stopped",
                    "initialized": match_recorder is not None
                }
            },
            "websocket_connections": len(manager.active_connections)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# Global getter functions for dependency injection
def get_duality_simulation():
    return duality_simulation

def get_anticheat_engine():
    return anticheat_engine

def get_analytics_pipeline():
    return analytics_pipeline

def get_match_recorder():
    return match_recorder

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 