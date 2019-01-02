
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
from ME325Common.PlotHelpers import *
from ME325Common.ContinuumMechanics import *
from ME325Common.UnitConversion import *

class MohrsCircle2D(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    # limits
    limit_stress = 1000

    # default values
    default_stress = 50



    # canvas
    __canvas = 0

    # Tresca and Mises plot
    __the_plot  = None
    __show_helpers = True

    slider_length = 220

    # dicts
    __labels = {}
    __sliders = {}
    __output = {}

    __results = {}

    # variables
    __var = {}

    # checkbox
    __checkbox_helpers = 0
    __combo = 0

    combobox_str = ["SI", "USCS"]
    __unit_str = "(N/mm^2)"

    #submenu
    menu = None
    entry_items = ["\u03C3_x", "\u03C3_y", "\u03C4_xy"]


    def __init__(self):
        super().__init__()


        # the plot
        self.__the_plot = MohrsCirclePlot()

        # init ui
        self.initUI()

        # menu
        self.menu = MohrsCircle2DDetails(self.master, self.manual_entry_callback)

        # update ui
        self.update_values(0.0)




    # ----------- Update the outputs ----------

    def update_plot(self):
        """
        Update the plot area
        :return:
        """

        sx = self.__var["sx"].get()
        sy = self.__var["sy"].get()
        txy = self.__var["txy"].get()

        s1 = self.__results["s1"]
        s2 = self.__results["s2"]
        a1 = self.__results["a1"]
        a2 = self.__results["a2"]
        t1 = self.__results["t1"]
        t2 = self.__results["t2"]

        # Update the plot
        self.__the_plot.update_plot(sx, sy, txy)
        self.__the_plot.update_helpers(s1, s2, a1, a2, t1, t2, self.__show_helpers)
        self.__canvas.draw_idle()


        self.menu.update_plot(s1, s2, a1)


    def update_output_display(self):
        """
        Update the output display, the stresses and factor of safeties this
        panel shows.
        :return:
        """

        self.__var["s1"].set(str(round(self.__results["s1"],2)))
        self.__var["s2"].set(str(round(self.__results["s2"],2)))
        self.__var["tmax"].set(str(round(abs(self.__results["t1"]), 2)))
        self.__var["a1"].set(str(round(self.__results["a1"], 2)))
        self.__var["a2"].set(str(round(self.__results["a2"], 2)))

        return


    # ---------Widget callbacks ---------------

    def update_values(self, val):
        """
        Update function for all widgets. The function updates the
        input values. Note that all slider widgets call this functions
        :param val: The value the widget passes
        :return: -
        """

        self.__var["sx"].set( round(self.__sliders["sx"].get(),2))
        self.__var["sx_str"].set(str(self.__var["sx"].get()))

        self.__var["sy"].set(round(self.__sliders["sy"].get(), 2))
        self.__var["sy_str"].set(str(self.__var["sy"].get()))

        self.__var["txy"].set(round(self.__sliders["txy"].get(), 2))
        self.__var["txy_str"].set(str(self.__var["txy"].get()))

        sx = self.__var["sx"].get()
        sy = self.__var["sy"].get()
        txy = self.__var["txy"].get()

        # Calculate new results
        s1, s2 = calcPrincipalStress(sx, sy, txy)
        a1, a2 = calcPrincipalAngles(sx, sy, txy)
        t1, t2 = calcMaxShearStress(sx, sy, txy)

        self.__results["s1"] = s1
        self.__results["s2"] = s2

        if sx >= sy:
            self.__results["a1"] = a1
            self.__results["a2"] = a2
        else:
            self.__results["a1"] = a2
            self.__results["a2"] = a1
        self.__results["t1"] = t1
        self.__results["t2"] = t2


        self.update_plot()
        self.update_output_display()

    def cb_update(self):
        """
        Checkbox update. Captures the ckeckbox clicks.
        Checkboxes do not pass any arguments to the function
        :return:
        """
        #self.failure_theory_plts.showVonMisesPlt(int(self.cb_mises.get()))
        #self.failure_theory_plts.showTrescaPlt(int(self.cb_tresca.get()))


        if self.__checkbox_helpers.get() == 1:
            self.__show_helpers = True
        else:
            self.__show_helpers = False


        self.update_values(0)

    def key_callback(self, event):
        """
        Create a subwindow to allow for user input
        :param event:
        :return:
        """
        if event.char == 'e':
            self.create_subUI()
        elif event.char == 'd':
            return


    def manual_entry_callback(self):
        """
        Apply the values that the user set in the sub window
        :return:
        """

        try:

            d = self.menu.get()

            self.__sliders["sx"].set(float(d[self.entry_items[0]].get()))
            self.__sliders["sy"].set(float(d[self.entry_items[1]].get()))
            self.__sliders["txy"].set(float(d[self.entry_items[2]].get()))

            # get values
            self.update_values(0)
        except ValueError:
            print("Something went wrong - invalid numbers")
        except KeyError:
            print("Something went wrong - wrong key")



    def __combobox_callback(self, event):
        c = self.__combo.get()
        self.__change_unit(c)
        self.update()



    def __save_plot(self):
        try:
            p = self.__the_plot.save_plot()
            messagebox.showinfo("Save Plot", str("Saved the plot as: " + p))
        except:
            pass
        try:
            self.menu.save_plot()
        except:
            pass




    def __change_unit(self, unit):
        if unit == self.combobox_str[0]: # change to si units
            self.__unit_str = "(N/mm^2)"
            self.__the_plot.set_unit(0)

            self.__sliders["sx"].configure(from_=-self.limit_stress, to=self.limit_stress)
            self.__sliders["sy"].configure(from_=-self.limit_stress, to=self.limit_stress)
            self.__sliders["txy"].configure(from_=-self.limit_stress, to=self.limit_stress)

            self.__sliders["sx"].set(UnitConversion.psi_to_Nmm2(self.__var["sx"].get()) * 1000)
            self.__sliders["sy"].set(UnitConversion.psi_to_Nmm2(self.__var["sy"].get()) * 1000)
            self.__sliders["txy"].set(UnitConversion.psi_to_Nmm2(self.__var["txy"].get()) * 1000)

            #d = {self.entry_items[0]: UnitConversion.psi_to_Nmm2(self.__var["sx"].get()) * 1000,
            #     self.entry_items[1]: UnitConversion.psi_to_Nmm2(self.__var["sy"].get()) * 1000,
            #     self.entry_items[2]: UnitConversion.psi_to_Nmm2(self.__var["txy"].get()) * 1000}
            #self.menu.set(d)

        else: # change to uscs units
            self.__unit_str = "(ksi)"
            self.__the_plot.set_unit(1)

            self.__sliders["sx"].configure(from_=-UnitConversion.Nmm2_to_psi(self.limit_stress / 1000),
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["sx"].set(UnitConversion.Nmm2_to_psi(self.__var["sx"].get()) / 1000)

            self.__sliders["sy"].configure(from_=-UnitConversion.Nmm2_to_psi(self.limit_stress / 1000),
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["sy"].set(UnitConversion.Nmm2_to_psi(self.__var["sy"].get()) / 1000)

            self.__sliders["txy"].configure(from_=-UnitConversion.Nmm2_to_psi(self.limit_stress / 1000),
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["txy"].set(UnitConversion.Nmm2_to_psi(self.__var["txy"].get()) / 1000)

            #d = {self.entry_items[0]: UnitConversion.Nmm2_to_psi(self.__var["sx"].get()) / 1000,
            #     self.entry_items[1]: UnitConversion.Nmm2_to_psi(self.__var["sy"].get()) / 1000,
            #     self.entry_items[2]: UnitConversion.Nmm2_to_psi(self.__var["txy"].get()) / 1000}
            #self.menu.set(d)



        self.__labels["sx"].configure(text=str("\u03C3_x " + self.__unit_str + ":"))
        self.__labels["sy"].configure(text=str("\u03C3_y " + self.__unit_str + ":"))
        self.__labels["txy"].configure(text=str("\u03C4_xy " + self.__unit_str + ":"))
        self.__labels["s1"].configure(text=str("\u03C3_1 " + self.__unit_str + ":"))
        self.__labels["s2"].configure(text=str("\u03C3_3 " + self.__unit_str + ":"))
        self.__labels["tmax"].configure(text=str("\u03C4_max " + self.__unit_str + ":"))
        self.__canvas.draw_idle()





    # ------------ Inits ---------------

    def create_subUI(self):
        """
        Create a window that allows a user to manually enter all the values
        instead of using sliders
        :return:
        """
        try:
            display_items = []
            self.menu.create_menu("Enter data", self.entry_items, None)
            d = {self.entry_items[0]: self.__var["sx"].get(),
                 self.entry_items[1]: self.__var["sy"].get(),
                 self.entry_items[2]: self.__var["txy"].get()}
            self.menu.set(d)

            s1 = self.__results["s1"]
            s2 = self.__results["s2"]
            a1 = self.__results["a1"]

            self.menu.update_plot(s1, s2, a1)
        except ValueError:
            print("Something went wrong")




    def create_plot(self):
        """
        Create the plot that shows the failure theories
        :return:
        """
        fig = self.__the_plot.create_plot(8) # 9 -> figure size
        self.__canvas = FigureCanvasTkAgg(fig, master=self)
        self.__canvas.draw()


    def initUI(self):
        """
        Init the user interface and all widgets
        :return: -
        """
        rows_for_plot = 24
        cols_for_plot = 5
        output_row_start = 14

        self.master.title("ME 325 Machine Component Design")
        self.pack(fill=BOTH, expand=True)

        # keyboard binding
        self.master.bind("e", self.key_callback)
        self.master.bind("d", self.key_callback)

        self.columnconfigure(0, weight=1) # first and last column can expand
        self.columnconfigure(0, pad=7)
        self.rowconfigure(rows_for_plot, weight=1)
        self.rowconfigure(rows_for_plot, pad=7)

        lbl = Label(self, text="Mohr's Circle for plane materials")
        lbl.grid(sticky=W, pady=4, padx=5)

        self.__canvas = Canvas(self, width=300, height=300)
        self.create_plot()
        self.__canvas.get_tk_widget().grid(row=1, column=0, columnspan=cols_for_plot, rowspan=rows_for_plot,
                         padx=5, sticky=E + W + S + N)


        Label(self, text="Input:",font='Helvetica 14 bold').grid(sticky=NW, row=1, column=cols_for_plot+1)

        #-----------
        # sx
        self.__labels["sx"] = Label(self, text=str("\u03C3_x "+self.__unit_str + ":"), width=13)
        self.__labels["sx"].grid(sticky=W, row=2, column=cols_for_plot+1)

        self.__var["sx_str"] = StringVar()
        self.__var["sx_str"].set(str(self.default_stress))

        self.__var["sx"] = DoubleVar()
        self.__var["sx"].set(self.default_stress)

        self.__output["sx"] = Label(self, textvariable=self.__var["sx_str"], width=15)
        self.__output["sx"].grid(sticky=W, row=2, column=cols_for_plot+2)

        self.__sliders["sx"] = Scale(self, value=self.default_stress, from_=-self.limit_stress,
                                        to=self.limit_stress,orient=HORIZONTAL,
                                        length=self.slider_length, command=self.update_values)
        self.__sliders["sx"].grid(sticky=W, row=3, column=cols_for_plot+1, columnspan=2)

        ##---------------------------------------------------------------------------------
        # sy
        self.__labels["sy"] = Label(self, text=str("\u03C3_y "+self.__unit_str + ":"))
        self.__labels["sy"].grid(sticky=W, row=4, column=cols_for_plot + 1)

        self.__var["sy_str"] = StringVar()
        self.__var["sy_str"].set(str("-" + str(self.default_stress)))

        self.__var["sy"] = DoubleVar()
        self.__var["sy"].set(-self.default_stress)

        self.__output["sy"] = Label(self, textvariable=self.__var["sy_str"])
        self.__output["sy"].grid(sticky=W, row=4, column=cols_for_plot + 2)

        self.__sliders["sy"] = Scale(self, value=-self.default_stress, from_=-self.limit_stress,
                                     to=self.limit_stress, orient=HORIZONTAL,
                                     length=self.slider_length, command=self.update_values)
        self.__sliders["sy"].grid(sticky=W, row=5, column=cols_for_plot + 1, columnspan=2)

        ##---------------------------------------------------------------------------------
        # t_xy
        self.__labels["txy"] = Label(self, text=str("\u03C4_xy "+self.__unit_str + ":"))
        self.__labels["txy"].grid(sticky=W, row=6, column=cols_for_plot + 1)

        self.__var["txy_str"] = StringVar()
        self.__var["txy_str"].set(str(self.default_stress/2))

        self.__var["txy"] = DoubleVar()
        self.__var["txy"].set(self.default_stress/2)

        self.__output["txy"] = Label(self, textvariable=self.__var["txy_str"])
        self.__output["txy"].grid(sticky=W, row=6, column=cols_for_plot + 2)

        self.__sliders["txy"] = Scale(self, value=self.default_stress/2, from_=-self.limit_stress,
                                     to=self.limit_stress, orient=HORIZONTAL,
                                     length=self.slider_length, command=self.update_values)
        self.__sliders["txy"].grid(sticky=W, row=7, column=cols_for_plot + 1, columnspan=2)



        ##---------------------------------------------------------------------------------
        # Output
        Label(self, text="Output:",font='Helvetica 14 bold').grid(sticky=NW, row=output_row_start, column=cols_for_plot+1)


        # s1
        self.__labels["s1"] = Label(self, text=str("\u03C3_1 "+self.__unit_str + ":"))
        self.__labels["s1"].grid(sticky=W, row=output_row_start+1, column=cols_for_plot + 1)

        self.__var["s1"] = StringVar()
        self.__var["s1"].set("0")

        self.__output["s1"] = Label(self, textvariable=self.__var["s1"])
        self.__output["s1"].grid(sticky=W, row=output_row_start + 1, column=cols_for_plot + 2)

        # s2
        self.__labels["s2"] = Label(self, text=str("\u03C3_3 "+self.__unit_str + ":"))
        self.__labels["s2"].grid(sticky=W, row=output_row_start + 2, column=cols_for_plot + 1)

        self.__var["s2"] = StringVar()
        self.__var["s2"].set("0")

        self.__output["s2"] = Label(self, textvariable=self.__var["s2"])
        self.__output["s2"].grid(sticky=W, row=output_row_start + 2, column=cols_for_plot + 2)

        # angle 1
        self.__labels["a1"] = Label(self, text="\u03B8_x (deg):")
        self.__labels["a1"].grid(sticky=W, row=output_row_start + 3, column=cols_for_plot + 1)

        self.__var["a1"] = StringVar()
        self.__var["a1"].set("0")

        self.__output["a1"] = Label(self, textvariable=self.__var["a1"])
        self.__output["a1"].grid(sticky=W, row=output_row_start + 3, column=cols_for_plot + 2)

        # angle 2
        self.__labels["a2"] = Label(self, text="\u03B8_y (deg):")
        self.__labels["a2"].grid(sticky=W, row=output_row_start + 4, column=cols_for_plot + 1)

        self.__var["a2"] = StringVar()
        self.__var["a2"].set("0")

        self.__output["a2"] = Label(self, textvariable=self.__var["a2"])
        self.__output["a2"].grid(sticky=W, row=output_row_start + 4, column=cols_for_plot + 2)


        # tau max
        self.__labels["tmax"] = Label(self, text=str("\u03C4_max "+self.__unit_str + ":"))
        self.__labels["tmax"].grid(sticky=W, row=output_row_start + 5, column=cols_for_plot + 1)

        self.__var["tmax"] = StringVar()
        self.__var["tmax"].set("0")

        self.__output["tmax"] = Label(self, textvariable=self.__var["tmax"])
        self.__output["tmax"].grid(sticky=W, row=output_row_start + 5, column=cols_for_plot + 2)




        #Label(self, text="press 'd' for details ",font='Helvetica 12').grid(sticky=NW, row=output_row_start + 6,
        #                                    column=cols_for_plot+1, columnspan=2)

        ##---------------------------------------------------------------------------------
        # Others

        cbtn = Button(self, text="Exit", command=self.quit)
        cbtn.grid(row=rows_for_plot+1, column=cols_for_plot+2, pady=4, sticky=E)

        Button(self, text="Save", command=self.__save_plot).grid(row=rows_for_plot + 1, column=cols_for_plot+1,
                                                                 pady=4, sticky=W)


        self.__checkbox_helpers = IntVar()
        self.__checkbox_helpers.set(1)
        check1 = Checkbutton(self, text="Helpers", variable=self.__checkbox_helpers, command=self.cb_update)
        check1.grid(row=rows_for_plot+1, column=cols_for_plot-1, sticky=W)

        Label(self, text="press 'e' for manual input.", font='Helvetica 12').grid(row=rows_for_plot+1, column=0, sticky=W, padx=7)

        self.__combo = Combobox(self, values=self.combobox_str, state='readonly', width=6)
        self.__combo.grid(sticky=W, row=rows_for_plot+1, column=cols_for_plot-4, columnspan=1, padx=1, pady=0)
        self.__combo.current(0)
        self.__combo.bind("<<ComboboxSelected>>", self.__combobox_callback)




class MohrsCircle2DDetails():

    __toplevel = 0 # Toplevel window
    __event_callback = 0 # main window callback
    __window = None # This window


    __dict = {}  #dict with output data
    __entry_dict = {} # dict to store reference to all Entry widgets

    __plot = 0
    __canvas = 0

    def __init__(self, toplevel, event_callback):

        self.__toplevel = toplevel
        self.__event_callback = event_callback



    def create_menu(self, title, entry_items, display_items ):
        """

        :param entry_items: list with data to enter
        :param display_items: list with data to display
        :return:
        """

        cols_for_plot = 4
        rows_for_plot = 4

        self.__window = Toplevel(self.__toplevel )

        tk.Label(self.__window, text=title, background='white', font="Helvetica 14 bold").grid(sticky=NW, row=0,
                                                                                               column=0)
        n = len(entry_items)

        for i in range(n):
            self.__dict[entry_items[i]] = StringVar()
            tk.Label(self.__window, text=entry_items[i], background='white').grid(sticky=NW, row=i + 1, column=0)
            e = Entry(self.__window, textvariable=self.__dict[entry_items[i]], width=15)
            e.grid(sticky=NW, row=i + 1, column=1)
            self.__entry_dict[entry_items[i]] = e




        tk.Button(self.__window, text="Use", command=self.__event_callback,
                  background='white').grid(sticky=NE, row=n + 1, column=1, padx=7, pady=7)

        tk.Label(self.__window, text="Stress tensor", background='white', font="Helvetica 14 bold").grid(sticky=NW, row=n+2,
                                                                                               column=0)

        ## Create the plot

        plot_start_row = n+3


        self.__plot = CauchyStressPlanePlot()
        fig = self.__plot.create_plot(4)


        self.__canvas = FigureCanvasTkAgg(fig, master=self.__window )
        self.__canvas.get_tk_widget().grid(row=plot_start_row, column=0, columnspan=cols_for_plot, rowspan=rows_for_plot,
                                           padx=5, sticky=E + W + S + N)
        self.__canvas.draw()

        self.__window.columnconfigure(cols_for_plot-1, weight=1)  # first and last column can expand
        self.__window.columnconfigure(cols_for_plot-1, pad=7)
        self.__window.rowconfigure(plot_start_row, weight=1)
        self.__window.rowconfigure(plot_start_row, pad=7)

        tk.Button(self.__window, text="Close", command=self.__destroyed_callback,
                  background='white').grid(sticky=NW, row=plot_start_row+ rows_for_plot + 2, column=0, padx=7, pady=7)


        return


    def get(self):
        return self.__dict

    def set(self, items_dict):
        try:
            keys = items_dict.keys()
            n = len(keys)
            for key, value in items_dict.items():
                self.__dict[key].set(str(value))

        except ValueError:
            print("Something went wrong - invalid values")
        except  KeyError:
            return

    def set_readonly(self, readonly_key):

        for key, value in self.__entry_dict.items():
            if key == readonly_key:
                value.configure(state='disabled')
            else:
                value.configure(state='normal')

    def __destroyed_callback(self):
        self.__window.destroy()
        self.__window = None

    def save_plot(self):
        self.__plot.save_plot()

    def update_plot(self, s1, s2, a1):
        try:
            self.__plot.update_plot(s1, s2, a1)
            self.__canvas.draw_idle()
        except AttributeError:
            return


def main():
    root = Tk()
    root.geometry("900x720+300+300")
    app = MohrsCircle2D()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()