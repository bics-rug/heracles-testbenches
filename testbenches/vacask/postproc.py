from rawfile import rawread
import matplotlib as mpl
import matplotlib.pyplot as plt 
import numpy as np
from scipy.integrate import cumulative_trapezoid

data_p = rawread("tran1.raw").get()
data_c = rawread("tran2.raw").get()

current_p = -data_p["vin:flow(br)"]
voltage_p = data_p["vin"]
time_p= data_p["time"]
polarization = cumulative_trapezoid(current_p, time_p)

current_c = -data_c["vpulse:flow(br)"]
voltage_c = data_c["vin"]
time_c = data_c["time"]

index = np.searchsorted(time_c, 1e-3)

cmap = plt.get_cmap("Dark2")

fig_p, (ax_iv, ax_pv) = plt.subplots(2, 1, sharex=True)
fig_c, ax_vsine = plt.subplots()
ax_isine = ax_vsine.twinx()

ax_iv.plot(voltage_p, current_p)
ax_pv.plot(voltage_p[1:], polarization)
ax_vsine.plot(time_c[index:], voltage_c[index:], c=cmap(0/6), label="V")
ax_isine.plot(time_c[index:], current_c[index:], c=cmap(1/6), label="I")

ax_vsine.legend()
ax_isine.legend()
ax_vsine.set_xlabel("Time [s]")
ax_vsine.set_ylabel("Voltage [V]")
ax_isine.set_ylabel("Current [A]")

fig_p.savefig("hysteresis_p.png", dpi=300)
fig_c.savefig("hysteresis_c.png", dpi=300)
