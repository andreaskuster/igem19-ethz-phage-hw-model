

class Host():

    def __init__(self,
                 growth_rate,
                 c0):
        """

        :param growth_rate:
        :param c0: initial host concentration
        """
        self.growth_rate = growth_rate
        self.c0 = c0