from enum import Enum


class I2CMultiplexer(Enum):

    REACTOR0 = 0
    REACTOR1 = 1
    REACTOR2 = 2

    def __init__(self):
        pass