import time

import smbus


class PCF8574:
    _BUS_NO = 1
    _DEVICE_ADDRESS = 0x38

    bus = smbus.SMBus(_BUS_NO)

    @staticmethod
    def init():
        """
        Initialize board.
        """
        pass

    @staticmethod
    def clear_all():
        """
        Resets all eight I/Os to zero.
        """
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, 0x00)

    @staticmethod
    def set_all():
        """
        Sets all eight I/Os to one.
        """
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, 0xff)

    @staticmethod
    def set(port: int):
        """
        Sets an individual I/O to one.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # set port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state | (0x1 << port))

    @staticmethod
    def clear(port: int):
        """
        Clears an individual I/O to zero.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # clear port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state & (0xff ^ (0x1 << port)))

    @staticmethod
    def toggle(port: int):
        """
        Toggles an individual I/O port.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # clear port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state ^ (0x1 << port))


if __name__ == "__main__":

    _CASE = 2

    if _CASE == 1:
        # run all on / all off interval
        while True:
            print("set all outputs")
            PCF8574.set_all()
            time.sleep(10)
            print("reset all outputs")
            PCF8574.clear_all()
            time.sleep(10)
    elif _CASE == 2:
        PCF8574.clear_all()

# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off
