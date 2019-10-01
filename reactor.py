# this is the top wrapper combining the hardware, model and real-time visualization.

import sys
import threading
import time
from typing import List
import os
import sys
import select

sys.path.append(os.path.join(os.path.dirname(__file__), "hardware"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices/drivers/hw/i2c"))

from devices.OpticalDensitySensor import OpticalDensitySensor
from devices.PeristalticPump import PeristalticPump
from devices.ReactorTemperatureControl import ReactorTemperatureControl
from devices.drivers.hw.i2c.TCA9548A import TCA9548A

_PUMP_MAP = {
    "pump0": 0,
    "pump1": 1,
    "pump2": 2,
    "pump3": 3,
    "pump4": 4,
    "pump5": 5,
    "pump6": 6,
    "pump7": 7,
    "pump8": 8
}

_REACTOR_MAP = {
    "reactor0": 0,
    "reactor1": 1,
    "reactor2": 2
}

_SENSOR_MAP = {
    "od0": 0,
    "od1": 1,
    "od2": 2
}


def print_help():
    print("usage: reactor.py command arg0 arg1 ..")
    print("required: command")
    print()
    print("example commands:")
    # temperature control
    print("set temperature reactor0 39.0 // [°C]")
    print("disable temperature reactor0")
    # peristaltic pumps
    print("enable pump0")
    print("set speed pump0 100 // [%]")
    print("disable pump0")
    # print("set volume pump0 50 // [ml]") TODO: not implemented yet
    # od sensor
    print("enable sensor od0")
    print("disable sensor od0")
    print()


def temperature_event_loop(reactors: List[ReactorTemperatureControl], interval):
    starttime = time.time()
    while True:
        for reactor in reactors:
            reactor.control_loop()
        time.sleep(interval - ((time.time() - starttime) % interval))


def od_sensor_event_loop(sensor: OpticalDensitySensor, interval):
    starttime = time.time()
    while True:
        sensor.event_loop()
        time.sleep(interval - ((time.time() - starttime) % interval))


if __name__ == "__main__":

    # instantiate locks
    i2c_lock = threading.Lock()
    one_wire_lock = threading.Lock()

    TCA9548A.init()
    TCA9548A.switch(2)

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

    pumps = [
        PeristalticPump(
            id=0,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=1,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=2,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=3,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=4,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=5,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=6,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=7,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False),
        PeristalticPump(
            id=8,
            i2c_lock=i2c_lock,
            enabled=False,
            verbose=False)
    ]

    print("start deamon threads")
    # start background event loops
    temperature_event_loop_thread.start()
    od_sensor0_event_loop_thread.start()
    od_sensor1_event_loop_thread.start()
    od_sensor2_event_loop_thread.start()

    try:
        print("run input loop")
        print_help()
        while True:
            if select.select([sys.stdin, ], [], [], 0.0)[0]:  # check if input is available
                for line in sys.stdin:  # read lines

                    command = line.split()  # split command into components

                    # go through all command queries
                    try:
                        if len(command) == 0 or command[0] == "help":
                            print_help()
                        elif command[0] == "enable":
                            if command[1] == "sensor":
                                od_sensor[_SENSOR_MAP[command[2]]].enable()
                            else:
                                pumps[_PUMP_MAP[command[1]]].enable()
                        elif command[0] == "disable":
                            if command[1] == "temperature":
                                reactor_temperature[_REACTOR_MAP[command[2]]].disable()
                            elif command[1] == "sensor":
                                od_sensor[_SENSOR_MAP[command[2]]].disable()
                            else:
                                pumps[_PUMP_MAP[command[1]]].disable()
                        elif command[0] == "set":
                            if command[1] == "temperature":
                                reactor_temperature[_REACTOR_MAP[command[2]]].set_target_temperature(float(command[3]))
                            elif command[1] == "speed":
                                pumps[_PUMP_MAP[command[2]]].set_speed(int(command[3]))
                            elif command[1] == "volume":
                                pumps[_PUMP_MAP[command[2]]].set_volume(int(command[3]))
                        else:
                            print_help()
                    except:
                        print("Invalid syntax, try again.")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting...but first put all devices into a safe state...")
    finally:
        # save log files: TODO
        # put all devices into a safe idle state
        for sensor in od_sensor:
            sensor.finalize()
        for pump in pumps:
            pump.finalize()
        for temp in reactor_temperature:
            temp.finalize()
        print("Goodbye.")

# https://docs.python.org/2/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement
# https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data