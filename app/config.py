from io import TextIOWrapper
import json
import os

CONFIG_FOLDER = "app/configs/"
DEFAULT_CONFIG_FILE = "default_config.json"
USER_CONFIG_FILE = "user_config.json"


class Config:
    def __init__(self) -> None:
        try:
            with open(CONFIG_FOLDER + USER_CONFIG_FILE) as file:
                self._load(file, isUserConfig=True)
        except FileNotFoundError:
            with open(CONFIG_FOLDER + DEFAULT_CONFIG_FILE) as file:
                self._load(file)
        except json.JSONDecodeError:
            self.restore_defaults()

    def _load(self, file: TextIOWrapper, isUserConfig: bool = False):
        config = json.load(file)
        if isUserConfig:
            self._check_data(config)
        self.BOARD_SIZE = config["BOARD_SIZE"]
        self.DEFAULT_ORIENTATION = config["DEFAULT_ORIENTATION"]
        self.BOAT_SIZES = config["BOAT_SIZES"]
        self.DEFAULT_SHIP_SET = config["DEFAULT_SHIP_SET"]
        self.DEFAULT_PLAYER_SIDE = config["DEFAULT_PLAYER_SIDE"]

    def save(self):
        with open(CONFIG_FOLDER + USER_CONFIG_FILE, "w") as file:
            json.dump(
                {
                    "BOARD_SIZE": self.BOARD_SIZE,
                    "DEFAULT_ORIENTATION": self.DEFAULT_ORIENTATION,
                    "BOAT_SIZES": self.BOAT_SIZES,
                    "DEFAULT_SHIP_SET": self.DEFAULT_SHIP_SET,
                    "DEFAULT_PLAYER_SIDE": self.DEFAULT_PLAYER_SIDE,
                },
                file,
            )

    def _check_data(self, config: dict):
        if config["BOARD_SIZE"] < 10:
            self.restore_defaults()
        elif config["DEFAULT_ORIENTATION"] not in ["UP", "RIGHT"]:
            self.restore_defaults()

    def restore_defaults(self):
        try:
            os.remove(CONFIG_FOLDER + USER_CONFIG_FILE)
            self.__init__()
        except FileNotFoundError:
            pass


config = Config()
