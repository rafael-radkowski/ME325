'#'"""

This script implements different fatigure lifetime theories.

This file is part of the course ME 325 "Machine Component Design"

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All copyrights reserved
"""


from pylab import *
import numpy as np;
import matplotlib.pyplot as plt
from enum import Enum




def plot_SN_diagram(Sut, Sy, Se, low_cycle, endurance):
    """

    :param Sut:
    :param Sy:
    :param Se:
    :param low_cycle:
    :param endurance:
    :return:
    """

    linewidth = 2.0
    max_n = 1E9

    ax = plt.subplot()
    plt.plot([1, low_cycle], [Sut, Sy], 'k-', color='b', lw=linewidth)
    plt.plot([low_cycle, endurance], [Sy, Se], 'k-', color='b', lw=linewidth)
    plt.plot([endurance, max_n], [Se, Se], 'k-', color='b', lw=linewidth)

    plt.xlabel("iterations [log(N)]")
    plt.ylabel("fatigue strength [kpsi]")

    ax.set_xscale("log", nonpos='clip')
    ax.set_xlim([0.0, max_n])


    ax.set_ylim([0, Sut + 10])


    plt.grid()



def compute_fatigue_strength( itrerations, Sut, Sy, Se, N_low_cycle, N_endurance):


    if itrerations < 0.0 and itrerations < N_low_cycle:

        a = (Sut - Sy)/ (0-N_low_cycle)
        b = Sy - a * N_low_cycle

        f = a * itrerations + b
        return f

    elif itrerations >= N_low_cycle and itrerations < N_endurance:


        Syl = np.log(Sy)
        Sel = np.log(Se)

        #a = ( Syl - Sel ) / (N_low_cycle - N_endurance)
        #b = Se - a * N_endurance

        f =  ( Syl - Sel ) / (N_low_cycle - N_endurance) * (itrerations - N_low_cycle)

        #print (a)
        #print (b)

        #f = a * itrerations + b
        return f

    else:

        return Se





def plot_mod_goodman_relation(Se, Sut):

    linewidth = 1.0
    plt.plot([0, Sut], [Se, 0], 'k-', color='b', lw=linewidth)
    plt.axis([0, Sut + 10, 0, Sut + 10])
    plt.grid()


def plot_gerber_relation(Se, Sut):


    linewidth = 1.0
    N = int(Sut/2.0)

    x = np.linspace(0,Sut, N)

    y =  ( 1.0 - (x/Sut)**2 ) * Se


    plt.plot(x, y, 'k-', color='r', lw=linewidth)
    plt.axis([0, Sut + 10, 0, Sut + 10])
    plt.grid()



def plot_yield_strength_limit(Sy):

    plt.plot([0, Sy], [ Sy, 0], '-', color='k', lw=1.0)



def plot_fatigue_diagram(Se, Sy, Sut):

    plot_mod_goodman_relation(Se, Sut)
    plot_gerber_relation(Se, Sut)
    plot_yield_strength_limit(Sy)

    plt.xlabel("midrange stress [kpsi]")
    plt.ylabel("alternating stress [kpsi]")



def Gerber_FoS(sa, sm, Se, Sut):


    a = (sm/Sut)**2
    b = (sa/Se)
    c = - 1.0

    p = b/a
    q = c/a


    n1 = - (p/2.0) + np.sqrt((p/2.0)**2 - q)
    n2 = - (p/2.0) - np.sqrt((p / 2.0) ** 2 - q)


    n = 0.5 * (Sut/sm)**2 * (sa/Se) * (-1 + ( np.sqrt(1 + (2* sm*Se)/(Sut*sa) )**2) )

    return n


