import os
import sys
import subprocess
from pathlib import Path

import urllib.request

class PyTerminalInstaller:
    def __init__(self):
        self.project_url = "https://github.com/Denie-Dev/pyterminal"
        self.install_dir = Path.home() / ".pyterminal"
    
    def download_project(self):
        """Clone or download the PyTerminal project"""
        print("Downloading PyTerminal...")
        try:
            subprocess.run(
                ["git", "clone", self.project_url, str(self.install_dir)],
                check=True
            )
            print("✓ Project downloaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Download failed: {e}")
            return False
        return True
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("Installing dependencies...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", 
                 self.install_dir / "requirements.txt"],
                check=True
            )
            print("✓ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Installation failed: {e}")
            return False
    
    def run(self):
        """Execute the installation"""
        if not self.download_project():
            return False
        if not self.install_dependencies():
            return False
        print("\n✓ PyTerminal installed successfully!")
        return True

if __name__ == "__main__":
    installer = PyTerminalInstaller()
    installer.run()