from typing import List


class Host():

    def __init__(self,
                 growth_rate: float,
                 c0: int = 1,
                 t_dep = lambda: 1.0,
                 lb_threshold = 7000,
                 lb_cons = lambda: 0.0):
        """

        :param growth_rate:
        :param c0:
        :param t_dep:
        :param lb_threshold:
        :param lb_cons:
        """
        self.growth_rate = growth_rate
        self.c0 = c0
        self.lb_threshold = lb_threshold
        self.t_dep = t_dep
        self.lb_cons = lb_cons

    def lb_dep(self, x):
        """
        :param x: lb concentration
        :return: growth rate factor
        """
        if x < self.lb_threshold:
            return x / self.lb_threshold
        else:
            return 1.0
