'#'"""

This script implements the solution for ME325, HW no 2.

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""

# Import the failure theory envelopes
from ME325Common.FailureTheories import *

from ME325Common.StressCalc import *

'# ---------------------------------------------'
'# Upper beam'
'# ---------------------------------------------'

'# Forces'
F = 2000.0
F_g = 0.0 # is recalculated later. It is unknown


' # dimensions'
l1 = 780 # in
x = l1 / 2


Sy = 95.0 #kpsi
n = 1.2


def plot_bending_stess(M1, x1, M2, x2, M3, x3):

    pl_moment, = plt.plot([0.0, x1, x2, x3], [0, M1, M2, M3], 'ro-', lw=1.0, label="bending moment")
    plt.xlabel("x-axis [in]")
    plt.ylabel("Bending moment")
    plt.grid()



def second_moment_of_area(w, h, t):
    """
    This function computes the second moment of area for a rectangular, hollow shaped beam
    :param w: width of the cross-section
    :param h: height of th cross-section
    :param t: thickness of the material
    :return: second moment of area.
    """

    I = 2* ( w*t**3/12 * w*t*(h/2)**2 ) + 2 * ( t * h**3/12)

    return I


def calc_force_from_volume(w, h, t):

    r = 0.291 #lbs/in3

    vol = ((w*h) -  ((w-2*t) * (h-2*t))) * l1 # inch ^3

    print ("Volumne: " + str(vol))

    F = vol * r * 32.17 # ft/s^2

    return F



def solve_stres(Fm, Fg, x_f):
    """

    :return:
    """

    '# Reaction forces'
    F_b = (Fg * (l1/2) + Fm * x_f)/ l1
    F_a = Fm + Fg - F_b

    print("Reaction forces")
    print("\tF_A = " + str(F_a))
    print("\tF_B = " + str(F_b))


    '# Bending moment'

    M1 = 0.0
    M2 = 0.0
    M3 = 0.0

    if x_f < l1/2:
        M1 = F_a * x_f  # for x_f
        M2 = F_a *  l1/2 - F*(l1/2 - x_f) # for l1/2
        M3 = 0  # for l1

        plot_bending_stess(M1, x_f, M2, l1/2, M3, l1)

    elif x_f > l1/2:
        M1 = F_a * x_f  # for l1/2
        M2 = F_a * x_f - Fg * (x_f - l1/2)  # for x_f
        M3 = 0.0 # for l1

        plot_bending_stess(M1, l1/2, M2, x_f / 2, M3, l1)

    else:  #x_f == l1/2
        M1 =  F_a  * l1/2
        M2 = 0.0 # this components do not exist anymore
        M3 = 0.0

        plot_bending_stess(M1, l1 / 2, M2, l1, M3, l1)

    print("Bending moments")
    print("\tM1 = " + str(M1) + " lbf-in")
    print("\tM2 = " + str(M2) + " lbf-in")
    print("\tM3 = " + str(M3) + " lbf-in")



    '# Dimensions'

    sigma_max = Sy / n

    print("Max stress")
    print("\tsigma max = " + str(sigma_max))

    return M1, M2, M3, F_a, F_b, sigma_max





'# ----------------------------------------------------------'
'# First round'

print("\n-------------------------\nFirst round")
M1, M2, M3, FA, FB, sigma_max = solve_stres(F, F_g, x)

# guessing
w = 35 #in
t = 1 # in
h = 40 # in

F_new = calc_force_from_volume(w, h, t)
print ("weight force = " + str(F_new) + " lbf")

I = second_moment_of_area(w, h, t)
print ("Second momemnt of area = " + str(I) + " in^4")

s = M1 * h/2/I
print ("Stress = " + str(s) + " psi")


'# ----------------------------------------------------------'
'# Second round'

print("\n-------------------------\nSecond round")

M1, M2, M3, FA, FB, sigma_max = solve_stres(F, F_new, x)
s = M1 * h/2/I
print ("Stress = " + str(s) + "ps1")

factor_of_safety = sigma_max / (s/1000.0)
print ("factor_of_safety = " + str(factor_of_safety))



'# ----------------------------------------------------------'
'# Lower support '

print("\n-------------------------\nLower support")

l2 = 384.0 # in
l3 = 144.0 # in
l4 = 216.0 # in



k = float(( (l4-l3)/2 ) / l2)
alpha = np.arctan(k)
print ("\talpha = " + str(alpha * 180.0 / math.pi) )

Fd = FB / np.cos(alpha)
print ("\tForce Fd = " + str(Fd) + "lbf")


radius  = np.sqrt(Fd / (math.pi * sigma_max * 1000.0))

print ("\tRadius for the lower support beam = " + str(radius))


plt.show()