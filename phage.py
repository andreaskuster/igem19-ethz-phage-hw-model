from typing import List


class Phage():

    def __init__(self,
                 c0: int = 1,
                 adsorption_rate: float,
                 burst_size = float,
                 death_rate = float):
        """

        :param c0:
        :param adsorption_rate:
        :param burst_size:
        :param death_rate:
        """
        self.c0 = c0
        self.adsorption_rate = adsorption_rate
        self.burst_size = burst_size
        self.death_rate = death_rate

