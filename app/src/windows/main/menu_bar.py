from tkinter import Menu
from tkinter.constants import DISABLED
from src.utils.record_file_management import RecordFileManagement
from src.windows.options.playback.delay import Delay
from src.windows.options.playback.speed import Speed
from src.windows.options.playback.repeat import Repeat
from src.windows.options.playback.time_gui import TimeGui
from sys import argv


class MenuBar(Menu):
    def __init__(self, parent):
        super().__init__(parent)

        # Menu Setup
        my_menu = Menu(parent)
        parent.config(menu=my_menu)
        self.file_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="File", menu=self.file_menu)
        record_file_management = RecordFileManagement(parent, self)
        if len(argv) > 1:
            self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=record_file_management.new_macro)
        else:
            self.file_menu.add_command(label="New", state=DISABLED, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Load", accelerator="Ctrl+L", command=record_file_management.load_macro)
        self.file_menu.add_separator()
        if len(argv) > 1:
            self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=record_file_management.save_macro)
            self.file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=record_file_management.save_macro_as)
        else:
            self.file_menu.add_command(label="Save", accelerator="Ctrl+S", state=DISABLED)
            self.file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", state=DISABLED)

        # Options Section
        self.options_menu = Menu(my_menu, tearoff=0)
        my_menu.add_cascade(label="Options", menu=self.options_menu)

        # Playback Sub
        playback_sub = Menu(self.options_menu, tearoff=0)
        self.options_menu.add_cascade(label="Playback", menu=playback_sub)
        playback_sub.add_command(label="Speed", command=lambda: Speed(self, parent))
        playback_sub.add_command(label="Repeat", command=lambda: Repeat(self, parent))
        playback_sub.add_command(label="Interval", command=lambda: TimeGui(self, parent, "Interval"))
        playback_sub.add_command(label="For", command=lambda: TimeGui(self, parent, "For"))
        playback_sub.add_command(label="Delay", command=lambda: Delay(self, parent))
