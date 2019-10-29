import numpy as np
from ddeint import ddeint
from pylab import array, sin, linspace, subplots

tau = 30.0


def foo(t):
    if t < 10.0:
        return 0.0
    elif 10.0 <= t < 10.0 * np.pi:
        return 1.0
    else:
        return 10.0 * sin(t * 0.5)


def values_before_zero(t):
    return array([0.0, 0.0])


def model(Y, t):
    x, y = Y(t)
    x_tau, y_tau = Y(t - tau)
    return array([foo(t), x_tau])


tt = linspace(0, 100, 1000)
yy = ddeint(model, values_before_zero, tt)

fig, ax = subplots(1, figsize=(8, 4))

ax.plot(tt, [x[0] for x in yy], label="trace1")
ax.plot(tt, [x[1] for x in yy], label="trace2")
fig.legend(loc='upper center', borderaxespad=2.0)
fig.show()
