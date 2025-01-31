import fabric 
from fabric.widgets.button import Button 

from fabric.audio.service import Audio

from fabric.widgets.label import Label
from fabric.widgets.image import Image 
from fabric.widgets.stack import Stack
from fabric.widgets.revealer import Revealer
from fabric.widgets.box import Box

import gi 
from gi.repository import Gtk, Gdk

class SpeakerVolume(Button):
    def __init__(self):
        self.audio = Audio(on_speaker_changed=self.update_label_and_icon)

        self.icon_stack = Stack(transition_type="slide-up-down")
        for i in ["overamplified", "high", "medium", "low", "muted"]:
            self.icon_stack.add_named(Image(icon_name=f"audio-volume-{i}-symbolic", icon_size=Gtk.IconSize(1), name="revealerIcon"), name=i)

        self.label_stack = Stack(transition_type="slide-up-down")
        for i in range(100, -10, -10):
            self.label_stack.add_named(Label(label=f"%{i}", name="revealerLabel"), name=f"{i}")

        self.revealer = Revealer(
                child=Button(label="test", spacing=4, on_clicked=lambda *_: print("TEST")),
            transition_type="slide-left"
        )

        super().__init__(
            on_scroll_event=self.on_scroll,
            on_enter_notify_event=lambda *args: self.revealer.set_reveal_child(True),
            on_leave_notify_event=lambda *args: self.revealer.set_reveal_child(False),
        child=Box(
                children=[
                    self.icon_stack,
                    self.revealer,
                ]
            ),
        )
        self.add_events(Gdk.EventMask.SCROLL_MASK)

    def on_scroll(self, widget, event):
        if self.audio.speaker.name != unwanted_sink:
            match not event.direction:
                case 0:
                    self.audio.speaker.volume -= 10
                case 1:
                    self.audio.speaker.volume += 10

    def mute(self, *args):
        self.audio.speaker.muted = not self.audio.speaker.muted

    def update_label_and_icon(self, *args):
        ...
    def find_icon_name(self):
        if self.audio.speaker.get_muted():
            return "muted"
        return (
            "overamplified" if (volume := self.audio.speaker.volume) >= 99
            else "high" if volume >= 66
            else "medium" if volume >= 33
            else "low" if volume >= 1
            else "muted"
        )
