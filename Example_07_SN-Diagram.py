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
Se = 30 # kpsi, the endurance limit

N_inv = 1E+7 # the infinte lifetime limit
N_lcc = 1E+2 # low cycle to high cycle switch.



def solve_example_07():

    itr = 100000

    Sf = compute_fatigue_strength(itr, Sut, Sy, Se, N_lcc, N_inv)
    print ("Sf = " + str(Sf))


    # plot the the sn diagram
    plot_SN_diagram(Sut, Sy, Se, N_lcc, N_inv)
    plt.plot([itr, itr], [0, Sf], 'r-', color='b', lw=1)

    plt.show()



solve_example_07()