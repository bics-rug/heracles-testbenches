.title Polarization-Voltage hysteresis

.options warn=1 
.model fecap heracles
.include modelcard.l

V1 in gnd dc 0 PULSE (-4 4 0 500u 500u 1u 1m)
N1 te gnd fecap
R1 in te 50

.probe I(V1)
.control
    pre_osdi heracles.osdi
    tran 1u 1m
    write pv.raw
.endc

.end
