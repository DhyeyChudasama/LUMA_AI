#!/usr/bin/env python3
"""
Setup script for the TTS Server
This script helps install dependencies and set up the environment
"""

import os
import sys
import subprocess
import shutil

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

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    # Check if pip is available
    if not shutil.which("pip"):
        print("❌ pip not found. Please install pip first.")
        return False
    
    # Install from requirements.txt
    if os.path.exists("requirements.txt"):
        return run_command("pip install -r requirements.txt", "Installing packages from requirements.txt")
    else:
        print("❌ requirements.txt not found")
        return False

def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_template.txt"):
        try:
            shutil.copy("env_template.txt", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your Murf API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_template.txt not found")
        return False

def main():
    """Main setup function"""
    print("🚀 TTS Server Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed during environment setup")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your Murf API key")
    print("2. Run the server: python main.py")
    print("3. Open http://localhost:8000/docs for API documentation")
    print("4. Open test_page.html in your browser to test the TTS functionality")
    print("\n🔑 Get your Murf API key from: https://murf.ai/")

if __name__ == "__main__":
    main() 