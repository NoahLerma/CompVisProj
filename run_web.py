"""
Simple launcher for the Streamlit web app
"""

import subprocess
import sys
import os

def main():
    print("Starting Ollama Vision Tester Web App...")
    print("Make sure Ollama server is running: ollama serve")
    print("Make sure you have a vision model: ollama pull llava")
    print("\nLaunching web browser...")
    
    # Run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "web_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit: {e}")
        print("Make sure streamlit is installed: pip install streamlit")
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
