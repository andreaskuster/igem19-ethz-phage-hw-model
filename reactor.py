# this is the top wrapper combining the hardware, model and real-time visualization.

import os
import select
import sys
import threading
import time
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), "hardware"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices/drivers/hw/i2c"))

from devices.OpticalDensitySensor import OpticalDensitySensor
from devices.PeristalticPump import PeristalticPump
from devices.ReactorTemperatureControl import ReactorTemperatureControl

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
    # controller
    print("enable controller reactor0 reactor1 sensor0 pump0 pump1 pump2 0.5 // target od")
    print("disable controller")
    print()

def output_info_event_loop(reactors: List[ReactorTemperatureControl], sensors: List[OpticalDensitySensor],
                           pumps: List[PeristalticPump], interval):
    starttime = time.time()
    while True:
        print()
        print("Bioreactor State Report:")
        for reactor in reactors:
            if reactor.enabled:
                reactor.info()
        for sensor in sensors:
            if sensor.enabled:
                sensor.info()
        for pump in pumps:
            if pump.enabled:
                pump.info()
        time.sleep(interval - ((time.time() - starttime) % interval))


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

class NaiveConstantConcentration:

    def __init__(self,
                 enabled: bool,
                 target_od: float,
                 reactors: List[ReactorTemperatureControl],
                 sensors: List[OpticalDensitySensor],
                 pumps: List[PeristalticPump]):
        """
        :param enabled: enable / disable control loop
        :param reactors: reactor[0] = bacteria only (control constant growth rate), reactor[2] = bacteria & phages
        :param sensors: sensor[0] = sensor for reactor[0], sensor[1]  = sensor for reactor[2]
        :param pumps: pump[0] = lb influx to reactor[0], pump[1] = pump from reactor[0] to reactor[1], pump[3] = from reactor[1] to the waste
        :param interval: control loop interval
        """
        self.enabled = enabled
        self.target_od = target_od
        self.reactors = reactors
        self.sensors = sensors
        self.pumps = pumps
        self.tol = 0.1

    def control_loop(self):
        if self.enabled:
            diff = self.sensor[0].last_od - (self.target_od + self.tol)
            if diff > 0:  # too high, pump out
                    pumps[0].enable()
                    pumps[1].enable()
                    pumps[2].enable()
                    time.sleep(diff*100)
                    pumps[0].disable()
                    pumps[1].disable()
                    pumps[2].disable()

    def finalize(self):
        for pump in self.pumps:
            pump.disable()
        for sensor in self.sensors:
            sensor.disable()
        for reactor in self.reactors:
            reactor.disable()


def naive_constant_concentration(configuration: NaiveConstantConcentration, interval):
    starttime = time.time()
    while True:
        configuration.control_loop()
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

    output_info_event_loop_thread = threading.Thread(target=output_info_event_loop,
                                                     args=(reactor_temperature, od_sensor,
                                                           pumps, 30.0,), daemon=True)
    controller: NaiveConstantConcentration = NaiveConstantConcentration(
        enabled=False,
        reactors=None,
        sensors=None,
        pumps=None,

    )
    naive_constant_concentration_thread  = threading.Thread(target=naive_constant_concentration, args=(controller, 10.0), daemon=True)



    print("start deamon threads")
    # start background event loops
    temperature_event_loop_thread.start()
    od_sensor0_event_loop_thread.start()
    od_sensor1_event_loop_thread.start()
    od_sensor2_event_loop_thread.start()
    output_info_event_loop_thread.start()
    naive_constant_concentration_thread.start()

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
                            elif command[1] == "controller":
                                controller.reactors = [
                                    reactor_temperature[_REACTOR_MAP[command[2]]],
                                    reactor_temperature[_REACTOR_MAP[command[3]]]
                                ]
                                controller.sensors = [od_sensor[_SENSOR_MAP[command[4]]]]
                                controller.pumps = [pumps[_PUMP_MAP[command[5]]],
                                                    pumps[_PUMP_MAP[command[6]]],
                                                    pumps[_PUMP_MAP[command[7]]]]
                                controller.enabled = True
                            else:
                                pumps[_PUMP_MAP[command[1]]].enable()
                        elif command[0] == "disable":
                            if command[1] == "temperature":
                                reactor_temperature[_REACTOR_MAP[command[2]]].disable()
                            elif command[1] == "sensor":
                                od_sensor[_SENSOR_MAP[command[2]]].disable()
                            elif command[1] == "controller":
                                controller.disable()
                            else:
                                pumps[_PUMP_MAP[command[1]]].disable()
                        elif command[0] == "set":
                            if command[1] == "temperature":
                                reactor_temperature[_REACTOR_MAP[command[2]]].set_target_temperature(float(command[3]))
                                reactor_temperature[_REACTOR_MAP[command[2]]].enable()
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
