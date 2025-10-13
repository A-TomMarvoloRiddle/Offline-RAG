#!/usr/bin/env python3
"""
Multimodal RAG System - SIH 2025 Demo Launcher
Simple script to launch the Streamlit application
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import PIL
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def launch_app():
    """Launch the Streamlit application"""
    if not check_requirements():
        return
    
    print("🚀 Launching Multimodal RAG System Demo...")
    print("📱 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thank you for trying the Multimodal RAG System!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching the app: {e}")
        print("Make sure you're in the correct directory with app.py")

if __name__ == "__main__":
    launch_app()
