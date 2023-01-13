import json
import os
from .translate import Translatore

class SpotibarConfig():
    translator = Translatore()

    def __init__(self, *args, **kwargs):
        self.config_file = kwargs.get('config_file', '.spotibar_config.json')
        self.path = os.path.expanduser("~") + "/" + self.config_file

    def get(self, key, default):
        if not os.path.exists(self.path):
            return default
        try:
            with open(self.path, 'r') as fh:
                config = json.load(fh)

                if key in config.keys():
                    return config[key]
                else:
                    return default
        except Exception as e:
            message = self.translator.translate("Problem reading from ~/")
            print(f"{ message } {self.config_file}!")
            print(e)

    def set(self, key, value):
        config = None

        try:
            with open(self.path, 'r') as fh:
                config = json.load(fh)
        except Exception as e:
            message = self.translator.translate("Problem reading from ~/")
            print(f"{ message } {self.config_file}!")
            print(e)

            return

        config[key] = value

        try:
            with open(self.path, 'w') as fh:
                json.dump(config, fh)
        except Exception as e:
            message = self.translator.translate("Problem writing to ~/")
            print(f"{ message } {self.config_file}!")
            print(e)

            return
