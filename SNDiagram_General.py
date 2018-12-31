
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
from tkinter import Canvas, messagebox
from tkinter import Tk, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Scale, Checkbutton, Combobox
import tkinter as tk

# for images
from PIL import Image, ImageTk

# failure theory implementation
from ME325Common.FailureTheories import *

# import the example
from ME325Common.ExampleBeamRound import *

# import plot
from ME325Common.PlotHelpers import *
from ME325Common.DynamicLoadTheories import *
from ME325Common.InputHelpers import DataEntryMenu


class LogScale(Scale):


    def __init__(self):
        super().__init__()




class SDDiagram_General(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    #limits
    limit_yieldstress = 200 # kpsi
    limit_fatigue_strength = 160 # kpsi
    limit_lifetime = 1E10 # iterations

    # log axis
    limit_lifetime_slider = 18421 # lifetime is exp( slider_value / 1000) = 1E7

    # defaults
    default_fatigue_strength = 50 # N
    default_lifetime = 10000
    default_ut_strength = 110
    default_yield_strength = 95
    default_endurance_strength = 40
    default_endurance_limit = 1E7
    default_low_cycle_limit = 1E2

    # strength
    yield_strength_var = 0
    ut_strength_var = 0
    endurance_strength_var = 0
    endurance_limit_var = 0
    low_cycle_var = 0

    sndata = 0

    # combo box
    combo = 0
    combobox_str = ["Lifetime", "Fatigue strength"]

    fatigue_strength_str = 0
    fatigue_strength_var = 0
    fatigue_strength_slider = None
    liftime_str = 0
    liftime_var = 0
    liftime_slider = None
    out_fatigue_strength_str = 0
    out_liftime_str = 0

    slider_length = 260

    # canvas
    canvas = 0

    # the plot
    plot = None

    # output values
    life_out = 0
    sf_out = 0

    __menu = 0

    def __init__(self):
        super().__init__()

        self.yield_strength_var = DoubleVar()
        self.ut_strength_var = DoubleVar()
        self.endurance_strength_var = DoubleVar()
        self.endurance_limit_var = DoubleVar()
        self.low_cycle_var = DoubleVar()
        self.yield_strength_var.set(self.default_yield_strength)
        self.ut_strength_var.set(self.default_ut_strength)
        self.endurance_strength_var.set(self.default_endurance_strength)
        self.endurance_limit_var.set(self.default_endurance_limit)
        self.low_cycle_var.set(self.default_low_cycle_limit)

        self.fatigue_strength_str = StringVar()
        self.fatigue_strength_str.set(str(self.default_fatigue_strength))
        self.liftime_str = StringVar()
        self.liftime_str.set(str(self.default_lifetime))

        self.fatigue_strength_var = DoubleVar()
        self.fatigue_strength_var.set(0)
        self.liftime_var = DoubleVar()
        self.liftime_var.set(0)

        self.out_fatigue_strength_str = StringVar()
        self.out_fatigue_strength_str.set("0")

        self.out_liftime_str = StringVar()
        self.out_liftime_str.set("0")


        self.sndata = SNData(self.default_ut_strength,
                             self.default_yield_strength,
                             self.default_endurance_strength,
                             self.default_low_cycle_limit,
                             self.default_endurance_limit)
        # init ui
        self.initUI()

        # update ui
        self.update_values(0.0)

        # init the manual entry menu
        self.__menu = DataEntryMenu(self.master, self.__manual_entry_callback)


    # ----------- Update the outputs ----------

    def update_plot(self):
        """
        Update the plot area
        :return:
        """
        # self.yield_strength_var
        # self.ut_strength_var
        # self.endurance_strength_var
        # self.low_cycle_var
        # self.endurance_limit_var

        c = self.combo.get()

        if c == self.combobox_str[0]:
            Sf_target =float(self.fatigue_strength_var.get())
            N_current = SNDiagram.ComputeMaxIterations(Sf_target, self.sndata)

            # check for limits
            Sf_target =  np.min([Sf_target, self.sndata.Sut])

            self.plot.update_plot(self.sndata.Sut, self.sndata.Sy, self.sndata.Se, self.sndata.Nlow,
                                  self.sndata.Nend, N_current, Sf_target)
            self.life_out= N_current + 1
            self.sf_out = Sf_target

        else:
            N_target = float(self.liftime_var.get())
            N_target = np.exp(N_target/1000)

            Sf_current = SNDiagram.ComputeFatigueStrength(N_target, self.sndata)
            self.plot.update_plot(self.sndata.Sut, self.sndata.Sy, self.sndata.Se, self.sndata.Nlow,
                                  self.sndata.Nend, N_target, Sf_current)

            self.life_out = N_target
            self.sf_out = round(Sf_current,2)

        # Update the plot
        self.canvas.draw_idle()

    def update_output_display(self):
        """
        Update the output display, the stresses and factor of safeties this
        panel shows.
        :return:
        """

        self.out_fatigue_strength_str.set(self.sf_out)

        if self.life_out < self.sndata.Nend:
            self.out_liftime_str.set(int(self.life_out))
        else:
            self.out_liftime_str.set("Infinite Life")


        return


    # ---------Widget callbacks ---------------

    def update_values(self, val):
        """
        Update function for all widgets. The function updates the
        input values. Note that all slider widgets call this functions
        :param val: The value the widget passes
        :return: -
        """
        sy = float(self.yield_strength_var.get())
        sut = float(self.ut_strength_var.get())
        se = float(self.endurance_strength_var.get())
        nlcc = float(self.low_cycle_var.get())
        ninv = float(self.endurance_limit_var.get())

        self.sndata.set(sut, sy, se, nlcc, ninv)

        self.fatigue_strength_var.set(round(self.fatigue_strength_slider.get(),2))
        self.fatigue_strength_str.set(str(self.fatigue_strength_var.get()))

        self.liftime_var.set(round(self.liftime_slider.get(), 6))

        LogN = float(self.liftime_var.get())
        LogN = np.exp(LogN / 1000)

        self.liftime_str.set(str(int(LogN)))

        self.update_plot()
        self.update_output_display()


    def use_manual_entry_values(self):

        try:
            # check for limits
            sy = float(self.yield_strength_var.get())
            sut = float(self.ut_strength_var.get())
            se = float(self.endurance_strength_var.get())
            nlcc = float(self.low_cycle_var.get())
            ninv = float(self.endurance_limit_var.get())

            sut = np.max([1, np.min([sut, self.limit_fatigue_strength])])
            sy = np.max([1, np.min([sy, sut - 1])])
            se = np.max([1, np.min([se, sy - 1])])

            ninv = np.max([nlcc + 1, np.min([ninv, 1E7])])
            nlcc = np.max([  1, np.min([nlcc, ninv-1])])

            self.yield_strength_var.set(round(sy,2))
            self.ut_strength_var.set(round(sut,2))
            self.endurance_strength_var.set(round(se,2))
            self.low_cycle_var.set(int(nlcc))
            self.endurance_limit_var.set(int(ninv))


            # update values
            self.update_values(0)
        except ValueError:
            print("Something went wrong - invalid numbers")




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
            self.__create_subwindow()
        elif event.char == 'd':
            return


    def combobox_callback(self, event):
        #swap the sliders
        c = self.combo.get()
        if c ==  self.combobox_str[0]:
            self.liftime_slider.state(["disabled"])
            self.fatigue_strength_slider.state(["!disabled"])
            self.__menu.set_readonly(self.combobox_str[0])
        else:
            self.liftime_slider.state(["!disabled"])
            self.fatigue_strength_slider.state(["disabled"])
            self.__menu.set_readonly(self.combobox_str[1])


    def __manual_entry_callback(self):

        try:
            d = self.__menu.get() # returns a dictionary

            lt = d[self.combobox_str[0]].get() # lifetime
            fs = d[self.combobox_str[1]].get() # fatigue strength

            log_lt = 1

            # check for limits
            c = self.combo.get()
            if c == self.combobox_str[0]:
                fs = np.max([1, np.min([float(fs), self.limit_fatigue_strength])])
                self.fatigue_strength_slider.set(fs)
            else:
                log_lt = np.log(float(lt)) * 1000 # the value limit_lifetime_slider is x 1000
                #log_lt = np.max([1, np.min([log_lt, self.limit_lifetime_slider])]) too many rounding errors, thus, if...
                if log_lt < 1 or log_lt >  self.limit_lifetime_slider:
                    log_lt = np.max([1, np.min([log_lt, self.limit_lifetime_slider])])
                    lt = int(np.exp(log_lt / 1000))
                self.liftime_slider.set(log_lt)



            d = {self.combobox_str[0]: str(lt),
                 self.combobox_str[1]: fs}
            self.__menu.set(d)


            self.update_values(0)

        except ValueError:
            print("Something went wrong - values do not match")



    # ------------ Inits ---------------

    def __create_subwindow(self):
        """
        Create a window that allows a user to manually enter all the values
        instead of using sliders
        :return:
        """
        self.__menu.create("Enter data:", self.combobox_str)
        d = {self.combobox_str[0] : self.liftime_str.get(),
             self.combobox_str[1] : self.fatigue_strength_str.get()}
        self.__menu.set(d)

        c = self.combo.get()
        if c == self.combobox_str[0]:
            self.__menu.set_readonly(self.combobox_str[0])
        else:
            self.__menu.set_readonly(self.combobox_str[1])



    def create_plot(self):
        """
        Create the plot that shows the diagram
        :return:
        """
        self.plot = SNDiagramPlot()
        fig = self.plot.create_plot(9, 6)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()


    def initUI(self):
        """
        Init the user interface and all widgets
        :return: -
        """
        rows_for_plot = 24
        cols_for_plot = 4
        output_row_start = 13

        self.master.title("ME 325 Machine Component Design")
        self.pack(fill=BOTH, expand=True)

        # keyboard binding
        self.master.bind("e", self.key_callback)
        self.master.bind("d", self.key_callback)

        self.columnconfigure(0, weight=1) # first and last column can expand
        self.columnconfigure(0, pad=7)
        self.rowconfigure(rows_for_plot, weight=1)
        self.rowconfigure(rows_for_plot, pad=7)

        lbl = Label(self, text="Load-Life (SN)-Diagram")
        lbl.grid(sticky=W, pady=4, padx=5)

        #area = Text(self)
        # area.grid(row=1, column=0, columnspan=3, rowspan=10,
        #          padx=5, sticky=E + W + S + N)
        self.canvas = Canvas(self, width=450, height=300)
        self.create_plot()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=cols_for_plot, rowspan=rows_for_plot,
                         padx=5, sticky=E + W + S + N)

        lbl0 = Label(self, text="Input:",font='Helvetica 14 bold')
        lbl0.grid(sticky=NW, row=1, column=cols_for_plot+1)

        ##---------------------------------------------------------------------------------
        #  strength

        Label(self, text="Ult. tensile strength (kpsi):").grid(sticky=W, row=2, column=cols_for_plot + 1)
        Entry(self, textvariable=self.ut_strength_var,  width=15).grid(sticky=NW, row=2, column=cols_for_plot + 2)
        Label(self, text="Yield strength (kpsi):").grid(sticky=W, row=3, column=cols_for_plot+1)
        Entry(self, textvariable=self.yield_strength_var,  width=15).grid(sticky=NW, row=3, column=cols_for_plot+2)
        Label(self, text="Endurance strength (kpsi):").grid(sticky=W, row=4, column=cols_for_plot + 1)
        Entry(self, textvariable=self.endurance_strength_var,  width=15).grid(sticky=NW, row=4, column=cols_for_plot + 2)
        Label(self, text="Low cycle limit (N):").grid(sticky=W, row=5, column=cols_for_plot + 1)
        Entry(self, textvariable=self.low_cycle_var,  width=15).grid(sticky=NW, row=5, column=cols_for_plot + 2)
        Label(self, text="Endurance limit (N):").grid(sticky=W, row=6, column=cols_for_plot + 1)
        Entry(self, textvariable=self.endurance_limit_var, state="disabled",  width=15).grid(sticky=NW, row=6, column=cols_for_plot + 2)

        Button(self, text="Use", command=self.use_manual_entry_values).grid(row=7, column=cols_for_plot + 2, pady=4, sticky=W)

        ##---------------------------------------------------------------------------------
        # INPUT
        # Fatigue strength

        Label(self, text="Search for (output):").grid(sticky=W, row=8, column=cols_for_plot + 1)
        self.combo = Combobox(self, values=self.combobox_str, state='readonly',  width=15)
        self.combo.grid(sticky=NW, row=8, column=cols_for_plot + 2, columnspan = 1)
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.combobox_callback)


        Label(self, text="Fatigue strength Sf (kpsi):").grid(sticky=N+W, row=9, column=cols_for_plot+1)
        Label(self, textvariable=self.fatigue_strength_str).grid(sticky=N+W, row=9, column=cols_for_plot+2)
        self.fatigue_strength_slider = Scale(self, from_=1, to=self.limit_fatigue_strength, orient=HORIZONTAL,
                                             value =self.default_fatigue_strength,
                                              length = self.slider_length, command=self.update_values)
        self.fatigue_strength_slider.grid(sticky=NW, row=10, column=cols_for_plot+1, columnspan=2)

        # Lifetime
        Label(self, text="Lifetime (N):").grid(sticky=NW, row=11, column=cols_for_plot+1)
        Label(self, textvariable=self.liftime_str).grid(sticky=NW, row=11, column=cols_for_plot+2)
        self.liftime_slider = Scale(self, from_=1, to=self.limit_lifetime_slider, orient=HORIZONTAL, value=self.default_lifetime,
                        length = self.slider_length, command=self.update_values)
        self.liftime_slider.grid(sticky=NW, row=12, column=cols_for_plot+1, columnspan=2)
        self.liftime_slider.state(["disabled"])

        ##---------------------------------------------------------------------------------
        # OUTPUT
        Label(self, text="Output:",font='Helvetica 14 bold').grid(sticky=NW, row=output_row_start, column=cols_for_plot+1)
        Label(self, text="Fatigue strength \u03C3_f (kpsi):").grid(sticky=NW, row=output_row_start+1, column=cols_for_plot+1)
        Label(self, textvariable=self.out_fatigue_strength_str).grid(sticky=NW, row=output_row_start+1, column=cols_for_plot+2)
        Label(self, text="Lifetime (N):").grid(sticky=NW, row=output_row_start+2, column=cols_for_plot+1)
        Label(self, textvariable=self.out_liftime_str).grid(sticky=NW, row=output_row_start+2, column=cols_for_plot+2)

        Label(self, text="Rounding errors may affect the lifetime +/- 1", font='Helvetica 12').grid(sticky=NW, row=output_row_start + 3,
                                                                       column=cols_for_plot+1, columnspan=2)
        #Label(self, text="press 'd' for details ",font='Helvetica 12').grid(sticky=NW, row=output_row_start + 3,
         #                                   column=cols_for_plot+1, columnspan=2)

        cbtn = Button(self, text="Exit", command=self.quit)
        cbtn.grid(row=rows_for_plot+2, column=cols_for_plot+2, pady=4, sticky=E)

        #check0 = Checkbutton(self, text="von Mises", variable=self.cb_mises, command=self.cb_update)
        #check0.grid(row=rows_for_plot+1,  column=cols_for_plot-2, sticky=W)

        #check1 = Checkbutton(self, text="Tresca", variable=self.cb_tresca, command=self.cb_update)
        #check1.grid(row=rows_for_plot+1, column=cols_for_plot-1, sticky=W)

        Button(self, text="Save", command=self.__save_plot).grid(row=rows_for_plot+2, column=cols_for_plot-1, pady=4,
                                                                            sticky=E)

        Label(self, text="press 'e' for manual input.", font='Helvetica 12').grid(row=rows_for_plot+2, column=0, sticky=W, padx=7)



    def __save_plot(self):
        p = self.plot.save_plot()
        messagebox.showinfo("Save Plot", str("Saved the plot as: " + p ))


def main():
    root = Tk()
    root.geometry("1024x720+300+300")
    app = SDDiagram_General()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()