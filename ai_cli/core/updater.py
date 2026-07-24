"""Version checking and self-update functionality."""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Optional, Callable

from ai_cli import __version__


PYPI_JSON_URL = "https://pypi.org/pypi/ai-cli-launcher/json"


class UpdateInfo:
    """Information about an available update."""
    def __init__(self):
        self.latest_version: Optional[str] = None
        self.is_update_available: bool = False
        self.error: Optional[str] = None
        self.current_version: str = __version__
        self._checked: bool = False

    @property
    def checked(self) -> bool:
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        self._checked = value


def _is_newer(latest: str) -> bool:
    """Compare two version strings using tuple comparison."""
    def _parts(v: str):
        parts = []
        for x in v.split("."):
            try:
                parts.append(int(x))
            except ValueError:
                parts.append(0)
        return parts
    current = _parts(__version__)
    latest_p = _parts(latest)
    while len(current) < len(latest_p):
        current.append(0)
    while len(latest_p) < len(current):
        latest_p.append(0)
    return latest_p > current


def check_latest_version(on_done: Optional[Callable[[UpdateInfo], None]] = None) -> UpdateInfo:
    """Synchronously check PyPI for the latest version (runs in calling thread)."""
    info = UpdateInfo()
    try:
        import urllib.request
        req = urllib.request.Request(
            PYPI_JSON_URL,
            headers={"User-Agent": f"ai-cli-launcher/{__version__}"},
        )
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read().decode("utf-8"))
        latest = data.get("info", {}).get("version", "")
        if latest:
            info.latest_version = latest
            info.is_update_available = _is_newer(latest)
    except Exception as e:
        info.error = str(e)
    info.checked = True
    if on_done:
        on_done(info)
    return info


def check_latest_version_async(on_done: Optional[Callable[[UpdateInfo], None]] = None) -> threading.Thread:
    """Check PyPI for latest version in a background daemon thread."""
    def _run():
        info = check_latest_version()
        if on_done:
            on_done(info)
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t


def _get_pip_command() -> str:
    """Detect the right pip command for the current Python environment."""
    python = sys.executable
    pipx_marker = Path(sys.prefix) / "pipx_metadata.json"
    if pipx_marker.exists():
        return "pipx upgrade ai-cli-launcher"
    return f'"{python}" -m pip install --upgrade ai-cli-launcher'


def perform_upgrade():
    """Create a temporary wrapper script and launch it, then exit the current process."""
    pip_cmd = _get_pip_command()

    if sys.platform == "win32":
        script = _create_windows_script(pip_cmd)
        subprocess.Popen(
            ["cmd.exe", "/c", script],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            close_fds=True,
        )
    else:
        script = _create_unix_script(pip_cmd)
        subprocess.Popen(
            ["sh", script],
            start_new_session=True,
            close_fds=True,
        )

    print("Upgrading ai-cli-launcher... The new version will start automatically.")
    sys.exit(0)


def _create_windows_script(pip_cmd: str) -> str:
    """Create a temporary Windows batch script that upgrades and relaunches."""
    content = f"""@echo off
title AI-CLI Updater
echo Checking current version...
timeout /t 1 /nobreak >nul
echo.
echo ========================================
echo   Upgrading ai-cli-launcher...
echo ========================================
echo.
{pip_cmd}
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Upgrade complete! Starting ai-cli...
    echo ========================================
    echo.
    ai-cli
) else (
    echo.
    echo [ERROR] Upgrade failed.
    echo Please try manually: pip install --upgrade ai-cli-launcher
    echo.
    pause
)
del "%~f0"
"""
    path = os.path.join(tempfile.gettempdir(), f"ai-cli-update-{uuid.uuid4().hex[:8]}.bat")
    with open(path, "w", newline="\r\n") as f:
        f.write(content)
    return path


def _create_unix_script(pip_cmd: str) -> str:
    """Create a temporary shell script that upgrades and relaunches."""
    content = f"""#!/bin/sh
sleep 1
echo ""
echo "========================================"
echo "  Upgrading ai-cli-launcher..."
echo "========================================"
echo ""
{pip_cmd}
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  Upgrade complete! Starting ai-cli..."
    echo "========================================"
    echo ""
    ai-cli
else
    echo ""
    echo "[ERROR] Upgrade failed."
    echo "Please try manually: pip install --upgrade ai-cli-launcher"
    echo ""
    read -p "Press Enter to exit..."
fi
rm -- "$0"
"""
    path = os.path.join(tempfile.gettempdir(), f"ai-cli-update-{uuid.uuid4().hex[:8]}.sh")
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, 0o755)
    return path
