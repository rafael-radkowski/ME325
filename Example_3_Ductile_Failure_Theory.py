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
l1 = 19.0 #in

# dimensions of the second beam
r2 = 0.9 #in
l2 = 15.0 #in





##-------------------------------------------------------
## computations

# helpers
set_theory = 'Principle'
current_val = F;


def example3(F, theory='Principle'):
    # ------------------------------------------------------------------------------
    #  Stress calculations

    print '\n-------------------------------------------------'

    #compute the second moment of area and the second polar moment of area
    I2_zz = np.pi * (r2*2)**4 / 64.0
    It = np.pi * (2*r2)**4 / 32.0

    # bending stress at the mounting point
    sigma_max = (F * l2 * r2) / I2_zz
    print "Sigma max: ", sigma_max/ 1000.0 , " kpsi"

    #compute the shear stress
    tau_max = F * l1 * r2 / It
    print "Tau max: ", tau_max / 1000.0, " kpsi"


    # ------------------------------------------------------------------------------
    #  principle stresses calculation
    [s1, s2, alpha] = PrincipleStress([sigma_max], [tau_max])
    print "Princ. stresses ", s1, "\t", s2, "\tat", alpha

    # helper for plotting, angle between stresses on the plot
    ang = arctan(s2/s1)

    # compute the factor of safety
    n1 = abs(Sy / (s1 / 1000.0));
    n2 = abs(Sy / (s2 / 1000.0));

    n_p = min(n1, n2)
    print "Principle stress factor of safety: ", n_p


    #-------------------------------------------------------------------------
    # the von Mises stress
    s_vm = vonMises([sigma_max], [tau_max])

    axis = sign(sigma_max)
    norm = sqrt(np.cos(ang) ** 2 + np.sin(ang) ** 2 - np.cos(ang) * np.sin(ang))
    vm_cos = axis * np.cos(ang) / norm * s_vm
    vm_sin = axis * np.sin(ang) / norm * s_vm

    print "von Mises eqv. stress s_vm = ", s_vm, " psi (", vm_cos, ", ", vm_sin, ")"
    n_vm = abs(Sy / (s_vm / 1000.0))
    print "von Mises factor of safety: ", n_vm

    # -------------------------------------------------------------------------
    # Tresca stress

    s_tresca = tresca([s1, s2])

    t_cos = 2.0 * np.cos(ang) * s_tresca
    t_sin = 2.0 * np.sin(ang) * s_tresca

    print "Tresca eqv. stress s_t = ", s_tresca
    n_tresca = axis * (1000.0*Sy/2.0)/( s_tresca)
    print "Tresca factor of safety n_t = ", n_tresca




    # -------------------------------------------------------------------------
    # Returns

    if theory == 'Principle': # principle stresses
        return [s1, s2, n_p]
    elif theory == 'vonMises': # von Mises
        return [vm_cos, vm_sin, n_vm]
    elif theory == 'Tresca': # Tresca
        return [t_cos, t_sin, n_tresca]
    else:
        return [s1, s2, n_p]




[s1, s2, n] = example3(F, set_theory)




fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.15)
fig.set_size_inches(8,8, forward=True)



# Plot the stress point
pl_s, = plt.plot([s1/1000.0], [s2/1000.0], 'ro')

plotVonMiesesFailureTheory(Sy)
plotTrescaFailureTheory(Sy)
plt.grid()
plt.xlabel("sigma_1")
plt.ylabel("sigma_3")
plt.title("Example 3 - Ductile Materia Failure Theories")



# ----------------------------------------------------------------------------
# Add a slider
forceF = plt.axes([0.2, 0.02, 0.65, 0.03], axisbg='lightyellow')
ForceFslider = Slider(forceF, 'Load', -4500.0, 4500.0, valinit=F)


# Update function for the slider
def update(val):
    global set_theory
    global current_val
    [sigma_1, sigma_3, n] = example3(val, set_theory)
    pl_s.set_data([sigma_1/1000.0], [sigma_3/1000.0])
    fig.canvas.draw_idle()
    current_val = val;
ForceFslider.on_changed(update)



# ----------------------------------------------------------------------------
# Add a radiobutton

#rax = plt.axes([0.13, 0.72, 0.15, 0.15], axisbg='white')
#radio = RadioButtons(rax, ('Principle', 'vonMises'), active=0)

def modefunc(label):
    global set_theory
    global current_val
    set_theory = label;
    print "mode is now ", set_theory

    [sigma_1, sigma_3, n] = example3(current_val, set_theory)
    pl_s.set_data([sigma_1 / 1000.0], [sigma_3 / 1000.0])
    fig.canvas.draw_idle()
#radio.on_clicked(modefunc)

# ----------------------------------------------------------------------------


#show the plot

plt.show()


show()