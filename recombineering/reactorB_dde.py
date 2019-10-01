import matplotlib.pyplot as plt
import numpy as np
#from scipy.integrate import odeint

from jitcdde import jitcdde, y, t
from host import Host
from phage import Phage



# simulation time and resolution of samples
xs = np.linspace(0, 120, 100)

fluxA= 0.0
fluxB= 0.0
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
    adsorption_rate = 0.00000000001,
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

def dXa_dt(X, t):
    [c_host_a, c_nutr_a] = X
    return np.array([
        0 if c_host_a <= 0 else new_host.per_cell_growth_rate(c_nutr_a,37)*c_host_a - out_a(t)*c_host_a - new_host.death_rate*c_host_a,  # new host concentration reactor A
        0 if c_nutr_a <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_a)*c_host_a
        + s0*in_a_lb(t) - c_nutr_a*out_a(t)  # nutrient concentration reactor A
    ])
    
def dXb_dt(X, t):#TODO add delay diff term for infected host and phages, change the integrator, merge both system
    [c_host_b, c_nutr_b, c_host_inf_poo, c_host_inf_pnn, c_poo, c_pnn] = X
    return np.array([
        0 if c_host_b <= 0 else new_host.per_cell_growth_rate(c_nutr_b)*c_host_b - new_phage.infection_rate(c_host_b) - original_phage.infection_rate(c_host_b)
        - new_host.death_rate - out_b(t)*c_host_b,  # new host concentration reactor A #TODO: c_host_a
        0 if c_nutr_b <= 0 else - new_host.yield_coeff*new_host.per_cell_growth_rate(c_nutr_b)*(c_host_b+c_host_inf_poo+c_host_inf_pnn)
        + s0*in_b_lb(t) - c_nutr_b*out_b(t),  # nutrient concentration reactor A #TODO: add s_a
        0 if c_host_inf_poo < 0 else original_phage.infection_rate(c_host_b) - out_b(t)*c_host_inf_poo, # concentration of host infected by new original phage
        0 if c_host_inf_pnn < 0 else new_phage.infection_rate(c_host_b) - out_b(t)*c_host_inf_pnn, # concentration of host infected by new new phage
        0 if c_poo <= 0 else original_phage.burst_size*c_host_inf_poo - original_phage.infection_rate(c_host_b)
        - out_b(t)*c_poo - original_phage.death_rate*c_poo + in_lib(t)*(1 - R_pnn), # original phage concentration
        0 if c_pnn <= 0 else new_phage.burst_size*c_host_inf_pnn - new_phage.infection_rate(c_host_b)
        - out_b(t)*c_pnn - new_phage.death_rate*c_pnn + in_lib(t)*R_pnn #new phage concentration
    ])


n=8
l=20
reactorA = [new_host.per_cell_growth_rate(y(1),temperature_b(t))*y(0) - out_a(t)*y(0) -new_host.death_rate*y(0),#c_host_a
            - new_host.yield_coeff*new_host.per_cell_growth_rate(y(1),temperature_b(t))*y(0) + s0*in_a_lb(t) - y(1)*out_a(t),#c_nutr_a
            new_host.per_cell_growth_rate(y(3),temperature_b(t))*y(2) + y(0)*in_nh(t) - new_phage.infection_rate(y(2)) - original_phage.infection_rate(y(2)) - new_host.death_rate*y(2) - out_b(t)*y(2),#c_host_b
            - new_host.yield_coeff*new_host.per_cell_growth_rate(y(3),temperature_b(t))*(y(2)+y(4)+y(5)) + y(1)*in_nh(t) + s0*in_b_lb(t) - y(3)*out_b(t),#c_nutr_b
            original_phage.infection_rate(y(2)) - out_b(t)*y(4),#host infected by original phage
            new_phage.infection_rate(y(2)) - out_b(t)*y(5),#host infected by new phage
            original_phage.burst_size*y(4,t-l) - original_phage.infection_rate(y(2)) - out_b(t)*y(6) - original_phage.death_rate*y(6) + in_lib(t)*(1 - R_pnn),#c_poo
            new_phage.burst_size*y(5,t-l) - new_phage.infection_rate(y(2)) - out_b(t)*y(7) - new_phage.death_rate*y(7) + in_lib(t)*(1 - R_pnn)]#c_pnn
def dX():
    for i in range(n):
        yield reactorA[i]

#initial_state = np.array([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
initial_state = np.array([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
DDE = jitcdde(dX, verbose=True)

#DDE.constant_past([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
DDE.constant_past([new_host.c0,s0,new_host.c0,s0,0.0,0.0,original_phage.c0,new_phage.c0])
DDE.step_on_discontinuities()

data = []
x = np.arange(DDE.t, DDE.t+220, 120/100)
for time in x:
	data.append( DDE.integrate(time) )
np.savetxt("timeseries.dat", data)
print(data)
print(x)


"""
ys = odeint(dXa_dt, [
    new_host.c0,  # initial new host concentration [cell/mL]
    s0  # initial nutrient concentration [g/mL]
], xs)
    
ybs = odeint(dXb_dt, [
    new_host.c0,
    s0,
    0,0,original_phage.c0,new_phage.c0
], xs)

c_new_host_a = [y[0] for y in ys]
c_nutrient_a = [y[1] for y in ys]
"""

plt.figure(figsize=(16, 16))


plt.subplot(3, 3, 1)
plt.plot(x, [data[t][0] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('conc')
plt.title('Host Concentration A over Time')
plt.legend()
plt.subplot(3, 3, 2)
plt.plot(x, [data[t][1] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('conc')
plt.title('Nutrient A over Time')
plt.legend()
plt.subplot(3, 3, 3)
plt.plot(x, [data[t][2] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('conc')
plt.title('Host Concentration B over Time')
plt.legend()
plt.subplot(3, 3, 4)
plt.plot(x, [data[t][3] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Nutrient B over Time')
plt.legend()

plt.subplot(3, 3, 5)
plt.plot(x, [data[t][4] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Host infected OO over Time')
plt.legend()
plt.subplot(3, 3, 6)
plt.plot(x, [data[t][5] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Host infected NN over Time')
plt.legend()
plt.subplot(3, 3, 7)
plt.plot(x, [data[t][6] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Phage OO over Time')
plt.legend()
plt.subplot(3, 3, 8)
plt.plot(x, [data[t][7] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Phage NN over Time')
plt.legend()

"""
plt.subplot(3, 3, 5)
plt.plot(x, [new_host.per_cell_growth_rate(data[t][1],temperature_a(t)) for t in range(len(x))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()

plt.subplot(3, 3, 6)
plt.plot(x, [data[t][1] for t in range(len(x))], label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('temperature [°C]')
plt.title('Nutrient Concentration over Time')
plt.legend()

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
"""
"""
plt.subplot(3, 3, 4)
plt.plot(xs, [y[0] for y in ys], label="new host")
plt.xlabel('time [min]')
plt.ylabel('concentration [#bacteria/mL]')
plt.title('Host Concentration over Time')
plt.legend()


plt.subplot(3, 3, 5)
plt.plot(xs, [new_host.t_dep(temperature_a(x))*new_host.per_cell_growth_rate(c_nutrient_a[x]) for x in np.arange(0, len(xs))], label="new host")
plt.xlabel('time [min]')
plt.ylabel('rate')
plt.title('Actual Growth Rate over Time')
plt.legend()


plt.subplot(3, 3, 6)
plt.plot(xs, c_nutrient_a, label="reactor A")
plt.xlabel('time [min]')
plt.ylabel('nutrient concentration [g/mL]')
plt.title('nutrient Concentration over Time')
plt.legend()
"""

"""
#Reactor B
plt.subplot(3, 3, 1)
plt.plot(xs, [y[0] for y in ybs], label="New host")
plt.xlabel('time [min]')
plt.ylabel('host conc. [bacteria/mL]')
plt.title('Host')
plt.legend()
plt.subplot(3, 3, 2)
plt.plot(xs, [y[1] for y in ybs], label="nutrient")
plt.xlabel('time [min]')
plt.ylabel('nutrient concentration [g/mL]')
plt.title('Nutrient')
plt.legend()
plt.subplot(3, 3, 3)
plt.plot(xs, [y[2] for y in ybs], label="host inf by original phage")
plt.xlabel('time [min]')
plt.ylabel('host conc. [bacteria/mL]')
plt.title('infected bact by poo')
plt.legend()
plt.subplot(3, 3, 4)
plt.plot(xs, [y[3] for y in ybs])
plt.xlabel('time [min]')
plt.ylabel('host conc. [bacteria/mL]')
plt.title('infected bact by pnn')
plt.legend()
plt.subplot(3, 3, 5)
plt.plot(xs, [y[4] for y in ybs])
plt.xlabel('time [min]')
plt.ylabel('phage conc. [phage/mL]')
plt.title('Phage original')
plt.legend()
plt.subplot(3, 3, 6)
plt.plot(xs, [y[5] for y in ybs])
plt.xlabel('time [min]')
plt.ylabel('phage conc. [phage/mL]')
plt.title('Phage new')
plt.legend()

"""
"""
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
plt.ylim([0,0.04])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.title('Growth Rate (nutrient)')
plt.legend()


plt.subplot(3, 3, 9)
nutrient_x = np.linspace(0.1, 1)
lin = [new_host.per_cell_growth_rate(x,37) for x in nutrient_x]
plt.plot(nutrient_x, lin, label="new host")
plt.ylim([0,0.04])
plt.xlabel('nutrient concentration [g/mL]')
plt.ylabel('per cell growth rate')
plt.title('Growth Rate at high conc. of nutrient')
plt.legend()
"""
plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()
