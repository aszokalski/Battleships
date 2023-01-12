from enum import Enum
import numpy as np


def uuid_generator():
    """Simple unique id generator. Id's are just consecutive numbers.

    Yields:
        int: uuid
    """
    current = 0
    while True:
        yield current
        current += 1


# global generator
uuid = uuid_generator()


def get_uuid():
    """Returns unique id

    Returns:
        int: uuid
    """
    return next(uuid)


class AttackResult(Enum):
    MISS = 0
    HIT = 1
    SUNK = 2


# Numpy setup
def formatter(x):
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    WARNING = "\033[93m"
    if not x:
        return "[ ]"
    if x.alive:
        return BOLD + "[O]" + ENDC
    return BOLD + WARNING + "[X]" + ENDC + ENDC


np.set_printoptions(formatter={"all": formatter}, linewidth=100)
