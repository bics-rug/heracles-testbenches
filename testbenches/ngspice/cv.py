import matplotlib.pyplot as plt
import numpy as np
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit

logger = Logging.setup_logging()

steps = 20

tstep = 1e-8
tstop = 1.2e-3

vset_list = np.linspace(-4, 4, steps)
vreset_list = [-4, 4]
tpulse = 1e-6
vsine = 42e-3
fsine = 10e3
tsine = 1e-3

splice = (tstop - tsine) / tstep

fig, ax = plt.subplots(figsize=[3.45, 2.3])
for vreset in vreset_list:
    capacitances = []

    for index, vset in enumerate(vset_list):

        circuit = Circuit("FeCap parameter extraction")
        circuit.raw_spice = f"""
            * Load OSDI model
            .control
            pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
            .endc

            * Model definition with current parameters
            .model fecap heracles ( 
                + area = 1e-12
                + t_fe = 10e-9 
                + t_int = 2e-9 
                + eps_fe = 70 
                + eps_int = 7
                + w_b = 1.05 
                + d_e = 7.5e-9 
                + e_off = 1e7
                + p_s = 20e-2 
                + n_depl = 1.2e28 
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

            * Circuit elements
            V1 vin_i 0 PULSE ( {vreset} {vset} {tpulse} 1n 1n 1k 2k )
            V2 vin vin_i SIN ( 0 {vsine} {fsine} {tsine} 0 0 )
            R1 vin te 50
            N1 te be fecap
            R2 be 0 50

            .probe I(V1)
            """

        simulator = circuit.simulator(temperature=21, nominal_temperature=21)
        analysis = simulator.transient(tstep, tstop)

        time = analysis.time[int(-splice*6/10):int(-splice/10)]
        voltage = analysis.vin[int(-splice*6/10):int(-splice/10)]
        current = analysis.v1[int(-splice*6/10):int(-splice/10)]

        vmax_index = np.argmax(voltage)
        vmin_index = np.argmin(voltage)
        imax_index = np.argmax(current)
        imin_index = np.argmin(current)

        v_amplitude = (voltage[vmax_index] - voltage[vmin_index]) / 2
        i_amplitude = (current[imax_index] - current[imin_index]) / 2

        z_abs = float(v_amplitude / i_amplitude)
        z_phase = float((time[vmax_index] - time[imax_index]) * fsine * 2*np.pi)
        impedance = z_abs * np.exp(1j*z_phase)

        c = -1/np.imag(impedance)/2/np.pi/fsine
        capacitances.append(c)

    ax.plot(vset_list, capacitances)

fig.savefig("cv.png")