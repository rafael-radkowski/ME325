


# matplotlib
import platform
import matplotlib
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import datetime


# base class for plots
from ME325Common.PlotBase import *


class DuctileFailureTheoriesPlot(PlotBase):
    """
    Generates a plot showing the failure theories for ductile materials.
    """

    fig  = None
    axis = None

    show_vonMises = 1
    show_Tresca = 1

    mises_plt = 0
    tresca_plt = [0,0,0,0,0,0]
    load_line_plt = 0
    principal_stress_plt = 0

    load_line_length = 400
    linewidth = 0

    plot_number = 1

    def __init__(self):
        self.linewidth = 1
        self.plot_number = PlotBase.GetPlotNumber()


    def create_plots(self, figsize_):
        plt.figure(self.plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figsize_, figsize_), num=self.plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        self.fig.set_size_inches(figsize_, figsize_, forward=True)

        Sy = 1

        # von Mises plot
        mises_x, mises_y = self.__get_vonMisesValues(Sy)
        self.mises_plt, = plt.plot(mises_x, mises_y, color='orange', label='von Mises')

        # Tresca plot
        color = 'purple'

        tx, ty = self.__get_Tresca_values(Sy)

        self.tresca_plt[0], = plt.plot(tx[0], ty[0], 'k-', color=color, lw=self.linewidth, label='Tresca')
        self.tresca_plt[1], = plt.plot(tx[1], ty[1], 'k-', color=color, lw=self.linewidth)
        self.tresca_plt[2], = plt.plot(tx[2], ty[2], 'k-', color=color, lw=self.linewidth)
        self.tresca_plt[3], = plt.plot(tx[3], ty[3], 'k-', color=color, lw=self.linewidth)
        self.tresca_plt[4], = plt.plot(tx[4], ty[4], 'k-', color=color, lw=self.linewidth)
        self.tresca_plt[5], = plt.plot(tx[5], ty[5], 'k-', color=color, lw=self.linewidth)

        #self.tresca_plt[0], = plt.plot([Sy, Sy], [0, Sy], 'k-', color=color, lw=self.linewidth, label='Tresca')
        #self.tresca_plt[1], = plt.plot([Sy, 0], [Sy, Sy], 'k-', color=color, lw=self.linewidth)
        #self.tresca_plt[2], = plt.plot([0, -Sy], [Sy, 0], 'k-', color=color, lw=self.linewidth)
        #self.tresca_plt[3], = plt.plot([-Sy, -Sy], [0, -Sy], 'k-', color=color, lw=self.linewidth)
        #self.tresca_plt[4], = plt.plot([-Sy, 0], [-Sy, -Sy], 'k-', color=color, lw=self.linewidth)
        #self.tresca_plt[5], = plt.plot([0, Sy], [-Sy, 0], 'k-', color=color, lw=self.linewidth)

        s1 = 0
        s2 = 0

        # load line

        llx, lly = self.__get_load_line_values(s1, s2)
        self.load_line_plt, = plt.plot(llx, lly, 'k--')

        # Principal stress
        self.principal_stress_plt, = plt.plot([s1], [s2], 'ro', label=r'$\sigma_{max}$')

        plt.figure(self.plot_number)
        plt.grid()
        plt.xlabel(r'$\sigma_1\;\;\left(\frac{N}{mm^2}\right)$')
        plt.ylabel(r'$\sigma_3\;\;\left(\frac{N}{mm^2}\right)$')
        plt.xlim(-Sy - 40, Sy + 40)
        plt.ylim(-Sy - 40, Sy + 40)
        plt.legend(loc=2)

        return self.fig


    def update_plot(self, Sy, s1, s3):
        plt.figure(self.plot_number)

        Sy_ = Sy
        if self.show_vonMises == 0:
            Sy_ = 0

        #-----------------------------------------------------
        # von Mises plot
        mises_x, mises_y = self.__get_vonMisesValues(Sy_)
        self.mises_plt.set_data(mises_x, mises_y)

        Sy_ = Sy
        if self.show_Tresca == 0:
            Sy_ = 0

        #------------------------------------------------------
        # Tresca plot
        tx, ty = self.__get_Tresca_values(Sy_)
        self.tresca_plt[0].set_data(tx[0], ty[0])
        self.tresca_plt[1].set_data(tx[1], ty[1])
        self.tresca_plt[2].set_data(tx[2], ty[2])
        self.tresca_plt[3].set_data(tx[3], ty[3])
        self.tresca_plt[4].set_data(tx[4], ty[4])
        self.tresca_plt[5].set_data(tx[5], ty[5])

        # ---------------------------------------------------
        # load line

        llx, lly = self.__get_load_line_values(s1, s3)
        self.load_line_plt.set_data(llx, lly)

        # ------------------------------------------------
        # Update principal stress
        self.principal_stress_plt.set_data([s1], [s3])

        # ------------------------------------------------
        # Update limits
        Sy_ = Sy

        plt.figure(self.plot_number)
        plt.xlim(-Sy_ - 40, Sy_ + 40)
        plt.ylim(-Sy_ - 40, Sy_ + 40)


    def showVonMisesPlt(self, show_):
        self.show_vonMises = show_


    def showTrescaPlt(self, show_):
        self.show_Tresca = show_


    def save_plot(self):
        plt.figure(self.plot_number)
        now = datetime.datetime.now()
        path = str("./Material_Failure_Plot_" + str(now) + ".png")
        PlotBase.SaveFigure(self.fig, path )
        return path



    def __get_vonMisesValues(self, Sy):
        # Von Mises stress

        angles_rad = np.linspace(0, 360, 360) * 3.1415 / 180.0
        mises_abs = np.sqrt(
            np.cos(angles_rad[:]) ** 2 + np.sin(angles_rad[:]) ** 2 - np.cos(angles_rad[:]) * np.sin(angles_rad[:]))
        mises_x = np.cos(angles_rad[:]) / mises_abs[:] * Sy
        mises_y = np.sin(angles_rad[:]) / mises_abs[:] * Sy

        return [mises_x, mises_y]



    def __get_load_line_values(self, s1, s3):

        flip = 1
        if s1 < 0.00001 and s1 > -0.00001:
            s1 = 0.00001
        if s1 < 0.0:
            flip = -1

        slope_load_line = s3 / s1
        return [0.0, flip * self.load_line_length],  [0.0, slope_load_line * self.load_line_length * flip]


    def __get_Tresca_values(self, Sy):

        tx = [[Sy, Sy], [Sy, 0], [0, -Sy], [-Sy, -Sy], [-Sy, 0], [0, Sy]]
        ty = [[0, Sy], [Sy, Sy], [Sy, 0], [0, -Sy], [-Sy, -Sy], [-Sy, 0]]

        return tx, ty


class SNDiagramPlot(PlotBase):

    plot_number = 0

    load_line_plt = 0
    life_line_plt = 0
    sn_plt = [0,0,0]
    linewidth = 1.0
    fig = 0
    axis = 0

    text_plt = [0,0]

    unit_str = 'kpsi'

    # SN parameters


    def __init__(self):
        self.plot_number = PlotBase.GetPlotNumber()



    def create_plot(self, figsize_x, figsize_y):
        plt.figure(self.plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figsize_x, figsize_y), num=self.plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        self.fig.set_size_inches(figsize_x, figsize_y, forward=True)

        Sut = 110  # kpsi
        Sy = 95  # kpsi,
        Se = 40  # kpsi, the endurance limit

        N_inv = 1E7  # the infinte lifetime limit
        N_lcc = 1E2  # low cycle to high cycle switch.
        max_n = 1E10

        self.sn_plt[0], = plt.plot([1, N_lcc], [Sut, Sy], 'k-', color='b', lw=self.linewidth)
        self.sn_plt[1], = plt.plot([N_lcc, N_inv], [Sy, Se], 'k-', color='b', lw=self.linewidth)
        self.sn_plt[2], = plt.plot([N_inv, max_n], [Se, Se], 'k-', color='b', lw=self.linewidth)

        self.load_line_plt, =  plt.plot([1, N_inv], [Se+10, Se+10], 'k--', color='black', lw=self.linewidth)
        self.life_line_plt, = plt.plot([1E4, 1E4], [0, Sut], 'k--', color='black', lw=self.linewidth)

        self.text_plt[0] = plt.text(1.2, Se+1, str(str(Se+10) + " kpsi"), color='blue', fontsize=10)
        self.text_plt[1] = plt.text(1E4, 1.0, str(str(1E4)), color='blue', fontsize=10)

        plt.grid()
        plt.xlabel("Iterations [log(N)]", fontsize = 11)
        plt.ylabel(str(r"Fatigue strength $S_f$ [" + self.unit_str + "]"), fontsize = 11 )

        plt.figure(self.plot_number)
        self.axis.set_xscale("log", nonpos='clip')
        self.axis.set_xlim([1, max_n])
        self.axis.set_ylim([0, Sut + 10])

        return self.fig


    def update_plot(self, Sut, Sy, Se, N_lcc, N_inv, curr_N, curr_Sf):
        """

        :param Sut: Ultimate tensile strength
        :param Sy:  Yield strength
        :param Se: Endurance limit
        :param N_lcc: low cycle limit iterations
        :param N_inv: endurance limit iterations
        :param curr_N: current N
        :param curr_Sf: current Sf for curr_N
        :return:
        """

        # dummy value indicating an area outside the plot
        max_n = 1E10

        plt.figure(self.plot_number)

        self.sn_plt[0].set_data([1, N_lcc], [Sut, Sy])
        self.sn_plt[1].set_data([N_lcc, N_inv], [Sy, Se])
        self.sn_plt[2].set_data([N_inv, max_n], [Se, Se])

        if curr_Sf < Se:
            curr_N = max_n

        self.load_line_plt.set_data([1, curr_N], [curr_Sf, curr_Sf])
        self.life_line_plt.set_data([curr_N, curr_N], [0, curr_Sf])


        self.text_plt[0].set_text(str(str(round(curr_Sf,2)) + " " + self.unit_str))
        self.text_plt[0].set_position(( 1.2, curr_Sf+1))

        if curr_Sf > Se or curr_N < N_inv:
            # check for limits
            curr_N = np.max([curr_N, 1])
            self.text_plt[1].set_text(str(int(curr_N )))
            self.text_plt[1].set_position(( curr_N, 1.2))
        else:
            self.text_plt[1].set_text("Infinite life")
            self.text_plt[1].set_position((N_inv, 1.2))


        self.axis.set_ylim([0, Sut + 10])


    def save_plot(self):
        plt.figure(self.plot_number)
        now = datetime.datetime.now()
        path_and_file = str("./SNDiagram_" + str(now) + ".png")
        PlotBase.SaveFigure(self.fig, path_and_file )
        return path_and_file