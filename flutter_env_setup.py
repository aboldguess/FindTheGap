"""
flutter_env_setup.py
====================
Mini README
-----------
This script automates the setup of the Flutter SDK on Windows and Linux. It attempts the preferred
installation method for each platform and falls back to a secondary plan if the first attempt fails.
A small Tkinter GUI provides real‑time feedback so users can follow progress without reading external
documentation.

Structure
---------
- `SetupGUI` class builds the interface and runs the setup in a background thread.
- Platform‑specific functions handle installation logic for Windows and Linux with fallback strategies.
- Logging is written to `flutter_setup.log` for debugging.

Usage
------
Run with Python 3:

```bash
python flutter_env_setup.py
```

The GUI will prompt you to start the setup.
"""

from __future__ import annotations
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext
from urllib.request import urlopen, urlretrieve

LOG_FILE = "flutter_setup.log"
logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# GUI COMPONENTS
class SetupGUI(tk.Tk):
    """Simple Tkinter GUI that runs the setup and displays progress."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Flutter Environment Setup")
        self.geometry("700x400")
        self.resizable(False, False)
        self.create_widgets()
        self.log("Click 'Start Setup' to begin installing Flutter.")

    def create_widgets(self) -> None:
        self.text = scrolledtext.ScrolledText(self, state="disabled")
        self.text.pack(expand=True, fill="both", padx=5, pady=5)

        self.start_button = tk.Button(self, text="Start Setup", command=self.run_setup)
        self.start_button.pack(pady=5)

    def log(self, message: str) -> None:
        logging.info(message)
        self.text.configure(state="normal")
        self.text.insert(tk.END, message + "\n")
        self.text.configure(state="disabled")
        self.text.see(tk.END)

    def run_setup(self) -> None:
        self.start_button.configure(state="disabled")
        thread = threading.Thread(target=self.setup)
        thread.start()

    def setup(self) -> None:
        system = platform.system().lower()
        self.log(f"Detected platform: {system}")
        try:
            if system == "windows":
                install_flutter_windows(self.log)
            elif system in {"linux", "darwin"}:  # macOS falls back to manual download similar to Linux
                install_flutter_linux(self.log)
            else:
                self.log("Unsupported OS for automated setup. Please install Flutter manually.")
        except Exception as exc:  # pylint: disable=broad-except
            self.log(f"Setup encountered an unexpected error: {exc}")
        finally:
            self.log("Setup complete. Review log for details.")
            self.start_button.configure(state="normal")


# HELPER FUNCTIONS

def run_command(cmd: list[str], log: callable) -> bool:
    """Run a system command, logging output; return True on success."""
    log(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False, text=True, capture_output=True)
        if result.stdout:
            log(result.stdout.strip())
        if result.stderr:
            log(result.stderr.strip())
        return result.returncode == 0
    except FileNotFoundError:
        log(f"Command not found: {cmd[0]}")
        return False


def get_latest_release(platform_name: str, log: callable) -> tuple[str, str]:
    """Fetch latest stable Flutter release URL and SHA256 for given platform."""
    releases_url = f"https://storage.googleapis.com/flutter_infra_release/releases/releases_{platform_name}.json"
    log(f"Fetching release info from {releases_url}")
    with urlopen(releases_url) as response:
        data = json.load(response)
    latest = next(r for r in data["releases"] if r["channel"] == "stable")
    version = latest["version"]
    archive = latest["archive"]
    sha256 = latest["sha256"]
    base = "https://storage.googleapis.com/flutter_infra_release/releases/"
    download_url = base + archive
    log(f"Latest stable version: {version}")
    return download_url, sha256


def download_and_verify(url: str, sha256: str, dest: Path, log: callable) -> Path:
    """Download file to dest and verify SHA256."""
    log(f"Downloading {url}")
    tmp_file = dest / Path(url).name
    urlretrieve(url, tmp_file)
    log("Download complete; verifying checksum")
    h = hashlib.sha256()
    with open(tmp_file, "rb") as f:  # noqa: PTH123
        h.update(f.read())
    if h.hexdigest() != sha256:
        raise ValueError("Checksum mismatch; aborting")
    log("Checksum verified")
    return tmp_file


def extract_zip(zip_path: Path, target_dir: Path, log: callable) -> None:
    """Extract zip file to target directory."""
    log(f"Extracting {zip_path} to {target_dir}")
    shutil.unpack_archive(zip_path, target_dir)
    log("Extraction complete")


def install_flutter_windows(log: callable) -> None:
    """Install Flutter on Windows with fallback strategies."""
    if run_command(["winget", "install", "-e", "--id=Flutter.Flutter"], log):
        log("Flutter installed via winget.")
        return
    log("winget install failed; attempting Chocolatey")
    if not shutil.which("choco"):
        run_command([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
            "Set-ExecutionPolicy Bypass -Scope Process -Force;"
            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;"
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))",
        ], log)
    if run_command(["choco", "install", "flutter", "--pre", "-y"], log):
        log("Flutter installed via Chocolatey.")
        return
    log("Chocolatey install failed; attempting manual download")
    tmp = Path(tempfile.mkdtemp())
    url, sha = get_latest_release("windows", log)
    zip_path = download_and_verify(url, sha, tmp, log)
    extract_zip(zip_path, Path("C:/src"), log)
    run_command(["setx", "PATH", f"C:/src/flutter/bin;%PATH%"], log)
    log("Manual installation completed; please restart terminal to use flutter.")


def install_flutter_linux(log: callable) -> None:
    """Install Flutter on Linux with fallback strategies."""
    if run_command(["sudo", "snap", "install", "flutter", "--classic"], log):
        log("Flutter installed via snap.")
        return
    log("snap install failed; attempting manual download")
    tmp = Path(tempfile.mkdtemp())
    url, sha = get_latest_release("linux", log)
    zip_path = download_and_verify(url, sha, tmp, log)
    target = Path.home() / "flutter"
    extract_zip(zip_path, target, log)
    bashrc = Path.home() / ".bashrc"
    path_cmd = "export PATH=\"$HOME/flutter/bin:$PATH\""
    with open(bashrc, "a", encoding="utf-8") as f:  # noqa: PTH123
        f.write(f"\n# Added by flutter_env_setup.py\n{path_cmd}\n")
    log("Manual installation completed; reload your shell to use flutter.")


def main() -> None:
    gui = SetupGUI()
    gui.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main()
