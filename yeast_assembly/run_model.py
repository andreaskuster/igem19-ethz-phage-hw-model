import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

from yeast_assembly.host import Host

# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)


def t_dep(x):
    """
    :param x: temperature
    :return: growth rate factor
    """
    mu = 39.7
    sigma_l = 120.0
    sigma_r = 10.0
    if x < mu:
        return np.exp(-0.5*(np.square(x-mu)/sigma_l)) # gaussian l: ~(39.7, 120)
    else:
        return np.exp(-0.5*(np.square(x-mu)/sigma_r)) # gaussian r: ~(39.7, 10)


lb_thresh = 7000
def lb_dep(x):
    """
    :param x: lb concentration
    :return: growth rate factor
    """
    if x < lb_thresh:
        return x / lb_thresh
    else:
        return 1.0 #  lb_thresh / lb_thresh


def lb_cons():
    """
    :return: lb consumption per bacterium [mg/minute]
    """
    return 1.5


def T(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    if t < 60:
        return 39.7
    else:
        return 25.0


# instantiate all hosts
original_host = Host(
    growth_rate=0.040773364,
    c0=1
)
new_host = Host(
    growth_rate=0.02,
    c0=8
)


# define system of differential equations
def dX_dt(X, t):
    [c1, c2, lb] = X
    return np.array([
        t_dep(T(t)) * lb_dep(lb)*original_host.growth_rate * c1,
        t_dep(T(t))*lb_dep(lb)*new_host.growth_rate * c2,
        -lb_cons() * (c1+c2)
    ])


ys = odeint(dX_dt, [original_host.c0, new_host.c0, 10000], xs)

plt.figure(figsize=(8, 8))

plt.subplot(3, 2, 1)
plt.plot(xs, [y[0] for y in ys], label="original host")
plt.plot(xs, [y[1] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [units]')
plt.title('Host Concentration over Time')
plt.legend()


plt.subplot(3, 2, 2)
plt.plot(xs, [T(t) for t in xs])
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Temperature over Time')

LB = [y[2] for y in ys]
plt.subplot(3, 2, 3)
plt.plot(xs, LB)
plt.xlabel('time [min]')
plt.ylabel('LB concentration [mg]')
plt.title('LB Concentration over Time')


plt.subplot(3, 2, 4)
plt.plot(np.linspace(0, 80, 100), [t_dep(x) for x in np.linspace(0, 80, 100)])
plt.xlabel('temperature [°C]')
plt.ylabel('rate')
plt.title('Growth Rate (T)')


plt.subplot(3, 2, 5)
lb_x = np.linspace(0, 1.3*lb_thresh)
plt.plot(lb_x, [lb_dep(x) for x in lb_x])
plt.xlabel('LB concentration [mg/bacteria]')
plt.ylabel('rate')
plt.title('Growth Rate (LB)')


plt.subplot(3, 2, 6)
plt.plot(xs, [lb_dep(LB[x])*t_dep(T(x))*original_host.growth_rate for x in np.arange(0, len(xs))], label="original host")
plt.plot(xs, [lb_dep(LB[x])*t_dep(T(x))*new_host.growth_rate for x in np.arange(0, len(xs))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()


plt.show()
