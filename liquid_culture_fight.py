from ddeint import ddeint
from pylab import array, linspace, subplots


def values_before_zero(t):
    return array([10000.0, 1.0])


def model(Y, t):
    x, y = Y(t)
    tot = x + y
    return array([
        0.04*x - 0.01*x/tot,
        0.06*y - 0.01*y/tot
    ])


tt = linspace(0, 1e2, 1000)
#tt = linspace(0, 6*1e2, 1000)

yy = ddeint(model, values_before_zero, tt)

fig, ax = subplots(1, figsize=(8, 4))

ax.plot(tt, [x[0] for x in yy], label="the weak")
ax.plot(tt, [x[1] for x in yy], label="the strong")
fig.legend(loc='upper center', borderaxespad=2.0)
fig.show()
