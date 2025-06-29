#!/usr/bin/env python3
"""
GhostLAN SimWorld Demo
Demonstrates the core functionality of the GhostLAN SimWorld platform
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any

# Import core modules
from duality_scene.simulation import SimulationManager, SimulationConfig
from ghostlan_core.anticheat import AntiCheatEngine
from analytics.pipeline import AnalyticsPipeline
from analytics.match_recorder import MatchRecorder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GhostLANDemo:
    """Demo class for GhostLAN SimWorld"""
    
    def __init__(self):
        self.simulation = None
        self.anticheat = None
        self.analytics = None
        self.match_recorder = None
        self.demo_results = {}
    
    async def initialize(self):
        """Initialize all demo components"""
        logger.info("🚀 Initializing GhostLAN SimWorld Demo...")
        
        try:
            # Initialize simulation
            logger.info("🤖 Initializing Duality AI Simulation...")
            self.simulation = SimulationManager()
            await self.simulation.initialize()
            
            # Initialize anti-cheat engine
            logger.info("🛡️ Initializing Anti-Cheat Engine...")
            self.anticheat = AntiCheatEngine()
            await self.anticheat.initialize()
            
            # Initialize analytics pipeline
            logger.info("📊 Initializing Analytics Pipeline...")
            self.analytics = AnalyticsPipeline()
            await self.analytics.initialize()
            
            # Initialize match recorder
            logger.info("🎬 Initializing Match Recorder...")
            # if hasattr(self, 'match_recorder'):
            #     await self.match_recorder.initialize()
            
            logger.info("✅ Demo components initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize demo: {e}")
            raise
    
    async def run_basic_demo(self):
        """Run basic demo with 5v5 match simulation"""
        logger.info("🎮 Starting Basic Demo - 5v5 Match Simulation")
        
        # Configure simulation
        config = SimulationConfig(
            num_agents=10,  # 5v5
            match_duration=120,  # 2 minutes for demo
            cheat_probability=0.3,  # 30% chance of cheat behavior
            voice_enabled=True,
            recording_enabled=True
        )
        
        if self.simulation is not None and hasattr(self.simulation, 'config'):
            self.simulation.config = config
        
        # Start match
        if self.simulation is not None and hasattr(self.simulation, 'start_match'):
            match_id = await self.simulation.start_match("DEMO_MATCH_001")
            logger.info(f"🏆 Match started: {match_id}")
        
        # Wait for match to complete
        await asyncio.sleep(config.match_duration + 5)  # Extra time for cleanup
        
        # Get results
        await self._collect_demo_results(match_id)
        
        logger.info("✅ Basic demo completed!")
    
    async def run_advanced_demo(self):
        """Run advanced demo with multiple scenarios"""
        logger.info("🎯 Starting Advanced Demo - Multiple Scenarios")
        
        scenarios = [
            {
                "name": "Normal Match",
                "config": SimulationConfig(
                    num_agents=10,
                    match_duration=60,
                    cheat_probability=0.0,
                    voice_enabled=True
                )
            },
            {
                "name": "High Cheat Rate",
                "config": SimulationConfig(
                    num_agents=10,
                    match_duration=60,
                    cheat_probability=0.7,
                    voice_enabled=True
                )
            },
            {
                "name": "Network Stress Test",
                "config": SimulationConfig(
                    num_agents=20,
                    match_duration=90,
                    cheat_probability=0.2,
                    voice_enabled=True
                )
            }
        ]
        
        for i, scenario in enumerate(scenarios):
            logger.info(f"🎮 Running scenario {i+1}: {scenario['name']}")
            
            # Configure simulation
            if self.simulation is not None and hasattr(self.simulation, 'config'):
                self.simulation.config = scenario["config"]
            
            # Start match
            if self.simulation is not None and hasattr(self.simulation, 'start_match'):
                match_id = f"DEMO_ADV_{i+1:03d}"
                await self.simulation.start_match(match_id)
            
            # Wait for match to complete
            await asyncio.sleep(scenario["config"].match_duration + 5)
            
            # Collect results
            await self._collect_demo_results(match_id, scenario["name"])
        
        logger.info("✅ Advanced demo completed!")
    
    async def _collect_demo_results(self, match_id: str, scenario_name: str = "Basic Demo"):
        """Collect and store demo results"""
        logger.info(f"📊 Collecting results for {scenario_name}")
        
        # Get simulation status
        if self.simulation is not None and hasattr(self.simulation, 'get_status'):
            sim_status = self.simulation.get_status()
        
        # Get events
        if self.simulation is not None and hasattr(self.simulation, 'get_events'):
            events = self.simulation.get_events()
        
        # Get analytics data
        if self.analytics is not None and hasattr(self.analytics, 'get_match_statistics'):
            analytics_data = self.analytics.get_match_statistics(match_id)
        
        # Store results
        self.demo_results[scenario_name] = {
            "match_id": match_id,
            "simulation_status": sim_status,
            "total_events": len(events),
            "analytics_data": analytics_data,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"📈 Results collected for {scenario_name}: {len(events)} events")
    
    async def run_anti_cheat_demo(self):
        """Run anti-cheat specific demo"""
        logger.info("🛡️ Starting Anti-Cheat Demo")
        
        # Create agents with known cheat behaviors
        cheat_scenarios = [
            {"name": "Aimbot Detection", "cheat_type": "aimbot"},
            {"name": "Wallhack Detection", "cheat_type": "wallhack"},
            {"name": "Speedhack Detection", "cheat_type": "speedhack"},
            {"name": "ESP Detection", "cheat_type": "esp"},
            {"name": "Macro Detection", "cheat_type": "macro"}
        ]
        
        for scenario in cheat_scenarios:
            logger.info(f"🔍 Testing {scenario['name']}")
            
            # Configure simulation with specific cheat
            config = SimulationConfig(
                num_agents=6,  # Smaller match for focused testing
                match_duration=30,  # Short match
                cheat_probability=0.5,
                voice_enabled=False
            )
            
            if self.simulation is not None and hasattr(self.simulation, 'config'):
                self.simulation.config = config
            
            # Start match
            if self.simulation is not None and hasattr(self.simulation, 'start_match'):
                match_id = f"ANTICHEAT_{scenario['cheat_type'].upper()}"
                await self.simulation.start_match(match_id)
            
            # Wait for match
            await asyncio.sleep(config.match_duration + 5)
            
            # Analyze results
            await self._analyze_anti_cheat_results(match_id, scenario)
        
        logger.info("✅ Anti-cheat demo completed!")
    
    async def _analyze_anti_cheat_results(self, match_id: str, scenario: Dict[str, str]):
        """Analyze anti-cheat detection results"""
        if self.simulation is not None and hasattr(self.simulation, 'get_events'):
            events = self.simulation.get_events(event_type="suspicious_behavior")
        
        if self.simulation is not None and hasattr(self.simulation, 'get_events'):
            detection_count = len(events)
            logger.info(f"🛡️ {scenario['name']}: {detection_count} suspicious behaviors detected")
        
        # Store anti-cheat results
        if "anti_cheat_results" not in self.demo_results:
            self.demo_results["anti_cheat_results"] = {}
        
        if self.simulation is not None and hasattr(self.simulation, 'get_events'):
            self.demo_results["anti_cheat_results"][scenario["name"]] = {
                "match_id": match_id,
                "cheat_type": scenario["cheat_type"],
                "detections": detection_count,
                "events": [e["data"] for e in events[:5]],  # First 5 events
                "timestamp": datetime.now().isoformat()
            }
    
    async def run_analytics_demo(self):
        """Run analytics specific demo"""
        logger.info("📊 Starting Analytics Demo")
        
        # Generate synthetic data
        await self._generate_synthetic_data()
        
        # Run analytics queries
        analytics_results = await self._run_analytics_queries()
        
        self.demo_results["analytics_demo"] = analytics_results
        
        logger.info("✅ Analytics demo completed!")
    
    async def _generate_synthetic_data(self):
        """Generate synthetic data for analytics demo"""
        logger.info("📈 Generating synthetic analytics data...")
        
        # Generate multiple matches
        for i in range(5):
            match_id = f"SYNTHETIC_{i+1:03d}"
            
            # Add match start event
            if self.analytics is not None and hasattr(self.analytics, 'add_event'):
                await self.analytics.add_event(
                    "match_start",
                    "SYSTEM",
                    match_id,
                    {
                        "map_name": f"map_{i+1}",
                        "game_mode": "5v5",
                        "player_count": 10
                    }
                )
            
            # Add player events
            for j in range(10):
                player_id = f"PLAYER_{j+1:03d}"
                
                if self.analytics is not None and hasattr(self.analytics, 'add_event'):
                    await self.analytics.add_event(
                        "player_join",
                        player_id,
                        match_id,
                        {"team": "T" if j < 5 else "CT"}
                    )
                
                # Add some actions
                for k in range(20):
                    if self.analytics is not None and hasattr(self.analytics, 'add_event'):
                        await self.analytics.add_event(
                            "agent_action",
                            player_id,
                            match_id,
                            {
                                "action_type": "shoot",
                                "kills": k % 3,
                                "accuracy": 0.7 + (k * 0.01),
                                "damage": 50 + (k * 5)
                            }
                        )
            
            # Add match end event
            if self.analytics is not None and hasattr(self.analytics, 'add_event'):
                await self.analytics.add_event(
                    "match_end",
                    "SYSTEM",
                    match_id,
                    {"duration": 300, "winner": "T"}
                )
    
    async def _run_analytics_queries(self):
        """Run various analytics queries"""
        logger.info("🔍 Running analytics queries...")
        
        results = {}
        
        # Get player statistics
        if self.analytics is not None and hasattr(self.analytics, 'get_player_statistics'):
            player_stats = self.analytics.get_player_statistics("PLAYER_001", limit=5)
            results["player_stats"] = player_stats
        
        # Get match statistics
        if self.analytics is not None and hasattr(self.analytics, 'get_match_statistics'):
            match_stats = self.analytics.get_match_statistics("SYNTHETIC_001")
            results["match_stats"] = match_stats
        
        # Get network statistics
        if self.analytics is not None and hasattr(self.analytics, 'get_network_statistics'):
            network_stats = self.analytics.get_network_statistics("SYNTHETIC_001")
            results["network_stats"] = network_stats
        
        return results
    
    def generate_demo_report(self) -> Dict[str, Any]:
        """Generate comprehensive demo report"""
        logger.info("📋 Generating demo report...")
        
        report = {
            "demo_info": {
                "title": "GhostLAN SimWorld Demo Report",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
                "total_scenarios": len(self.demo_results)
            },
            "scenarios": self.demo_results,
            "summary": {
                "total_matches": len([k for k in self.demo_results.keys() if "DEMO" in k]),
                "total_events": sum(
                    len(self.demo_results[k].get("total_events", 0)) 
                    for k in self.demo_results.keys() 
                    if isinstance(self.demo_results[k], dict)
                ),
                "anti_cheat_detections": len(
                    self.demo_results.get("anti_cheat_results", {})
                )
            }
        }
        
        return report
    
    async def shutdown(self):
        """Shutdown demo components"""
        logger.info("🛑 Shutting down GhostLAN SimWorld Demo...")
        
        if self.simulation is not None and hasattr(self.simulation, 'shutdown'):
            await self.simulation.shutdown()
        if self.anticheat is not None and hasattr(self.anticheat, 'shutdown'):
            await self.anticheat.shutdown()
        if self.analytics is not None and hasattr(self.analytics, 'shutdown'):
            await self.analytics.shutdown()
        # if self.match_recorder is not None and hasattr(self.match_recorder, 'shutdown'):
        #     await self.match_recorder.shutdown()
        
        logger.info("✅ Demo shutdown complete")

async def main():
    """Main demo function"""
    demo = GhostLANDemo()
    
    try:
        # Initialize demo
        await demo.initialize()
        
        # Run demos
        await demo.run_basic_demo()
        await demo.run_advanced_demo()
        await demo.run_anti_cheat_demo()
        await demo.run_analytics_demo()
        
        # Generate report
        report = demo.generate_demo_report()
        
        # Save report
        with open("demo_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info("📄 Demo report saved to demo_report.json")
        
        # Print summary
        print("\n" + "="*60)
        print("🎮 GHOSTLAN SIMWORLD DEMO COMPLETED")
        print("="*60)
        print(f"📊 Total scenarios: {report['summary']['total_scenarios']}")
        print(f"🏆 Total matches: {report['summary']['total_matches']}")
        print(f"📈 Total events: {report['summary']['total_events']}")
        print(f"🛡️ Anti-cheat detections: {report['summary']['anti_cheat_detections']}")
        print("="*60)
        print("📄 Full report saved to: demo_report.json")
        print("🌐 Access web interface at: http://localhost:8000")
        print("📚 API documentation at: http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise
    finally:
        await demo.shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 