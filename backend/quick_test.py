#!/usr/bin/env python3
"""
Quick Test Script for GhostLAN SimWorld Backend
Tests core functionality and components
"""

import asyncio
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_imports():
    """Test that all modules can be imported"""
    logger.info("🧪 Testing module imports...")
    
    try:
        # Test core imports
        from duality_scene.simulation import SimulationManager
        from duality_scene.agents import AIAgent, AgentBehavior
        from duality_scene.environment import LANEnvironment
        from duality_scene.voice_simulation import VoiceSimulation
        
        from ghostlan_core.anticheat import AntiCheatEngine
        
        from analytics.pipeline import AnalyticsPipeline
        from analytics.match_recorder import MatchRecorder
        
        from api.server import start_api_server
        
        logger.info("✅ All imports successful!")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False

async def test_simulation():
    """Test simulation functionality"""
    logger.info("🤖 Testing simulation...")
    
    try:
        from duality_scene.simulation import SimulationManager
        
        sim = SimulationManager()
        await sim.initialize()
        
        # Test basic functionality
        status = sim.get_status()
        assert status["state"] == "idle"
        
        await sim.shutdown()
        logger.info("✅ Simulation test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Simulation test failed: {e}")
        return False

async def test_agents():
    """Test AI agents"""
    logger.info("👥 Testing AI agents...")
    
    try:
        from duality_scene.agents import AIAgent, AgentBehavior, CheatBehavior
        
        # Create normal agent
        normal_agent = AIAgent(
            agent_id="TEST_001",
            name="TestAgent",
            behavior=AgentBehavior.NORMAL,
            skill_level=5
        )
        
        # Create cheat agent
        cheat_agent = AIAgent(
            agent_id="TEST_002",
            name="CheatAgent",
            behavior=AgentBehavior.CHEAT,
            cheat_type=CheatBehavior.AIMBOT,
            skill_level=8
        )
        
        await normal_agent.initialize()
        await cheat_agent.initialize()
        
        # Test agent status
        normal_status = normal_agent.get_status()
        cheat_status = cheat_agent.get_status()
        
        assert normal_status["behavior"] == "normal"
        assert cheat_status["behavior"] == "cheat"
        assert cheat_status["cheat_type"] == "aimbot"
        
        await normal_agent.shutdown()
        await cheat_agent.shutdown()
        
        logger.info("✅ AI agents test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ AI agents test failed: {e}")
        return False

async def test_environment():
    """Test LAN environment"""
    logger.info("🌐 Testing LAN environment...")
    
    try:
        from duality_scene.environment import LANEnvironment
        
        env = LANEnvironment()
        await env.initialize()
        
        # Test network conditions
        conditions = await env.get_network_conditions()
        assert "latency" in conditions
        assert "packet_loss" in conditions
        
        # Test agent connection
        await env.connect_agent("TEST_AGENT")
        await env.disconnect_agent("TEST_AGENT")
        
        await env.shutdown()
        
        logger.info("✅ LAN environment test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ LAN environment test failed: {e}")
        return False

async def test_anticheat():
    """Test anti-cheat engine"""
    logger.info("🛡️ Testing anti-cheat engine...")
    
    try:
        from ghostlan_core.anticheat import AntiCheatEngine
        
        engine = AntiCheatEngine()
        await engine.initialize()
        
        # Test basic functionality
        status = engine.get_status()
        assert "initialized" in status
        
        await engine.shutdown()
        
        logger.info("✅ Anti-cheat engine test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Anti-cheat engine test failed: {e}")
        return False

async def test_analytics():
    """Test analytics pipeline"""
    logger.info("📊 Testing analytics pipeline...")
    
    try:
        from analytics.pipeline import AnalyticsPipeline
        
        pipeline = AnalyticsPipeline()
        await pipeline.initialize()
        
        # Test adding events
        await pipeline.add_event(
            "test_event",
            "TEST_PLAYER",
            "TEST_MATCH",
            {"test_data": "value"}
        )
        
        # Test getting statistics
        stats = pipeline.get_match_statistics("TEST_MATCH")
        
        await pipeline.shutdown()
        
        logger.info("✅ Analytics pipeline test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Analytics pipeline test failed: {e}")
        return False

async def test_api():
    """Test API server"""
    logger.info("🌐 Testing API server...")
    
    try:
        from api.server import start_api_server
        
        app = start_api_server()
        
        # Test basic endpoints
        assert app is not None
        
        logger.info("✅ API server test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ API server test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    logger.info("🚀 Starting GhostLAN SimWorld Quick Tests...")
    
    tests = [
        ("Module Imports", test_imports),
        ("Simulation", test_simulation),
        ("AI Agents", test_agents),
        ("LAN Environment", test_environment),
        ("Anti-Cheat Engine", test_anticheat),
        ("Analytics Pipeline", test_analytics),
        ("API Server", test_api)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            success = await test_func()
            results[test_name] = "PASS" if success else "FAIL"
            if success:
                passed += 1
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results[test_name] = "CRASH"
    
    # Print results
    logger.info(f"\n{'='*60}")
    logger.info("🎯 TEST RESULTS SUMMARY")
    logger.info(f"{'='*60}")
    
    for test_name, result in results.items():
        status_icon = "✅" if result == "PASS" else "❌"
        logger.info(f"{status_icon} {test_name}: {result}")
    
    logger.info(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Backend is ready to use.")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed. Please check the logs.")
        return False

async def main():
    """Main test function"""
    try:
        success = await run_all_tests()
        
        if success:
            print("\n" + "="*60)
            print("🎉 GHOSTLAN SIMWORLD BACKEND READY!")
            print("="*60)
            print("🚀 To start the application:")
            print("   python main.py")
            print("\n🌐 Access the web interface:")
            print("   http://localhost:8000")
            print("\n📚 View API documentation:")
            print("   http://localhost:8000/docs")
            print("\n🎮 Run the demo:")
            print("   python demo.py")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ BACKEND TESTS FAILED")
            print("="*60)
            print("Please check the logs above for details.")
            print("Make sure all dependencies are installed:")
            print("   pip install -r requirements.txt")
            print("="*60)
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 