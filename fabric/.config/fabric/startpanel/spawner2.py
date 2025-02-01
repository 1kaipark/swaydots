import os
import sys
import time
from multiprocessing import Process, Pipe
from fabric import Application
from fabric.utils import get_relative_path
from startpanel import StartPanel
from i3ipc import Connection

SCRIPT_NAME = "startpanel"
LOCKFILE = f"/tmp/{SCRIPT_NAME}.pid"

def get_focused_monitor() -> int:
    monitors = Connection().get_outputs()
    if len(monitors) == 1:
        return 0
    for i in range(len(monitors)):
        if monitors[i].focused:
            return i 
    return 0

def spawn_panel(conn):
    start_panel = StartPanel()
    start_panel.monitor = get_focused_monitor()
    app = Application("start-panel", start_panel)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    conn.send("ready")  # Notify the parent process that the panel is ready
    app.run()

def is_locked() -> bool:
    if os.path.exists(LOCKFILE):
        with open(LOCKFILE, "r") as f:
            pid = int(f.read().strip())
            try:
                os.kill(pid, 0)  # Check if the process is running
                return True
            except ProcessLookupError:
                pass
    return False

def lock() -> None:
    with open(LOCKFILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock() -> None:
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def daemon_process():
    parent_conn, child_conn = Pipe()
    p = Process(target=spawn_panel, args=(child_conn,))
    p.start()
    parent_conn.recv()  # Wait for the panel to be ready
    lock()
    p.join()  # Wait for the process to finish
    remove_lock()

if __name__ == "__main__":
    if is_locked():
        with open(LOCKFILE, "r") as f:
            pid = int(f.read().strip())
            os.kill(pid, 9)  # SIGKILL
        remove_lock()
    else:
        daemon_process()
