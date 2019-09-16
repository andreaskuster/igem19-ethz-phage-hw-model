import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensors = {
    'sensor1': {
        'socket': '/sys/bus/w1/devices/28-0114536b03aa/w1_slave'
    },
    'sensor2': {
        'socket': '/sys/bus/w1/devices/28-80000026f3d8/w1_slave'
    },
    'sensor3': {
        'socket': '/sys/bus/w1/devices/28-0114534081aa/w1_slave'
    }
}


def raw_sensor_data(socket_path: str) -> str:
    with open(socket_path, 'r') as socket:
        lines = socket.readlines()
    return lines


def extract_temperature(raw_sensor_data: str) -> float:
    position = raw_sensor_data[1].find('t=')
    if position != -1:
        temperature = raw_sensor_data[1].strip()[position + 2:]
    return float(temperature) / 1000.0


while True:
    for sensor in sensors:
        print("{}: {}°C".format(sensor, extract_temperature(raw_sensor_data(sensors[sensor]))))
    time.sleep(10)

# credits: https://thepihut.com/blogs/raspberry-pi-tutorials/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
