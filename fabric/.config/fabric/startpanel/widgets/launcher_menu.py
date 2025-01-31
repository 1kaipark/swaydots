
from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label


from fabric.utils import exec_shell_command_async

from enum import Enum

from typing import Literal

class LauncherCommands(Enum):
    SEARCH = "rofi -show drun"
    TERM = "ghostty"
    BROWSER = "firefox"
    FILES = "dolphin"
    SETTINGS = "systemsettings"

class LauncherMenu(Box):
    def __init__(self, **kwargs):
        "Lock, Logout, Reboot, Shutdown"
        super().__init__(**kwargs)

        search_icon = Label(label=" ", name="menu-icon-a")
        self.search_button = Button(
            child=search_icon,
            on_clicked=lambda *_: self.execute("s")
        )

        term_icon = Label(label=" ", name="menu-icon-a")
        self.term_button = Button(
            child=term_icon,
            on_clicked=lambda *_: self.execute("t")
        )

        browser_icon = Label(label="󰖟 ", name="menu-icon-a")
        self.browser_button = Button(
            child=browser_icon,
            on_clicked=lambda *_: self.execute("b")
        )

        files_icon = Label(label=" ", name="menu-icon-a")
        self.files_button = Button(
            child=files_icon,
            on_clicked=lambda *_: self.execute("f")
        )

        self.settings_icon = Label(label=" ", name="menu-icon-a")
        self.settings_button = Button(
            child=self.settings_icon, 
            on_clicked=lambda *_: self.execute("st")
        )

        self.add(self.search_button)
        self.add(self.term_button)
        self.add(self.browser_button)
        self.add(self.files_button)
        self.add(self.settings_button)

    @staticmethod
    def execute(what: Literal["s", "t", "b", "f", "st"]):
        match what:
            case "s":
                exec_shell_command_async(LauncherCommands.SEARCH.value)
            case "t":
                exec_shell_command_async(LauncherCommands.TERM.value)
            case "b":
                exec_shell_command_async(LauncherCommands.BROWSER.value)
            case "f":
                exec_shell_command_async(LauncherCommands.FILES.value)
            case "st":
                exec_shell_command_async(LauncherCommands.SETTINGS.value)

