from tkinter import *
from tkinter.ttk import *

from src.windows.window import Window
from src.windows.main.menu_bar import MenuBar
from src.utils.user_settings import UserSettings
from src.utils.get_file import resource_path
from src.utils.warning_pop_up_save import confirm_save
from src.utils.record_file_management import RecordFileManagement
from src.hotkeys.hotkeys_manager import HotkeysManager
from src.macro.macro import Macro
from os import path


class MainApp(Window):
    """Main windows of the application"""

    def __init__(self):
        super().__init__("Macro Recorder", 400, 200)
        self.attributes("-topmost", 1)

        # For save message purpose
        self.macro_saved = False
        self.macro_recorded = False
        self.prevent_record = False

        self.settings = UserSettings()

        self.menu = MenuBar(self)  # Menu Bar
        self.macro = Macro(self)

        self.validate_cmd = self.register(self.validate_input)

        self.hotkeyManager = HotkeysManager(self)

        # Main Buttons (Start record, stop record, start playback, stop playback)

        # Play Button
        self.playImg = PhotoImage(file=resource_path(path.join("assets", "button", "play.png")))

        self.playBtn = Button(self, image=self.playImg, state=DISABLED)
        self.playBtn.pack(side=LEFT, padx=50)

        # Record Button
        self.recordImg = PhotoImage(file=resource_path(path.join("assets", "button", "record.png")))
        self.recordBtn = Button(self, image=self.recordImg, command=self.macro.start_record)
        self.recordBtn.pack(side=RIGHT, padx=50)

        # Stop Button
        self.stopImg = PhotoImage(file=resource_path(path.join("assets", "button", "stop.png")))

        record_management = RecordFileManagement(self, self.menu)

        self.bind('<Control-Shift-S>', record_management.save_macro_as)
        self.bind('<Control-s>', record_management.save_macro)
        self.bind('<Control-l>', record_management.load_macro)
        self.bind('<Control-n>', record_management.new_macro)

        self.protocol("WM_DELETE_WINDOW", self.quit_software)

        self.attributes("-topmost", 0)

        self.mainloop()

    def validate_input(self, action, value_if_allowed):
        """Prevents from adding letters on an Entry label"""
        if action == "1":  # Insert
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        return True

    def quit_software(self, force=False):
        if not self.macro_saved and self.macro_recorded and not force:
            wantToSave = confirm_save()
            if wantToSave:
                RecordFileManagement(self, self.menu).save_macro()
            elif wantToSave == None:
                return
        self.destroy()
        self.quit()
