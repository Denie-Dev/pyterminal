import os
import sys
import subprocess
from pathlib import Path
import urllib.request


self.project_url = "https://github.com/Denie-Dev/pyterminal"
self.install_dir = Path.home() / "pyterminal"

print("Downloading PyTerminal...")
try:
    subprocess.run(
        ["git", "clone", self.project_url, str(self.install_dir)],
        check=True
    )
    print("PyTerminal downloaded")
except subprocess.CalledProcessError as e:
    print(f"Download failed: {e}")
    return False
return True
