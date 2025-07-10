import matplotlib.pyplot as plt
import numpy as np
from PySpice.Spice.Netlist import Circuit
from scipy.integrate import cumulative_trapezoid

steps = 10
sweep = np.linspace(-4, 4, steps)

tstep = 1e-6
tstop = 1e-3

circuit = Circuit("FeCap parameter extraction")
circuit.raw_spice = """
    * Load OSDI model
    .control
    pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
    .endc

    * Model definition with current parameters
    .model fecap heracles ( 
        + area = 1e-12
        + t_fe = 10e-9 
        + t_int = 0.5e-9 
        + eps_fe = 30 
        + eps_int = 7
        + w_b = 1.05 
        + d_e = 7.5e-9 
        + e_off = 1e7
        + p_s = 25e-2 
        + n_depl = 1.2e29
        + eps_depl = 2.2
        + q_fix_depl_u = -8e-2 
        + q_fix_depl_d = 20e-2 
        + m_eff_fe = 0.4 
        + m_eff_int = 0.3
        + phi_b_fe = 2 
        + phi_b_int = 2.7
        + mu_fe = 0.2
        + n_c_fe = 1e24 
        + phi_tr_fe = 1.5 
        + area_mc = 0 
        + t_fe_mc = 0 
        + t_int_mc = 0 
        + p_s_mc = 0 
        + n_depl_mc = 0)

    * Circuit elements
    V1 vin gnd PULSE (-4 4 0 500u 500u 1u 1m)
    N1 te gnd fecap
    R1 vin te 50
    """

simulator = circuit.simulator(temperature=21, nominal_temperature=21)
analysis = simulator.transient(tstep, tstop)

time = analysis.time
voltage = analysis.vin
current = -analysis.v1
v_fe = analysis.nodes["n1#n_int"] - analysis.nodes["n1#n_be"]
v_be = analysis.nodes["n1#n_be"]

polarization = cumulative_trapezoid(current, time)

fig, axs = plt.subplots(2, figsize=[3.45, 2.3])
axs[0].plot(voltage, current)
axs[1].plot(voltage[:-1], polarization)

fig.savefig("pv", dpi=600)

fig, axs = plt.subplots(2, figsize=[3.45, 2.3])
axs[0].plot(time*1e3, voltage)
axs[1].plot(time*1e3, v_fe)
axs[1].plot(time*1e3, v_be)

fig.savefig("pv_internal.png", dpi=600)