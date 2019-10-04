import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

from host import Host

# simulation time and resolution of samples
simulation_time = 120
number_samples = 100
xs = np.linspace(0, simulation_time, number_samples)


f = 0.007

#Reactor A
# lb influx profile of reactor A
def in_a_lb(t):
    """
    :param t: time t
    :return: lb influx to reactor a at time t
    """
    return f
    
# biomass outflux profile of reactor A
def out_a(t):
    """
    :param t: time t
    :return: biomass outflux of reactor a at time t
    """
    return f

# temperature profile of reactor A
def temperature_a(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    if t<60:
        return 39.7
    else:
        return 36
    
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


# instantiate all hosts
original_host = Host(
    c0 = 1,
    g_max = 0.040773364, # doubling time of 17min at optimal temperatures
    yield_coeff = 0.000000000001,
    half_sat = 0.00000125,
    death_rate = 0.001,
    t_dep = t_dep_original_host,
)

new_host = Host(
    c0 = 8,
    g_max = 0.02, # doubling time of ~34min at optimal temperature
    yield_coeff = 0.000000000001,
    half_sat = 0.00000125,
    death_rate = 0.001,
    t_dep = t_dep_new_host,
)

s0 = 0.0000025 #stock concentration of nutrient (g/mL)#0.0000025

# define system of differential equations
def dX_dt(X, t):
    [c_original_host_a, c_new_host_a, c_nutr_a] = X
    return np.array([
        0 if c_original_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a,temperature_a(t))*c_original_host_a - out_a(t)*c_original_host_a - original_host.death_rate*c_original_host_a,  # original host concentration reactor A
        0 if c_new_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a,temperature_a(t))*c_new_host_a - out_a(t)*c_new_host_a - new_host.death_rate*c_new_host_a,  # new host concentration reactor A
        0 if c_nutr_a <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_a,temperature_a(t))*(c_original_host_a+c_new_host_a)
        + s0*in_a_lb(t) - c_nutr_a*out_a(t)  # nutrient concentration reactor A
        ])


ys = odeint(dX_dt, [
    original_host.c0,  # initial original host concentration
    new_host.c0,  # initial new host concentration
    s0  # initial nutrient concentration
], xs)
    
    
    
    
c_original_host_a = [y[0] for y in ys]
c_new_host_a = [y[1] for y in ys]
c_nutrient_a = [y[2] for y in ys]

plt.figure(figsize=(12, 6))


plt.subplot(2, 3, 4)
plt.plot(xs, [temperature_a(t) for t in xs], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Temperature over Time')


plt.subplot(2, 3, 1)
plt.plot(xs, [y[0] for y in ys], label="original host")
plt.plot(xs, [y[1] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration over Time')
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
plt.legend()


plt.subplot(2, 3, 2)
plt.plot(np.arange(0, simulation_time), [original_host.per_cell_growth_rate(c_nutrient_a[int(x/simulation_time * number_samples)],temperature_a(x)) for x in np.arange(0, simulation_time)], label="original host")
plt.plot(np.arange(0, simulation_time), [new_host.per_cell_growth_rate(c_nutrient_a[int(x/simulation_time * number_samples)],temperature_a(x)) for x in np.arange(0, simulation_time)], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()


plt.subplot(2, 3, 3)
plt.plot(xs, c_nutrient_a, label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('nutrient concentration [g/mL]')
plt.title('Nutrient Concentration')
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))


plt.subplot(2, 3, 5)
plt.plot(np.linspace(0, 80, 100), [original_host.t_dep(x) for x in np.linspace(0, 80, 100)], label="original host")
plt.plot(np.linspace(0, 80, 100), [new_host.t_dep(x) for x in np.linspace(0, 80, 100)], label="new host")
plt.xlabel('temperature [°C]')
plt.ylabel('rate')
plt.title('Growth Rate (T)')
plt.legend()


plt.subplot(2, 3, 6)
nutrient_x = np.linspace(0, 0.0001)
plt.plot(nutrient_x, [new_host.per_cell_growth_rate(x,37) for x in nutrient_x])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))
plt.title('Growth Rate (nutrient)')


plt.subplots_adjust(wspace=0.4, hspace=0.4)

plt.show()
"""
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
plt.xlabel('nutrient concentration [mg/bacteria]')
plt.ylabel('rate')
plt.title('Growth Rate (Nutrient)')
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
"""