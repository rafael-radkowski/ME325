
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

from ME325Common.UnitConversion import *
from ME325Common.METypes import *
from ME325Common.DynamicLoadTheories import *
from ME325Common.InputHelpers import  *

class FatigueDiagram_General(Frame):
    """
    This class implements examples for two failure theories for ductile materials.
    See documentation
    """

    # limits
    limit_stress = 1000  # in MPa or N/mm2. Needs to be converted into ksi

    # default values
    default_Sut = 110
    default_Sy = 90
    default_Se = 35
    default_Sa = 20
    default_Sm = 30

    # canvas
    __canvas = 0

    # The plot
    __the_plot  = None

    slider_length = 200

    # dicts
    __labels = {}
    __sliders = {}
    __output = {}
    __checkboxes = {}

    __results = {}

    # variables
    __var = {}

    # checkbox
    __checkbox_helpers = 0
    __combo = 0

    __units = ["SI", "USCS"]
    __unit_str = "(N/mm^2)"

    #material
    __mat = None

    # recursion stop
    __rec = True

    #submenu
    menu = None
    entry_items = ["Sut", "Sy", "Se", "Sa", "Sm"]


    def __init__(self):
        super().__init__()

        self.__mat = DMaterialData(110, 95, 35)

        # the plot
        self.__the_plot = FatigueDiagramPlot()

        # init ui
        self.initUI()

        # menu
        self.menu = DataEntryMenu(self.master, self.manual_entry_callback)

        # update ui
        self.update_values(0.0)




    # ----------- Update the outputs ----------

    def update_plot(self):
        """
        Update the plot area
        :return:
        """

        self.__mat.Sut = self.__var["Sut"].get()
        self.__mat.Sy = self.__var["Sy"].get()
        self.__mat.Se = self.__var["Se"].get()
        Sa = self.__var["Sa"].get()
        Sm = self.__var["Sm"].get()

        # Update the plot
        self.__the_plot.update_plot(Sa, Sm, self.__mat)
        self.__canvas.draw_idle()


        #self.menu.update_plot(s1, s2, a1)


    def update_output_display(self):
        """
        Update the output display, the stresses and factor of safeties this
        panel shows.
        :return:
        """

        self.__var["n_Goodman"].set(str(round(self.__results["n_Goodman"],2)))
        self.__var["n_Sonderberg"].set(str(round(self.__results["n_Sonderberg"], 2)))
        self.__var["n_Gerber"].set(str(round(self.__results["n_Gerber"], 2)))



        return


    # ---------Widget callbacks ---------------

    def update_values(self, val):
        """
        Update function for all widgets. The function updates the
        input values. Note that all slider widgets call this functions
        :param val: The value the widget passes
        :return: -
        """
        # stops recursion when updating the slider at a different location
        if self.__rec == False:
            return

        self.__update_slider("Sut", 2)
        self.__update_slider("Sy", 2)
        self.__update_slider("Se", 2)
        self.__update_slider("Sa", 2)
        self.__update_slider("Sm", 2)

        Sut = self.__var["Sut"].get()
        Sy = self.__var["Sy"].get()
        Se = self.__var["Se"].get()
        Sa = self.__var["Sa"].get()
        Sm = self.__var["Sm"].get()

        # check for limits
        if Sut < Sy:
            self.__sliders["Sut"].set( Sy + 1)
        if Sy < Se:
            self.__sliders["Sy"].set(Se + 1)

        # calc results

        self.__results["n_Goodman"] = FatigueDiagram.calc_mod_Goodman_FoS(Sa, Sm, Se, Sut )
        self.__results["n_Sonderberg"] = FatigueDiagram.calc_Sonderberg_FoS(Sa, Sm, Se, Sy)
        self.__results["n_Gerber"] = FatigueDiagram.calc_Gerber_FoS(Sa, Sm, Se, Sut)




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

        self.__the_plot.set_helpers(self.__show_helpers)
        self.__canvas.draw_idle()

        #self.update_values(0)


    def cb2_update(self):
        visible = True
        if self.__checkboxes["Goodman"].get() != 1:
            visible = False
        self.__the_plot.set_visible(0, visible)

        visible = True
        if self.__checkboxes["Gerber"].get() != 1:
            visible = False
        self.__the_plot.set_visible(1, visible)

        visible = True
        if self.__checkboxes["Sonderberg"].get() != 1:
            visible = False
        self.__the_plot.set_visible(2, visible)

        visible = True
        if self.__checkboxes["Yield"].get() != 1:
            visible = False
        self.__the_plot.set_visible(3, visible)

        self.__canvas.draw_idle()



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

            self.__sliders["Sut"].set(float(d[self.entry_items[0]].get()))
            self.__sliders["Sy"].set(float(d[self.entry_items[1]].get()))
            self.__sliders["Se"].set(float(d[self.entry_items[2]].get()))
            self.__sliders["Sa"].set(float(d[self.entry_items[3]].get()))
            self.__sliders["Sm"].set(float(d[self.entry_items[4]].get()))

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

        self.__rec = False

        if unit == self.__units[0]: # change to si units
            self.__unit_str = "(N/mm^2)"
            self.__the_plot.set_units(0)

            self.__sliders["Sut"].configure(from_=0, to=self.limit_stress)
            self.__sliders["Sy"].configure(from_=0, to=self.limit_stress)
            self.__sliders["Se"].configure(from_=0, to=self.limit_stress)
            self.__sliders["Sa"].configure(from_=0, to=self.limit_stress)
            self.__sliders["Sm"].configure(from_=0, to=self.limit_stress)

            self.__sliders["Sut"].set(UnitConversion.psi_to_Nmm2(self.__var["Sut"].get()) * 1000)
            self.__sliders["Sy"].set(UnitConversion.psi_to_Nmm2(self.__var["Sy"].get()) * 1000)
            self.__sliders["Se"].set(UnitConversion.psi_to_Nmm2(self.__var["Se"].get()) * 1000)
            self.__sliders["Sa"].set(UnitConversion.psi_to_Nmm2(self.__var["Sa"].get()) * 1000)
            self.__sliders["Sm"].set(UnitConversion.psi_to_Nmm2(self.__var["Sm"].get()) * 1000)

        else: # change to uscs units
            self.__unit_str = "(ksi)"
            self.__the_plot.set_units(1)

            self.__sliders["Sut"].configure(from_=0, to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["Sut"].set(UnitConversion.Nmm2_to_psi(self.__var["Sut"].get()) / 1000)

            self.__sliders["Sy"].configure(from_=0,
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["Sy"].set(UnitConversion.Nmm2_to_psi(self.__var["Sy"].get()) / 1000)

            self.__sliders["Se"].configure(from_=0,
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["Se"].set(UnitConversion.Nmm2_to_psi(self.__var["Se"].get()) / 1000)

            self.__sliders["Sa"].configure(from_=0,
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["Sa"].set(UnitConversion.Nmm2_to_psi(self.__var["Sa"].get()) / 1000)

            self.__sliders["Sm"].configure(from_=0,
                                           to=UnitConversion.Nmm2_to_psi(self.limit_stress / 1000))
            self.__sliders["Sm"].set(UnitConversion.Nmm2_to_psi(self.__var["Sm"].get()) / 1000)


        self.__labels["Sut"].configure(text=str("Sut " + self.__unit_str + ":"))
        self.__labels["Sy"].configure(text=str("Sy " + self.__unit_str + ":"))
        self.__labels["Se"].configure(text=str("Se " + self.__unit_str + ":"))
        self.__labels["Sa"].configure(text=str("Sa " + self.__unit_str + ":"))
        self.__labels["Sm"].configure(text=str("Sm " + self.__unit_str + ":"))
        self.__canvas.draw_idle()

        self.__rec = True
        self.update_values(0)




    # ------------ Inits ---------------

    def create_subUI(self):
        """
        Create a window that allows a user to manually enter all the values
        instead of using sliders
        :return:
        """
        try:
            self.menu.create("Enter data", self.entry_items)

            d = {self.entry_items[0]: self.__var["Sut"].get(),
                 self.entry_items[1]: self.__var["Sy"].get(),
                 self.entry_items[2]: self.__var["Se"].get(),
                 self.entry_items[3]: self.__var["Sa"].get(),
                 self.entry_items[4]: self.__var["Sa"].get()}
            self.menu.set(d)

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
        # INPUT

        self.__add_slider("Sut", self.default_Sut, 0, self.limit_stress, 2, cols_for_plot)
        self.__add_slider("Sy", self.default_Sy, 0, self.limit_stress, 4, cols_for_plot)
        self.__add_slider("Se", self.default_Se, 0, self.limit_stress, 6, cols_for_plot)
        self.__add_slider("Sa", self.default_Sa, 0, self.limit_stress, 8, cols_for_plot)
        self.__add_slider("Sm", self.default_Sm, 0, self.limit_stress, 10, cols_for_plot)

        ##---------------------------------------------------------------------------------
        # OUTPUT
        Label(self, text="Output:",font='Helvetica 14 bold').grid(sticky=NW, row=output_row_start, column=cols_for_plot+1)

        # s1
        self.__add_label("n_Goodman", "n_Goodman", 0.0, output_row_start, cols_for_plot)
        self.__add_label("n_Gerber", "n_Gerber", 0.0, output_row_start+1, cols_for_plot)
        self.__add_label("n_Sonderberg", "n_Sonderberg", 0.0, output_row_start+2, cols_for_plot)

        ##---------------------------------------------------------------------------------
        # Display
        Label(self, text="Display:", font='Helvetica 14 bold').grid(sticky=NW, row=output_row_start+5,
                                                                   column=cols_for_plot + 1)

        self.__add_checkbox("Goodman", "Goodman line", output_row_start + 6, cols_for_plot + 1, self.cb2_update)
        self.__add_checkbox("Gerber", "Gerber line" , output_row_start+7, cols_for_plot + 1, self.cb2_update)
        self.__add_checkbox("Sonderberg", "Sonderberg line", output_row_start + 8, cols_for_plot + 1, self.cb2_update)
        self.__add_checkbox("Yield", "Yield stress", output_row_start + 9, cols_for_plot + 1, self.cb2_update)


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

        self.__combo = Combobox(self, values=self.__units, state='readonly', width=6)
        self.__combo.grid(sticky=W, row=rows_for_plot+1, column=cols_for_plot-4, columnspan=1, padx=1, pady=0)
        self.__combo.current(0)
        self.__combo.bind("<<ComboboxSelected>>", self.__combobox_callback)



    def __add_slider(self, name, default_value, min, max, row_, cols_):
        self.__labels[name] = Label(self, text=str(name + " " + self.__unit_str + ":"), width=15)
        self.__labels[name].grid(sticky=W, row=row_, column=cols_ + 1)

        self.__var[str(name + "_str")] = StringVar()
        self.__var[str(name + "_str")].set(str(default_value))

        self.__var[name] = DoubleVar()
        self.__var[name].set(default_value)

        self.__output[name] = Label(self, textvariable=self.__var[str(name + "_str")])
        self.__output[name].grid(sticky=W, row=row_, column=cols_ + 2)

        self.__sliders[name] = Scale(self, value=default_value, from_=min,
                                     to=max, orient=HORIZONTAL,
                                     length=self.slider_length, command=self.update_values)
        self.__sliders[name].grid(sticky=W, row=row_+1, column=cols_ + 1, columnspan=2)


    def __update_slider(self, name, round_):
        try:
            # update value
            self.__var[name].set(round(self.__sliders[name].get(), round_))
            self.__var[str(name + "_str")].set(str(self.__var[name].get()))
        except RecursionError:
            pass


    def __add_label(self, name, text_, default_value, row_, col_ ):
        self.__labels[name] = Label(self, text=str(text_ + " " + self.__unit_str + ":"))
        self.__labels[name].grid(sticky=W, row=row_ + 1, column=col_ + 1)

        self.__var[name] = StringVar()
        self.__var[name].set(str(default_value))

        self.__output[name] = Label(self, textvariable=self.__var[name])
        self.__output[name].grid(sticky=W, row=row_ + 1, column=col_ + 2)


    def __add_checkbox(self, name_, text_ , row_, col_, callback_):
        self.__checkboxes[name_] = IntVar()
        self.__checkboxes[name_].set(1)
        check1 = Checkbutton(self, text=text_, variable=self.__checkboxes[name_], command=callback_)
        check1.grid(row=row_, column=col_, sticky=W)




def main():
    root = Tk()
    root.geometry("900x720+300+300")
    app = FatigueDiagram_General()

    # To jump the window to the front
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, '-topmost', False)

    # run
    root.mainloop()


if __name__ == '__main__':
    main()