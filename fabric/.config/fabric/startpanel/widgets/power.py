from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from .popup import PopupWindow

from fabric.utils import exec_shell_command_async, get_relative_path

from enum import Enum

class PowerCommands(Enum):
    PAPER = get_relative_path("../scripts/wpswitch.sh")
    LOCK = "hyprlock"
    LOGOUT = "swaymsg exit"
    REBOOT = "reboot"
    SHUTDOWN = "shutdown -h now"

class ConfirmationBox(PopupWindow):
    def __init__(self, parent, command: str, **kwargs):
        self.command = command

        self.text = Label(label="r u sure")
        self.yes = Button(label="yes", on_clicked=self.execute)
        self.no = Button(label="no", on_clicked=lambda *_: self.hide())

        buttonbox = CenterBox(orientation="h", start_children=[self.no], end_children=[self.yes], spacing=24)


        super().__init__(
            parent=parent,
            name="window-inner",
            margin="10px 10px 10px 10px",
            child=Box(children=[self.text, buttonbox], spacing=24, orientation="v", name="window-inner"),
            visible=False,
            all_visible=False,
        )

    def execute(self, *_):
        exec_shell_command_async(self.command)
        self.hide()

    def set_text(self, text: str):
        self.text.set_text(text) # beautiful and readable btw



class PowerMenu(Box):
    def __init__(self, **kwargs):
        "Lock, Logout, Reboot, Shutdown"
        super().__init__(**kwargs)

        self.wallpaper_icon = Label(label="󰸉 ", name="menu-icon-b")
        self.wallpaper_button = Button(child=self.wallpaper_icon, on_clicked=self.wallpaper)

        self.lock_icon = Label(label=" ", name="menu-icon-b")
        self.lock_button = Button(child=self.lock_icon, on_clicked=self.lock)

        self.logout_icon = Label(label="󰍃 ", name="menu-icon-b")
        self.logout_button = Button(child=self.logout_icon, on_clicked=self.logout)

        self.reboot_icon = Label(label=" ", name="menu-icon-b")
        self.reboot_button = Button(child=self.reboot_icon, on_clicked=self.reboot)


        self.shutdown_icon = Label(label="󰐥 ", name="menu-icon-b")
        self.shutdown_button = Button(child=self.shutdown_icon, on_clicked=self.shutdown)


        self.add(self.wallpaper_button)
        self.add(self.lock_button)
        self.add(self.logout_button)
        self.add(self.reboot_button)
        self.add(self.shutdown_button)

        self.confirm = ConfirmationBox(parent=self, command="echo hi")

    @staticmethod
    def wallpaper(*args):
        exec_shell_command_async(PowerCommands.PAPER.value)

    @staticmethod
    def lock(*args): 
        exec_shell_command_async(PowerCommands.LOCK.value)

    def logout(self, *args): 
        self.confirm.command = PowerCommands.LOGOUT.value
        self.confirm.set_text("rly logout fr")
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()


    def reboot(self, *args): 
        self.confirm.command = PowerCommands.REBOOT.value
        self.confirm.set_text("ts will reboot ur shit")
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()


    def shutdown(self, *args): 
        self.confirm.command = PowerCommands.SHUTDOWN.value
        self.confirm.set_text("Are you sure you want to shut down?")
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()
