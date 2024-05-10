from pynput import keyboard
from src.utils.get_key_pressed import getKeyPressed
from tkinter import messagebox
from src.utils.keys import vk_nb


class HotkeysManager:
    def __init__(self, main_app):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release,
            win32_event_filter=self.__win32_event_filter,
        )
        self.main_app = main_app
        self.settings = main_app.settings
        self.hotkeys = []
        self.hotkey_visible = []
        self.hotkey_detection = []
        self.macro = main_app.macro
        self.hotkey_button = None
        self.type_of_hotkey = None
        self.entry_to_change = None
        self.changeKey = False
        self.index_to_change = 0
        self.keyboard_listener.start()

    def enable_hot_key_detection(self, type_of_hotkey, entry_to_change, index):
        self.hotkey_button = entry_to_change
        self.type_of_hotkey = type_of_hotkey
        self.index_to_change = index
        self.changeKey = True
        self.entry_to_change = entry_to_change
        self.entry_to_change.configure(text="Please key")

    def clear_hot_key(self, type, entry_to_change):
        self.settings.change_settings("Hotkeys", type, None, [])
        entry_to_change.configure(text="")

    def __win32_event_filter(self, msg, data):
        """Detect if key is pressed by real keyboard or pynput"""
        if data.flags == 0x10:
            if self.macro.playback == True and self.macro.record == False:
                return False
            else:
                return True

    def __on_press(self, key):
        user_settings = self.settings.get_config()
        if self.changeKey:
            key_pressed = getKeyPressed(self.keyboard_listener, key)
            if key_pressed not in self.hotkeys:
                if ">" in key_pressed:
                    try:
                        key_pressed = vk_nb[key_pressed]
                    except:
                        pass
                self.hotkeys.append(key_pressed)
                key_pressed = (
                    key_pressed.replace("Key.", "")
                    .replace("_l", "")
                    .replace("_r", "")
                    .replace("_gr", "")
                )
                self.hotkey_visible.append(key_pressed.upper())
            self.hotkey_button.configure(text=self.hotkey_visible)

            if all(keyword not in key_pressed for keyword in ["ctrl", "alt", "shift"]):
                if (
                    self.type_of_hotkey == "Record_Start"
                    and user_settings["Hotkeys"]["Playback_Start"] == self.hotkeys
                    or self.type_of_hotkey == "Playback_Start"
                    and user_settings["Hotkeys"]["Record_Start"] == self.hotkeys
                ):
                    messagebox.showerror(
                        "Error",
                        "You can't have same hotkeys on start record and start playback.",
                    )
                    self.entry_to_change.configure(text="Please key")
                    self.hotkeys = []
                    self.hotkey_visible = []
                    return
                self.settings.change_settings(
                    "Hotkeys", self.type_of_hotkey, None, self.hotkeys
                )
                self.changeKey = False
                self.hotkeys = []
                self.hotkey_visible = []

        if self.changeKey == False and self.main_app.prevent_record == False:
            key_pressed = getKeyPressed(self.keyboard_listener, key)
            if ">" in key_pressed:
                try:
                    key_pressed = vk_nb[key_pressed]
                except:
                    pass
            for keys in user_settings["Hotkeys"]:
                if not user_settings["Hotkeys"][keys]:
                    user_settings["Hotkeys"][keys] = ""
            if key_pressed not in self.hotkey_detection:
                self.hotkey_detection.append(key_pressed)
            by_hotkey = True
            if (
                self.hotkey_detection == user_settings["Hotkeys"]["Record_Start"]
                and self.macro.record == False
                and self.macro.playback == False
            ):
                self.macro.start_record(by_hotkey)

            elif (
                self.hotkey_detection == user_settings["Hotkeys"]["Record_Stop"]
                and self.macro.record == True
                and self.macro.playback == False
            ):
                self.macro.stop_record()

            elif (
                self.hotkey_detection == user_settings["Hotkeys"]["Playback_Start"]
                and self.macro.record == False
                and self.macro.playback == False
                and self.main_app.macro_recorded == True
            ):
                self.macro.start_playback()

            elif (
                self.hotkey_detection == user_settings["Hotkeys"]["Playback_Stop"]
                and self.macro.record == False
                and self.macro.playback == True
            ):
                self.macro.stop_playback(by_hotkey)

    def __on_release(self, key):
        if len(self.hotkey_detection) != 0:
            self.hotkey_detection.pop()
