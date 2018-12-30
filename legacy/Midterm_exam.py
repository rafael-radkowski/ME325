# Import the failure theory envelopes
from ME325Common.FailureTheories import *
from StressCalc import *

from ME325Common.FatigueFailureTheories import *


def problem_01():


    F = 500.0 #lbf
    T = 5500.0 #lbf-in
    l = 1 #in
    d = 1 #in

    Sut = 80.0 #kpis
    Suc = 110.0 # kpsi

    Kf = 1.8
    Kfs = 1.5

    # stress
    s = ( F * l * 32) / (np.pi * d**3) * Kf
    print ("normal stress: s = %0.04f psi" %(s))

    t = (16*T)/ (np.pi * d**3) *Kfs
    print ("shear stress: t = %0.04f psi" %(t))


    s1, s2, t1 = PrincipleStress([s/1000.0], [t/1000.0])
    print ("principle stresses: s1=%0.04f kpsi, s2=%0.04f kpsi, t=%0.04f kpsi" %(s1, s2, t1))

    print ('stress ratio: %0.04f' % abs(s1/s2))

    n = brittle_coulumb_fos(s1, s2, Sut, Suc)
    print ('Fos: n=%0.04f' %(n))

    #########################################################
    ## Plot

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(left=0.1, bottom=0.15)
    # fig.set_size_inches(8,8, forward=True)


    # Plot the stress point
    pl_s, = plt.plot([s1], [s2], 'ro')


    # Plot the failure envelopes
    plotModMohrFailureTheory(Sut, Suc)
    plotCoulumbMohrFailureTheory(Sut, Suc)
    plotMaxNormalFailureTheory(Sut, Suc)

    x = np.linspace(-Suc-10, Sut+10, 200)
    y = np.linspace(0, 0, 200)
    plt.plot([x], [y], 'r--')


    pass



def problem_02():


    print('\nProblem 2 ------')

    F = 500.0  # lbf
    T = 5500.0  # lbf-in
    l = 1  # in
    Sy = 55 #kpsi
    n = 1.10

    Kf = 1.8
    Kfs = 1.5

    s_max = Sy / n

    print('max stress s_max= %0.04f kpsi' % (s_max))

    d = 1.15 # in, assumption

    # stress
    s = (F * l * 32) / (np.pi * d ** 3) * Kf
    print ("normal stress: s = %0.04f psi" % (s))

    t = (16 * T) / (np.pi * d ** 3) * Kfs
    print ("shear stress: t = %0.04f psi" % (t))

    s1, s2, t1 = PrincipleStress([s / 1000.0], [t / 1000.0])
    print ("principle stresses: s1=%0.04f kpsi, s2=%0.04f kpsi, t=%0.04f kpsi" % (s1, s2, t1))

    s_vm = vonMises([s/1000.0], [t/1000.0])
    print ("von Mises eq. stress =%0.04f kpsi" %(s_vm))

    n_ist = Sy / s_vm

    print ('Fos = %0.04f' % (n_ist))

    pass



def problem_03():

    h = 1.5 #in
    l = 5 # in
    t = 0.5 # in
    n = 1.2

    F = 2500.0 #lbf

    Se = 30.0
    Sut = 100

    # stress
    s = (6 * F * l ) / (t * h**2)

    print('stress s = %0.04f psi' % (s))


    # problem b
    h_new = np.sqrt ((6*F*l)/(t*Se*1000.0))
    print ('new h = %0.04f in' %(h_new))

    t_new = (6 * F * l) / ( h**2 * Se * 1000.0)
    print ('new t = %0.04f in' % (t_new))



    # problem 3 b
    # I am using h_new

    s_m = (6 * F * l) / (t * h_new**2)
    print('midrange stress sm=%0.04f psi' % (s_m))

    s_a = Se * ( 1/n - s_m/(1000.0*Sut) )
    print ('alternating stres sa = %0.04f psi' %(s_a))


    Fa = (s_a *1000.0* t * h_new**2 )/ (6 * l)
    print ('alternating load Fa = %0.04f lbf' % (Fa))
    pass




def problem_04():


    h = 2  # in
    l = 2  # in
    t = 0.6  # in
    n = 1.2

    Fmax = 3000.0  # lbf
    Fmin = -1000


    Kc = 65
    ai = 0.2
    a = ai / 2

    beta = 1.1

    m = 3.0
    C = 3.8E-11


    Fm = (Fmax + Fmin) / 2
    print('mindrange load Fm = %0.04f lbf' % (Fm))

    Fa = np.abs( (Fmax - Fmin) / 2 )
    print('alternating load Fa = %0.04f lbf' % (Fa))

    dF = Fa * 2
    print('load range dF = %0.04f' %(dF))

    #stress range
    ds = (6 * dF * l) / (t * h ** 2)
    print('stress range ds= %0.04f psi' % (ds))



    a_c = 1/np.pi * ( Kc / (n * ds/1000.0 * beta))**2
    print('critical crack length ac = %0.04f' % (a_c))



    N = 2 * (a_c ** ((2 - m) / 2) - a ** ((2 - m) / 2)) / ((2 - m) * C * (beta * ds/1000.0 * np.pi ** 0.5) ** m) * n

    print ('Remaining lifetime N = %0.04f' %(N) )

    pass

#problem_01()
#problem_02()
#problem_03()
problem_04()

plt.show()