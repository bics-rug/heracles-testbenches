import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit

tstep = 1e-8
tstop = 170e-6
vgate_list = [4, -5]

fig_vt, axs_vt = plt.subplots(figsize=[3.45, 2.3], constrained_layout=True)
fig_it, axs_it = plt.subplots(2, figsize=[3.45, 2.3], constrained_layout=True)

for vgate in vgate_list:
    circuit = Circuit("FeFET")
    circuit.raw_spice = f"""
        * Load OSDI model
        .control
        pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
        .endc
        .options reltol=0.001 abstol=1e-12 gmin=1e-12

        * Model definition with current parameters
        .model fecap heracles ( 
            + area = 4e-14
            + t_fe = 10e-9 
            + t_int = 0.5e-9 
            + eps_fe = 70 
            + eps_int = 90
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
            + phi_tr_fe = 1.05
            + area_mc = 0 
            + t_fe_mc = 0 
            + t_int_mc = 0 
            + p_s_mc = 0 
            + n_depl_mc = 0)

        .model n1 nmos level=54 version=4.8.2

        * Circuit elements
        V1 vin vin_n PULSE (0 {vgate} 0 10u 10u 50u 1m)
        V2 vin_n gnd PULSE (0 2.5 70u 100u 100u 1m 1m)
        V3 vdd gnd DC 0.2
        N1 te gate fecap
        R1 vin te 50
        R2 gate gnd 10T
        M1 vdd gate gnd gnd n1 l=200n w=200n
        """

    simulator = circuit.simulator(temperature=21, nominal_temperature=21)
    analysis = simulator.transient(tstep, tstop)

    time = analysis.time
    voltage = analysis.vin
    ig = -analysis.v1
    id = -analysis.v3
    vgmos = analysis.nodes["gate"]

    axs_vt.plot(time*1e6, voltage, label="Applied")
    axs_vt.plot(time*1e6, vgmos, label="Internal")
    axs_it[0].plot(time*1e6, voltage)
    axs_it[1].plot(time*1e6, id*1e6)

axs_vt.set_ylabel("Voltage [V]")
axs_vt.set_xlabel("Time [μs]")
axs_vt.legend()
fig_vt.savefig("fefet_vt.png", dpi=600)
axs_it[0].set_ylabel("Voltage [V]")
axs_it[1].set_xlabel("Time [μs]")
axs_it[1].set_ylabel("Drain current [μA]")
#axs_it[1].set_yscale("log")
fig_it.savefig("fefet_it.png", dpi=600)