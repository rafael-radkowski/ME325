
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
    app = DuctileMaterial_FailureTheory_01()
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


class DuctileMaterial_FailureTheory_01(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    #limits
    limit_yieldstress = 200
    limit_sigma1 = limit_yieldstress + 20
    limit_sigma2 = limit_yieldstress + 20


    # Yield stress
    yieldstress_default = 120
    yieldstress_slider = 0
    yieldstress_str = 0
    yieldstress_var = 0

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
    vonMises_str = 0;
    vonMisesFoS_str = 0;

    # Tresca output
    Tresca_str = 0
    Tresca_FoS_str = 0

    PrincipalStress_FoS_str = 0

    # checkboxes
    cb_tresca = 0
    cb_mises = 0

    # manual entry variables
    input_window = None
    entry_Sy = 0
    entry_s1 = 0
    entry_s2 = 0

    # canvas
    window = 0
    canvas = 0

    # plotted output data
    mises_values = 0
    tresca_values = [0,0,0,0,0,0]
    sigma12_values = 0
    load_line_values = 0


    def __init__(self):
        super().__init__()


        self.yieldstress_var = DoubleVar()
        self.yieldstress_var.set(0)
        self.yieldstress_str = StringVar()
        self.yieldstress_str.set("0")

        self.sigma1_var = DoubleVar()
        self.sigma1_var.set(0)
        self.sigma1_str = StringVar()
        self.sigma1_str.set("0")

        self.sigma2_var = DoubleVar()
        self.sigma2_var.set(0)
        self.sigma2_str = StringVar()
        self.sigma2_str.set("0")

        self.cb_tresca = IntVar()
        self.cb_tresca.set(1)
        self.cb_mises = IntVar()
        self.cb_mises.set(1)

        self.vonMises_str = StringVar()
        self.vonMises_str.set("0")
        self.vonMisesFoS_str = StringVar()
        self.vonMisesFoS_str.set("0")

        self.Tresca_str = StringVar()
        self.Tresca_str.set("0")
        self.Tresca_FoS_str = StringVar()
        self.Tresca_FoS_str.set("0")

        self.PrincipalStress_FoS_str = StringVar()
        self.PrincipalStress_FoS_str.set("0")

        self.entry_Sy = StringVar()
        self.entry_Sy.set("0")
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
        Sy = self.yieldstress_var.get()
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()

        #------------------------------------------------
        # Update von Mises stres
        if self.cb_mises.get() == 0:
            Sy = 0

        angles_rad = np.linspace(0, 360, 360) * 3.1415 / 180.0
        mises_abs = np.sqrt(
            np.cos(angles_rad[:]) ** 2 + np.sin(angles_rad[:]) ** 2 - np.cos(angles_rad[:]) * np.sin(angles_rad[:]))
        mises_x = np.cos(angles_rad[:]) / mises_abs[:] * Sy
        mises_y = np.sin(angles_rad[:]) / mises_abs[:] * Sy

        self.mises_values.set_data(mises_x, mises_y)

        # ------------------------------------------------
        # Update Tresca stres
        Sy = self.yieldstress_var.get()

        if  self.cb_tresca.get() == 0:
            Sy = 0

        self.tresca_values[0].set_data([Sy, Sy], [0, Sy])
        self.tresca_values[1].set_data([Sy, 0], [Sy, Sy])
        self.tresca_values[2].set_data([0, -Sy], [Sy, 0])
        self.tresca_values[3].set_data([-Sy, -Sy], [0, -Sy])
        self.tresca_values[4].set_data([-Sy, 0], [-Sy, -Sy])
        self.tresca_values[5].set_data([0, Sy], [-Sy, 0])

        #---------------------------------------------------
        # load line
        flip = 1
        if s1 < 0.00001 and s1 > -0.00001:
            s1 = 0.00001
        if s1 < 0.0:
            flip = -1;

        slope_load_line = s2 / s1;
        self.load_line_values.set_data([0.0,flip * 400], [0.0,slope_load_line * 400 * flip])


        # ------------------------------------------------
        # Update principal stress
        self.sigma12_values.set_data([s1], [s2])

        # ------------------------------------------------
        # Update limits
        Sy = self.yieldstress_var.get()

        plt.xlim(-Sy - 40, Sy + 40)
        plt.ylim(-Sy - 40, Sy + 40)

        self.canvas.draw_idle()

    def update_stresses(self):
        """
        Update the output display, the stresses and factor of safeties this
        panel shows.
        :return:
        """
        Sy = self.yieldstress_var.get()
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()

        vonMisesEq, FoS_vonMisesEq = CalcVonMiesesFoS(s1, s2, Sy)

        # Update the plot
        self.vonMises_str.set(str(round(vonMisesEq,2)))
        if FoS_vonMisesEq < 100:
            self.vonMisesFoS_str.set(str(round(FoS_vonMisesEq,2)))
        else:
            self.vonMisesFoS_str.set("Inf")


        TrescaEqStress, FoS_TrescaEqStress = CalcTrescaFoS(s1,s2, Sy)

        # Update the plot
        self.Tresca_str.set(str(round(TrescaEqStress, 2)))
        if FoS_TrescaEqStress < 100:
            self.Tresca_FoS_str.set(str(round(FoS_TrescaEqStress,2)))
        else:
            self.Tresca_FoS_str.set("Inf")



        N = CalcPrincipalStressFos(s1,s2, Sy)
        if N < 100:
            self.PrincipalStress_FoS_str.set(str(round(N,2)))
        else:
            self.PrincipalStress_FoS_str.set("Inf")


    # ---------Widget callbacks ---------------

    def update_values(self, val):
        """
        Update function for all widgets. The function updates the
        input values. Note that all slider widgets call this functions
        :param val: The value the widget passes
        :return: -
        """
        self.yieldstress_var.set(round(self.yieldstress_slider.get() ,2))
        self.yieldstress_str.set(str(self.yieldstress_var.get()))

        self.sigma1_var.set(round(self.sigma1_slider.get(),2))
        self.sigma1_str.set(str(self.sigma1_var.get()))

        self.sigma2_var.set(round(self.sigma2_slider.get(), 2))
        self.sigma2_str.set(str(self.sigma2_var.get()))

        self.update_plot()
        self.update_stresses()

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
            Sy =  np.min( [ float(self.limit_yieldstress), np.max([ float(0) ,float(self.entry_Sy.get()) ]) ]  )
            self.entry_Sy.set(Sy)
            s1 = np.min( [ float(self.limit_sigma1), np.max([ float(-self.limit_sigma1) ,float(self.entry_s1.get()) ]) ]  )
            self.entry_s1.set(s1)
            s2 = np.min([float(self.limit_sigma2), np.max([float(-self.limit_sigma2), float(self.entry_s2.get())])])
            self.entry_s2.set(s2)

            # copy values
            self.yieldstress_slider.set(Sy )
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

        tk.Label(self.input_window, text="Yield stress (N/mm^2):", background='white').grid(sticky=NW, row=0, column=0)
        tk.Label(self.input_window, text="Sigma 1 (N/mm^2):", background='white').grid(sticky=NW, row=1, column=0)
        tk.Label(self.input_window, text="Sigma 3 (N/mm^2):", background='white').grid(sticky=NW, row=2, column=0)

        # copy values
        self.entry_Sy.set(self.yieldstress_str.get())
        self.entry_s1.set(self.sigma1_str.get())
        self.entry_s2.set(self.sigma2_str.get())

        e1 = Entry(self.input_window, textvariable=self.entry_Sy).grid(sticky=NW, row=0, column=1)
        e2 = Entry(self.input_window, textvariable=self.entry_s1).grid(sticky=NW, row=1, column=1)
        e3 = Entry(self.input_window, textvariable=self.entry_s2).grid(sticky=NW, row=2, column=1)

        b = tk.Button(self.input_window, text="Use", command=self.sub_button_use_callback,
                   background='white').grid(sticky=NE, row=3, column=1, padx=7, pady=7)

        c = tk.Button(self.input_window, text="Close", command=self.sub_window_destroyed_callback,
                      background='white').grid(sticky=NW, row=3, column=0, padx=7, pady=7)

    def create_plot(self):
        """
        Create the plot and the plot area
        :return:
        """

        fig, ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(left=0.15, bottom=0.15)
        fig.set_size_inches(9, 9, forward=True)

        Sy = self.yieldstress_default
        s1 = self.sigma1_var.get()
        s2 = self.sigma2_var.get()

        # Von Mises stress

        angles_rad = np.linspace(0, 360, 360) * 3.1415 / 180.0
        mises_abs = np.sqrt(
            np.cos(angles_rad[:]) ** 2 + np.sin(angles_rad[:]) ** 2 - np.cos(angles_rad[:]) * np.sin(angles_rad[:]))
        mises_x = np.cos(angles_rad[:]) / mises_abs[:] * Sy
        mises_y = np.sin(angles_rad[:]) / mises_abs[:] * Sy

        self.mises_values, = plt.plot(mises_x, mises_y, color='orange', label='von Mises')

        # Tresca stress
        color = 'purple'
        linewidth = 1

        self.tresca_values[0], = plt.plot([Sy, Sy], [0, Sy], 'k-', color=color, lw=linewidth, label='Tresca')
        self.tresca_values[1], = plt.plot([Sy, 0], [Sy, Sy], 'k-', color=color, lw=linewidth)
        self.tresca_values[2], = plt.plot([0, -Sy], [Sy, 0], 'k-', color=color, lw=linewidth)
        self.tresca_values[3], = plt.plot([-Sy, -Sy], [0, -Sy], 'k-', color=color, lw=linewidth)
        self.tresca_values[4], = plt.plot([-Sy, 0], [-Sy, -Sy], 'k-', color=color, lw=linewidth)
        self.tresca_values[5], = plt.plot([0, Sy], [-Sy, 0], 'k-', color=color, lw=linewidth)

        # load line
        if s1 < 0.00001 and s1 > -0.00001:
            s1 = 0.00001
        slope_load_line = s2 / s1 * 400;
        self.load_line_values, = plt.plot([0.0, 400], [0.0, slope_load_line], 'k--')

        # Principal stress
        self.sigma12_values, = plt.plot([s1], [s2], 'ro')

        # fig = Figure(figsize=(5, 4), dpi=100)
        # fig.add_subplot(111).plot(mises_x, mises_y)

        plt.grid()
        plt.xlabel(r'$\sigma_1\;\;\left(\frac{N}{mm^2}\right)$')
        plt.ylabel(r'$\sigma_3\;\;\left(\frac{N}{mm^2}\right)$')
        plt.xlim(-Sy - 40, Sy + 40)
        plt.ylim(-Sy - 40, Sy + 40)
        plt.legend()

        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.canvas.draw()

    def initUI(self):
        """
        Init the user interface and all widgets
        :return: -
        """
        rows_for_plot = 13
        cols_for_plot = 3

        self.master.title("ME 325 Machine Component Design")
        self.pack(fill=BOTH, expand=True)

        # keyboard binding
        self.master.bind("e", self.key_callback)

        self.columnconfigure(0, weight=1) # first and last column can expand
        self.columnconfigure(0, pad=7)
        self.rowconfigure(rows_for_plot, weight=1)
        self.rowconfigure(rows_for_plot, pad=7)

        lbl = Label(self, text="Failure Theories for Ductile Materials")
        lbl.grid(sticky=W, pady=4, padx=5)

        #area = Text(self)
        # area.grid(row=1, column=0, columnspan=3, rowspan=10,
        #          padx=5, sticky=E + W + S + N)
        self.canvas = Canvas(self, width=300, height=300)
        self.create_plot()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=cols_for_plot, rowspan=rows_for_plot,
                         padx=5, sticky=E + W + S + N)

        lbl0 = Label(self, text="Input:",font='Helvetica 14 bold')
        lbl0.grid(sticky=NW, row=1, column=cols_for_plot+1)

        # Yield stress
        lbl3 = Label(self, text="Yield stress (N/mm^2):")
        lbl3.grid(sticky=W, row=2, column=cols_for_plot+1)


        self.yieldstress_label = Label(self, textvariable=self.yieldstress_str)
        self.yieldstress_label.grid(sticky=W, row=2, column=cols_for_plot+2)

        self.yieldstress_slider = Scale(self, value=self.yieldstress_default, from_=0.0,
                                        to=self.limit_yieldstress,orient=HORIZONTAL,
                                        length=self.slider_length, command=self.update_values)
        self.yieldstress_slider.grid(sticky=W, row=3, column=4, columnspan=cols_for_plot+2)


        # Principle stress sigma 1
        lbl4 = Label(self, text="Sigma 1 (N/mm^2):")
        lbl4.grid(sticky=N+W, row=4, column=cols_for_plot+1)

        lbl4 = Label(self, textvariable=self.sigma1_str)
        lbl4.grid(sticky=N+W, row=4, column=cols_for_plot+2)

        self.sigma1_slider = Scale(self, from_=-self.limit_sigma1, to=self.limit_sigma1, orient=HORIZONTAL,
                                   length = self.slider_length, command=self.update_values)
        self.sigma1_slider.grid(sticky=NW, row=5, column=cols_for_plot+1, columnspan=2)

        # Principle stress sigma 2
        lbl4 = Label(self, text="Sigma 3 (N/mm^2):")
        lbl4.grid(sticky=NW, row=6, column=cols_for_plot+1)

        lbl4 = Label(self, textvariable=self.sigma2_str)
        lbl4.grid(sticky=NW, row=6, column=cols_for_plot+2)

        self.sigma2_slider = Scale(self, from_=-self.limit_sigma2, to=self.limit_sigma2, orient=HORIZONTAL,
                        length = self.slider_length, command=self.update_values)
        self.sigma2_slider.grid(sticky=NW, row=7, column=cols_for_plot+1, columnspan=2)

        # Output
        lbl5 = Label(self, text="Output:",font='Helvetica 14 bold')
        lbl5.grid(sticky=NW, row=8, column=cols_for_plot+1)

        lbl6 = Label(self, text="von Mises stress (N/mm^2):")
        lbl6.grid(sticky=NW, row=9, column=cols_for_plot+1)

        lbl7 = Label(self, textvariable=self.vonMises_str)# #text="1.0")
        lbl7.grid(sticky=NW, row=9, column=cols_for_plot+2)

        lbl8 = Label(self, text="von Mises FoS:")
        lbl8.grid(sticky=NW, row=10, column=cols_for_plot+1)

        lbl9 = Label(self, textvariable=self.vonMisesFoS_str)  # #text="1.0")
        lbl9.grid(sticky=NW, row=10, column=cols_for_plot+2)

        ##
        # Tresca output
        lbl10 = Label(self, text="Tresca stress (N/mm^2):")
        lbl10.grid(sticky=NW, row=11, column=cols_for_plot+1)

        lbl11 = Label(self, textvariable=self.Tresca_str)  # #text="1.0")
        lbl11.grid(sticky=NW, row=11, column=cols_for_plot+2)

        lbl12 = Label(self, text="Tresca FoS:")
        lbl12.grid(sticky=NW, row=12, column=cols_for_plot+1)

        lbl13 = Label(self, textvariable=self.Tresca_FoS_str)  # #text="1.0")
        lbl13.grid(sticky=NW, row=12, column=cols_for_plot+2)

        ## principle stress fos

       # lbl14 = Label(self, text="Princ. stress FoS:")
       # lbl14.grid(sticky=NW, row=13, column=4)

        #lbl15 = Label(self, textvariable=self.PrincipalStress_FoS_str)
        #lbl15.grid(sticky=NW, row=13, column=5)




        cbtn = Button(self, text="Exit", command=self.quit)
        cbtn.grid(row=rows_for_plot+1, column=cols_for_plot+2, pady=4)


        check0 = Checkbutton(self, text="von Mises", variable=self.cb_mises, command=self.cb_update)
        check0.grid(row=rows_for_plot+1,  column=cols_for_plot-2, sticky=W)

        check1 = Checkbutton(self, text="Tresca", variable=self.cb_tresca, command=self.cb_update)
        check1.grid(row=rows_for_plot+1, column=cols_for_plot-1, sticky=W)

        Label(self, text="press 'e' for manual input.", font='Helvetica 12').grid(row=rows_for_plot+1, column=0, sticky=W, padx=7)



def main():
    root = Tk()
    root.geometry("960x720+300+300")
    app = DuctileMaterial_FailureTheory_01()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()