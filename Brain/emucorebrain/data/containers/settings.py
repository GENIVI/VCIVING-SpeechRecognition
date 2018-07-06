import os
import json


class SettingsContainer:

    SETTING_DISPLAY_KEY = "display_key"
    SETTING_VALUE = "value"

    def __init__(self, file_path):
        self._file_path = file_path

        if not os.path.exists(file_path):
            settings_file_creator_file = open(file_path, "a+")
            json.dump({}, settings_file_creator_file)
            settings_file_creator_file.close()

        settings_file = open(self._file_path, "r+")
        self._settings = json.load(settings_file)
        settings_file.close()

    def get_setting_display_key(self, setting):
        return self._settings[setting][SettingsContainer.SETTING_DISPLAY_KEY]

    def get_setting(self, setting):
        return self._settings[setting][SettingsContainer.SETTING_VALUE]

    def set_setting(self, setting, value):
        self._settings[setting][SettingsContainer.SETTING_VALUE] = value

        settings_file = open(self._file_path, "r+")
        json.dump(self._settings, settings_file)
        settings_file.close()

    @staticmethod
    def is_valid_file(file_path):
        try:
            settings_file = open(file_path, "r+")
            json.load(settings_file)
            return True

        except:
            return False

