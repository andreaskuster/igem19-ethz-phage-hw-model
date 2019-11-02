import json
import time
from model.prediction import Prediction


sys.path.append(os.path.join(os.path.dirname(__file__), "hardware"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices/drivers/hw/i2c"))

from devices.OpticalDensitySensor import OpticalDensitySensor
from devices.PeristalticPump import PeristalticPump
from devices.ReactorTemperatureControl import ReactorTemperatureControl


class PredictionConstantConcentrationController:

    def __init__(self,
                 enabled: bool,
                 target_od: float,
                 continuous_pump_time: float,
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
        self.tol = float(self.config["prediction_constant_concentration"]["tol"])
        self.continuous_pump_time = continuous_pump_time
        self.predictor = Prediction(verbose=False)
        with open("params.json") as file:
            self.config = json.load(file)

    def control_loop(self):
        if self.enabled:

            with open("params.json") as file:
                self.config = json.load(file)
                self.tol = float(self.config["prediction_constant_concentration"]["tol"])

            diff = self.sensors[0].last_od - float(self.config["prediction_constant_concentration"]["target_od_reactor0"])
            if diff > self.tol:
                self.pumps[1].enable()
                self.pumps[3].enable()
                time.sleep(20.0)
                self.pumps[1].disable()
                self.pumps[3].disable()
            elif diff < -self.tol and self.sensors[1].last_od > self.sensors[0].last_od:
                self.pumps[0].enable()
                self.pumps[2].enable()
                self.pumps[3].enable()
                time.sleep(10.0)
                self.pumps[0].disable()
                self.pumps[2].disable()
                self.pumps[3].disable()
            self.pumps[0].enable()
            self.pumps[2].enable()
            self.pumps[3].enable()
            time.sleep(float(self.config["prediction_constant_concentration"]["continuous_pump_time"]))
            self.pumps[0].disable()
            self.pumps[2].disable()
            self.pumps[3].disable()

            # adjust temperature in the host growth reactor
            diff = self.sensors[1].last_od - float(self.config["prediction_constant_concentration"]["target_od_reactor1"])
            if diff > 0:
                self.reactors[0].set_target_temperature(39.0 - diff*100)
            else:
                self.reactors[0].set_target_temperature(39.0)

    def finalize(self):
        for pump in self.pumps:
            pump.disable()
        for sensor in self.sensors:
            sensor.disable()
        for reactor in self.reactors:
            reactor.disable()

