


# matplotlib
import platform
import matplotlib
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np



class DuctileFailureTheoriesPlot():

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


    def create_plots(self, figsize_):
        plt.figure(self.plot_number)
        self.fig, self.axis = plt.subplots(figsize=(figsize_, figsize_), num=1)
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