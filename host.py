from typing import List


class Host():

        
    def __init__(self,
                 yield_coeff: float,
                 g_max: float,
                 half_sat: float,
                 death_rate: float,
                 c0: int = 1,
                 t_dep = lambda: 1.0):
        """

        :param g_max:
        :param c0:
        :param yield_coeff:
        :param half_sat:
        :param death_rate:
        :param t_dep:
        """
        self.c0 = c0
        self.g_max = g_max       
        self.yield_coeff = yield_coeff
        self.half_sat = half_sat
        self.death_rate = death_rate
        self.t_dep = t_dep
        
    def per_cell_growth_rate(self, s):
        
        """
        :param s: nutrient concentration
        :return: per cell growth rate
        """
        return (self.g_max * s) / (self.half_sat + s)

        
