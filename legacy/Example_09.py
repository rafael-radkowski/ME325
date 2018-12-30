# Import the failure theory envelopes
from ME325Common.FailureTheories import *
from StressCalc import *

from ME325Common.FatigueFailureTheories import *

# dimensions, all in inch
l1 = 1
l2 = 3
l3 = 4
l4 = 2
l5 = 2.5
d1 = 1
d2 = 1.5
d3 = 2
d4 = 1.5


# Material parameters
Sut = 110
Sy = 90
Se = 30


# force
F = 20000 # lbf

F_a = 20000 # lbf

# overall dimension
l = l1 + l2 + l3 + l4

N_low_cycle = 1E3
N_endurance = 1E6



def example_09_Q1(F):


    # 1) Compute the reaction forces
    By =  F * (l1 + l2 + l3/2.0) / l
    Ay = - By + F
    print ("Reaction forces Ay = " + str(Ay) + ", By = " + str(By) )


    # 2) Compute the max. bending stress
    s_zz = (Ay * (l1+ l2+l3/2) * 32) / (np.pi * d3**3)

    s_zz_2 = (By * (l4 + l3 / 2) * 32) / (np.pi * d3 ** 3) # to doublecheck.
    print ("Max. bending stress = " + str(s_zz)  )


    # Compute the endurance limit

    iterations = compute_fatigue_iterations(s_zz/ 1000.0, Sut, Sy, Se, N_low_cycle, N_endurance)
    print ("Expected iterations = " + str(iterations))


    return  iterations, s_zz



def example_09_Q2(F):


    # 1) Compute the reaction forces
    By = F * (l1 + l2 + l3 / 2.0) / l
    Ay = - By + F

    Ax = F_a

    print ("Reaction forces Ay = " + str(Ay) + ", Ax = " + str(Ax)+ ", By = " + str(By))

    # 2) Compute the max. bending stress
    s_zz = (- Ay * (l1 + l2 + l3 / 2) * 32) / (np.pi * d3 ** 3)
    print ("Bending stress = " + str(s_zz))


    # 3) Compute the normal stress
    s_n = - 4.0 * F_a / (np.pi * d3**2)
    print ("Axial stress = " + str(s_n))
    pass



itr, sf = example_09_Q1(F)
print("------------------------")
example_09_Q2(F)


# plot the the sn diagram
fig1, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.150)


plot_SN_diagram(Sut, Sy, Se, N_low_cycle, N_endurance)
l1, = plt.plot([itr, itr], [0, sf/1000.0], 'r-', color='r', lw=1)
l2, = plt.plot([0, itr], [sf/1000.0, sf/1000.0], 'r-', color='r', lw=1)


plt.show()