import os
import signal
import asyncio
from pathlib import Path
from fabric import Application
from fabric.utils import get_relative_path
from startpanel import StartPanel
from i3ipc import Connection

SCRIPT_NAME = "startpanel"
LOCKFILE = f"/tmp/{SCRIPT_NAME}.pid"

async def get_focused_monitor() -> int:
    """Asynchronously get the focused monitor index."""
    conn = Connection()
    monitors = conn.get_outputs()
    return next((i for i, monitor in enumerate(monitors) if monitor.focused), 0)

async def spawn() -> None:
    """Asynchronously spawn the StartPanel application."""
    start_panel = StartPanel()
    start_panel.monitor = await get_focused_monitor()
    app = Application("start-panel", start_panel)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    app.run()

def is_locked() -> bool:
    """Check if the process is already running using the lock file."""
    if not os.path.exists(LOCKFILE):
        return False
    try:
        pid = int(Path(LOCKFILE).read_text().strip())
        os.kill(pid, 0)  # Check if the process is running
        return True
    except (ProcessLookupError, ValueError):
        return False

def lock() -> None:
    """Create a lock file with the current process ID."""
    Path(LOCKFILE).write_text(str(os.getpid()))

def remove_lock() -> None:
    """Remove the lock file if it exists."""
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

async def main() -> None:
    """Asynchronous main function to handle process locking and toggling."""
    if is_locked():
        # Kill the running process
        pid = int(Path(LOCKFILE).read_text().strip())
        os.kill(pid, signal.SIGKILL)
        remove_lock()
    else:
        lock()
        try:
            await spawn()
        finally:
            remove_lock()

if __name__ == "__main__":
    asyncio.run(main())
