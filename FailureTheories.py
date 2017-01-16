"""
Example for ME325 - Machine Component Design

Plot functions to plot the safety zones /safety envelopes for ductile and brittle failure theories.

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""


from pylab import *
import numpy as np;
import matplotlib.pyplot as plt
from enum import Enum




def plotMaxNormalFailureTheory(Sut, Suc, linewidth =1):
    """
    Plots the maximum normal stress failure theory envelope
    :param Sut: ultimate tensile in kpsi as scalar
    :param Suc: ultimate compression in kpsi as scalar
    :param linewidth: the linewidth as inter scalar
    :return: -
    """
    plt.plot([Sut, Sut], [-Suc, Sut], 'k-', color='b', lw=linewidth)
    plt.plot([Sut, -Suc], [Sut, Sut], 'k-', color='b', lw=linewidth)
    plt.plot([-Suc, -Suc], [Sut, -Suc], 'k-', color='b', lw=linewidth)
    plt.plot([-Suc, Sut], [-Suc, -Suc], 'k-', color='b', lw=linewidth)




def plotModMohrFailureTheory(Sut, Suc, linewidth =1):
    """
    Plots the modified mohr failure theory envelope
    :param Sut: ultimate tensile in kpsi as scalar
    :param Suc: ultimate compression in kpsi as scalar
    :param linewidth: the linewidth as inter scalar
    :return: -
    """
    plt.plot([Sut, Sut], [-Sut, Sut], 'k-', color='r', lw=linewidth)
    plt.plot([Sut, -Sut], [Sut, Sut], 'k-', color='r', lw=linewidth)
    plt.plot([-Sut, -Suc], [Sut, 0], 'k-', color='r', lw=linewidth)
    plt.plot([-Suc, -Suc], [0, -Suc], 'k-', color='r', lw=linewidth)
    plt.plot([-Suc, 0], [-Suc, -Suc], 'k-', color='r', lw=linewidth)
    plt.plot([0, Sut], [-Suc, -Sut], 'k-', color='r', lw=linewidth)





def plotCoulumbMohrFailureTheory(Sut, Suc, linewidth =1):
    """
    Plots the Coulumb Mohr failure theory envelope
    :param Sut: ultimate tensile in kpsi as scalar
    :param Suc: ultimate compression in kpsi as scalar
    :param linewidth: the linewidth as inter scalar
    :return: -
    """
    plt.plot([Sut, Sut], [0, Sut], 'k-', color='g', lw=linewidth)
    plt.plot([Sut, 0], [Sut, Sut], 'k-', color='g', lw=linewidth)
    plt.plot([0, -Suc], [Sut, 0], 'k-', color='g', lw=linewidth)
    plt.plot([-Suc, -Suc], [0, -Suc], 'k-', color='g', lw=linewidth)
    plt.plot([-Suc, 0], [-Suc, -Suc], 'k-', color='g', lw=linewidth)
    plt.plot([0, Sut], [-Suc, 0], 'k-', color='g', lw=linewidth)




def plotVonMiesesFailureTheory(Sy, linewidth = 1):
    """
    Plots the von Mises safety envelope.
    :param Sy:  the yield strength
    :param linewidth:
    :return: -
    """

    angles_rad = linspace(0,360,360) * math.pi / 180.0
    mises_abs = sqrt(  np.cos(angles_rad[:])**2  + np.sin(angles_rad[:])**2  -  np.cos(angles_rad[:]) * np.sin(angles_rad[:]) )
    mises_x = np.cos(  angles_rad[:])/mises_abs[:] *  Sy
    mises_y = np.sin(angles_rad[:]) / mises_abs[:] * Sy

    plt.plot(mises_x, mises_y, color='orange')



def plotTrescaFailureTheory(Sy, linewidth = 1):

    color = 'purple'

    plt.plot([Sy, Sy], [0, Sy], 'k-', color=color, lw=linewidth)
    plt.plot([Sy, 0], [Sy, Sy], 'k-', color=color, lw=linewidth)
    plt.plot([0, -Sy], [Sy, 0], 'k-', color=color, lw=linewidth)
    plt.plot([-Sy, -Sy], [0, -Sy], 'k-', color=color, lw=linewidth)
    plt.plot([-Sy, 0], [-Sy, -Sy], 'k-', color=color, lw=linewidth)
    plt.plot([0, Sy], [-Sy, 0], 'k-', color=color, lw=linewidth)
