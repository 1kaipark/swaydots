from fabric import Application 
from fabric.utils import get_relative_path

from startpanel.startpanel import StartPanel 

import setproctitle

if __name__ == "__main__":
    panel = StartPanel()
    app = Application("start-panel", panel)

    app.run()

