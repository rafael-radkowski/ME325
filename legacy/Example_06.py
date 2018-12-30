'#'"""

This script implements the solution for ME325, example no 6.

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""

# Import the failure theory envelopes

from ME325Common.StressCalc import *

'#' """
##################################################################
Dimensions:
All dimensions in inch
"""

l1 = 3.5
l2 = 6
l3 = 3
l4 = 0.25
l5 = 1.5
l6 = 3

d1 = 1.5
d2 = 2.5
d3 = 1.4
d4 = 1


'# Radius of the notch'
r = 0.2


'# The force'
F = 2000 # lbf

'# Yield strength'
Sy = 90.0 # kpsi


def example_06():
    """

    :return:
    """


    '# Reaction forces'

    k1 = l1 + l6
    k2 = l2 - l6 + l3 + l4


    F_B = (F * k1) / (k1 + k2)
    F_A = F - F_B

    print ("Reaction forces")
    print ("\tF_A = " + str(F_A))
    print ("\tF_B = " + str(F_B))

    '# ---------------------------------'
    '# Bending moment'

    M_1_l = F_A * k1
    M_1_r = F_B * k2

    print ("Bending moment (both must be equal")
    print ("\tM_1 = " + str(M_1_l))
    print ("\tM_1 = " + str(M_1_r))

    print ("Forces (both must be equal")


    '#--------------------------------------------------------'
    '# Bending moment at most critial locations'

    M_c1 = F_A * l1
    M_c2 = F_A * (l1 + l5)
    M_c3 = F_B * (l3 + l4)

    print ("Bending moment at critical locations")
    print ("\tM_c1 = " + str(M_c1))
    print ("\tM_c2 = " + str(M_c2))
    print ("\tM_c3 = " + str(M_c3))

    '#--------------------------------------------------------'
    '# Second moment of area'

    I_c1 = math.pi * d1 / 64.0 # in^4
    I_c2 = math.pi * d2 / 64.0 # in^4
    I_c3 = math.pi * d3 / 64.0 # in^4

    print ("Second moment of area")
    print ("\tI_c1 = " + str(I_c1))
    print ("\tI_c2 = " + str(I_c2))
    print ("\tI_c3 = " + str(I_c3))

    '#--------------------------------------------------------'
    '# Bending stress '

    s_c1 = M_c1 * (d1/2) / I_c1
    s_c2 = M_c2 * (d2/2) / I_c2
    s_c3 = M_c3 * (d3/2) / I_c3

    print ("Stresses at the critical locations")
    print ("\ts_c1 = " + str(s_c1))
    print ("\ts_c2 = " + str(s_c2))
    print ("\ts_c3 = " + str(s_c3))

    '#--------------------------------------------------------'
    '# Stress intensity factors from chart'

    kt_c1 = 1.7
    kt_c3 = kt_c1
    kt_c2 = 1.5

    s_c1_m = s_c1 * kt_c1
    s_c2_m = s_c2 * kt_c2
    s_c3_m = s_c3 * kt_c3

    print ("MAXIMUM stresses at the critical locations")
    print ("\ts_c1_max = " + str(s_c1_m))
    print ("\ts_c2_max = " + str(s_c2_m))
    print ("\ts_c3_max = " + str(s_c3_m))



    n_c1 = Sy * 1000.0/ s_c1_m
    n_c2 = Sy * 1000.0 / s_c2_m
    n_c3 = Sy * 1000.0 / s_c3_m

    print ("Factor of safety")
    print ("\tn_c1 = " + str(n_c1))
    print ("\tn_c2 = " + str(n_c2))
    print ("\tn_c3 = " + str(n_c3))







    '# PLOT'

    fig1 = plt.figure()
    pl_moment, = plt.plot([0.0, k1, k1 + k2], [0, M_1_l, 0], 'ro-', lw=1.0, label="bending moment")
    pl_forces, = plt.plot([0.0, 0.0, k1, k1, k1+k2, k1 + k2], [0, F_A, F_A, F_A - F, F_A -F,  F_A -F + F_B], 'bo-', lw=1.0, label="shear forces")
    plt.plot([0.0,  k1 + k2], [0, 0], 'k-', lw=4.0)
    plt.xlabel("x-axis [in]")
    plt.ylabel("load distribution")
    plt.legend(handles=[pl_moment, pl_forces])
    plt.grid()

    fig1 = plt.figure()
    plotVonMiesesFailureTheory(Sy)
    plotTrescaFailureTheory(Sy)
    plt.grid()

    plt.plot([s_c1_m / 1000.0], [0.0], 'ro-', lw=1.0, label="sigma_c1")
    plt.plot([s_c2_m / 1000.0], [0.0], 'ro-', lw=1.0, label="sigma_c2")
    plt.plot([s_c3_m / 1000.0], [0.0], 'ro-', lw=1.0, label="sigma_c3")





    plt.show()






example_06()


