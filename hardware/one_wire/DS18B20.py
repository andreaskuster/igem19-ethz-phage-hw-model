import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensor1 = '/sys/bus/w1/devices/28-0114536b03aa/w1_slave'
sensor2 = '/sys/bus/w1/devices/28-80000026f3d8/w1_slave'
sensor3 = '/sys/bus/w1/devices/28-0114534081aa/w1_slave'


def temp_raw(socket_path: str):
    with open(socket_path) as socket:
        lines = socket.readlines()
    return lines


while True:
    for sensor in [sensor1, sensor2, sensor3]:
        print(temp_raw(sensor))
    time.sleep(10)