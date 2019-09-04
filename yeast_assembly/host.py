from typing import List


class Host():

    def __init__(self,
                 growth_rate: float,
                 c0: int,
                 t_dep,
                 lb_dep):
        """

        :param growth_rate:
        :param c0: initial host concentration
        """
        self.growth_rate = growth_rate
        self.c0 = c0
        self.t_dep = t_dep
        self.lb_dep = lb_dep