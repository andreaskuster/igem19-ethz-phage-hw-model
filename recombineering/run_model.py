import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

from host import Host

# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)


# lb influx profile of reactor a
def in_a_lb(t):
    """
    :param t: time t
    :return: lb influx to reactor a at time t
    """
    return 0.0


# biomass outflux profile of reactor a
def out_a(t):
    """
    :param t: time t
    :return: biomass outflux of reactor a at time t
    """
    return 0.0


# temperature profile of reactor A
def temperature_a(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    return 39.7


# temperature profile of reactor B
def temperature_b(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    return 39.7


def temperature_dependency_new_host(x):
    """
    :param x: temperature
    :return: growth rate factor
    """
    mu = 39.7
    sigma_l = 120.0
    sigma_r = 10.0
    if x < mu:
        return np.exp(-0.5*(np.square(x-mu)/sigma_l)) # gaussian l: ~(28.0, 120)
    else:
        return np.exp(-0.5*(np.square(x-mu)/sigma_r)) # gaussian r: ~(28.0, 10)


new_host = Host(
    growth_rate=0.040773364,  # doubling time of 17min at optimal temperatures
    c0=8,
    t_dep=temperature_dependency_new_host,
    lb_threshold=9000,
    lb_cons=lambda: 1.5  # lb consumption per bacterium
)

# define system of differential equations
def dX_dt(X, t):
    [c_host_a, c_lb_a] = X
    return np.array([
        new_host.t_dep(temperature_a(t))*new_host.lb_dep(c_lb_a)*new_host.growth_rate * c_host_a,  # new host concentration reactor A
        0 if c_lb_a <= 0 else -c_host_a*new_host.lb_cons()  # lb concentration reactor A
    ])


ys = odeint(dX_dt, [
    new_host.c0,  # initial new host concentration
    8000  # initial lb concentration
], xs)

c_lb_a = [y[1] for y in ys]


plt.figure(figsize=(16, 16))

plt.subplot(6, 3, 1)
plt.plot(xs, [temperature_a(t) for t in xs])
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Temperature over Time')

plt.subplot(6, 3, 2)
plt.plot(xs, [in_a_lb(t) for t in xs])
plt.xlabel('time [min]')
plt.ylabel('LB influx [ml]')
plt.title('LB influx over Time')

plt.subplot(6, 3, 3)
plt.plot(xs, [out_a(t) for t in xs])
plt.xlabel('time [min]')
plt.ylabel('biomass outflux [ml]')
plt.title('Biomass Outflux over Time')

plt.subplot(6, 3, 4)
plt.plot(xs, [y[0] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria]')
plt.title('Host Concentration over Time')
plt.legend()



plt.subplot(6, 3, 2)
plt.plot(xs, [new_host.lb_dep(c_lb_a[x])*new_host.t_dep(temperature_a(x))*new_host.growth_rate for x in np.arange(0, len(xs))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()





plt.subplot(6, 3, 4)
plt.plot(xs, c_lb_a)
plt.xlabel('time [min]')
plt.ylabel('LB concentration [mg]')
plt.title('LB Concentration over Time')


plt.subplot(6, 3, 5)
plt.plot(np.linspace(0, 80, 100), [new_host.t_dep(x) for x in np.linspace(0, 80, 100)], label="new host")
plt.xlabel('temperature [°C]')
plt.ylabel('rate')
plt.title('Growth Rate (T)')
plt.legend()


plt.subplot(6, 3, 6)
lb_x = np.linspace(0, 1.3*new_host.lb_threshold)
plt.plot(lb_x, [new_host.lb_dep(x) for x in lb_x], label="new host")
plt.xlabel('LB concentration [mg/bacteria]')
plt.ylabel('rate')
plt.title('Growth Rate (LB)')
plt.legend()


#plt.savefig("test2.png")
plt.show()
