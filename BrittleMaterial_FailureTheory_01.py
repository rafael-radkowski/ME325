
"""Failure theories for ductile materials - principal stress example

# -*- coding: utf-8 -*-
This module provides and example explaining the failure theorie for ductile materials
in a plane. The user can set the principal stresses and the yield stress for a material.
The class show a plot with the two envelopes and the principal stress:
Implemented theories are:

- Maximum shear stress theory or Tresca theory
- Distortion enerty theory or von Mises theory.

User input:
- Yield strength
- Principal stresses

Press 'e' for manual input.

Example:
    root = Tk()
    root.geometry("800x600+300+300")
    app = DuctileFailureTheory01()
    root.mainloop()

    or from a console.

    $ python DuctileFailureTheory01.py

Note that this script was developed and tested with Python 3.5.3

Attributes:
    -

Todo:
    *

Rafael Radkowski
Iowa State University
Dec. 28, 2018

rafael@iastate.edu
All copyright reserved.
"""

# matplotlib
import platform
import matplotlib
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# tkinter for the display
from tkinter import *
from tkinter import Canvas
from tkinter import Tk, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Scale, Checkbutton
import tkinter as tk

# failure theory implementatio.
from ME325Common.FailureTheories import *


class BrittleMaterial_FailureTheory_01(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    #limits
    limit_ut_stress = 200
    limit_uc_stress = 200
    limit_sigma1 = limit_ut_stress + 20
    limit_sigma2 = limit_ut_stress + 20


    # Ultimate tensile stress
    stress_ut_default = 80
    stress_ut_slider = 0
    stress_ut_str = 0
    stress_ut_var = 0

    # Ultimate compression stress
    stress_uc_default = 120
    stress_uc_slider = 0
    stress_uc_str = 0
    stress_uc_var = 0


    # principle stress
    slider_length = 220
    sigma1_slider = 0
    sigma1_str = 0
    sigma1_var = 0

    # principle stress
    sigma2_slider = 0
    sigma2_str = 0
    sigma2_var = 0

    # von Mises output
    MNST = 0
    MNSTFoS_str = 0

    # MM output
    MM_str = 0
    MM_FoS_str = 0

    # BCM Output
    BCM_str = 0
    BCM_Fos_str = 0

    PrincipalStress_FoS_str = 0

    # checkboxes
    cb_mod_mohr = 0
    cb_mnst = 0
    cb_coulomb_mohr = 0

    # manual entry variables
    input_window = None
    entry_Sut = 0
    entry_Suc = 0
    entry_s1 = 0
    entry_s2 = 0

    # canvas
    window = 0
    canvas = 0

    # plotted output data
    normal_theory_plot = [0, 0, 0, 0]
    mod_mohr_theory_plot = [0, 0, 0, 0, 0, 0]
    coulomb_mohr_theory_plot =  [0, 0, 0, 0, 0, 0]
    mises_values = 0
    tresca_values = [0,0,0,0,0,0]
    sigma12_values = 0
    load_line_values = 0


    def __init__(self):
        super().__init__()


        self.stress_ut_var = DoubleVar()
        self.stress_ut_var.set(0)
        self.stress_ut_str = StringVar()
        self.stress_ut_str.set("0")

        self.stress_uc_var = DoubleVar()
        self.stress_uc_var.set(0)
        self.stress_uc_str = StringVar()
        self.stress_uc_str.set("0")

        self.sigma1_var = DoubleVar()
        self.sigma1_var.set(0)
        self.sigma1_str = StringVar()
        self.sigma1_str.set("0")

        self.sigma2_var = DoubleVar()
        self.sigma2_var.set(0)
        self.sigma2_str = StringVar()
        self.sigma2_str.set("0")

        self.cb_mod_mohr = IntVar()
        self.cb_mod_mohr.set(1)
        self.cb_mnst = IntVar()
        self.cb_mnst.set(1)
        self.cb_coulomb_mohr = IntVar()
        self.cb_coulomb_mohr.set(1)


        self.MNST_str = StringVar()
        self.MNST_str.set("0")
        self.MNSTFoS_str = StringVar()
        self.MNSTFoS_str.set("0")

        self.MM_str = StringVar()
        self.MM_str.set("0")
        self.MM_FoS_str = StringVar()
        self.MM_FoS_str.set("0")

        self.BCM_str = StringVar()
        self.BCM_str.set("0")
        self.BCM_Fos_str = StringVar()
        self.BCM_Fos_str.set("0")

        self.PrincipalStress_FoS_str = StringVar()
        self.PrincipalStress_FoS_str.set("0")

        self.entry_Sut = StringVar()
        self.entry_Sut.set("0")
        self.entry_Suc = StringVar()
        self.entry_Suc.set("0")
        self.entry_s1 = StringVar()
        self.entry_s1.set("0")
        self.entry_s2 = StringVar()
        self.entry_s2.set("0")


        self.initUI()
        self.update_values(0.0)
        #self.plot()


    # ----------- Update the outputs ----------

    def update_plot(self):
        """
        Update teh plot area
        :return:
        """
        Sut = self.stress_ut_var.get()
        Suc = self.stress_uc_var.get()
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()

        #------------------------------------------------
        # Update Normal failure theory
        if self.cb_mnst.get() == 0:
            Sut = 0
            Suc = 0

        # Normal failure theory
        self.normal_theory_plot[0].set_data([Sut, Sut], [-Suc, Sut])
        self.normal_theory_plot[1].set_data([Sut, -Suc], [Sut, Sut])
        self.normal_theory_plot[2].set_data([-Suc, -Suc], [Sut, -Suc])
        self.normal_theory_plot[3].set_data([-Suc, Sut], [-Suc, -Suc])

        # ------------------------------------------------
        # Update modified morh failure theory


        Sut = self.stress_ut_var.get()
        Suc = self.stress_uc_var.get()

        if self.cb_mod_mohr.get() == 0:
            Sut = 0
            Suc = 0

        self.mod_mohr_theory_plot[0].set_data([Sut, Sut], [-Sut, Sut])
        self.mod_mohr_theory_plot[1].set_data([Sut, -Sut], [Sut, Sut])
        self.mod_mohr_theory_plot[2].set_data([-Sut, -Suc], [Sut, 0])
        self.mod_mohr_theory_plot[3].set_data([-Suc, -Suc], [0, -Suc])
        self.mod_mohr_theory_plot[4].set_data([-Suc, 0], [-Suc, -Suc])
        self.mod_mohr_theory_plot[5].set_data([0, Sut], [-Suc, -Sut])

        # ------------------------------------------------
        # Update Coulomb Mohr failure theory

        Sut = self.stress_ut_var.get()
        Suc = self.stress_uc_var.get()

        if self.cb_coulomb_mohr.get() == 0:
            Sut = 0
            Suc = 0

        # Coulomb mohr strength
        self.coulomb_mohr_theory_plot[0].set_data([Sut, Sut], [0, Sut])
        self.coulomb_mohr_theory_plot[1].set_data([Sut, 0], [Sut, Sut])
        self.coulomb_mohr_theory_plot[2].set_data([0, -Suc], [Sut, 0])
        self.coulomb_mohr_theory_plot[3].set_data([-Suc, -Suc], [0, -Suc])
        self.coulomb_mohr_theory_plot[4].set_data([-Suc, 0], [-Suc, -Suc])
        self.coulomb_mohr_theory_plot[5].set_data([0, Sut], [-Suc, 0])


        #---------------------------------------------------
        # load line
        flip = 1
        if s1 < 0.00001 and s1 > -0.00001:
            s1 = 0.00001
        if s1 < 0.0:
            flip = -1

        slope_load_line = s2 / s1
        self.load_line_values.set_data([0.0,flip * 400], [0.0,slope_load_line * 400 * flip])


        # ------------------------------------------------
        # Update principal stress
        self.sigma12_values.set_data([s1], [s2])

        # ------------------------------------------------
        # Update limits
        Sut = self.stress_ut_var.get()
        Suc = self.stress_uc_var.get()

        plt.xlim(-Suc - 40, Sut + 40)
        plt.ylim(-Suc - 40, Sut + 40)

        self.canvas.draw_idle()

    def update_output_display(self):
        """
        Update the output display, the stresses and factor of safeties this
        panel shows.
        :return:
        """
        Sut = self.stress_ut_var.get()
        Suc = self.stress_uc_var.get()
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()



        MNSTStress, MNSTFoS = CalcMNSTStressFoS(s1, s2, Sut, Suc)

        # Update the plot
        self.MNST_str.set(str(round(MNSTStress,2)))
        if MNSTFoS < 100:
            self.MNSTFoS_str.set(str(round(MNSTFoS,2)))
        else:
            self.MNSTFoS_str.set("Inf")


        MMStress, MMFOS = CalcMMStressFoS(s1,s2, Sut, Suc)

        # Update the plot
        self.MM_str.set(str(round(MMStress, 2)))
        if MMFOS < 100:
            self.MM_FoS_str.set(str(round(MMFOS,2)))
        else:
            self.MM_FoS_str.set("Inf")


        BCMStress, BCMFoS = CalcBCMStressFoS(s1, s2, Sut, Suc)

        # Update the plot
        self.BCM_str.set(str(round(BCMStress, 2)))
        if BCMFoS < 100:
            self.BCM_Fos_str.set(str(round(BCMFoS, 2)))
        else:
            self.BCM_Fos_str.set("Inf")





    # ---------Widget callbacks ---------------

    def update_values(self, val):
        """
        Update function for all widgets. The function updates the
        input values. Note that all slider widgets call this functions
        :param val: The value the widget passes
        :return: -
        """
        self.stress_ut_var.set(round(self.stress_ut_slider.get() ,2))
        self.stress_ut_str.set(str(self.stress_ut_var.get()))

        self.stress_uc_var.set(round(self.stress_uc_slider.get(), 2))
        self.stress_uc_str.set(str(self.stress_uc_var.get()))

        self.sigma1_var.set(round(self.sigma1_slider.get(),2))
        self.sigma1_str.set(str(self.sigma1_var.get()))

        self.sigma2_var.set(round(self.sigma2_slider.get(), 2))
        self.sigma2_str.set(str(self.sigma2_var.get()))

        self.update_plot()
        self.update_output_display()

    def cb_update(self):
        """
        Checkbox update. Captures the ckeckbox clicks.
        Checkboxes do not pass any arguments to the function
        :return:
        """
        self.update_values(0)

    def key_callback(self, event):
        """
        Create a subwindow to allow for user input
        :param event:
        :return:
        """
        self.create_subwindow()

    def sub_button_use_callback(self):
        """
        Apply the values that the user set in the sub window
        :return:
        """
        try:
            # check for limits
            Sut =  np.min( [ float(self.limit_ut_stress), np.max([ float(0) ,float(self.entry_Sut.get()) ]) ]  )
            self.entry_Sut.set(Sut)
            Suc = np.min([float(self.limit_uc_stress), np.max([float(0), float(self.entry_Suc.get())])])
            self.entry_Suc.set(Suc)
            s1 = np.min( [ float(self.limit_sigma1), np.max([ float(-self.limit_sigma1) ,float(self.entry_s1.get()) ]) ]  )
            self.entry_s1.set(s1)
            s2 = np.min([float(self.limit_sigma2), np.max([float(-self.limit_sigma2), float(self.entry_s2.get())])])
            self.entry_s2.set(s2)

            # copy values
            self.stress_ut_slider.set(Sut )
            self.stress_uc_slider.set(Suc)
            self.sigma1_slider.set(s1)
            self.sigma2_slider.set(s2)

            self.update_values(0)
        except ValueError:
            print("Something went wrong - invalid numbers")

    def sub_window_destroyed_callback(self):
        """
        Destroy the subwindow
        :return:
        """
        self.input_window.destroy()
        self.input_window = None


    # ------------ Inits ---------------

    def create_subwindow(self):

        self.input_window = Toplevel(self.master)

        #style = ttk.Style(input_window)
        #style.theme_use('classic')

        tk.Label(self.input_window, text="Ultimate tensile, Sut (N/mm^2):", background='white').grid(sticky=NW, row=0, column=0)
        tk.Label(self.input_window, text="Ultimate compression, Suc (N/mm^2):", background='white').grid(sticky=NW, row=1, column=0)
        tk.Label(self.input_window, text="Enter Sut and Suc as positive values", background='white').grid(sticky=NW, row=2,
                                                                                                       column=0, columnspan=2)
        tk.Label(self.input_window, text="Sigma 1 (N/mm^2):", background='white').grid(sticky=NW, row=3, column=0)
        tk.Label(self.input_window, text="Sigma 3 (N/mm^2):", background='white').grid(sticky=NW, row=4, column=0)

        # copy values
        self.entry_Sut.set(self.stress_ut_str.get())
        self.entry_Suc.set(self.stress_uc_str.get())
        self.entry_s1.set(self.sigma1_str.get())
        self.entry_s2.set(self.sigma2_str.get())

        e1 = Entry(self.input_window, textvariable=self.entry_Sut).grid(sticky=NW, row=0, column=1)
        e2 = Entry(self.input_window, textvariable=self.entry_Suc).grid(sticky=NW, row=1, column=1)
        e3 = Entry(self.input_window, textvariable=self.entry_s1).grid(sticky=NW, row=3, column=1)
        e4 = Entry(self.input_window, textvariable=self.entry_s2).grid(sticky=NW, row=4, column=1)

        b = tk.Button(self.input_window, text="Use", command=self.sub_button_use_callback,
                   background='white').grid(sticky=NE, row=5, column=1, padx=7, pady=7)

        c = tk.Button(self.input_window, text="Close", command=self.sub_window_destroyed_callback,
                      background='white').grid(sticky=NW, row=5, column=0, padx=7, pady=7)

    def create_plot(self):
        """
        Create the plot and the plot area
        :return:
        """

        fig, ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(left=0.15, bottom=0.15)
        fig.set_size_inches(9, 9, forward=True)

        Sut = self.stress_ut_default
        Suc = self.stress_uc_default
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()

        linewidth = 1

        # Normal failure theory
        self.normal_theory_plot[0], = plt.plot([Sut, Sut], [-Suc, Sut], 'k-', color='b', lw=linewidth, label='MNST')
        self.normal_theory_plot[1], = plt.plot([Sut, -Suc], [Sut, Sut], 'k-', color='b', lw=linewidth)
        self.normal_theory_plot[2], = plt.plot([-Suc, -Suc], [Sut, -Suc], 'k-', color='b', lw=linewidth)
        self.normal_theory_plot[3], = plt.plot([-Suc, Sut], [-Suc, -Suc], 'k-', color='b', lw=linewidth)

        # Modified mohr strength
        self.mod_mohr_theory_plot[0], = plt.plot([Sut, Sut], [-Sut, Sut], 'k-', color='r', lw=linewidth, label='MM')
        self.mod_mohr_theory_plot[1], = plt.plot([Sut, -Sut], [Sut, Sut], 'k-', color='r', lw=linewidth)
        self.mod_mohr_theory_plot[2], = plt.plot([-Sut, -Suc], [Sut, 0], 'k-', color='r', lw=linewidth)
        self.mod_mohr_theory_plot[3], = plt.plot([-Suc, -Suc], [0, -Suc], 'k-', color='r', lw=linewidth)
        self.mod_mohr_theory_plot[4], = plt.plot([-Suc, 0], [-Suc, -Suc], 'k-', color='r', lw=linewidth)
        self.mod_mohr_theory_plot[5], = plt.plot([0, Sut], [-Suc, -Sut], 'k-', color='r', lw=linewidth)

        # Coulomb mohr strength
        self.coulomb_mohr_theory_plot[0], = plt.plot([Sut, Sut], [0, Sut], 'k-', color='g', lw=linewidth, label='BCM')
        self.coulomb_mohr_theory_plot[1], = plt.plot([Sut, 0], [Sut, Sut], 'k-', color='g', lw=linewidth)
        self.coulomb_mohr_theory_plot[2], = plt.plot([0, -Suc], [Sut, 0], 'k-', color='g', lw=linewidth)
        self.coulomb_mohr_theory_plot[3], = plt.plot([-Suc, -Suc], [0, -Suc], 'k-', color='g', lw=linewidth)
        self.coulomb_mohr_theory_plot[4], = plt.plot([-Suc, 0], [-Suc, -Suc], 'k-', color='g', lw=linewidth)
        self.coulomb_mohr_theory_plot[5], = plt.plot([0, Sut], [-Suc, 0], 'k-', color='g', lw=linewidth)


        # load line
        if s1 < 0.00001 and s1 > -0.00001:
            s1 = 0.00001
        slope_load_line = s2 / s1 * 400
        self.load_line_values, = plt.plot([0.0, 400], [0.0, slope_load_line], 'k--')

        # Principal stress
        self.sigma12_values, = plt.plot([s1], [s2], 'ro')

        # fig = Figure(figsize=(5, 4), dpi=100)
        # fig.add_subplot(111).plot(mises_x, mises_y)

        plt.grid()
        plt.xlabel(r'$\sigma_1\;\;\left(\frac{N}{mm^2}\right)$')
        plt.ylabel(r'$\sigma_3\;\;\left(\frac{N}{mm^2}\right)$')
        plt.xlim(-Suc - 40, Sut + 40)
        plt.ylim(-Suc - 40, Sut + 40)
        plt.legend(loc=2)

        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()

    def initUI(self):
        """
        Init the user interface and all widgets
        :return: -
        """
        rows_for_plot = 17
        cols_for_plot = 4

        self.master.title("ME 325 Machine Component Design")
        self.pack(fill=BOTH, expand=True)

        # keyboard binding
        self.master.bind("e", self.key_callback)

        self.columnconfigure(0, weight=1) # first and last column can expand
        self.columnconfigure(0, pad=7)
        self.rowconfigure(rows_for_plot, weight=1)
        self.rowconfigure(rows_for_plot, pad=7)

        lbl = Label(self, text="Failure Theories for Brittle Materials")
        lbl.grid(sticky=W, pady=4, padx=5)

        ##------------------------------------------------------------------
        # PLOT
        self.canvas = Canvas(self, width=300, height=300)
        self.create_plot()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=cols_for_plot, rowspan=rows_for_plot,
                         padx=5, sticky=E + W + S + N)

        ##------------------------------------------------------------------
        # INPUT
        lbl0 = Label(self, text="Input:",font='Helvetica 14 bold')
        lbl0.grid(sticky=NW, row=1, column=cols_for_plot+1)

        # Ultimate tensile stress
        lbl3 = Label(self, text="Ultimate tensile s. (N/mm^2):")
        lbl3.grid(sticky=W, row=2, column=cols_for_plot+1)


        self.stress_ut_label = Label(self, textvariable=self.stress_ut_str)
        self.stress_ut_label.grid(sticky=W, row=2, column=cols_for_plot+2)

        self.stress_ut_slider = Scale(self, value=self.stress_ut_default, from_=0.0,
                                        to=self.limit_ut_stress,orient=HORIZONTAL,
                                        length=self.slider_length, command=self.update_values)
        self.stress_ut_slider.grid(sticky=W, row=3, column=4, columnspan=cols_for_plot+2)

        # Ultimate compression stress, row 4+5

        Label(self, text="Ultimate compression s. (N/mm^2):").grid(sticky=W, row=4, column=cols_for_plot + 1)

        self.stress_uc_label = Label(self, textvariable=self.stress_uc_str)
        self.stress_uc_label.grid(sticky=W, row=4, column=cols_for_plot + 2)

        self.stress_uc_slider = Scale(self, value=self.stress_uc_default, from_=0.0,
                                      to=self.limit_uc_stress, orient=HORIZONTAL,
                                      length=self.slider_length, command=self.update_values)
        self.stress_uc_slider.grid(sticky=W, row=5, column=4, columnspan=cols_for_plot + 2)


        # Principle stress sigma 1, rows 6 + 7
        lbl4 = Label(self, text="Sigma 1 (N/mm^2):")
        lbl4.grid(sticky=N+W, row=6, column=cols_for_plot+1)

        lbl4 = Label(self, textvariable=self.sigma1_str)
        lbl4.grid(sticky=N+W, row=6, column=cols_for_plot+2)

        self.sigma1_slider = Scale(self, from_=-self.limit_sigma1, to=self.limit_sigma1, orient=HORIZONTAL,
                                   length = self.slider_length, command=self.update_values)
        self.sigma1_slider.grid(sticky=NW, row=7, column=cols_for_plot+1, columnspan=2)

        # Principle stress sigma 2, rows 8 + 9
        lbl4 = Label(self, text="Sigma 3 (N/mm^2):")
        lbl4.grid(sticky=NW, row=8, column=cols_for_plot+1)

        lbl4 = Label(self, textvariable=self.sigma2_str)
        lbl4.grid(sticky=NW, row=8, column=cols_for_plot+2)

        self.sigma2_slider = Scale(self, from_=-self.limit_sigma2, to=self.limit_sigma2, orient=HORIZONTAL,
                        length = self.slider_length, command=self.update_values)
        self.sigma2_slider.grid(sticky=NW, row=9, column=cols_for_plot+1, columnspan=2)

        ##-----------------------------------------------------------------------------
        # Output
        lbl5 = Label(self, text="Output:",font='Helvetica 14 bold')
        lbl5.grid(sticky=NW, row=10, column=cols_for_plot+1)

        lbl6 = Label(self, text="MNST rel. stress (N/mm^2):")
        lbl6.grid(sticky=NW, row=11, column=cols_for_plot+1)

        lbl7 = Label(self, textvariable=self.MNST_str)# #text="1.0")
        lbl7.grid(sticky=NW, row=11, column=cols_for_plot+2)

        lbl8 = Label(self, text="MNST FoS:")
        lbl8.grid(sticky=NW, row=12, column=cols_for_plot+1)

        lbl9 = Label(self, textvariable=self.MNSTFoS_str)  # #text="1.0")
        lbl9.grid(sticky=NW, row=12, column=cols_for_plot+2)

        ##
        # MM output
        lbl10 = Label(self, text="MM rel. stress (N/mm^2):")
        lbl10.grid(sticky=NW, row=13, column=cols_for_plot+1)

        lbl11 = Label(self, textvariable=self.MM_str)  # #text="1.0")
        lbl11.grid(sticky=NW, row=13, column=cols_for_plot+2)

        lbl12 = Label(self, text="MM FoS:")
        lbl12.grid(sticky=NW, row=14, column=cols_for_plot+1)

        lbl13 = Label(self, textvariable=self.MM_FoS_str)  # #text="1.0")
        lbl13.grid(sticky=NW, row=14, column=cols_for_plot+2)


        ##------
        # BCM output
        Label(self, text="BCM rel. stress (N/mm^2):").grid(sticky=NW, row=15, column=cols_for_plot + 1)
        Label(self, textvariable=self.BCM_str).grid(sticky=NW, row=15, column=cols_for_plot + 2)

        Label(self, text="BCM FoS:").grid(sticky=NW, row=16, column=cols_for_plot + 1)
        Label(self, textvariable=self.BCM_Fos_str).grid(sticky=NW, row=16, column=cols_for_plot + 2)


        cbtn = Button(self, text="Exit", command=self.quit)
        cbtn.grid(row=rows_for_plot+1, column=cols_for_plot+2, pady=4)


        check0 = Checkbutton(self, text="MNST", variable=self.cb_mnst, command=self.cb_update)
        check0.grid(row=rows_for_plot+1,  column=cols_for_plot-3, sticky=W)

        check1 = Checkbutton(self, text="MM", variable=self.cb_mod_mohr, command=self.cb_update)
        check1.grid(row=rows_for_plot+1, column=cols_for_plot-2, sticky=W)

        check1 = Checkbutton(self, text="BCM", variable=self.cb_coulomb_mohr, command=self.cb_update)
        check1.grid(row=rows_for_plot + 1, column=cols_for_plot - 1, sticky=W)

        Label(self, text="press 'e' for manual input.", font='Helvetica 12').grid(row=rows_for_plot + 1, column=0,
                                                                                  sticky=W, padx=7)


def main():
    root = Tk()
    root.geometry("960x720+300+300")
    app = BrittleMaterial_FailureTheory_01()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()