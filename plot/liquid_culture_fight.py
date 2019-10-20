from ddeint import ddeint
from pylab import array, linspace, subplots, subplot


def values_before_zero(t):
    return array([10000.0, 1.0])


def model(Y, t):
    x, y = Y(t)
    tot = x + y
    return array([
        0.04*x - 0.01*x/tot,
        0.06*y - 0.01*y/tot
    ])


tt0 = linspace(0, 6*1e1, 1000)
tt1 = linspace(0, 6*1e2, 1000)

yy0 = ddeint(model, values_before_zero, tt0)
yy1 = ddeint(model, values_before_zero, tt1)


fig, (ax0, ax1) = subplots(2, figsize=(8, 6))

ax0.plot(tt0, [x[0] for x in yy0], label="slower growing, quantitatively more")
ax0.ticklabel_format(axis='y', style='sci', scilimits=(2,3))
ax0.plot(tt0, [x[1] for x in yy0], label="faster growing, quantitatively less")
ax0.set_xlabel('Time [min]')
ax0.set_ylabel('Number of Phages')
ax0.legend(loc='upper left', borderaxespad=2.0)


ax1.plot(tt1, [x[0] for x in yy1], label="slower growing, quantitatively more")
ax1.plot(tt1, [x[1] for x in yy1], label="faster growing, quantitatively less")
ax1.set_xlabel('Time [min]')
ax1.set_ylabel('Number of Phages')
ax1.legend(loc='upper left', borderaxespad=2.0)
fig.show()
