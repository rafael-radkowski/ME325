# Import the failure theory envelopes
from ME325Common.FailureTheories import *
from StressCalc import *

from ME325Common.FatigueFailureTheories import *

params = dict()
# Dimensions
params["l1"] = 5 #in
params["l2"] = 7 #in
params["l3"] = 5 #in
# Loads
params["F1"] = 5000 # lbf
params["F2"] = 3000 #lbf
params["T"] = 5000.0 #lbf-in


Se = 30
Sut = 110
n = 1.2

def torque(p, x):

    return p['T']


def bending_moment(p, x):

    if x <= p['l1']:
        M = p['Ay'] * x
        return M
    elif x <= p['l1'] + p['l2']:
        M = p['Ay'] * x - p['F1'] * (x - p['l1'])
        return M
    else:
        M = p['Ay'] * x - p['F1'] * (x - p['l1']) - p['F2'] * (x - p['l1'] - p['l2'])
        return M



def calc_diameter(Se, Sut, Ma, Tm, Kf, Kfs, n):

    f1 = (2.0 / Se ) * Kf * Ma/1000.0
    f2 = (3.0 / Sut) * Kfs * Tm/1000.0

    d = ((16*n)/np.pi * ( f1 + f2) )**(1.0/3.0)

    return d


def example_15(p):


    l12 = p['l1'] + p["l2"]
    l123 = p['l1'] + p["l2"] + p["l3"]

    # reaction forces
    By = (p["F2"] *  l12 + p["F1"] * p["l1"]) / l123

    Bx = 0.0

    Ay = p["F1"] + p["F2"] - By

    print('Reaction forces, Ay=%0.02f lbf, By=%0.02f, Bx=%0.02f '%(Ay, By, Bx))

    sum = -Ay - By + p['F1'] + p['F2']
    print ("check sum = %0.02f"% (sum))

    p['Bx'] = Bx
    p['By'] = By
    p['Ay'] = Ay

    M_1 = bending_moment(p, 0.5)
    M_2 = bending_moment(p, 2.0)
    M_3 = bending_moment(p, p['l1'])
    M_4 = bending_moment(p, 6.0) # 4
    M_5 = bending_moment(p, 8.5) # center
    M_6 = bending_moment(p, 11.25)  # center
    M_7 = bending_moment(p, 12.00)  # center
    M_8 = bending_moment(p, 15.00)  # center
    M_9 = bending_moment(p, 16.25)  # center
    M_10 = bending_moment(p, l123)  # center


    print ("Bending moments")
    print ("0.5\t\t2.0\t\t%0.02f\t\t6.0\t\t\t8.5\t\t\t11.25\t\t12.00\t\t15.00\t\t16.25" % (p['l1']))
    print ("%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t\t%0.02f\t" % (M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9 ))
    #print ("check end: %0.02f" %(M_10))

    T = torque(p,5)

    d1 = calc_diameter(Se, Sut, M_1, 0.0, 1.0, 1.0, n)
    d2 = calc_diameter(Se, Sut, M_2, 0.0, 1.0, 1.0, n)
    d3 = calc_diameter(Se, Sut, M_3, T, 1.0, 1.0, n)
    d4 = calc_diameter(Se, Sut, M_4, T, 1.0, 1.0, n)
    d5 = calc_diameter(Se, Sut, M_5, T, 1.0, 1.0, n)
    d6 = calc_diameter(Se, Sut, M_6, T, 1.0, 1.0, n)
    d7 = calc_diameter(Se, Sut, M_7, T, 1.0, 1.0, n)
    d8 = calc_diameter(Se, Sut, M_8, 0.0, 1.0, 1.0, n)
    d9 = calc_diameter(Se, Sut, M_9, 0.0, 1.0, 1.0, n)

    print ("\nDiameters with Kf = 1 and Kfs = 1")
    print ("%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t\t%0.02f\t" % (
    d1, d2, d3, d4, d5, d6, d7, d8, d9))

    print ('torque %0.03f' %(torque(p,5)))

    x = np.linspace(0, l123, 200 )
    m = np.zeros(200)
    t = np.zeros(200)
    count = 0
    for i in x:
        m[count] = bending_moment(p, i)
        if i > 5 and i < 12:
            t[count] = torque(p,i)
        else:
            t[count] = 0.0
        count = count + 1

    d1 = calc_diameter(Se, Sut, M_1, 0.0, 1.5, 1.7, n)
    d2 = calc_diameter(Se, Sut, M_2, 0.0, 1.5, 1.9, n)
    d3 = calc_diameter(Se, Sut, M_3, T, 1.0, 1.0, n)
    d4 = calc_diameter(Se, Sut, M_4, T, 1.5, 1.7, n)
    d5 = calc_diameter(Se, Sut, M_5, T, 1.0, 1.0, n)
    d6 = calc_diameter(Se, Sut, M_6, T, 1.7, 1.7, n)
    d7 = calc_diameter(Se, Sut, M_7, T, 1.0, 1.0, n)
    d8 = calc_diameter(Se, Sut, M_8, 0.0, 1.5, 1.7, n)
    d9 = calc_diameter(Se, Sut, M_9, 0.0, 1.5, 1.7, n)

    print ("\nDiameters wit Kf and Kfs")
    print ("%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t%0.02f\t\t%0.02f\t" % (
        d1, d2, d3, d4, d5, d6, d7, d8, d9))



    pl_s1, = plt.plot(x, m, 'r-', label="bending moment")
    pl_s2, = plt.plot(x, t, 'b-', label="torque")
    plt.ylabel('stress [psi-in]')
    plt.xlabel('x [in]')
    plt.title('bending moment & torque')
    plt.legend(handles=[pl_s1, pl_s2])

example_15(params)
plt.show()