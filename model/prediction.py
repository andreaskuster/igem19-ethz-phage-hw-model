from ddeint import ddeint
from pylab import array, sin, linspace, subplots
from sklearn.svm import SVR
import numpy as np
import warnings
import matplotlib.pyplot as plt


class Prediction:
    """
    This is a simpl
    """

    def __init__(self,
                 optimal_growth_rate: float = 1.0,
                 verbose=True):
        self.optimal_growth_rate = optimal_growth_rate  # optimal growth rate
        self.temperature_profile = lambda t: 39.0  # default: constant 39.0
        self.temperature_dependency = lambda T: 1.0  # default: independent
        self.verbose = verbose
        self.calibrate()

    def calibrate(self):
        self.svr = SVR(gamma='scale', C=10.0, epsilon=0.001)
        y = np.array([
            0.01,  # pad
            0.03380233992181625,
            0.03090358015587697,
            0.023030174817693854,
            0.01])  # pad

        X = np.array([
            43.0,  # pad
            39.0,
            34.0,
            29.0,
            24.0])  # pad

        self.svr.fit(X.reshape(-1, 1), y.reshape(-1, 1))

        if self.verbose:
            xx = linspace(20.0, 45.0, 300)
            yy = self.svr.predict(np.array(xx).reshape(-1, 1))

            fig = plt.figure()
            ax = fig.add_subplot(111)

            ax.plot(xx, yy, label='regression')
            ax.scatter(X, y, label='measurements')
            plt.legend()
            plt.show()

    def model(self, Y, t):
        c0, c1 = Y(t)
        # return np.array([self.optimal_growth_rate * self.temperature_dependency(self.temperature_profile(t)) * c0, 0.0])
        return np.array([self.svr.predict(np.array([self.temperature_profile(t)]).reshape(-1, 1)) * c0, 0.0])

    def values_before_zero(self, t):
        return np.array([1.0, 1.0])

    @staticmethod
    def concentration_to_od(concentration: float) -> float:
        # concentration in cells/ml
        return concentration / 8.0e8

    @staticmethod
    def od_to_concentration(od: float) -> float:
        # concentration in cells/ml
        return 8.0e8 * od  # assumption: od is linear, approximately valid in the interval [0.0, 1.0]

    def predict_cell_concentration(self,
                                   simulation_time,
                                   temperature_profile,
                                   initial_concentration=1.0,
                                   plot=False) -> float:
        self.temperature_profile = temperature_profile
        tt = linspace(0, simulation_time, 1000)

        # simulation_data = ddeint(self.model, self.values_before_zero, tt)
        simulation_data = ddeint(func=self.model, g=lambda t: np.array([initial_concentration, 1.0]), tt=tt)

        if plot:
            fig, ax = subplots(1, figsize=(8, 4))
            ax.plot(tt, [x[0] for x in simulation_data], label="cell concentration")
            fig.legend(loc='upper center', borderaxespad=2.0)
            fig.show()

        return simulation_data[-1][0]  # return last value

    def predict_od(self,
                   simulation_time,
                   temperature_profile,
                   initial_od=0.3,
                   plot=False):
        return Prediction.concentration_to_od(self.predict_cell_concentration(simulation_time=simulation_time,
                                                                              temperature_profile=temperature_profile,
                                                                              initial_concentration=Prediction.od_to_concentration(
                                                                                  initial_od),
                                                                              plot=plot))


if __name__ == "__main__":
    _SIMULATION_TIME = 10
    _TEMPERATURE_PROFILE = lambda t: 30.0  # lambda t: 33.0 if (t < 50) else 45.0

    _INITIAL_OD = 0.2
    _INITIAL_CONCENTRATION = Prediction.od_to_concentration(_INITIAL_OD)

    model = Prediction(verbose=False)

    warnings.warn("The current implementation only supports temperature profiles in the interval []")

    model.calibrate()

    c_final = model.predict_cell_concentration(simulation_time=_SIMULATION_TIME,
                                               temperature_profile=_TEMPERATURE_PROFILE,
                                               initial_concentration=_INITIAL_CONCENTRATION,
                                               plot=True)

    od_final = Prediction.concentration_to_od(c_final)
    
    print("OD before simulation: {}, after {}min of simulation: {}".format(_INITIAL_OD, _SIMULATION_TIME, od_final))

# credits:
# - od conversion: https://www.labtools.us/bacterial-cell-number-od600/
