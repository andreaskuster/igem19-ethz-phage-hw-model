# this is the top wrapper combining the hardware, model and real-time visualization.

import sys
import threading
import time
from typing import List

from hardware.devices.OpticalDensitySensor import OpticalDensitySensor
from hardware.devices.PeristalticPump import PeristalticPump
from hardware.devices.ReactorTemperatureControl import ReactorTemperatureControl


def print_help():
    print("usage: reactor.py command arg0 arg1 ..")
    print("required: command")
    print()
    print("example commands:")
    # temperature control
    print("set temperature reactor0 39.0 // [°C]")
    print("disable temperature reactor0")
    # peristaltic pumps
    print("set speed pump0 100.0 // [%]")
    print("disable speed pump0")
    print("set volume pump0 50 // [ml]")
    # od sensor
    print("enable sensor od0")
    print("disable sensor od0")
    print()


def temperature_event_loop(reactors: List[ReactorTemperatureControl], interval):
    while True:
        starttime = time.time()

        for reactor in reactors:
            reactor.control_loop()

        time.sleep(interval - ((time.time() - starttime) % interval))


def od_sensor_event_loop(sensor: OpticalDensitySensor, interval):
    while True:
        starttime = time.time()

        sensor.event_loop()

        time.sleep(interval - ((time.time() - starttime) % interval))


if __name__ == "__main__":

    # instantiate locks
    i2c_lock = threading.Lock()
    one_wire_lock = threading.Lock()

    # instantiate all devices
    reactor_temperature = [
        ReactorTemperatureControl(id=0,
                                  i2c_lock=i2c_lock,
                                  one_wire_lock=one_wire_lock,
                                  target_temperature=25.0,
                                  enabled=False,
                                  verbose=False),
        ReactorTemperatureControl(id=1,
                                  i2c_lock=i2c_lock,
                                  one_wire_lock=one_wire_lock,
                                  target_temperature=25.0,
                                  enabled=False,
                                  verbose=False),
        ReactorTemperatureControl(id=2,
                                  i2c_lock=i2c_lock,
                                  one_wire_lock=one_wire_lock,
                                  target_temperature=25.0,
                                  enabled=False,
                                  verbose=False),
    ]
    temperature_event_loop_thread = threading.Thread(target=temperature_event_loop, args=(reactor_temperature, 2.0,),
                                                     daemon=True)

    od_sensor = [
        OpticalDensitySensor(
            id=0,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False
        ),
        OpticalDensitySensor(
            id=1,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False
        ),
        OpticalDensitySensor(
            id=2,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False
        )
    ]
    od_sensor0_event_loop_thread = threading.Thread(target=od_sensor_event_loop, args=(od_sensor[0], 30.0,),
                                                    daemon=True)
    od_sensor1_event_loop_thread = threading.Thread(target=od_sensor_event_loop, args=(od_sensor[1], 30.0,),
                                                    daemon=True)
    od_sensor2_event_loop_thread = threading.Thread(target=od_sensor_event_loop, args=(od_sensor[2], 30.0,),
                                                    daemon=True)

    pump = [
        PeristalticPump(
            id=0,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=1,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=2,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=3,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=4,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=5,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=6,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=7,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=8,
            enabled=False,
            verbose=False)
    ]

    # start background event loops
    temperature_event_loop_thread.start()
    od_sensor0_event_loop_thread.start()
    od_sensor1_event_loop_thread.start()
    od_sensor2_event_loop_thread.start()

    while True:
        if not sys.stdin.isatty():  # check if input is available
            for line in sys.stdin:  # read lines

                command = line.split()  # split command into components

                # go through all command queries
                try:
                    if len(command) == 0 or command[0] == "help":
                        print_help()
                    elif command[0] == "enable":
                        if command[1] == "sensor":
                            pass  # TODO
                    elif command[0] == "disable":
                        if command[1] == "temperature":
                            pass  # TODO
                        elif command[1] == "speed":
                            pass  # TODO
                        elif command[1] == "sensor":
                            pass  # TODO
                    elif command[0] == "set":
                        if command[1] == "temperature":
                            pass  # TODO
                        elif command[1] == "speed":
                            pass  # TODO
                        elif command[1] == "volume":
                            pass  # TODO
                    else:
                        print_help()
                except:
                    print("Invalid syntax, try again.")
        time.sleep(0.5)

# https://docs.python.org/2/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement
# https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data
