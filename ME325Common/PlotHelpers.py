
# matplotlib
import platform
import matplotlib
import matplotlib.patches as mpatches
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ME325Common.WidgetHelpers import *

import numpy as np
import datetime
import os


# base class for plots
from ME325Common.PlotBase import *


g_plot_path = "./plots"


class DuctileFailureTheoriesPlot(PlotBase):
    """
    Generates a plot showing the failure theories for ductile materials.
    """

    fig  = None
    axis = None

    show_vonMises = 1
    show_Tresca = 1

    mises_plt = 0
    tresca_plt = [0 ,0 ,0 ,0 ,0 ,0]
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

        # self.tresca_plt[0], = plt.plot([Sy, Sy], [0, Sy], 'k-', color=color, lw=self.linewidth, label='Tresca')
        # self.tresca_plt[1], = plt.plot([Sy, 0], [Sy, Sy], 'k-', color=color, lw=self.linewidth)
        # self.tresca_plt[2], = plt.plot([0, -Sy], [Sy, 0], 'k-', color=color, lw=self.linewidth)
        # self.tresca_plt[3], = plt.plot([-Sy, -Sy], [0, -Sy], 'k-', color=color, lw=self.linewidth)
        # self.tresca_plt[4], = plt.plot([-Sy, 0], [-Sy, -Sy], 'k-', color=color, lw=self.linewidth)
        # self.tresca_plt[5], = plt.plot([0, Sy], [-Sy, 0], 'k-', color=color, lw=self.linewidth)

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

        # -----------------------------------------------------
        # von Mises plot
        mises_x, mises_y = self.__get_vonMisesValues(Sy_)
        self.mises_plt.set_data(mises_x, mises_y)

        Sy_ = Sy
        if self.show_Tresca == 0:
            Sy_ = 0

        # ------------------------------------------------------
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

##---------------------------------------------------------

##---------------------------------------------------------
class SNDiagramPlot(PlotBase):

    plot_number = 0

    load_line_plt = 0
    life_line_plt = 0
    sn_plt = [0 ,0 ,0]
    linewidth = 1.0
    fig = 0
    axis = 0

    text_plt = [0 ,0]

    unit_str = 'kpsi'

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

        self.load_line_plt, =  plt.plot([1, N_inv], [Se +10, Se +10], 'k--', color='black', lw=self.linewidth)
        self.life_line_plt, = plt.plot([1E4, 1E4], [0, Sut], 'k--', color='black', lw=self.linewidth)

        self.text_plt[0] = plt.text(1.2, Se +1, str(str(Se +10) + " kpsi"), color='blue', fontsize=10)
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


        self.text_plt[0].set_text(str(str(round(curr_Sf ,2)) + " " + self.unit_str))
        self.text_plt[0].set_position(( 1.2, curr_Sf +1))

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

"""
##---------------------------------------------------------
Fatigue diagram to render teh mod. Goodman line, and Gerber line.
##---------------------------------------------------------
"""
class FatigueDiagramPlot(PlotBase):

    __plot_number = None

    __goodman_line_plt = 0
    __gerber_line_plt = 0
    __sonderberg_line_plt = 0
    __asme_line_plt = 0
    __yieldstress_line_plt = 0
    __load_point = 0
    __load_line = 0
    __helper_lines = [0,0]
    __helper_text = [0,0,0,0,0]

    __unit_si = r"$\left(\frac{N}{mm^2}\right)$"
    __unit_uscs = r"$\left(ksi\right)$"

    __linewidth = 1


    def __init__(self):
        self.__plot_number = PlotBase.GetPlotNumber()


    def create_plot(self, figure_size):
        plt.figure(self.__plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figure_size, figure_size), num=self.__plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        self.fig.set_size_inches(figure_size, figure_size, forward=True)

        Se = 30
        Sy = 70
        Sut = 100

        x, y = self.__get_mod_goodman_points( Se, Sut)
        self.__goodman_line_plt, = plt.plot(x, y, 'k-', color='blue', lw=self.__linewidth, label="Mod. Goodman")

        x,y = self.__get_gerber_points(Se, Sut)
        self.__gerber_line_plt, = plt.plot(x, y, 'k-', color='red', lw=self.__linewidth, label="Gerber")

        x, y = self.__get_sonderberg_points(Se, Sy)
        self.__sonderberg_line_plt, = plt.plot(x, y, 'k-', color='green', lw=self.__linewidth, label="Sonderberg")

        #x, y = self.__get_asme_points(Se, Sy)
        #self.__asme_line_plt, = plt.plot(x, y, 'k-', color='purple', lw=self.__linewidth, label="ASME-elliptic")

        x,y = self.__get_yieldstress_points(Sy)
        self.__yieldstress_line_plt, = plt.plot(x, y, 'k-', color='black', lw=self.__linewidth, label="Yield stress")


        x, y = self.__get_helper_lines(20, 20)
        self.__helper_lines[0], =  plt.plot(x,y, 'k--', color='black', lw=self.__linewidth)

        x, y = self.__get_load_line(20, 20)
        self.__load_line,  = plt.plot(x,y, 'k--', color='black', lw=self.__linewidth)
        self.__load_point, = plt.plot(20, 20, 'o', color='red', lw=2, label="Load")

        self.__helper_text[0] = plt.text(20 + 2, 2, r"$S_m$", color='k', fontsize=10)
        self.__helper_text[1] = plt.text(2, 20 + 2, r"$S_a$", color='k', fontsize=10)
        self.__helper_text[2] = plt.text(Sy + 2, 2, r"$S_y$", color='k', fontsize=10)
        self.__helper_text[3] = plt.text(Sut + 2, 2, r"$S_{ut}$", color='k', fontsize=10)
        self.__helper_text[4] = plt.text(2, Se + 2, r"$S_e$", color='k', fontsize=10)

        plt.grid()
        plt.legend(loc=1, fontsize=9)
        plt.xlabel(str(r"Midrange stress $\sigma_m$ " + self.__unit_si), fontsize=11)
        plt.ylabel(str(r"Alternating stress $\sigma_a$ " + self.__unit_si), fontsize=11)

        plt.figure(self.__plot_number)
        self.axis.set_xlim([0, Sut + 10])
        self.axis.set_ylim([0, Sy ])

        return self.fig



    def update_plot(self, sa, sm, mat):
        plt.figure(self.__plot_number)

        x, y = self.__get_mod_goodman_points(mat.Se, mat.Sut)
        self.__goodman_line_plt.set_data(x, y)

        x, y = self.__get_gerber_points(mat.Se, mat.Sut)
        self.__gerber_line_plt.set_data(x, y)

        x, y = self.__get_sonderberg_points(mat.Se, mat.Sy)
        self.__sonderberg_line_plt.set_data(x, y)

        #x, y = self.__get_asme_points(mat.Se, mat.Sy)
        #self.__asme_line_plt.set_data(x, y)

        x, y = self.__get_yieldstress_points(mat.Sy)
        self.__yieldstress_line_plt.set_data(x, y)

        x, y = self.__get_helper_lines(sa, sm)
        self.__helper_lines[0].set_data(x, y)

        x, y = self.__get_load_line(sa, sm)
        self.__load_line.set_data(x, y)
        self.__load_point.set_data(sm, sa)

        plt.figure(self.__plot_number)
        self.axis.set_xlim([0, mat.Sut + mat.Sut * 0.1])
        self.axis.set_ylim([0, mat.Sy])

        self.__helper_text[0].set_position((sm + mat.Sut * 0.01, mat.Sut * 0.01))
        self.__helper_text[1].set_position((mat.Sut * 0.01, sa + mat.Sut * 0.01))
        self.__helper_text[2].set_position((mat.Sy + mat.Sut * 0.01, mat.Sut * 0.01))
        self.__helper_text[3].set_position((mat.Sut + mat.Sut * 0.01, mat.Sut * 0.01))
        self.__helper_text[4].set_position((mat.Sy * 0.01, mat.Se + mat.Sy * 0.01))


    def set_units(self, unit_):
        """
        Set the units
        :param unit_:  0 -> SI units, else USCS units
        :return:
        """
        plt.figure(self.__plot_number)

        if unit_ == 0:
            plt.xlabel(str(r"Midrange stress $\sigma_m$ " + self.__unit_si), fontsize=11)
            plt.ylabel(str(r"Alternating stress $\sigma_a$ " + self.__unit_si), fontsize=11)
        else:
            plt.xlabel(str(r"Midrange stress $\sigma_m$ " + self.__unit_uscs), fontsize=11)
            plt.ylabel(str(r"Alternating stress $\sigma_a$ " + self.__unit_uscs), fontsize=11)



    def set_helpers(self, visible_):
        self.__helper_text[0].set_visible(visible_)
        self.__helper_text[1].set_visible(visible_)
        self.__helper_text[2].set_visible(visible_)
        self.__helper_text[3].set_visible(visible_)
        self.__helper_text[4].set_visible(visible_)


    def set_visible(self, line_, visible_):
        """
        Set individual lines visible or invisible
        :param line_: the line id,
                0 - mod goodman
                1 - gerber
                2 - sonderberg
                3 - yield stress
                4 - all
        :param visible_:  True or False to set a line visible or invisible.
        :return:
        """

        if line_ == 0: # mod goodman
            self.__goodman_line_plt.set_visible(visible_)
        elif line_ == 1:
            self.__gerber_line_plt.set_visible(visible_)
        elif line_ == 2:
            self.__sonderberg_line_plt.set_visible(visible_)
        elif line_ == 3:
            self.__yieldstress_line_plt.set_visible(visible_)
        elif line_ == 4:
            self.__goodman_line_plt.set_visible(visible_)
            self.__gerber_line_plt.set_visible(visible_)
            self.__sonderberg_line_plt.set_visible(visible_)
            self.__yieldstress_line_plt.set_visible(visible_)

    def save_plot(self):
        try:
            os.stat(g_plot_path)
        except:
            os.mkdir(g_plot_path)

        try:
            plt.figure(self.__plot_number)
            now = datetime.datetime.now()
            #now = datetime.now().strftime('%y-%m-%d_%I-%M-%S')
            path_and_file = str("./plots/Fatigue_diagram_" + str(now) + ".png")
            PlotBase.SaveFigure(self.fig, path_and_file )
            return path_and_file
        except:
            print("Error - could not save plot")


    def __get_mod_goodman_points(self, Se, Sut):
        """
        Return points to draw the mod Godman line
        :param Se:
        :param Sut:
        :return:
        """
        return [0,Sut], [Se, 0]
    def __get_gerber_points(self, Se, Sut):
        N = int(Sut )
        x = np.linspace(0, Sut, N)
        y = (1.0 - (x / Sut) ** 2) * Se

        return x, y
    def __get_asme_points(self, Se, Sy):
        N = int(Sy)
        x = np.linspace(0, Sy, N)
        y =  np.sqrt( (1.0 - (x / Sy)**2) * Se**2)

        return x, y
    def __get_yieldstress_points(self, Sy):

        return [0,Sy], [Sy,0]
    def __get_sonderberg_points(self, Se, Sy):

        return [0, Sy], [Se, 0]
    def __get_load_line(self, sa, sm):
        x = 500
        y =  sa/(sm+ 0.000001) * x

        return [0,x], [0,y]
    def __get_helper_lines(self, sa, sm):

        return [0, sm, sm], [sa, sa, 0]




"""
##---------------------------------------------------------

##---------------------------------------------------------
"""
class ModGoodmanDiagramPlot(PlotBase):
    __plot_number = None


    def __init__(self):
        __plot_number = super().GetPlotNumber()


    def create_plot(self, figure_size):
        return


    def update_plot(self):
        return


""""
---------------------------------------------------------
 Mohr's circle Plot
---------------------------------------------------------
"""
class MohrsCirclePlot(PlotBase):

    __plot_number = -1

    __plot = [0 ,0 ,0, 0, 0, 0, 0]
    __text_plt = [0, 0, 0]
    __helper_plt = [0, 0, 0, 0, 0,0,0,0,0,0]
    __acr_plt = [0,0,0,0]
    __center_plt = [0,0]
    __linewidth = 1

    __unit_si = r"$\left(\frac{N}{mm^2}\right)$"
    __unit_uscs = r"$\left( ksi \right)$"

    def __init__(self):
        self.__plot_number = PlotBase.GetPlotNumber()


    def create_plot(self, figure_size):
        plt.figure(self.__plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figure_size, figure_size), num=self.__plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        self.fig.set_size_inches(figure_size, figure_size, forward=True)

        sx = 20
        sy = -20
        txy = 10


        s_mean, R = self.__calc_parameters(sx, sy, txy)
        p_s13x, p_s13y  = self.__get_circular_area_plt(s_mean, 0, R)

        # Kartesian line
        self.__helper_plt[8], = plt.plot([sx, sy], [txy, -txy], 'k--', color='k', lw=self.__linewidth/2, visible=False)
        self.__helper_plt[9], = plt.plot([sx, sy], [txy, -txy], 'k--', color='k', lw=self.__linewidth / 2,
                                         visible=False)


        self.__plot[0], = plt.plot(p_s13x, p_s13y, 'k-', color='k', lw=self.__linewidth)
        self.__plot[1], = plt.plot([sx, sy], [txy, -txy], 'k--', color='k', lw=self.__linewidth, visible=True) #line
        self.__plot[2], = plt.plot(sx, txy, 'o-', color='red', lw=self.__linewidth)
        self.__plot[3], = plt.plot(sy, -txy,'o-', color='red', lw=self.__linewidth)
        self.__plot[4], = plt.plot(s_mean, 0, 'o', fillstyle='none', color='red', lw=self.__linewidth)

        self.__text_plt[0] = plt.text(sx-1, txy + 2, r"$\sigma_x$", color='red', fontsize=10)
        self.__text_plt[1] = plt.text(sy-1, -txy + 2, r"$\sigma_y$", color='red', fontsize=10)
        self.__text_plt[2] = plt.text(s_mean + 2, 2, r"$\sigma_{mean}$", color='red', fontsize=10)

        # plot helpers
        # sigma 1, 2
        self.__helper_plt[0], = plt.plot(10, 0, 'o', fillstyle='none', color='red', lw=self.__linewidth, visible=False)
        self.__helper_plt[1], = plt.plot(-10, 0,'o', fillstyle='none', color='red', lw=self.__linewidth, visible=False)
        self.__helper_plt[2] = plt.text(20, 1, r"$\sigma_1$", color='red', fontsize=10, visible=False)
        self.__helper_plt[3] = plt.text(-20, 1, r"$\sigma_3$", color='red', fontsize=10,  visible=False)

        self.__helper_plt[4], = plt.plot(0, 10, 'o', fillstyle='none', color='red', lw=self.__linewidth, visible=False)
        self.__helper_plt[5], = plt.plot(0, -10, 'o', fillstyle='none', color='red', lw=self.__linewidth, visible=False)
        self.__helper_plt[6] = plt.text(0, 10, r"$\tau_{max}$", color='red', fontsize=10, visible=False)
        self.__helper_plt[7] = plt.text(0, -10, r"$\tau_{max}$", color='red', fontsize=10, visible=False)

        # create the arc
        arcx, arcy, a11, a12, a21, a22 = self.__get_arc_plt(0, 0, R * 0.5, 0.0, 20)
        self.__acr_plt[0], = plt.plot(arcx, arcy, 'k--', color='k', lw=self.__linewidth)
        self.__acr_plt[1], = plt.plot(a11, a12, 'k--', color='k', lw=self.__linewidth)
        self.__acr_plt[2], = plt.plot(a21, a22, 'k--', color='k', lw=self.__linewidth)
        self.__acr_plt[3] = plt.text(0, -10, r"2$\theta$", color='red', fontsize=10, visible=True)

        # center plot
        self.__center_plt[0],  = plt.plot([-10,10], [0,0], 'k--', color='blue', lw=1.0)
        self.__center_plt[1], = plt.plot([0, 0], [-10, 10], 'k--', color='blue', lw=1.0)


        plt.grid()
        plt.xlabel(str(r"Normal stress $\sigma$ " + self.__unit_si), fontsize=11)
        plt.ylabel(str(r"Shear stress $\tau$ "+ self.__unit_si ), fontsize=11)

        plt.figure(self.__plot_number)
        length = np.max( [np.max([ sx/2 + 30, txy + 30]), sy/2 + 30])
        self.axis.set_xlim([s_mean - length, s_mean + length])
        self.axis.set_ylim([-length, length])

        return self.fig


    def update_plot(self, sx, sy, txy):
        plt.figure(self.__plot_number)
        s_mean, R = self.__calc_parameters(sx, sy, txy)
        p_s13x, p_s13y = self.__get_circular_area_plt(s_mean, 0, R)

        self.__plot[0].set_data(p_s13x, p_s13y)
        self.__plot[1].set_data([sx, sy], [txy, -txy])
        self.__plot[2].set_data(sx, txy)
        self.__plot[3].set_data(sy, -txy)
        self.__plot[4].set_data(s_mean,0)

        self.__text_plt[0].set_position((sx + np.abs(0.05* R), txy + np.abs(0.05 * R))) # sx
        self.__text_plt[1].set_position((sy - np.abs(0.1* R), -txy - np.abs(0.1 * R))) #sy
        self.__text_plt[2].set_position((s_mean + np.abs(R * 0.05), np.abs(R * 0.05))) #s mean

        plt.figure(self.__plot_number)
        length = R +  R * 0.2 #np.max([np.max([np.abs(sx) / 2 + 30, np.abs(txy) + 30]), np.abs(sy) / 2 + 30])
        self.axis.set_xlim([s_mean - length, s_mean + length])
        self.axis.set_ylim([-length, length])



    def update_helpers(self, s1, s2, a1, a2, t1, t2,  visible_):
        plt.figure(self.__plot_number)

        m = (s1 - s2)/2 + s2
        r = (s1 - s2)/2

        # principal stress circle
        self.__helper_plt[0].set_data(s1, 0)
        self.__helper_plt[1].set_data(s2, 0)
        self.__helper_plt[0].set_visible(visible_)
        self.__helper_plt[1].set_visible(visible_)

        # principal stress text
        self.__helper_plt[2].set_position((s1 - np.abs(r * 0.1), r * 0.05))
        self.__helper_plt[3].set_position((s2, r * 0.05))
        self.__helper_plt[2].set_visible(visible_)
        self.__helper_plt[3].set_visible(visible_)

        self.__helper_plt[2].set_text( str(str(r"$\sigma_1= $" + str(round(s1, 2)))))
        self.__helper_plt[3].set_text( str( str(r"$\sigma_3= $" + str(round(s2,2)) )))

        # max shear circle
        self.__helper_plt[4].set_data(m, t1)
        self.__helper_plt[5].set_data(m, t2)
        self.__helper_plt[4].set_visible(visible_)
        self.__helper_plt[5].set_visible(visible_)

        # max shear line
        self.__helper_plt[6].set_position((m-r * 0.05, t1+r * 0.05))
        self.__helper_plt[7].set_position((m-r * 0.05, t2-r * 0.1))
        self.__helper_plt[6].set_visible(visible_)
        self.__helper_plt[7].set_visible(visible_)

        self.__helper_plt[6].set_text(str(str(r"$\tau_{max}= $" + str(round(t1, 2)))))
        self.__helper_plt[7].set_text(str(str(r"$-\tau_{max}=$" + str(round(t2, 2)))))

        # update the angle
        arcx, arcy, a11, a12, a21, a22 = self.__get_arc_plt(m, 0, r * 0.5, 0.0, a1 * 2)
        self.__acr_plt[0].set_data(arcx, arcy)
        self.__acr_plt[1].set_data(a11, a12)
        self.__acr_plt[2].set_data(a21, a22)
        self.__acr_plt[0].set_visible(visible_)
        self.__acr_plt[1].set_visible(visible_)
        self.__acr_plt[2].set_visible(visible_)

        # center plot
        a = r * 0.2
        self.__center_plt[0].set_data([-a, a], [0, 0])
        self.__center_plt[1].set_data([0, 0], [-a, a])
        self.__center_plt[0].set_visible(visible_)
        self.__center_plt[1].set_visible(visible_)

        n = len(arcx)
        if n != 0:
            self.__acr_plt[3].set_position((arcx[int(n/2)], arcy[int(n/2)]))
        else:
            self.__acr_plt[3].set_position((m + r * 0.5,0))

        self.__acr_plt[3].set_visible(visible_)

        # Kartesian line
        self.__helper_plt[8].set_data([s1, s2], [0,0])
        self.__helper_plt[8].set_visible(visible_)
        self.__helper_plt[9].set_data([m, m], [t1, t2])
        self.__helper_plt[9].set_visible(visible_)



    def __get_circular_area_plt(self, x, y, radius):
        """
        Calculate the points for a circle
        :param x: center point x
        :param y: center point y
        :param radius: the radius of the circe.
        :return:
        """
        angles_rad = np.linspace(0, 360, 360) * 3.1415 / 180.0
        p_x = x + np.cos(angles_rad[:]) * radius
        p_y = y + np.sin(angles_rad[:]) * radius

        return p_x, p_y

    def __get_arc_plt(self, x, y, radius, start_a, stop_a):
        """
        Calcuate the points to render an arc with an arrow.
        :param x:
        :param y:
        :param radius:
        :param start_a:
        :param stop_a:
        :return: arc_points_x, arc_points_y, arrow 1 start, arrow 1 end, arrow 2 start, arrow 2 end
        """

        # the arc
        angles_rad = np.linspace(start_a, stop_a, np.abs(stop_a-start_a)) * 3.1415 / 180.0
        p_x = np.cos(angles_rad[:]) * radius + x
        p_y = np.sin(angles_rad[:]) * radius + y

        # the arrow
        ang = 135
        if stop_a < 0:
            ang = ang -180 # to flip the arrow head

        a_x0 = np.cos(stop_a * 3.1415 / 180.0) * radius + x
        a_y0 = np.sin(stop_a * 3.1415 / 180.0) * radius + y
        a_x1 = np.cos((stop_a - ang) * 3.1415 / 180.0) * radius * 0.1
        a_y1 = np.sin((stop_a - ang) * 3.1415 / 180.0) * radius * 0.1
        a_x2 = np.cos((stop_a - ang + 90) * 3.1415 / 180.0) * radius * 0.1
        a_y2 = np.sin((stop_a - ang + 90) * 3.1415 / 180.0) * radius * 0.1

        return p_x, p_y, [a_x0, a_x0 + a_x1], [a_y0, a_y0 + a_y1], [a_x0, a_x0 + a_x2], [a_y0, a_y0 + a_y2]

    def __calc_parameters(self, s_x, s_y, t_xy):
        """
        Calculate the radius and the center point of the circle
        :param s_x: sigma x
        :param s_y:  sigma y
        :param t_xy: tau xy
        :return: mean stress (circle center), and radius
        """
        s_mean = (s_x + s_y)/2
        R = np.sqrt( ((s_x-s_y)/2)**2 + t_xy**2  )

        return s_mean, R


    def set_unit(self, unit):
        """
        Set the unit for this plot. It is either metric SI or USCS imperial
        :param unit: unit index, 0=SI unitys, 1=USCS units
        :return:
        """

        plt.figure(self.__plot_number)
        if unit == 0:
            plt.xlabel(str(r"Normal stress $\sigma$ " + self.__unit_si), fontsize=11)
            plt.ylabel(str(r"Shear stress $\tau$ " + self.__unit_si), fontsize=11)
        else:
            plt.xlabel(str(r"Normal stress $\sigma$ " + self.__unit_uscs), fontsize=11)
            plt.ylabel(str(r"Shear stress $\tau$ " + self.__unit_uscs), fontsize=11)



    def save_plot(self):
        try:
            os.stat(g_plot_path)
        except:
            os.mkdir(g_plot_path)

        try:
            plt.figure(self.__plot_number)
            now = datetime.datetime.now()
            #now = datetime.now().strftime('%y-%m-%d_%I-%M-%S')
            path_and_file = str("./plots/MohrsCircle_" + str(now) + ".png")
            PlotBase.SaveFigure(self.fig, path_and_file )
            return path_and_file
        except:
            print("Error - could not save plot")



""""
---------------------------------------------------------
 Stress tensor 2D
---------------------------------------------------------
"""
class CauchyStressPlanePlot(PlotBase):
    __plot_number = -1

    __box = [0, 0, 0, 0]
    __arrows = [0, 0, 0, 0]
    __text_plt = [0, 0, 0, 0]
    __arc_plt = [0,0,0,0]
    __linewidth = 1

    __new_arrow = [0,0,0,0]

    __unit_si = r"$\left(\frac{N}{mm^2}\right)$"
    __unit_uscs = r"$\left( ksi \right)$"

    __axis_length = 25


    def __init__(self):
        self.__plot_number = PlotBase.GetPlotNumber()



    def create_plot(self, figure_size):
        plt.figure(self.__plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figure_size, figure_size), num=self.__plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        plt.grid()
        self.fig.set_size_inches(figure_size, figure_size, forward=True)

        ## Coordinate system
        arrowx = mpatches.Arrow(0, 0, self.__axis_length * 0.9, 0.0, width=1.0, color='k')
        self.axis.add_patch(arrowx)
        arrowy = mpatches.Arrow(0, 0, 0.0, self.__axis_length * 0.9, width=1.0, color='k')
        self.axis.add_patch(arrowy)

        # static box
        x,y = self.__get_box_coordinates( 20, 0)
        self.__box[0], = plt.plot(x,y, 'k--', color='k')

        # rotated box
        px, py = self.__get_box_coordinates(20, 10)
        self.__box[1], = plt.plot(px, py, 'k-', color='blue')

        # ARROWS
       # ax, ay = self.__get_arrow_coordinates( 20, 1, 0)
        # s2 -> y
       # ar1 = mpatches.Arrow(ax[0], ay[0], ax[1], ay[1], width=1.0, color='red')
       # self.__arrows[0] = self.axis.add_patch(ar1)
        # s2 -> -y
       # ar2 = mpatches.Arrow(ax[2], ay[2], ax[3], ay[3], width=1.0, color='red')
       # self.__arrows[1] = self.axis.add_patch(ar2)

        # s1 -> x
       # ar3 = mpatches.Arrow(ax[4], ay[4], ax[5], ay[5], width=1.0, color='red')
       # self.__arrows[2] = self.axis.add_patch(ar3)
        # s1 -> -x
       # ar4 = mpatches.Arrow(ax[6], ay[6], ax[7], ay[7], width=1.0, color='red')
       # self.__arrows[3] = self.axis.add_patch(ar4)

        self.__text_plt[0] = plt.text(0, 10, r"$\sigma_1$", color='red', fontsize=10, visible=True)
        self.__text_plt[1] = plt.text(0, -10, r"$\sigma_1$", color='red', fontsize=10, visible=True)
        self.__text_plt[2] = plt.text(10, 0, r"$\sigma_3$", color='red', fontsize=10, visible=True)
        self.__text_plt[3] = plt.text(-10, 0, r"$\sigma_3$", color='red', fontsize=10, visible=True)

        ## angle arc

        # create the arc
        arcx, arcy, a11, a12, a21, a22 = self.__get_arc_plt(0, 0, 1 * 0.5, 0.0, 20)
        self.__arc_plt[0], = plt.plot(arcx, arcy, 'k--', color='k', lw=self.__linewidth)
        self.__arc_plt[1], = plt.plot(a11, a12, 'k--', color='k', lw=self.__linewidth)
        self.__arc_plt[2], = plt.plot(a21, a22, 'k--', color='k', lw=self.__linewidth)
        self.__arc_plt[3] = plt.text(0, -10, r"$\theta$", color='red', fontsize=10, visible=True)


        self.__new_arrow[0] = Arrow(10, 0, 10, 0, 0)
        self.__new_arrow[1] = Arrow(-10, 0, -10, 0, 0)
        self.__new_arrow[2] = Arrow(0, 10, 0, 10, 0)
        self.__new_arrow[3] = Arrow(0, -10, 0, -10, 0)

       # x, y, a0, a1 = self.__get_arrow_points(10, 10, 10, 0, 0)
        #self.__new_arrow[0], = plt.plot(x, y, 'k-', color='red', lw=self.__linewidth)
        #self.__new_arrow[1], = plt.plot(a1, a1, 'k-', color='red', lw=self.__linewidth)

        plt.xlabel(str(r"x"), fontsize=11)
        plt.ylabel(str(r"y"), fontsize=11)

        plt.figure(self.__plot_number)
        self.axis.set_xlim([-self.__axis_length, self.__axis_length])
        self.axis.set_ylim([-self.__axis_length, self.__axis_length])


        return self.fig


    def update_plot(self, s1, s2, a1):

        try:
            plt.figure(self.__plot_number)
            px, py = self.__get_box_coordinates(20, a1)
            self.__box[1].set_data(px, py)

            ax, ay = self.__get_arrow_coordinates(20, 2.0, a1)



          #  self.__arrows[0].remove()
          #  self.__arrows[1].remove()
            # s2 -> y
          #  ar1 = mpatches.Arrow(ax[0], ay[0], ax[1], ay[1], width=1.0, color='red')
          #  self.__arrows[0] = self.axis.add_patch(ar1)
            # s2 -> -y
          #  ar2 = mpatches.Arrow(ax[2], ay[2], ax[3], ay[3], width=1.0, color='red')
          # self.__arrows[1] = self.axis.add_patch(ar2)



          #  self.__arrows[2].remove()
         #   self.__arrows[3].remove()
            # s1 -> x
           # ar3 = mpatches.Arrow(ax[4], ay[4], ax[5], ay[5], width=1.0, color='red')
           # self.__arrows[2] = self.axis.add_patch(ar3)
            # s1 -> -x
          #  ar4 = mpatches.Arrow(ax[6], ay[6], ax[7], ay[7], width=1.0, color='red')
          #  self.__arrows[3] = self.axis.add_patch(ar4)

            ## Text positions
            c = 1.8
            self.__text_plt[0].set_position((ax[5]* c, ay[5]* c))  #s1
            self.__text_plt[1].set_position((ax[7]* c - 2, ay[7]* c))  # s1
            self.__text_plt[2].set_position((ax[1]* c, ay[1]* c))  # s2
            self.__text_plt[3].set_position((ax[3]* c, ay[3]* c))  # s2


            # update the angle
            arcx, arcy, a11, a12, a21, a22 = self.__get_arc_plt(0, 0, 20/2 + 20/2 * 0.5, 0.0, a1)
            self.__arc_plt[0].set_data(arcx, arcy)
            self.__arc_plt[1].set_data(a11, a12)
            self.__arc_plt[2].set_data(a21, a22)
            n = len(arcx)
            if n != 0:
                self.__arc_plt[3].set_position((arcx[int(n / 2)], arcy[int(n / 2)]))
            else:
                self.__arc_plt[3].set_position(( 20/2 + 20/2 * 0.5,0))

            self.__new_arrow[0].set(10, 0, 10, 0, a1, np.sign(s1))
            self.__new_arrow[1].set(-10, 0, -10, 0, a1, np.sign(s1))
            self.__new_arrow[2].set(0, 10, 0, 10, a1, np.sign(s2))
            self.__new_arrow[3].set(0, -10, 0, -10, a1, np.sign(s2))

        except ValueError:
            print("ValueError")

            return

        except IndexError:
            print("IndexError")
            return

    def save_plot(self):
        try:
            os.stat(g_plot_path)
        except:
            os.mkdir(g_plot_path)

        try:
            plt.figure(self.__plot_number)
            now = datetime.datetime.now()
            #now = datetime.now().strftime('%y-%m-%d_%I-%M-%S')
            path_and_file = str("./plots/StressElement_" + str(now) + ".png")
            PlotBase.SaveFigure(self.fig, path_and_file )
            return path_and_file
        except:
            print("Error - could not save plot")


    def __get_box_coordinates(self, length, angle):

        px = []
        py = []

        l = length / 2

        #  cos  -sin
        #  sin  cos

        #(l, -l)
        x = l
        y = -l
        p1x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p1y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p1x)
        py.append(p1y)

        #(l, l)
        x = l
        y = l
        p2x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p2y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p2x)
        py.append(p2y)

        # (-l, l)
        x = -l
        y = l
        p3x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p3y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p3x)
        py.append(p3y)

        # (-l, -l)
        x = -l
        y = -l
        p4x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p4y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p4x)
        py.append(p4y)

        px.append(p1x)
        py.append(p1y)

        return px, py

    def __get_arrow_coordinates(self, box_side_length, arrow_length, angle):


        l = box_side_length / 2;


        px = []
        py = []


        #  cos  -sin
        #  sin  cos

        # (0, l)
        x = 0
        y = l
        p1x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p1y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p1x)
        py.append(p1y)

        # (0, l + arrow_length)
        x = 0
        y = l + arrow_length
        p2x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p2y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p2x)
        py.append(p2y)

        # (0, -l)
        x = 0
        y = -l
        p3x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p3y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p3x)
        py.append(p3y)

        # (0, -l - arrow_length)
        x = 0
        y = -l - arrow_length
        p4x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p4y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p4x)
        py.append(p4y)


        ###
        # x

        # (0, l)
        x = l
        y = 0
        p5x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p5y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p5x)
        py.append(p5y)

        # (0, l + arrow_length)
        x = l + arrow_length
        y = 0
        p6x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p6y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p6x)
        py.append(p6y)


        # (0, -l)
        x = -l
        y = 0
        p7x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p7y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p7x)
        py.append(p7y)

        # (0, l + arrow_length)
        x = -l - arrow_length
        y = 0
        p8x = x * np.cos(np.deg2rad(angle)) - y * np.sin(np.deg2rad(angle))
        p8y = x * np.sin(np.deg2rad(angle)) + y * np.cos(np.deg2rad(angle))
        px.append(p8x)
        py.append(p8y)

        return px, py

    def __get_arc_plt(self, x, y, radius, start_a, stop_a):
        """
        Calcuate the points to render an arc with an arrow.
        :param x:
        :param y:
        :param radius:
        :param start_a:
        :param stop_a:
        :return: arc_points_x, arc_points_y, arrow 1 start, arrow 1 end, arrow 2 start, arrow 2 end
        """

        # the arc
        angles_rad = np.linspace(start_a, stop_a, np.abs(stop_a-start_a)) * 3.1415 / 180.0
        p_x = np.cos(angles_rad[:]) * radius + x
        p_y = np.sin(angles_rad[:]) * radius + y

        # the arrow
        ang = 135
        if stop_a < 0:
            ang = ang -180 # to flip the arrow head

        a_x0 = np.cos(stop_a * 3.1415 / 180.0) * radius + x
        a_y0 = np.sin(stop_a * 3.1415 / 180.0) * radius + y
        a_x1 = np.cos((stop_a - ang) * 3.1415 / 180.0) * radius * 0.1
        a_y1 = np.sin((stop_a - ang) * 3.1415 / 180.0) * radius * 0.1
        a_x2 = np.cos((stop_a - ang + 90) * 3.1415 / 180.0) * radius * 0.1
        a_y2 = np.sin((stop_a - ang + 90) * 3.1415 / 180.0) * radius * 0.1

        return p_x, p_y, [a_x0, a_x0 + a_x1], [a_y0, a_y0 + a_y1], [a_x0, a_x0 + a_x2], [a_y0, a_y0 + a_y2]


    def __get_arrow_points(self, p0x, p0y, d1x, d1y, angle ):

        l = np.sqrt(  (d1x-p0x)**2 + (d1y-p0y)**2  )

        #  cos  -sin
        #  sin  cos
        r1x = p0x * np.cos(np.deg2rad(angle)) - p0y * np.sin(np.deg2rad(angle))
        r1y = p0x * np.sin(np.deg2rad(angle)) + p0y * np.cos(np.deg2rad(angle))

        r2x = (p0x + d1x) * np.cos(np.deg2rad(angle)) - (p0y+d1y) * np.sin(np.deg2rad(angle))
        r2y = (p0x + d1x) * np.sin(np.deg2rad(angle)) + (p0y+d1y) * np.cos(np.deg2rad(angle))


        a2x = (p0x + d1x - l * 0.15) * np.cos(np.deg2rad(angle)) - (p0y + d1y - l * 0.1) * np.sin(np.deg2rad(angle))
        a2y = (p0x + d1x - l * 0.15) * np.sin(np.deg2rad(angle)) + (p0y + d1y - l * 0.1) * np.cos(np.deg2rad(angle))

        a3x = (p0x + d1x - l * 0.15) * np.cos(np.deg2rad(angle)) - (p0y + d1y + l * 0.1) * np.sin(np.deg2rad(angle))
        a3y = (p0x + d1x - l * 0.15) * np.sin(np.deg2rad(angle)) + (p0y + d1y + l * 0.1) * np.cos(np.deg2rad(angle))

        return [r1x, r2x], [r1y, r2y], [ a2x, r2x, a3x], [ a2y, r2y, a3y]




""""
---------------------------------------------------------
da/dN diagram
---------------------------------------------------------
"""
class CrackPropagationDiagramPlot(PlotBase):
    __plot_number = -1

    __plot = [0, 0, 0, 0]
    __helper_lines = [0, 0, 0, 0]
    __text_plt = [0, 0, 0, 0, 0]
    __load_plt = 0
    __linewidth = 1


    # range linear area
    __dk_min = 0
    __dk_max = 0

    # threshold
    __dk_th = 0


    __unit_si = r"$\left(\frac{N}{mm^2}\right)$"
    __unit_uscs = r"$\left( ksi \right)$"

    __axis_length = 25

    __min_cracklength = 0
    __max_dad_max = 0

    def __init__(self):
        self.__plot_number = PlotBase.GetPlotNumber()



    def create_plot(self, figure_size_x, figure_size_y):
        plt.figure(self.__plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figure_size_x, figure_size_y), num=self.__plot_number)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        plt.grid()
        self.fig.set_size_inches(figure_size_x, figure_size_y, forward=True)

        C = 0.0000012
        m = 2.85

        dk_th = 7  # dk threshold
        dK1 = 10 # linear area
        dk2 = 120

        dadn_0 = 2E-6 # smalles crack
        t = 0.5

        self.__dk_min = dK1
        self.__dk_max = dk2


        dK, da_dn = self.__get_section_2(C, m, dK1, dk2)
        self.__plot[0], = plt.plot(dK, da_dn, c='b')

        px, py = self.__get_section_1(dadn_0, da_dn[0], dk_th, dK[0])
        self.__plot[1], = plt.plot(px, py, c='b')

        start = da_dn[int(len(da_dn)-1)]
        dk_start = dK[int(len(dK)-1)]

        px, py = self.__get_section_3(start, start+10, dk_start, dk_start+1, t)
        self.__plot[2], = plt.plot(px, py, c='b')

        self.__helper_lines[0], = plt.plot([dK1, dK1], [dadn_0, start+100], 'k--', c='k')
        self.__helper_lines[1], = plt.plot([dk2, dk2], [start+100, start+100], 'k--', c='k')

        self.__helper_lines[2], = plt.plot([dK1+10, dK1+10], [dadn_0, start + 100], 'k--', c='r')
        self.__helper_lines[3], = plt.plot([1, dk2], [ start + 10, start + 10], 'k--', c='r')

        self.__text_plt[0] = plt.text(10, dadn_0 + dadn_0*0.01, r"$\Delta K_{th}$" )
        self.__text_plt[1] = plt.text(dk_start+1, (start+10) + (start+10) * 0.01, r"$\Delta K_{c}$")


        self.__load_plt, = plt.plot(10,0.01, 'o', c='red')


        plt.xlabel(str(r"$\log ( \Delta K \sqrt{m} ) $"), fontsize=11)
        plt.ylabel(str(r"$\log ( \frac{da}{dN} )$"), fontsize=13)

        plt.grid()
        plt.figure(self.__plot_number)
        #self.axis.set_xlim([-self.__axis_length, self.__axis_length])
        #self.axis.set_ylim([-self.__axis_length, self.__axis_length])

        self.axis.set_xlim([dk_th - 1, dk_start + 100])
        self.axis.set_xscale("log", nonpos='clip')
        self.axis.set_yscale("log", nonpos='clip')
        self.axis.grid()

        return self.fig


    def update_material(self, m, C, dk_th, dk1, dk2, min_cracklength):

        t = 1

        self.__dk_th = dk_th
        self.__dk_min = dk1
        self.__dk_max = dk2

        plt.figure(self.__plot_number)

        self.__min_cracklength = min_cracklength

        if dk1 >= dk2:
            return

        if dk_th >= dk1:
            return

        if min_cracklength > C:
            min_cracklength = C - C*10

        dK, da_dn = self.__get_section_2(C, m, dk1, dk2)
        self.__plot[0].set_data(dK, da_dn)

        px, py = self.__get_section_1(min_cracklength, da_dn[0], dk_th, dK[0])
        self.__plot[1].set_data(px, py)

        start = da_dn[int(len(da_dn) - 1)]
        range = da_dn[int(len(da_dn) - 1)] - da_dn[0]
        dk_start = dK[int(len(dK) - 1)]

        px, py = self.__get_section_3(start, start + range * 40, dk_start, dk_start + 10, t)
        self.__plot[2].set_data(px, py)

        self.__max_dad_max = dk_start + 100

        self.axis.set_xlim([dk_th-1, dk_start + 100])
        self.axis.set_ylim([min_cracklength, (start + range * 40) +(start + range * 40) * 2])

        self.__text_plt[0].set_position((dk_th +dk_th * 0.01 , min_cracklength + min_cracklength * 0.01))
        self.__text_plt[1].set_position((dk_start + 1,  (start + range * 40) + (start + range * 40) * 0.01))

        self.__helper_lines[0].set_data([dk1, dk1], [min_cracklength, start + 250])
        self.__helper_lines[1].set_data([dk2, dk2], [min_cracklength, start + 250])



    def update_plot(self, dK, daDN):

        try:
            plt.figure(self.__plot_number)

            self.__load_plt.set_data(dK, daDN)

            self.__helper_lines[2].set_data(([dK, dK],[self.__min_cracklength, daDN ] ))
            self.__helper_lines[3].set_data(([1,dK],[daDN, daDN]))


        except ValueError:
            print("ValueError")

            return

        except IndexError:
            print("IndexError")
            return

    def save_plot(self):
        try:
            os.stat(g_plot_path)
        except:
            os.mkdir(g_plot_path)

        try:
            plt.figure(self.__plot_number)
            now = datetime.datetime.now()
            #now = datetime.now().strftime('%y-%m-%d_%I-%M-%S')
            path_and_file = str("./plots/da_dN_diagram_" + str(now) + ".png")
            PlotBase.SaveFigure(self.fig, path_and_file )
            return path_and_file
        except:
            print("Error - could not save plot")


    def __get_section_1(self, dadn_0, dadn_1, dK0, dK1):
        a = (dadn_0 - dadn_1) / (dK0**2 - dK1**2)
        b = dadn_1 - a * dK1**2

        px = np.linspace(dK0, dK1, 100)
        py = a * px**2 + b

        return px, py


    def __get_section_2(self, C, m, N_start, Nstop):

        dK = np.linspace(N_start, Nstop, Nstop-N_start)
        da_dn = C * dK**m

        return dK, da_dn


    def __get_section_3(self, dadn_2, dadn3, dk2, dk3,  t):
        a = (dadn_2 - dadn3) / (np.exp(t * dk2) - np.exp(t * dk3))
        b = dadn3 - a * np.exp(t * dk3)
        px = np.linspace(dk2, dk3, 100)
        py = a * np.exp(t * px) + b

        return px, py
