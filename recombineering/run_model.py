import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

from host import Host


# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)

f= 0.0

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
        return np.exp(-0.5*(np.square(x-mu)/sigma_l)) # gaussian l: ~(39.7, 120)
    else:
        return np.exp(-0.5*(np.square(x-mu)/sigma_r)) # gaussian r: ~(39.7, 10)


new_host = Host( 
    c0 = 10**5,
    g_max = 0.024,
    yield_coeff = 0.000000000001,
    half_sat = 0.00000125,
    death_rate = 0.001,
    t_dep = temperature_dependency_new_host,
)


s0 = 0.0000025 #stock concentration of nutrient (g/mL)#0.0000025

# define system of differential equations
def dXa_dt(X, t):
    [c_host_a, c_nutr_a] = X
    return np.array([
        0 if c_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a,temperature_a(t))*c_host_a - out_a(t)*c_host_a - new_host.death_rate*c_host_a,  # new host concentration reactor A
        0 if c_nutr_a <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_a,temperature_a(t))*c_host_a
        + s0*in_a_lb(t) - c_nutr_a*out_a(t)  # nutrient concentration reactor A
    ])
    
    
ys = odeint(dXa_dt, [
    new_host.c0,  # initial new host concentration [cell/mL]
    s0  # initial nutrient concentration [g/mL]
], xs)


c_new_host_a = [y[0] for y in ys]
c_nutrient_a = [y[1] for y in ys]


plt.figure(figsize=(16, 16))


plt.subplot(3, 3, 1)
plt.plot(xs, [temperature_a(t) for t in xs], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Temperature over Time')
plt.legend()


plt.subplot(3, 3, 2)
plt.plot(xs, [in_a_lb(t) for t in xs], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('LB influx [ml]')
plt.title('LB influx over Time')
plt.legend()


plt.subplot(3, 3, 3)
plt.plot(xs, [out_a(t) for t in xs], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('biomass outflux [ml]')
plt.title('Biomass Outflux over Time')
plt.legend()


plt.subplot(3, 3, 4)
plt.plot(xs, [y[0] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration over Time')
plt.legend()


plt.subplot(3, 3, 5)
plt.plot(xs, [new_host.per_cell_growth_rate(c_nutrient_a[x],temperature_a(x)) for x in np.arange(0, len(xs))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
#plt.ylim([0.014,0.025])
plt.title('Actual Growth Rate over Time')
plt.legend()


plt.subplot(3, 3, 6)
plt.plot(xs, c_nutrient_a, label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('nutrient concentration [g/mL]')
plt.title('nutrient Concentration over Time')
plt.legend()


plt.subplot(3, 3, 7)
nutrient_x = np.linspace(0, 0.0001)
plt.plot(nutrient_x, [new_host.per_cell_growth_rate(x,37) for x in nutrient_x], label="new host")
plt.ylim([0,0.015])
plt.xlim([0,0.000002])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.title('Growth Rate at low conc. of nutrient')
plt.legend()


plt.subplot(3, 3, 8)
nutrient_x = np.linspace(0, 0.0001)
plt.plot(nutrient_x, [new_host.per_cell_growth_rate(x,37) for x in nutrient_x], label="new host")
plt.ylim([0,0.025])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.title('Growth Rate (nutrient)')
plt.legend()


plt.subplot(3, 3, 9)
nutrient_x = np.linspace(0.1, 1)
lin = [new_host.per_cell_growth_rate(x,37) for x in nutrient_x]
plt.plot(nutrient_x, lin, label="new host")
plt.ylim([0,0.025])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.title('Growth Rate at high conc. of nutrient')
plt.legend()

plt.subplots_adjust(wspace=0.4, hspace=0.4)

#plt.savefig("test2.png")
plt.show()
