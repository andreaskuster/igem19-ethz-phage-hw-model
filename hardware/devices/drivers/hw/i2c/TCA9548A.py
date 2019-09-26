import smbus


class TCA9548A:
    _BUS_NO = 1
    _DEVICE_ADDRESS = 0x70

    bus = smbus.SMBus(_BUS_NO)

    @staticmethod
    def switch(port: int):
        """
        Sets an individual I/O to one.
        :param port: I2C channel (0,..,7)
        """
        # set port
        TCA9548A.bus.write_byte(TCA9548A._DEVICE_ADDRESS, 0x1 << port)


if __name__ == "__main__":
    _CHANNEL = 4

    TCA9548A.switch(_CHANNEL)
