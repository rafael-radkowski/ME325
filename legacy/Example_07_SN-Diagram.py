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

# Import the failure theory envelopes
from StressCalc import *

from ME325Common.FatigueFailureTheories import *

Sut = 110 # kpsi
Sy = 95 # kpsi,
Se = 40 # kpsi, the endurance limit

N_inv = 1E+7 # the infinte lifetime limit
N_lcc = 1E+2 # low cycle to high cycle switch.



def solve_example_07(itr):


    Sf = compute_fatigue_strength(itr, Sut, Sy, Se, N_lcc, N_inv)
    print ("Sf = " + str(Sf))

    return Sf





itr = 100000
Sf = solve_example_07(itr)



fig1, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.150)

# plot the the sn diagram
plot_SN_diagram(Sut, Sy, Se, N_lcc, N_inv)
l1, = plt.plot([itr, itr], [0, Sf], 'r-', color='r', lw=1)
l2, = plt.plot([0, itr], [Sf, Sf], 'r-', color='r', lw=1)




itr_slider_obj = plt.axes([0.1, 0.04, 0.6, 0.03], axisbg='lightyellow')
itr_slider = Slider(itr_slider_obj, 'itr', 0.0, 10000000, valinit=itr)

# Update function for the slider
def update1(val):
    global T1

    itr = val

    Sf = solve_example_07(itr)

    # update the lines
    l1.set_data([itr, itr], [0, Sf])
    l2.set_data([0, itr], [Sf, Sf])



    fig1.canvas.draw_idle()
itr_slider.on_changed(update1)


plt.show()

