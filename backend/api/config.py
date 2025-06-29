"""
API Configuration Module for GhostLAN SimWorld
Manages API settings, environment variables, and configuration
"""

import os
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi import APIRouter, HTTPException
import logging

logger = logging.getLogger(__name__)

class APIConfig(BaseModel):
    """API Configuration settings"""
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    debug: bool = Field(default=False, description="Debug mode")
    reload: bool = Field(default=True, description="Auto reload")
    
    # CORS settings
    cors_origins: List[str] = Field(default=["*"], description="CORS origins")
    cors_methods: List[str] = Field(default=["*"], description="CORS methods")
    cors_headers: List[str] = Field(default=["*"], description="CORS headers")
    
    # Security settings
    secret_key: str = Field(default="ghostlan-secret-key-change-in-production", description="Secret key")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Token expiry minutes")
    
    # Database settings
    database_url: str = Field(default="sqlite:///./ghostlan.db", description="Database URL")
    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL")
    
    # AI and ML settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    google_api_key: Optional[str] = Field(default=None, description="Google API key")
    duality_api_key: Optional[str] = Field(default=None, description="Duality AI API key")
    
    # Simulation settings
    max_agents: int = Field(default=20, description="Max agents")
    simulation_tick_rate: float = Field(default=60.0, description="Simulation tick rate")
    match_duration: int = Field(default=300, description="Match duration in seconds")
    
    # Anti-cheat settings
    cheat_detection_enabled: bool = Field(default=True, description="Enable cheat detection")
    detection_sensitivity: float = Field(default=0.8, description="Detection sensitivity")
    
    # Analytics settings
    analytics_enabled: bool = Field(default=True, description="Enable analytics")
    analytics_db_path: str = Field(default="./analytics.db", description="Analytics DB path")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Log level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    
    # File paths
    base_dir: Path = Field(default=Path(__file__).parent.parent, description="Base directory")
    data_dir: Path = Field(default=Path("./data"), description="Data directory")
    logs_dir: Path = Field(default=Path("./logs"), description="Logs directory")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

class DevelopmentConfig(APIConfig):
    """Development configuration"""
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"

class ProductionConfig(APIConfig):
    """Production configuration"""
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"
    cors_origins: List[str] = ["https://ghostlan.com", "https://www.ghostlan.com"]

class TestingConfig(APIConfig):
    """Testing configuration"""
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379/1"
    log_level: str = "DEBUG"

def get_config() -> APIConfig:
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

def validate_config(config: APIConfig) -> bool:
    """Validate configuration settings"""
    errors = []
    
    # Check required directories
    for dir_path in [config.data_dir, config.logs_dir]:
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Failed to create directory {dir_path}: {e}")
    
    # Check API keys if required
    if not config.openai_api_key and os.getenv("REQUIRE_OPENAI", "false").lower() == "true":
        errors.append("OpenAI API key is required but not provided")
    
    if not config.google_api_key and os.getenv("REQUIRE_GOOGLE", "false").lower() == "true":
        errors.append("Google API key is required but not provided")
    
    if not config.duality_api_key and os.getenv("REQUIRE_DUALITY", "false").lower() == "true":
        errors.append("Duality AI API key is required but not provided")
    
    # Check database connection
    try:
        if config.database_url.startswith("sqlite"):
            # SQLite database - check if directory exists
            db_path = Path(config.database_url.replace("sqlite:///", ""))
            if not db_path.parent.exists():
                db_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        errors.append(f"Database configuration error: {e}")
    
    if errors:
        for error in errors:
            print(f"Configuration Error: {error}")
        return False
    
    return True

def create_env_template() -> str:
    """Create a template .env file"""
    template = """# GhostLAN SimWorld API Configuration
# Copy this file to .env and modify as needed

# Environment
ENVIRONMENT=development

# Server Settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
API_RELOAD=true

# CORS Settings
CORS_ORIGINS=["*"]
CORS_METHODS=["*"]
CORS_HEADERS=["*"]

# Security
SECRET_KEY=ghostlan-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./ghostlan.db
REDIS_URL=redis://localhost:6379

# AI/ML APIs
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
DUALITY_API_KEY=your-duality-api-key-here

# Simulation
MAX_AGENTS=20
SIMULATION_TICK_RATE=60.0
MATCH_DURATION=300

# Anti-cheat
CHEAT_DETECTION_ENABLED=true
DETECTION_SENSITIVITY=0.8

# Analytics
ANALYTICS_ENABLED=true
ANALYTICS_DB_PATH=./analytics.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/ghostlan.log

# Paths
BASE_DIR=.
DATA_DIR=./data
LOGS_DIR=./logs
"""
    return template

# Global config instance
config = get_config()

# Validate configuration on import
if not validate_config(config):
    print("Warning: Configuration validation failed. Some features may not work correctly.")

# Create API router for configuration endpoints
config_router = APIRouter(prefix="/config", tags=["configuration"])

@config_router.get("/")
async def get_configuration():
    """Get current configuration (non-sensitive fields only)"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "host": config.host,
        "port": config.port,
        "debug": config.debug,
        "max_agents": config.max_agents,
        "simulation_tick_rate": config.simulation_tick_rate,
        "match_duration": config.match_duration,
        "cheat_detection_enabled": config.cheat_detection_enabled,
        "analytics_enabled": config.analytics_enabled,
        "log_level": config.log_level
    }

@config_router.get("/env-template")
async def get_env_template():
    """Get environment template"""
    return {"template": create_env_template()}

@config_router.post("/validate")
async def validate_current_config():
    """Validate current configuration"""
    is_valid = validate_config(config)
    return {
        "valid": is_valid,
        "config_path": str(config.base_dir),
        "data_dir": str(config.data_dir),
        "logs_dir": str(config.logs_dir)
    }

# Config API Endpoints
router = APIRouter(prefix="/api/v1/config", tags=["config"])

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

@router.post("/start_match")
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

@router.post("/stop_match")
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

@router.get("/matches")
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

@router.get("/match/{match_id}")
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