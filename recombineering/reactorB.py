import matplotlib.pyplot as plt
import numpy as np
from pylab import array

from ddeint import ddeint
from host import Host
from phage import Phage

# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)

fluxA= 0.01
fluxB= 0.01

#Reactor A
# lb influx profile of reactor A
def in_a_lb(t):
    """
    :param t: time t
    :return: lb influx to reactor a at time t
    """
    return fluxA
    
# biomass outflux profile of reactor A
def out_a(t):
    """
    :param t: time t
    :return: biomass outflux of reactor a at time t
    """
    return fluxA
    
# temperature profile of reactor A
def temperature_a(t):
    """
    :param t: time t
    :return: temperature at time t
    """
    return 39.7
    
#Reactor B
# lb influx profile of reactor B
def in_b_lb(t):
    """
    :param t: time t
    :return: lb influx to reactor b at time t
    """
    return fluxB/3
    
# lb influx profile of reactor B
def in_nh(t):
    """
    :param t: time t
    :return: new_host influx from reactor a to reactor b at time t
    """
    return fluxB/3

# phage library influx in reactor B
def in_lib(t):
    """
    param t: time t
    :return: library influx in reator b at time t
    """
    
    return fluxB/3
    
# biomass outflux profile of reactor B
def out_b(t):
    """
    :param t: time t
    :return: biomass outflux of reactor b at time t
    """
    return fluxB


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
        return np.exp(-0.5*(np.square(x-mu)/sigma_l)) # gaussian l: ~(39.7, 120)
    else:
        return np.exp(-0.5*(np.square(x-mu)/sigma_r)) # gaussian r: ~(39.7, 10)


new_host = Host( 
    c0 = 10**5,
    g_max = 0.036, #lit: 0.012
    yield_coeff = 0.000000000001,
    half_sat = 0.00000125,
    death_rate = 0.001,
    t_dep = temperature_dependency_new_host,
)

original_phage = Phage(
    c0 = 1000,
    adsorption_rate = 0.000000000001,
    burst_size = 100,
    death_rate = 0.00272,
)
new_phage = Phage(
    c0 = 1,
    adsorption_rate = 0.0000001,
    burst_size = 100,
    death_rate = 0.00272,
)

s0 = 0.0000025 #stock concentration of nutrient (g/mL)#0.0000025
R_pnn = 1/1000 # fraction of new phage in library


d = 7#lysis time delay

# define system of differential equations
def model(Y, t, d):
    c_host_a, c_nutr_a, c_host_b, c_nutr_b, c_inf_poo, c_inf_pnn, c_poo, c_pnn = Y(t)
    c_host_a_d, c_nutr_a_d, c_host_b_d, c_nutr_b_d, c_inf_poo_d, c_inf_pnn_d, c_poo_d, c_pnn_d = Y(t - d)
    return np.array([0 if c_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a, 37)*c_host_a - out_a(t)*c_host_a - new_host.death_rate*c_host_a,
                     0 if c_nutr_a <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_a,37)*c_host_a
        + s0*in_a_lb(t) - c_nutr_a*out_a(t),
        0 if c_host_b <= 0 else new_host.per_cell_growth_rate(c_nutr_b,37)*c_host_b - new_phage.infection_rate(c_host_b, new_phage.c0) - original_phage.infection_rate(c_host_b, original_phage.c0)
        - new_host.death_rate - out_b(t)*c_host_b,
         0 if c_nutr_b <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_b,37)*(c_host_b+c_inf_poo+c_inf_pnn)
        + s0*in_b_lb(t) - c_nutr_b*out_b(t),
        0 if c_inf_poo < 0 else original_phage.infection_rate(c_host_b, original_phage.c0) - out_b(t)*c_inf_poo,
        0 if c_inf_pnn < 0 else new_phage.infection_rate(c_host_b,new_phage.c0) - out_b(t)*c_inf_pnn,
        0 if c_poo <= 0 else original_phage.burst_size*c_inf_poo - original_phage.infection_rate(c_host_b, original_phage.c0)
        - out_b(t)*c_poo - original_phage.death_rate*c_poo + in_lib(t)*(1 - R_pnn),
        0 if c_pnn <= 0 else new_phage.burst_size*c_inf_pnn - new_phage.infection_rate(c_host_b,new_phage.c0)
        - out_b(t)*c_pnn - new_phage.death_rate*c_pnn + in_lib(t)*R_pnn])
    
def initial_conditions(t):
    return array([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])

data = ddeint(model, initial_conditions, xs, fargs=(d,))

plt.figure(figsize=(16, 16))

plt.subplot(3, 3, 1)
plt.plot(xs, [data[t][0] for t in range(len(xs))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration A over Time')
plt.legend()
plt.subplot(3, 3, 2)
plt.plot(xs, [data[t][1] for t in range(len(xs))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('concentration [g/mL]')
plt.title('Nutrient A over Time')
plt.legend()
plt.subplot(3, 3, 3)
plt.plot(xs, [data[t][2] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration B over Time')

plt.subplot(3, 3, 4)
plt.plot(xs, [data[t][3] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [g/mL]')
plt.title('Nutrient B over Time')

plt.subplot(3, 3, 5)
plt.plot(xs, [data[t][4] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host infected OO over Time')

plt.subplot(3, 3, 6)
plt.plot(xs, [data[t][5] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host infected NN over Time')

plt.subplot(3, 3, 7)
plt.plot(xs, [data[t][6] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage OO over Time')

plt.subplot(3, 3, 8)
plt.plot(xs, [data[t][7] for t in range(len(xs))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage NN over Time')

plt.subplot(3, 3, 9)
plt.plot(xs, [data[t][6] for t in range(len(xs))], label="original")
plt.plot(xs, [data[t][7] for t in range(len(xs))], label="new")
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage over Time')
plt.legend()


plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()
