from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from .popup import PopupWindow

from fabric.utils import exec_shell_command_async

from enum import Enum

class PowerCommands(Enum):
    LOCK = "hyprlock"
    LOGOUT = "swaymsg exit"
    REBOOT = "reboot"
    SHUTDOWN = "shutdown -h now"

class ConfirmationBox(PopupWindow):
    def __init__(self, parent, command: str, prompt: str = "oh ong?", **kwargs):
        self.command = command

        self.text = Label(label=prompt)
        self.yes = Button(label="yes", on_clicked=self.execute)
        self.no = Button(label="no", on_clicked=lambda *_: self.hide())

        buttonbox = Box(orientation="h", children=[self.no, self.yes], spacing=24)


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



class PowerMenu(Box):
    def __init__(self, **kwargs):
        "Lock, Logout, Reboot, Shutdown"
        super().__init__(**kwargs)

        self.lock_icon = Image(icon_name="system-lock-screen-symbolic")
        self.lock_button = Button(child=self.lock_icon, on_clicked=self.lock)

        self.logout_icon = Image(icon_name="system-log-out-symbolic")
        self.logout_button = Button(child=self.logout_icon, on_clicked=self.logout)

        self.reboot_icon = Image(icon_name="system-reboot-symbolic")
        self.reboot_button = Button(child=self.reboot_icon, on_clicked=self.reboot)


        self.shutdown_icon = Image(icon_name="system-shutdown-symbolic")
        self.shutdown_button = Button(child=self.shutdown_icon, on_clicked=self.shutdown)

        self.add(self.lock_button)
        self.add(self.logout_button)
        self.add(self.reboot_button)
        self.add(self.shutdown_button)

        self.confirm = ConfirmationBox(parent=self, command="echo hi")

    @staticmethod
    def lock(*args): 
        print(PowerCommands.LOCK.value)
        exec_shell_command_async(PowerCommands.LOCK.value)

    def logout(self, *args): 
        self.confirm.command = PowerCommands.LOGOUT.value
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()


    def reboot(self, *args): 
        self.confirm.command = PowerCommands.REBOOT.value
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()


    def shutdown(self, *args): 
        self.confirm.command = PowerCommands.SHUTDOWN.value
        if not self.confirm.is_visible():
            self.confirm.show()
        else:
            self.confirm.hide()

