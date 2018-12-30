
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

# for images
from PIL import Image, ImageTk

# failure theory implementatio.
from ME325Common.FailureTheories import *

# import the example
from ME325Common.example_beam import *

# import plot
from ME325Common.PlotHelpers import *


class DuctileMaterial_FailureTheory_02(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    #limits
    limit_yieldstress = 200 #N/mm^2
    limit_load = 2000 # n
    limit_torsion = 100 #Nm
    limit_angle = 90 # deg
    limit_wh = 100 # mm
    limit_l = 1000 # mm

    # defaults
    yieldstress_default = 120 # N/mm^2
    force_default = 100 # N
    width_default = 10 # mm
    height_default = 20 # mm
    length_default = 100 # mm
    angle_default = 90 # deg
    torsion_default = 10 # Nm

    # Yield stress
    yieldstress_slider = 0
    yieldstress_str = 0
    yieldstress_var = 0

    # principle stress
    slider_length = 260

    # Load input
    Load_slider = 0
    Load_str = 0
    Load_var = 0

    # Torsion input
    Torsion_slider = 0
    Torsion_str = 0
    Torsion_var = 0

    # Angle input
    Angle_slider = 0
    Angle_str = 0
    Angle_var = 0

    # dimensions
    height_slider = 0
    height_var = 0
    height_str = 0
    width_slider = 0
    width_var = 0
    width_str = 0
    length_slider = 0
    length_var = 0
    length_str = 0

    # von Mises output
    vonMises_str = 0;
    vonMisesFoS_str = 0;

    # Tresca output
    Tresca_str = 0
    Tresca_FoS_str = 0


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

    # the plot
    axis = None
    thefig = None

    # plotted output data
    mises_values = 0
    tresca_values = [0,0,0,0,0,0]
    sigma12_values = 0
    load_line_values = 0


    # The example
    example = None

    # Tresca and Mises plot
    failure_theory_plts  = None


    def __init__(self):
        super().__init__()


        self.yieldstress_var = DoubleVar()
        self.yieldstress_var.set(0)
        self.yieldstress_str = StringVar()
        self.yieldstress_str.set("0")

        self.Load_var = DoubleVar()
        self.Load_var.set(0)
        self.Load_str = StringVar()
        self.Load_str.set("0")

        self.Torsion_str = StringVar()
        self.Torsion_str.set("0")
        self.Torsion_var = DoubleVar()
        self.Torsion_var.set(0)

        self.Angle_var = DoubleVar()
        self.Angle_var.set(0)
        self.Angle_str = StringVar()
        self.Angle_str.set("0")

        self.height_var = DoubleVar()
        self.height_var.set(0)
        self.height_str = StringVar()
        self.height_str.set(0)
        self.width_var = DoubleVar()
        self.width_var.set(0)
        self.width_str = StringVar()
        self.width_str.set(0)
        self.length_var = DoubleVar()
        self.length_var.set(0)
        self.length_str = StringVar()
        self.length_str.set(0)

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

        self.entry_Sy = StringVar()
        self.entry_Sy.set("0")
        self.entry_s1 = StringVar()
        self.entry_s1.set("0")
        self.entry_s2 = StringVar()
        self.entry_s2.set("0")


        self.example = ExampleBeam()
        self.example.setLimits(self.limit_yieldstress, self.limit_load, self.limit_torsion, self.limit_angle, self.limit_wh, self.limit_l)


        self.failure_theory_plts = DuctileFailureTheoriesPlot()


        self.initUI()
        self.update_values(0.0)
        #self.plot()




    # ----------- Update the outputs ----------

    def update_plot(self):
        """
        Update teh plot area
        :return:
        """
        plt.figure(1)


        Sy = self.yieldstress_var.get()
        F = self.Load_var.get()
        T = self.Torsion_var.get()
        a = self.Angle_var.get()
        b = self.width_var.get()
        h = self.height_var.get()
        l = self.length_var.get()

        # Calculate streses
        Ixx, Iyy = self.example.calcI(b, h)
        s1, s2, sx, sy = self.example.calcPrincipalStress(F, T, l, a)

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

        plt.figure(1)
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
        F = self.Load_var.get()
        T = self.Torsion_var.get()
        a = self.Angle_var.get()
        b = self.width_var.get()
        h = self.height_var.get()
        l = self.length_var.get()

        # Calculate streses
        Ixx, Iyy = self.example.calcI(b, h)
        s1, s2, sx, sy = self.example.calcPrincipalStress(F, T, l, a)

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

        self.Load_var.set(round(self.Load_slider.get(),2))
        self.Load_str.set(str(self.Load_var.get()))

        self.Angle_var.set(round(self.Angle_slider.get(), 2))
        self.Angle_str.set(str(self.Angle_var.get()))

        self.Torsion_var.set(round(self.Torsion_slider.get(), 2))
        self.Torsion_str.set(str(self.Torsion_var.get()))

        self.height_var.set(round(self.height_slider.get(),2))
        self.height_str.set(str(self.height_var.get()))

        self.width_var.set(round(self.width_slider.get(), 2))
        self.width_str.set(str(self.width_var.get()))

        self.length_var.set(round(self.length_slider.get(), 2))
        self.length_str.set(str(self.length_var.get()))

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
        if event.char == 'e':
            self.create_subwindow()
        elif event.char == 'd':
            self.example.createDetailsWindow(self.master)


    def sub_button_use_callback(self):
        """
        Apply the values that the user set in the sub window
        :return:
        """

        try:
            # get values
            Sy, F, a, T,  h, w, l = self.example.getManualEntryValues()

            # copy values
            self.yieldstress_slider.set(Sy )
            self.Load_slider.set(F)
            self.Torsion_slider.set(T)
            self.Angle_slider.set(a)
            self.height_slider.set(h)
            self.width_slider.set(w)
            self.length_slider.set(l)

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


        self.example.createManualEntryMenu(self.master, self.sub_button_use_callback)
        self.example.setMenuValue(self.yieldstress_str.get(), self.Load_str.get(), self.Torsion_str.get(),self.Angle_str.get(),
                                  self.height_str.get(), self.width_str.get(), self.length_str.get())

    def create_plot(self):
        """
        Create the plot and the plot area
        :return:
        """

        plt.figure(1)
        fig, self.axis = plt.subplots(figsize=(8, 8), num=1)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        fig.set_size_inches(9, 9, forward=True)

        Sy = self.yieldstress_default
        F = self.Load_var.get()
        T = self.Torsion_var.get()
        a = self.Angle_var.get()
        l = self.length_var.get()

        # Calculate streses
        self.example.calcI(1,1)
        s1, s2, sx, sy = self.example.calcPrincipalStress(F, T, l, a)


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

        plt.figure(1)
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
        rows_for_plot = 24
        cols_for_plot = 3
        output_row_start = 16

        self.master.title("ME 325 Machine Component Design")
        self.pack(fill=BOTH, expand=True)

        # keyboard binding
        self.master.bind("e", self.key_callback)
        self.master.bind("d", self.key_callback)

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

        self.yieldstress_slider = Scale(self, value=self.yieldstress_default, from_=1.0,
                                        to=self.limit_yieldstress,orient=HORIZONTAL,
                                        length=self.slider_length, command=self.update_values)
        self.yieldstress_slider.grid(sticky=W, row=3, column=4, columnspan=cols_for_plot+2)

        ##---------------------------------------------------------------------------------
        # Load input
        Label(self, text="Load F (N):").grid(sticky=N+W, row=4, column=cols_for_plot+1)
        Label(self, textvariable=self.Load_str).grid(sticky=N+W, row=4, column=cols_for_plot+2)

        self.Load_slider = Scale(self, from_=-self.limit_load, to=self.limit_load, orient=HORIZONTAL, value =self.force_default,
                                   length = self.slider_length, command=self.update_values)
        self.Load_slider.grid(sticky=NW, row=5, column=cols_for_plot+1, columnspan=2)

        # Angle
        Label(self, text="Angle alpha (deg):").grid(sticky=NW, row=6, column=cols_for_plot+1)
        Label(self, textvariable=self.Angle_str).grid(sticky=NW, row=6, column=cols_for_plot+2)

        self.Angle_slider = Scale(self, from_=-self.limit_angle, to=self.limit_angle, orient=HORIZONTAL, value=self.angle_default,
                        length = self.slider_length, command=self.update_values)
        self.Angle_slider.grid(sticky=NW, row=7, column=cols_for_plot+1, columnspan=2)

        ##---------------------------------------------------------------------------------
        # Torsion input
        Label(self, text="Load T (Nm):").grid(sticky=N + W, row=8, column=cols_for_plot + 1)
        Label(self, textvariable=self.Torsion_str).grid(sticky=N + W, row=8, column=cols_for_plot + 2)

        self.Torsion_slider = Scale(self, from_=-self.limit_torsion, to=self.limit_torsion, orient=HORIZONTAL,
                                 value=self.torsion_default,
                                 length=self.slider_length, command=self.update_values)
        self.Torsion_slider.grid(sticky=NW, row=9, column=cols_for_plot + 1, columnspan=2)

        ##---------------------------------------------------------------------------------
        # Dimensions

        # height
        Label(self, text="height h (mm):").grid(sticky=NW, row=10, column=cols_for_plot + 1)
        Label(self, textvariable=self.height_str).grid(sticky=NW, row=10, column=cols_for_plot + 2)
        self.height_slider = Scale(self, from_=1, to=self.limit_wh, orient=HORIZONTAL, value=self.height_default,
                                  length=self.slider_length, command=self.update_values)
        self.height_slider.grid(sticky=NW, row=11, column=cols_for_plot + 1, columnspan=2)

        # width
        Label(self, text="width w (mm):").grid(sticky=NW, row=12, column=cols_for_plot + 1)
        Label(self, textvariable=self.width_str).grid(sticky=NW, row=12, column=cols_for_plot + 2)
        self.width_slider = Scale(self, from_=1, to=self.limit_wh, orient=HORIZONTAL, value=self.width_default,
                                   length=self.slider_length, command=self.update_values)
        self.width_slider.grid(sticky=NW, row=13, column=cols_for_plot + 1, columnspan=2)

        # length
        Label(self, text="length l (mm):").grid(sticky=NW, row=14, column=cols_for_plot + 1)
        Label(self, textvariable=self.length_str).grid(sticky=NW, row=14, column=cols_for_plot + 2)
        self.length_slider = Scale(self, from_=1, to=self.limit_l, orient=HORIZONTAL,value=self.length_default,
                                  length=self.slider_length, command=self.update_values)
        self.length_slider.grid(sticky=NW, row=15, column=cols_for_plot + 1, columnspan=2)


        ##---------------------------------------------------------------------------------
        # Output
        lbl5 = Label(self, text="Output:",font='Helvetica 14 bold')
        lbl5.grid(sticky=NW, row=output_row_start, column=cols_for_plot+1)

        lbl6 = Label(self, text="von Mises stress \u03C3 (N/mm^2):")
        lbl6.grid(sticky=NW, row=output_row_start+1, column=cols_for_plot+1)

        lbl7 = Label(self, textvariable=self.vonMises_str)# #text="1.0")
        lbl7.grid(sticky=NW, row=output_row_start+1, column=cols_for_plot+2)

        lbl8 = Label(self, text="von Mises FoS:")
        lbl8.grid(sticky=NW, row=output_row_start+2, column=cols_for_plot+1)

        lbl9 = Label(self, textvariable=self.vonMisesFoS_str)  # #text="1.0")
        lbl9.grid(sticky=NW, row=output_row_start+2, column=cols_for_plot+2)

        ##
        # Tresca output
        lbl10 = Label(self, text="Tresca stress \u03C4 (N/mm^2):")
        lbl10.grid(sticky=NW, row=output_row_start+3, column=cols_for_plot+1)

        lbl11 = Label(self, textvariable=self.Tresca_str)  # #text="1.0")
        lbl11.grid(sticky=NW, row=output_row_start+3, column=cols_for_plot+2)

        lbl12 = Label(self, text="Tresca FoS:")
        lbl12.grid(sticky=NW, row=output_row_start+4, column=cols_for_plot+1)

        lbl13 = Label(self, textvariable=self.Tresca_FoS_str)
        lbl13.grid(sticky=NW, row=output_row_start+4, column=cols_for_plot+2)

        Label(self, text="press 'd' for details ",font='Helvetica 12').grid(sticky=NW, row=output_row_start + 5,
                                            column=cols_for_plot+1, columnspan=2)


        cbtn = Button(self, text="Exit", command=self.quit)
        cbtn.grid(row=rows_for_plot+1, column=cols_for_plot+2, pady=4)


        check0 = Checkbutton(self, text="von Mises", variable=self.cb_mises, command=self.cb_update)
        check0.grid(row=rows_for_plot+1,  column=cols_for_plot-2, sticky=W)

        check1 = Checkbutton(self, text="Tresca", variable=self.cb_tresca, command=self.cb_update)
        check1.grid(row=rows_for_plot+1, column=cols_for_plot-1, sticky=W)

        Label(self, text="press 'e' for manual input.", font='Helvetica 12').grid(row=rows_for_plot+1, column=0, sticky=W, padx=7)


        # Load and init the image
        tk.Label(self, image=self.example.getImage(), height = 120, width=300).grid(sticky=SW, row=rows_for_plot,
                                                                   padx=0, pady = 0, column=cols_for_plot+1, columnspan=2)


def main():
    root = Tk()
    root.geometry("960x720+300+300")
    app = DuctileMaterial_FailureTheory_02()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()