import os
import sys
import subprocess
from pathlib import Path
import urllib.request


project_url = "https://github.com/Denie-Dev/pyterminal"
install_dir = Path.home() / "pyterminal"

print("Downloading PyTerminal...")
try:
    subprocess.run(
        ["git", "clone", project_url, str(install_dir)],
        check=True
    )
    print("PyTerminal downloaded")
except subprocess.CalledProcessError as e:
    print(f"Download failed: {e}")