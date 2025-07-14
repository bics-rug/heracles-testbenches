* Load OSDI model
.control
pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
write fefet.raw
tran 1u 1m
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
V1 vin vin_n PULSE (0 4 0 10u 10u 50u 1m)
V2 vin_n gnd PULSE (0 2.5 70u 100u 100u 1m 1m)
V3 vdd gnd DC 0.2
N1 te gate fecap
R1 vin te 50
R2 gate gnd 10T
M1 vdd gate gnd gnd n1 l=200n w=200n

