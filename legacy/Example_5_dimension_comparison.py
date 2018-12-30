"""
Example for ME325 - Machine Component Design
Ductule Failure Theory Example

This code contains the calculations for Example 5. Please review the example for further information.

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""

# Import the failure theory envelopes

from ME325Common.StressCalc import *

##-------------------------------------------------------
## Parameters

# Brittle material strengt
Sut = 55.0 #kpsi
Suc = 100.0 #kpsi

# Torque on the first pulley
T1 = 1000.0 # lbf-in

#distance between the pulleys
all = 12.0
l1 = 4.0 # in
l2 = 4.0 # in
l3 = 4.0 # in

# radius of the pully
r1 = 2.0 # in
r2 = 1.5 # in

## diameter of the hollow pipe
D = 2*1.0 # in
ti = 2*0.15 # in, thickness


fig1 = 0;
pl_moment = 0
pl_torque = 0
fig1_ready = False


def plot_load(F1, F2, Fa, Fb):
    global fig1
    global pl_torque
    global pl_moment
    global fig1_ready

    m_0 = 0.0;
    m_l1 = Fa * l1 # moment from the left side
    m_l11 = Fb * (l2 + l3) - F1 * l2 # moment from the rigth side

    if abs(m_l1 - m_l11 > 1E-6):
        print "ERROR"
        print m_l1, '\t', m_l11

    #print m_l1, '\t', m_l11

    m_l2 = Fb * l3
    m_3 = 0.0;

    t1 = F2 * r2;
    t2 = F1 * r1;

    if fig1_ready == False:
        fig1 = plt.figure()
        pl_moment, = plt.plot([0.0, l1, l1+l2, l1+l2+l3 ], [0, m_l1, m_l2, m_3 ], 'ro-', lw=1.0, label = "bending moment")
        pl_torque, = plt.plot([0.0, l1, l1, l1 + l2,l1 + l2, l1 + l2 + l3], [0, 0.0, t1, t2, 0.0, 0], 'bo-', lw=1.0, label="torque")
        plt.xlabel("x-axis [in]")
        plt.ylabel("load distribution")
        plt.legend(handles=[pl_moment, pl_torque])
        plt.grid()
        fig1_ready = True
    else:
        pl_moment.set_data([0.0, l1, l1+l2, l1+l2+l3 ], [0, m_l1, m_l2, m_3 ])
        pl_torque.set_data([0.0, l1, l1, l1 + l2,l1 + l2, l1 + l2 + l3], [0, 0.0, t1, t2, 0.0, 0])
        fig1.canvas.draw_idle()

    #plt.show()



def example5(T):

    print "\n-------------------------------------------------"


    # --------------------------------------------
    # Compute the reaction forces

    # force on the incomming pulley
    F1 = T / r1

    # force on the outgoing pulley
    F2 = T / r2

    # F_B
    F_B = (F1 * (l1 + l2) + F2 * l1) / (l1 + l2 + l3)

    # F_A
    F_A = F1 + F2 - F_B

    print "Forces\n F1 = ", F1 ,"psi\n F2 = ", F2, "psi\n FA = ", F_A, "psi\n FB = ", F_B, "psi."
    print -F1  -F2 + F_B + F_A

    plot_load(F1, F2, F_A, F_B)


    # --------------------------------------------
    # Compute the  polar second moment of area

    d = D - (ti*2.0)

    Ip = math.pi * (D**4 - d**4) / 32.0

    Izz = math.pi * (D**4 - d**4) / 64.0

    print "second moment of area\n J_p (polar) = ", Ip, "in^4\n Izz = ", Izz, "in^4"


    # --------------------------------------------
    # Compute the max. bending stress
    # sigma = M * c / I


    # Max. moment at l1
    M_l1 = F_A * l1

    # Max. moment at l2
    M_l2 = F_B * l3

    # the normal stresses
    s_l1 = M_l1 * (D/2) / Izz
    s_l2 = M_l2 * (D/2) / Izz

    # the shear stress
    t = T * (D/2) / Ip

    print "Stresses:\n sigma(l1) = ", s_l1, "psi\n sigma(l2) = ", s_l2, "psi\n tau =", t, "psi"


    # --------------------------------------------
    # Compute the principle stresses

    [s1_l1, s2_l1, angle1] = PrincipleStress([s_l1], [t])
    [s1_l2, s2_l2, angle2] = PrincipleStress([s_l2], [t])

    print "Principle stresses\n s1(l1) = ", s1_l1, "psi\n s2(l2) = ", s2_l1, "psi\n s1(l2) = ", s1_l2, "psi\n s2(l2) =", s2_l2, "psi"


    n_cm1 = brittle_coulumb_fos(s1_l1 / 1000.0, s2_l1 / 1000.0, Sut, Suc)
    n_cm2 = brittle_coulumb_fos(s1_l2 / 1000.0, s2_l2 / 1000.0, Sut, Suc)
    print "Coulumb-Mohr failure theory factor of safety:\n l1: ", n_cm1, "\n l2: ", n_cm2


    return [s1_l1, s2_l1, s1_l2, s2_l2]



# compute the example
[s1_l1, s2_l1, s1_l2, s2_l2] = example5(T1)

const = 1000.0

#fig, ax = plt.subplots(figsize=(8, 8))
# Plot the failure envelopes
#fig2, ax = plt.figure(figsize=(8, 8))

fig2, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.20)

plotModMohrFailureTheory(Sut, Suc)
plotCoulumbMohrFailureTheory(Sut, Suc)
plotMaxNormalFailureTheory(Sut, Suc)


# load lines
ll1y = s2_l1/s1_l1 * 300;
ll2y = s2_l2/s1_l2 * 300;

pl_ll1, = plt.plot([0.0, 300], [0.0, ll1y], 'k--')
pl_ll2, = plt.plot([0.0, 300], [0.0, ll2y], 'k--')


# Plot the stress point
pl_s1, = plt.plot([s1_l1/ const], [s2_l1/ const], 'ro', label="location C")
pl_s2, = plt.plot([s1_l2/ const], [s2_l2/ const], 'bo', label="location D")





plt.axis([-110, 110, -110, 110])
plt.legend(handles=[pl_s1, pl_s2])
plt.xlabel("sigma_1")
plt.ylabel("sigma_3")
plt.grid()


#------------------------------------------------------------------------------------
# Add a slider
torqueF = plt.axes([0.1, 0.02, 0.3, 0.03], axisbg='lightyellow')
Torqueslider = Slider(torqueF, 'Load', -1500.0, 3500.0, valinit=T1)

# Update function for the slider
def update(val):
    global T1

    T1 = val

    [s1_l1, s2_l1, s1_l2, s2_l2] = example5(val)


    #update load lines
    pl_ll1.set_data([0.0, 300], [0.0, s2_l1 / s1_l1 * 300])
    pl_ll2.set_data([0.0, 300], [0.0, s2_l2 / s1_l2 * 300])


    pl_s1.set_data([s1_l1 / const], [s2_l1 / const])
    pl_s2.set_data([s1_l2 / const], [s2_l2 / const])

    fig2.canvas.draw_idle()
Torqueslider.on_changed(update)




D_slider = plt.axes([0.6, 0.02, 0.3, 0.03], axisbg='lightyellow')
D_slider_obj = Slider(D_slider, 'Diameter', 0.1, 3.0, valinit=D)
# Update function for the slider
def update_D(val):
    global D
    global T1

    D = val

    [s1_l1, s2_l1, s1_l2, s2_l2] = example5(T1)

    # update load lines
    pl_ll1.set_data([0.0, 300], [0.0, s2_l1 / s1_l1 * 300])
    pl_ll2.set_data([0.0, 300], [0.0, s2_l2 / s1_l2 * 300])

    pl_s1.set_data([s1_l1 / const], [s2_l1 / const])
    pl_s2.set_data([s1_l2 / const], [s2_l2 / const])

    fig2.canvas.draw_idle()
D_slider_obj.on_changed(update_D)



r1_slide = plt.axes([0.1, 0.08, 0.3, 0.03], axisbg='lightyellow')
RadiusSlider = Slider(r1_slide, 'Pulley r', 0.1, 10.0, valinit=r1)

# Update function for the slider
def update_radius(val):
    global T1
    global r1

    r1 = val

    [s1_l1, s2_l1, s1_l2, s2_l2] = example5(T1)

    pl_s1.set_data([s1_l1 / const], [s2_l1 / const])
    pl_s2.set_data([s1_l2 / const], [s2_l2 / const])

    # update load lines
    pl_ll1.set_data([0.0, 300], [0.0, s2_l1 / s1_l1 * 300])
    pl_ll2.set_data([0.0, 300], [0.0, s2_l2 / s1_l2 * 300])

    fig2.canvas.draw_idle()
RadiusSlider.on_changed(update_radius)






dist_slider = plt.axes([0.6, 0.08, 0.3, 0.03], axisbg='lightyellow')
dist_slider_obj = Slider(dist_slider, 'Distance l2', 0.1, 11.0, valinit=l2)
# Update function for the slider
def update_distance(val):
    global l1
    global l2
    global l3
    global T1
    global all

    l2 = val
    l1 = (all - l2)/2.0
    l3 = (all - l2) / 2.0

    print "NEW DIST: ", l1, "\t",  l2, "\t", l3

    [s1_l1, s2_l1, s1_l2, s2_l2] = example5(T1)

    pl_s1.set_data([s1_l1 / const], [s2_l1 / const])
    pl_s2.set_data([s1_l2 / const], [s2_l2 / const])

    # update load lines
    pl_ll1.set_data([0.0, 300], [0.0, s2_l1 / s1_l1 * 300])
    pl_ll2.set_data([0.0, 300], [0.0, s2_l2 / s1_l2 * 300])

    fig2.canvas.draw_idle()
dist_slider_obj.on_changed(update_distance)





plt.show()
