"""
Example for ME325 - Machine Component Design
Brittle Failure Theory Example no 1.

This example deomonstrates the application of brittle failure envolopes using a toy example.
A 1-axis load exerted on a rectangluar bar.
Please review the related class notes for further information about the example and the values.


In general:
Sut - Ultimate tensile strength
Suc - Ultimate compression strength
F - load
width, height - the cross-section of the bar.

The code returns the principle stresses along w
ith the factor of safety and plots the brittle failure theory plots.


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



## Values, note, the values should be positive
## And all values in kpsi

#-- Material parameters
Sut = 35.0 # kpsi
Suc = 95.0 # kpsi

#-- Load
F = 10000.0 # lbf


#-- Dimensions
width = 1.0 # in
height = 0.35 # in


#############################################################################################

def example1(Load):
    """
    Solves ME325 Example problem no 1
    :param Load: the load in kpsi
    :return: a vector with [sigma_1, sigma_3, n], the first and third principle stress, and n, the factor of safety.
    """

    ##
    # stress calculations

    sigma_x = Load / (width * height)
    sigma_y = 0.0;

    print "Sigma_x: ", sigma_x, "\tSigma_y: ", sigma_y



    # principle stresses (there are equal to sigma_x and sigma_y in this case.
    # But we always search for the principle stresses.

    [sigma_1, sigma_3, angle] = PrincipleStress([sigma_x/1000.0], [0.0])

    print "Sigma_1: ", sigma_1, "\tSigma_3: ", sigma_3, "angle: ", angle


    #factor of safety

    n = FoS(sigma_1, sigma_3, Sut, Suc)
    print "Factor of safety: ", n


    # uncertainty
    # with a material Sut and Suc certainty of 5%
    x = n * 0.95;
    print "Load uncertainty: ", (x*100)-100, "%"


    return[sigma_1, sigma_3, n]


############################################################################

[sigma_1, sigma_3, n] = example1(F)



#########################################################
## Plot

fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.15)
#fig.set_size_inches(8,8, forward=True)


# Plot the stress point
pl_s, = plt.plot([sigma_1], [sigma_3], 'ro')

# Plot the failure envelopes
plotModMohrFailureTheory(Sut, Suc)
plotCoulumbMohrFailureTheory(Sut, Suc)
plotMaxNormalFailureTheory(Sut, Suc)

pl_t = text(-90, 90, ["FoS", n], fontsize=12)



# Axis
plt.axis([-100, 100, -100, 100])

plt.ylabel('sigma_3 [kpsi]')
plt.xlabel('sigma_1 [kpsi]')
plt.grid()


# Add a slider
forceF = plt.axes([0.2, 0.02, 0.65, 0.03], axisbg='lightyellow')
ForceFslider = Slider(forceF, 'Load', -40000.0, 40000.0, valinit=F)

# Update function for the slider
def update(val):
    [sigma_1, sigma_3, n] = example1(val)
    pl_s.set_data([sigma_1], [sigma_3])
    pl_t.set_text(["FoS", n])
    fig.canvas.draw_idle()
ForceFslider.on_changed(update)



#show the plot
plt.show()






