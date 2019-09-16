import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

from host import Host

# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)


def t_dep_original_host(x):
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


def t_dep_new_host(x):
    """
    :param x: temperature
    :return: growth rate factor
    """
    mu = 28.0
    sigma_l = 120.0
    sigma_r = 10.0
    if x < mu:
        return np.exp(-0.5*(np.square(x-mu)/sigma_l)) # gaussian l: ~(28.0, 120)
    else:
        return np.exp(-0.5*(np.square(x-mu)/sigma_r)) # gaussian r: ~(28.0, 10)


# define temperature profile over time for simulation
def T(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    if t < 60:
        return 39.7
    else:
        return 24.0


# instantiate all hosts
original_host = Host(
    growth_rate=0.040773364, # doubling time of 17min at optimal temperatures
    c0=1,
    t_dep=t_dep_original_host,
    lb_threshold=7000,
    lb_cons=lambda: 1.5  # lb consumption per bacterium
)

new_host = Host(
    growth_rate=0.02, # doubling time of ~34min at optimal temperature
    c0=8,
    t_dep=t_dep_new_host,
    lb_threshold=9000,
    lb_cons=lambda: 1.5  # lb consumption per bacterium
)

# define system of differential equations
def dX_dt(X, t):
    [c1, c2, lb] = X
    return np.array([
        original_host.t_dep(T(t)) * original_host.lb_dep(lb)*original_host.growth_rate * c1,  # original host concentration
        new_host.t_dep(T(t))*new_host.lb_dep(lb)*new_host.growth_rate * c2,  # new host concentration
        -c1*original_host.lb_cons() + -c2*new_host.lb_cons()  # lb concentration
    ])


ys = odeint(dX_dt, [
    original_host.c0,  # initial original host concentration
    new_host.c0,  # initial new host concentration
    8000  # initial lb concentration
], xs)

plt.figure(figsize=(8, 8))

plt.subplot(3, 2, 1)
plt.plot(xs, [y[0] for y in ys], label="original host")
plt.plot(xs, [y[1] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria]')
plt.title('Host Concentration over Time')
plt.legend()


plt.subplot(3, 2, 3)
plt.plot(xs, [T(t) for t in xs])
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Temperature over Time')


LB = [y[2] for y in ys]
plt.subplot(3, 2, 4)
plt.plot(xs, LB)
plt.xlabel('time [min]')
plt.ylabel('LB concentration [mg]')
plt.title('LB Concentration over Time')


plt.subplot(3, 2, 5)
plt.plot(np.linspace(0, 80, 100), [original_host.t_dep(x) for x in np.linspace(0, 80, 100)], label="original host")
plt.plot(np.linspace(0, 80, 100), [new_host.t_dep(x) for x in np.linspace(0, 80, 100)], label="new host")
plt.xlabel('temperature [°C]')
plt.ylabel('rate')
plt.title('Growth Rate (T)')
plt.legend()


plt.subplot(3, 2, 6)
lb_x = np.linspace(0, 1.3*max(original_host.lb_threshold, new_host.lb_threshold))
plt.plot(lb_x, [original_host.lb_dep(x) for x in lb_x], label="original host")
plt.plot(lb_x, [new_host.lb_dep(x) for x in lb_x], label="new host")
plt.xlabel('LB concentration [mg/bacteria]')
plt.ylabel('rate')
plt.title('Growth Rate (LB)')
plt.legend()


plt.subplot(3, 2, 2)
plt.plot(xs, [original_host.lb_dep(LB[x])*original_host.t_dep(T(x))*original_host.growth_rate for x in np.arange(0, len(xs))], label="original host")
plt.plot(xs, [new_host.lb_dep(LB[x])*new_host.t_dep(T(x))*new_host.growth_rate for x in np.arange(0, len(xs))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()

#plt.savefig("test2.png")
plt.show()
