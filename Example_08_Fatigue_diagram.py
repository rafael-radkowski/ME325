'#'"""

This script implements an example demonstrating the use of an SN-diagram to identify the
fatigue strenght for a material (steel, alloys, etc.)
Note, the SN-diagram is empirically determined. Thus, the fatigue strength is no gurantee
that a part will not fail.

The SN-diagram implementation can be found in file FatigueFailureTheories.

This file is part of the course ME 325 "Machine Component Design"

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""

from pylab import *
import numpy as np;
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# Import the failure theory envelopes
from FailureTheories import *
from StressCalc import *
from FatigueFailureTheories import *


Sut = 110 # kpsi
Sy = 95 # kpsi,
Se = 33.8 # kpsi, the endurance limit

N_inv = 1E+7 # the infinte lifetime limit
N_lcc = 1E+2 # low cycle to high cycle switch.



sa = 20.0
sm = 20.0


def factor_of_safety(sa, sm, Se, Sut):
    n_gerber = Gerber_FoS(sa, sm, Se, Sut)
    n_goodman = mod_Goodman_Fos(sa, sm, Se, Sut)

    print ("FoS, Geber = " + str(n_gerber) + "\t Goodman = " + str(n_goodman))

    return n_gerber, n_goodman


def load_line_slope(sa_, sm_):
    """
    Computes the slope of the load line
    :param sa_: alternating load
    :param sm_: midrange load
    :return:
    """
    return sa_ / sm_ * 300;




fig2, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.150)


# plot the diagram
plot_fatigue_diagram(Se, Sy, Sut)


# Plot the stress point
pl_s1, = plt.plot([sm], [sa], 'ro', label="location C")


# load lines
pl_ll, = plt.plot([0.0, 300], [0.0, load_line_slope(sa, sm)], 'k--')


# Compute the initial factor of safety.
fos_gerber, fos_goodman = factor_of_safety(sa, sm, Se, Sut)
pl_text1 = text(5, 112, ["FoS Gerber", fos_gerber], fontsize=14)
pl_text2 = text(5, 106, ["FoS Mod. Goodman", fos_goodman], fontsize=14)



sa_slider_obj = plt.axes([0.1, 0.04, 0.3, 0.03], axisbg='lightyellow')
sa_slider = Slider(sa_slider_obj, 's_a', 0.0, 100.0, valinit=sa)
# Update function for the slider
def update1(val):
    global T1

    sa = val

    # update the point
    pl_s1.set_data([sm], [sa])

    # update load lines
    pl_ll.set_data([0.0, 300], [0.0, load_line_slope(sa, sm)])

    # Update the factor of safety
    fos_gerber, fos_goodman = factor_of_safety(sa, sm, Se, Sut)
    pl_text1.set_text(["FoS Gerber", fos_gerber])
    pl_text2.set_text(["FoS Mod. Goodman", fos_goodman])


    fig2.canvas.draw_idle()
sa_slider.on_changed(update1)




sm_slider_obj = plt.axes([0.55, 0.04, 0.3, 0.03], axisbg='lightyellow')
sm_slider = Slider(sm_slider_obj, 's_m', 0.0, 100.0, valinit=sa)
# Update function for the slider
def update2(val):
    global T1

    sm = val

    # update the point
    pl_s1.set_data([sm], [sa])

    # update load lines
    pl_ll.set_data([0.0, 300], [0.0, load_line_slope(sa, sm)])

    # Update the factor of safety
    fos_gerber, fos_goodman = factor_of_safety(sa, sm, Se, Sut)
    pl_text1.set_text(["FoS Gerber", fos_gerber])
    pl_text2.set_text(["FoS Mod. Goodman", fos_goodman])


    fig2.canvas.draw_idle()
sm_slider.on_changed(update2)


plt.show()