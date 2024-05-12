import json
import os


class SpotibarConfig:
    def __init__(self, *args, **kwargs):
        self.config_file = os.path.expanduser(
            kwargs.get("config_file", "~/.config/spotibar/default.json")
        )

    def get(self, key, default):
        if not os.path.exists(self.config_file):
            return default
        try:
            with open(self.config_file, "r") as fh:
                config = json.load(fh)

                if key in config.keys():
                    return config[key]
                else:
                    return default
        except Exception as e:
            print(f"Problem reading from {self.config_file}!")
            print(e)

    def set(self, key, value):
        config = None

        try:
            with open(self.config_file, "r") as fh:
                config = json.load(fh)
        except Exception as e:
            print(f"Problem reading from {self.config_file}!")
            print(e)

            return

        config[key] = value

        try:
            with open(self.config_file, "w") as fh:
                json.dump(config, fh)
        except Exception as e:
            print(f"Problem writing to {self.config_file}!")
            print(e)

            return
