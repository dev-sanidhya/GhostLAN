#!/usr/bin/env python3
"""
Installation script for GhostLAN SimWorld Backend
Helps resolve dependency conflicts and install required packages
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main installation function"""
    print("🚀 GhostLAN SimWorld Backend Installation")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️ Failed to upgrade pip, continuing anyway...")
    
    # Try minimal installation first
    print("\n📦 Installing minimal dependencies...")
    if run_command(f"{sys.executable} -m pip install -r requirements-minimal.txt", "Installing minimal dependencies"):
        print("✅ Minimal installation successful!")
        
        # Try to install additional packages one by one
        additional_packages = [
            "matplotlib==3.10.1",
            "scikit-learn==1.6.1",
            "torch==2.7.1",
            "opencv-python==4.11.0.86",
            "redis==6.2.0",
            "pymongo==4.13.1",
            "google-api-python-client==2.172.0",
            "openai==1.68.2"
        ]
        
        print("\n📦 Installing additional packages...")
        for package in additional_packages:
            if run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
                print(f"✅ {package} installed")
            else:
                print(f"⚠️ Failed to install {package}, skipping...")
        
        print("\n🎉 Installation completed!")
        print("\nNext steps:")
        print("1. Run: python quick_test.py")
        print("2. Run: python demo.py")
        print("3. Run: python main.py")
        
    else:
        print("\n❌ Minimal installation failed!")
        print("\nTroubleshooting:")
        print("1. Try: python -m pip install --upgrade pip")
        print("2. Try: python -m pip install -r requirements-minimal.txt --no-deps")
        print("3. Check your Python environment")
        sys.exit(1)

if __name__ == "__main__":
    main() 