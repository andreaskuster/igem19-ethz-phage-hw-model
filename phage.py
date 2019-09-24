
class Phage():

    def __init__(self,
                 adsorption_rate: float,
                 c0: int = 1,
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
        
        
    def infection_rate(self, host_c):
        
        """
        :param host_c: host_concentration
        :return: infection rate
        """
        
        return self.adsorption_rate * self.c0 * host_c

