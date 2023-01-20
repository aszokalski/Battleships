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

    def _load(self, file: TextIOWrapper, isUserConfig: bool = False):
        config = json.load(file)
        if isUserConfig:
            self._check_data(config)
        self._BOARD_SIZE = config["BOARD_SIZE"]
        self._DEFAULT_ORIENTATION = config["DEFAULT_ORIENTATION"]
        self._BOAT_SIZES = config["BOAT_SIZES"]
        self._DEFAULT_SHIP_SET = config["DEFAULT_SHIP_SET"]
        self._DEFAULT_PLAYER_SIDE = config["DEFAULT_PLAYER_SIDE"]

    def _save(self):
        with open(CONFIG_FOLDER + USER_CONFIG_FILE, "w") as file:
            json.dump(
                {
                    "BOARD_SIZE": self._BOARD_SIZE,
                    "DEFAULT_ORIENTATION": self._DEFAULT_ORIENTATION,
                    "BOAT_SIZES": self._BOAT_SIZES,
                    "DEFAULT_SHIP_SET": self._DEFAULT_SHIP_SET,
                    "DEFAULT_PLAYER_SIDE": self._DEFAULT_PLAYER_SIDE,
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

    @property
    def BOARD_SIZE(self):
        return self._BOARD_SIZE

    @BOARD_SIZE.setter
    def BOARD_SIZE(self, value: int):
        self._BOARD_SIZE = value
        self._save()

    @property
    def DEFAULT_ORIENTATION(self):
        return self._DEFAULT_ORIENTATION

    @DEFAULT_ORIENTATION.setter
    def DEFAULT_ORIENTATION(self, value: int):
        self._DEFAULT_ORIENTATIOND = value
        self._save()

    @property
    def BOAT_SIZES(self):
        return self._BOAT_SIZES

    @BOAT_SIZES.setter
    def BOAT_SIZES(self, value: dict):
        self._BOAT_SIZES = value
        self._save()

    @property
    def DEFAULT_SHIP_SET(self):
        return self._DEFAULT_SHIP_SET

    @DEFAULT_SHIP_SET.setter
    def DEFAULT_SHIP_SET(self, value: list):
        self._DEFAULT_SHIP_SET = value
        self._save()

    @property
    def DEFAULT_PLAYER_SIDE(self):
        return self._DEFAULT_PLAYER_SIDE

    @DEFAULT_PLAYER_SIDE.setter
    def DEFAULT_PLAYER_SIDE(self, value: int):
        self._DEFAULT_PLAYER_SIDE = value
        self._save()


config = Config()
