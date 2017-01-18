"""

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
Sut = 50.0 # kpsi
Suc = 110.0 # kpsi

#-- factor of safety
n = 1.2

#-- Load is unknowns

#-- Dimensions
#dimensions of the first beam
r1 = 1.0 #in
l1 = 8.0 #in

# dimensions of the second beam
r2 = 0.6 #in
l2 = 20.0 #in






# 1. Compute the max. normal stress
# since the load is unknown, we describe the load as function of F.
def sigma_x(F, l, d):
    return (F*l*32)/(math.pi * d**3)

# 2. Compute the max. shear stress
def tau_xz(T,d):
    return (T * 16)/(math.pi * d**3)

print sigma_x(1,l1,r1*2.0)
print tau_xz(l2,r1*2.0)

# 3. Compute the principle stresses as a factor of F
[s1, s2, a] = PrincipleStress([sigma_x(1,l1,r1*2.0)], [tau_xz(l2,r1*2.0)] ) # x F
print "Principle stresses for s1:", s1, "* F [kpsi] and \ts2: ", s2 ,"* F [kpsi]"


# 4. Compute the missing forces
F1 = 0.0
F2 = 0.0
if s1 > 0.0:
    F1 = Sut * 1000.0 / (n * s1)
else:
    F1 = -Suc * 1000.0 / (n * s1)


if s2 > 0.0:
    F2 = Sut * 1000.0 / (n * s2)
else:
    F2 = -Suc * 1000.0 / (n * s2)

# we proceed with the smaller one since the material would fail at the lower falue first.
F = min(F1, F2)
print "The force is F = ", F, " lbf"

#-----------------------------------------------------------------
# For Modified-Mohr and MNST Theory


s1_f = s1 * F / 1000.0
s3_f = s2 * F / 1000.0
print "The final stress is sigma_1 = ", s1_f, "kpsi, and sigma_3 =", s3_f, 'kpsi'



#-----------------------------------------------------------------
# For Coulumb-Mohr Theory

n_cm = brittle_coulumb_fos(s1_f, s3_f, Sut, Suc)
print "Coulumb-Mohr failure theory factor of safety: ", n_cm

print "---------\nCorrecting for Coulumb Mohr theory"
F_cm = 1.0/( n *( (s1/Sut) - (s2/Suc) )  ) * 1000.0 # from psi to kpsi
print "Max. force accoriding to Coulumb-Mohr theory: F=", F_cm, " lbf"

s1_cm = s1 * F_cm / 1000.0
s3_cm = s2 * F_cm / 1000.0
print "The final stresses using CM theory sigma_1 = ", s1_cm, "kpsi, and sigma_3 =", s3_cm, 'kpsi'

#######
# PLOT

fig = plt.figure(figsize=(8, 8))

# Plot the stress point
pl_s, = plt.plot([s1_f], [s3_f], 'ro')
pl_s2, = plt.plot([s1_cm], [s3_cm], 'bo')

# Plot the failure envelopes
plotModMohrFailureTheory(Sut, Suc)
plotCoulumbMohrFailureTheory(Sut, Suc)
plotMaxNormalFailureTheory(Sut, Suc)


# Axis
plt.axis([-120, 120, -120, 120])

plt.ylabel('sigma_3 [kpsi]')
plt.xlabel('sigma_1 [kpsi]')
plt.grid()
plt.show()