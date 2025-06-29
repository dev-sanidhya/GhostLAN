"""
API Server Configuration
Main FastAPI server setup and configuration
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import routers
from .export import router as export_router
from .match import router as match_router

logger = logging.getLogger(__name__)

def start_api_server(lifespan=None) -> FastAPI:
    """Create and configure the FastAPI server"""
    
    app = FastAPI(
        title="GhostLAN SimWorld API",
        description="Advanced eSports Anti-Cheat Testing Platform API",
        version="2.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(export_router)
    app.include_router(match_router)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception handler: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(exc),
                "type": type(exc).__name__
            }
        )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """API health check"""
        return {
            "status": "healthy",
            "service": "GhostLAN API Server",
            "version": "2.0.0"
        }
    
    # API status endpoint
    @app.get("/api/v1/status")
    async def api_status():
        """API status information"""
        return {
            "status": "operational",
            "timestamp": "2025-06-28T21:00:00Z",
            "version": "2.0.0",
            "services": {
                "duality_simulation": {"status": "operational", "initialized": True},
                "anticheat_engine": {"status": "operational", "initialized": True},
                "analytics_pipeline": {"status": "operational", "initialized": True},
                "match_recorder": {"status": "operational", "initialized": True}
            },
            "websocket_connections": 0,
            "endpoints": {
                "export": "/api/v1/export",
                "match": "/api/v1/match",
                "health": "/health",
                "websocket": "/ws"
            }
        }
    
    return app 