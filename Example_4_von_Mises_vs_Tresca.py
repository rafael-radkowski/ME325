"""
Example for ME325 - Machine Component Design
Ductule Failure Theory Example

Please review the related class notes for further information about the example and the values.

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

##-------------------------------------------------------
## Parameters

# Yield strength
Sy = 110.0 # kpsi

# Load exerted to the beam
F = 3600.0 # lbf

#dimensions of the first beam
r1 = 0.6 #in
l1 = 9.0 #in

# dimensions of the second beam
r2 = 0.9 #in
l2 = 15.0 #in


##-------------------------------------------------------
## computations

def example3(F):

    s11 = 60
    s22 = 40
    t12 = -15

    # find the principle stresses
    [s1, s2, alpha] = PrincipleStress([60,40], [-15])
    print "Princ. stresses ", s1, "\t", s2, "\tat", alpha



    # the von Mieses stress
    s_vm = vonMises([s11,s22], [t12])
    #s_vm = sqrt(s11**2 - s11 * s22 + s22 ** 2 + 3.0 *(t12**2))
    #s_vm = sqrt(s1**2 - s1*s2 + s2**2)
    print "von Mises stress s_vm = ", s_vm, " psi"



    norm = sqrt(np.cos(-alpha)**2 + np.sin(-alpha)**2  -  np.cos(-alpha) * np.sin(-alpha))
    a_cos = np.cos(-alpha)/norm * s_vm
    a_sin = np.sin(-alpha)/norm * s_vm
    print a_cos, "\t", a_sin

    n = abs(Sy / (s_vm / 1000.0))
    print "Final factor of safety: ", n

    #return [a_cos, a_sin, n]

    # compute the factor of safety
    n1 = abs(Sy/(s1/1000.0));
    n2 = abs(Sy/(s2/1000.0));

    print "Computed factors n1 ", n1, "\tn2: ", n2
    print "Final factor of safety: ", min(n1, n2)

    return [s1, s2, min(n1, n2)]

[s1, s2, n] = example3(F)




fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.15)
fig.set_size_inches(8,8, forward=True)



# Plot the stress point
pl_s, = plt.plot([s1], [s2], 'ro')

plotVonMiesesFailureTheory(Sy)
plotTrescaFailureTheory(Sy)
plt.grid()
plt.xlabel("sigma_1")
plt.ylabel("sigma_3")
plt.title("Example 3 - Ductile Materia Failure Theories")



# Add a slider
forceF = plt.axes([0.2, 0.02, 0.65, 0.03], axisbg='lightyellow')
ForceFslider = Slider(forceF, 'Load', -4500.0, 4500.0, valinit=F)


# Update function for the slider
def update(val):
    [sigma_1, sigma_3, n] = example3(val)
    pl_s.set_data([sigma_1], [sigma_3])
    fig.canvas.draw_idle()
ForceFslider.on_changed(update)



#show the plot

plt.show()


show()