import time

import smbus


class ESC:
    _BUS_NO = 1
    _DEVICE_ADDRESS = 0x07

    bus = smbus.SMBus(_BUS_NO)

    def __init__(self):
        pass

    @staticmethod
    def init():
        """
        Initialize board.
        """
        pass

    @staticmethod
    def set_value(device: int,
                  value: int):
        """
        Sets the speed of the ESC.
        :param device: ESC device id {0, 1, 2}
        :param value: speed value [-100, 100]
        """
        ESC.bus.write_i2c_block_data(ESC._DEVICE_ADDRESS, device, [value + 100])  # needs to be mapped to [0, 200]

    @staticmethod
    def stop_esc(device: int):
        """
        Put esc device into idle mode.
        :param device: device id
        """
        ESC.set_value(device, 0)

    @staticmethod
    def full_forward(device: int):
        """
        Put esc device in maximum heating mode.
        :param device: device id
        """
        ESC.set_value(device, 100)

    @staticmethod
    def full_reverse(device: int):
        """
        Put esc device into maximum cooling mode.
        :param device: device id
        """
        ESC.set_value(device, -100)


if __name__ == "__main__":

    _CASE = 2

    if _CASE == 1:
        while True:
            # run cyclic program
            print("stop all escs")
            ESC.stop_esc(0)
            ESC.stop_esc(1)
            ESC.stop_esc(2)
            time.sleep(10)
            print("run full forward")
            ESC.full_forward(0)
            ESC.full_forward(1)
            ESC.full_forward(2)
            time.sleep(10)
            print("stop all escs")
            ESC.stop_esc(0)
            ESC.stop_esc(1)
            ESC.stop_esc(2)
            time.sleep(10)
            print("run full reverse")
            ESC.full_reverse(0)
            ESC.full_reverse(1)
            ESC.full_reverse(2)
            time.sleep(10)
    elif _CASE == 2:
        # stop all
        ESC.stop_esc(0)
        ESC.stop_esc(1)
        ESC.stop_esc(2)
