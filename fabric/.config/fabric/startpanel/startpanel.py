"""side panel example, contains info about the system"""

import os
import time
import psutil
from loguru import logger
from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.datetime import DateTime
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils import invoke_repeater, get_relative_path

from widgets.media import NowPlaying
from widgets.power import PowerMenu
from widgets.launcher_menu import LauncherMenu

import pyfiglet

def get_profile_picture_path() -> str | None:
    path = os.path.expanduser("~/Pictures/profile.jpg")
    if not os.path.exists(path):
        path = os.path.expanduser("~/.face")
    if not os.path.exists(path):
        logger.warning(
            "put yo fuckin picture in ~/Pictures/profile.jpg or ~/.face"
        )
        path = None
    return path


class StartPanel(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            title="fabric-overlay",
            anchor="top left",
            margin="10px 10px 10px 10px",
            exclusivity="none",
            visible=False,
            all_visible=False,
            keyboard_mode="on-demand",
            on_key_press_event=lambda _,event: self.application.quit() if event.keyval == 65307 else True, # handle ESC = exit
            **kwargs,
        )

        self.profile_pic = Box(
            name="profile-pic",
            style=f"background-image: url(\"file://{get_profile_picture_path() or ''}\")",
        )
        self.uptime_label = Label(label=f"{self.get_current_uptime()}")

        self.header = Box(
            spacing=14,
            name="header",
            orientation="h",
            children=[
                self.profile_pic,
                Box(
                    orientation="v",
                    children=[
                        DateTime(
                            name="date-time",
                            style="margin-top: 4px; min-width: 180px;",
                        ),
                        self.uptime_label,
                    ],
                ),
            ],
        )
        
        
        greeter=f"good {'morning' if time.localtime().tm_hour < 12 else 'afternoon'}, \n {os.getlogin().title()}!"
        self.greeter_label = Label(
            label=pyfiglet.figlet_format(greeter.lower(), "small_slant"),
            style="font-size: 10px;",
            name="generic-color-2",
            h_align="center",
        )

        invoke_repeater(
            15 * 60 * 1000,  # every 15min
            lambda: (self.uptime_label.set_label(self.get_current_uptime()), True)[1],
        )

        self.v_box = Box(
                name="window-inner",
                orientation="v",
                spacing=14,
                children=[self.header,
                          self.greeter_label, 
                          NowPlaying(name="window-inner"),
                          LauncherMenu(spacing=70, name="window-inner", h_align="fill"),
                ],
            )

        self.add(
            Box(
                name="window-inner",
                orientation="h",
                spacing=10,
                children=[
                    PowerMenu(spacing=55, name="window-inner", orientation="v"),
                    self.v_box,
                ],

            ),
        )

        self.show_all()

    def get_current_uptime(self):
        uptime = time.time() - psutil.boot_time()
        uptime_days, remainder = divmod(uptime, 86400)
        uptime_hours, remainder = divmod(remainder, 3600)
        # uptime_minutes, _ = divmod(remainder, 60)
        return f"{int(uptime_days)} {'days' if uptime_days > 1 else 'day'}, {int(uptime_hours)} {'hours' if uptime_hours > 1 else 'hour'}"


if __name__ == "__main__":
    start_panel = StartPanel()
    app = Application("start-panel", start_panel)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()
