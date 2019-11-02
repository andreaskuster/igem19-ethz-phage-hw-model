from ddeint import ddeint
from pylab import array, linspace, subplots, subplot


@staticmethod
def concentration_to_od(concentration: float) -> float:
    # concentration in cells/ml
    return concentration / 8.0e8


@staticmethod
def od_to_concentration(od: float) -> float:
    # concentration in cells/ml
    return 8.0e8 * od  # assumption: od is linear, approximately valid in the interval [0.0, 1.0]


def values_before_zero(t):
    return array([0.2, 0.2, 0.2])


def model(Y, t):
    x0, x1, x2 = Y(t)
    return array([
        0.01*x0,
        0.02*x1,
        0.03*x2
    ])


tt0 = linspace(0, 100, 1000)

yy0 = ddeint(model, values_before_zero, tt0)

fig, ax0 = subplots(1, figsize=(8, 6))

ax0.plot(tt0, [concentration_to_od(x[0]) for x in yy0], label="T=21.0")
ax0.ticklabel_format(axis='y', style='sci', scilimits=(2, 3))
ax0.plot(tt0, [concentration_to_od(x[1]) for x in yy0], label="T=30.0")
ax0.plot(tt0, [concentration_to_od(x[2]) for x in yy0], label="T=39.0")

ax0.set_xlabel('Time [min]')
ax0.set_ylabel('Host Concentration')
ax0.legend(loc='upper left', borderaxespad=2.0)
ax0.set_xlim(xmin=0)


fig.show()
