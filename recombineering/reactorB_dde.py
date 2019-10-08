import matplotlib.pyplot as plt
import numpy as np

from jitcdde import jitcdde, y, t
from host import Host
from phage import Phage



# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)

fluxA= 0.02
fluxB= 0.02

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

# define system of differential equations
"""
def dXa_dt(X, t):
    [c_host_a, c_nutr_a] = X
    return np.array([
        0 if c_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a,37)*c_host_a - out_a(t)*c_host_a - new_host.death_rate*c_host_a,  # new host concentration reactor A
        0 if c_nutr_a <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_a)*c_host_a
        + s0*in_a_lb(t) - c_nutr_a*out_a(t)  # nutrient concentration reactor A
    ])
    
def dXb_dt(X, t):#TODO add delay diff term for infected host and phages
    [c_host_b, c_nutr_b, c_host_inf_poo, c_host_inf_pnn, c_poo, c_pnn] = X
    return np.array([
        0 if c_host_b <= 0 else new_host.per_cell_growth_rate(c_nutr_b)*c_host_b - new_phage.infection_rate(c_host_b) - original_phage.infection_rate(c_host_b)
        - new_host.death_rate - out_b(t)*c_host_b,  # new host concentration reactor A
        0 if c_nutr_b <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_b)*(c_host_b+c_host_inf_poo+c_host_inf_pnn)
        + s0*in_b_lb(t) - c_nutr_b*out_b(t),  # nutrient concentration reactor A
        0 if c_host_inf_poo < 0 else original_phage.infection_rate(c_host_b) - out_b(t)*c_host_inf_poo, # concentration of host infected by new original phage
        0 if c_host_inf_pnn < 0 else new_phage.infection_rate(c_host_b) - out_b(t)*c_host_inf_pnn, # concentration of host infected by new new phage
        0 if c_poo <= 0 else original_phage.burst_size*c_host_inf_poo - original_phage.infection_rate(c_host_b)
        - out_b(t)*c_poo - original_phage.death_rate*c_poo + in_lib(t)*(1 - R_pnn), # original phage concentration
        0 if c_pnn <= 0 else new_phage.burst_size*c_host_inf_pnn - new_phage.infection_rate(c_host_b)
        - out_b(t)*c_pnn - new_phage.death_rate*c_pnn + in_lib(t)*R_pnn #new phage concentration
    ])
"""

n=8
l=1
equations = [new_host.per_cell_growth_rate(y(1),temperature_b(t))*y(0) - out_a(t)*y(0) - new_host.death_rate*y(0),#c_host_a
            - new_host.yield_coeff*new_host.per_cell_growth_rate(y(1),temperature_b(t))*y(0) + s0*in_a_lb(t) - y(1)*out_a(t),#c_nutr_a
            new_host.per_cell_growth_rate(y(3),temperature_b(t))*y(2) + y(0)*in_nh(t) - new_phage.infection_rate(y(2),new_phage.c0) - original_phage.infection_rate(y(2),original_phage.c0) - new_host.death_rate*y(2) - out_b(t)*y(2),#c_host_b
            - new_host.yield_coeff*new_host.per_cell_growth_rate(y(3),temperature_b(t))*(y(2)+y(4)+y(5)) + y(1)*in_nh(t) + s0*in_b_lb(t) - y(3)*out_b(t),#c_nutr_b
            original_phage.infection_rate(y(2),original_phage.c0) -y(4,t-l) - out_b(t)*y(4),#host infected by original phage
            new_phage.infection_rate(y(2),new_phage.c0) -y(5,t-l) - out_b(t)*y(5),#host infected by new phage
            original_phage.burst_size*y(4,t-l) - original_phage.infection_rate(y(2),original_phage.c0) - out_b(t)*y(6) - original_phage.death_rate*y(6) + in_lib(t)*(1 - R_pnn),#c_poo
            new_phage.burst_size*y(5,t-l) - new_phage.infection_rate(y(2),new_phage.c0) - out_b(t)*y(7) - new_phage.death_rate*y(7) + in_lib(t)*(R_pnn)]#c_pnn
def dX():
    for i in range(n):
        yield equations[i]

initial_state = np.array([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
DDE = jitcdde(dX, delays=[l], max_delay=l, verbose=True)

DDE.constant_past([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
DDE.step_on_discontinuities()

data = []
x = np.arange(DDE.t, DDE.t+120, 100/50)
for time in x:
	data.append(DDE.integrate(time))
np.savetxt("timeseries.dat", data)
#print(data)
#print(x)


plt.figure(figsize=(16, 16))


plt.subplot(3, 3, 1)
plt.plot(x, [data[t][0] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration A over Time')
plt.legend()
plt.subplot(3, 3, 2)
plt.plot(x, [data[t][1] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('concentration [g/mL]')
plt.title('Nutrient A over Time')
plt.legend()
plt.subplot(3, 3, 3)
plt.plot(x, [data[t][2] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration B over Time')

plt.subplot(3, 3, 4)
plt.plot(x, [data[t][3] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [g/mL]')
plt.title('Nutrient B over Time')

plt.subplot(3, 3, 5)
plt.plot(x, [data[t][4] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host infected OO over Time')

plt.subplot(3, 3, 6)
plt.plot(x, [data[t][5] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host infected NN over Time')

plt.subplot(3, 3, 7)
plt.plot(x, [data[t][6] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage OO over Time')

plt.subplot(3, 3, 8)
plt.plot(x, [data[t][7] for t in range(len(x))])
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage NN over Time')

plt.subplot(3, 3, 9)
plt.plot(x, [data[t][6] for t in range(len(x))], label="original")
plt.plot(x, [data[t][7] for t in range(len(x))], label="new")
plt.xlabel('time [min]')
plt.ylabel('concentration [#phage/mL]')
plt.title('Phage over Time')
plt.legend()


plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()
