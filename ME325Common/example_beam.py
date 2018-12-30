

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

from ME325Common.ContinuumMechanics import *
from ME325Common.SecondMoment import *

# for images
from PIL import Image, ImageTk

import numpy as np

class ExampleBeam():
    """
            /\ y
        b   |
            |
        ---------
        |       |
        |       |
        |       |  h --->x
        |       |
        ---------

    """

    # limits
    limit_yieldstress = 200  # N/mm^2
    limit_load = 10000  # n
    limit_torsion = 15  # Nm
    limit_angle = 90  # deg
    limit_wh = 100  # mm
    limit_l = 1000  # mm


    # load
    Force = 0 # N

    # dimensions
    length = 1 # meter
    width = 0.1 # meter
    height = 0.1 # meter
    alpha = 0 # degree

    # Second moment of area
    I_yy = 0
    I_xx = 0

    # polar moment of intertial of area
    Jxy = 0

    sigma_max = 0

    # The free body diagram
    img = None
    render = None

    # submenu for manual entry
    window = None
    input_Sy = 0
    input_F = 0
    input_alpha = 0
    input_w = 0
    input_h = 0
    input_l = 0
    input_T = 0

    # window showing details
    window_details = None
    detail_s1 = 0
    detail_s2 = 0
    detail_s_xx = 0
    detail_s_yy = 0
    detail_t_xy = 0
    detail_I_xx = 0
    detail_I_yy = 0
    detail_J_p = 0
    detail_s_max = 0

    canvas = 0
    arrow = [0,0,0]
    area_plt = 0
    plot_init = 0

    def __init__(self):
        self.img = Image.open("resources/Example_01.png")
        self.img = self.img.resize((300, 120), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.img)

        self.input_Sy = StringVar()
        self.input_F = StringVar()
        self.input_T = StringVar()
        self.input_alpha = StringVar()
        self.input_w = StringVar()
        self.input_h = StringVar()
        self.input_l = StringVar()
        self.detail_s1 = StringVar()
        self.detail_s2 = StringVar()
        self.detail_s_xx = StringVar()
        self.detail_s_yy = StringVar()
        self.detail_t_xy = StringVar()
        self.detail_I_xx = StringVar()
        self.detail_I_yy = StringVar()
        self.detail_s_max = StringVar()
        self.detail_J_p = StringVar()


    def setLimits(self, Sy_, L_, T_,  alpha_, wh_, l_):
        self.limit_yieldstress = Sy_
        self.limit_load = L_
        self.limit_torsion = T_
        self.limit_angle = alpha_
        self.limit_wh = wh_
        self.limit_l = l_

    def calcI(self, b, h ):

        self.height = h
        self.width = b
        self.I_xx, self.I_yy = SecondMoment.RectArea(b,h)

        self.Jxy = SecondMoment.PolarRectArea(b,h)

        #print(self.I_xx, " ", self.I_yy)
        return [self.I_xx, self.I_yy]



    def calcPrincipalStress(self, F, T, l, angle):

        self.alpha = angle
        self.Force = F
        self.length = l
        Fx = F * np.cos(np.deg2rad(angle))
        Fy = F * np.sin(np.deg2rad(angle))

        #print(Fx, " ", Fy)

        r = self.calc_radius(self.width, self.height)

        # the two stress components in z-direction
        s_yy = (Fx * l * self.width)/(2 * self.I_yy)
        s_xx = (Fy * l * self.height) / (2 * self.I_xx)
        self.sigma_max = s_xx + s_yy

        # shear stress
        t_xy = (T * 1000 * r)/ self.Jxy # T * 1000-> Nm to Nmm


        # principal stresses
        s1, s3 = calcPrincipalStress(self.sigma_max, 0.0, t_xy)

        #print(Fx, " ", Fy, "  ", s_xx, " " ,  s_yy, "  ", s1, " " ,  s3)

        self.setDetails( s1, s3, s_xx, s_yy, self.sigma_max, t_xy, self.I_xx, self.I_yy, self.Jxy)
        self.updateLoadPlot()

        return [s1, s3, s_xx, s_yy]

    def calc_radius(self, b, h):
        r = np.sqrt((b / 2) ** 2 + (h / 2) ** 2)
        return r

    ##-----------------------------------------------------------------------------
    ## Helper windows


    def getImage(self):
        return self.render


    def sub_window_destroyed_callback(self):
        """
        Destroy the subwindow
        :return:
        """
        self.window.destroy()
        self.window = None


    def createManualEntryMenu(self, toplevel, event_callback):

        self.window = Toplevel(toplevel)


        tk.Label(self.window, text="Yield stress (N/mm^2):", background='white').grid(sticky=NW, row=0, column=0)
        tk.Label(self.window, text="Load F (N):", background='white').grid(sticky=NW, row=1, column=0)
        tk.Label(self.window, text="Angle alpha (deg):", background='white').grid(sticky=NW, row=2, column=0)
        tk.Label(self.window, text="Load T (Nm):", background='white').grid(sticky=NW, row=3, column=0)
        tk.Label(self.window, text="height h (mm):", background='white').grid(sticky=NW, row=4, column=0)
        tk.Label(self.window, text="width w (mm):", background='white').grid(sticky=NW, row=5, column=0)
        tk.Label(self.window, text="length l (mm):", background='white').grid(sticky=NW, row=6, column=0)




        Entry(self.window, textvariable=self.input_Sy).grid(sticky=NW, row=0, column=1)
        Entry(self.window, textvariable=self.input_F).grid(sticky=NW, row=1, column=1)
        Entry(self.window, textvariable=self.input_alpha).grid(sticky=NW, row=2, column=1)
        Entry(self.window, textvariable=self.input_T).grid(sticky=NW, row=3, column=1)
        Entry(self.window, textvariable=self.input_h).grid(sticky=NW, row=4, column=1)
        Entry(self.window, textvariable=self.input_w).grid(sticky=NW, row=5, column=1)
        Entry(self.window, textvariable=self.input_l).grid(sticky=NW, row=6, column=1)

        b = tk.Button(self.window, text="Use", command=event_callback,
                      background='white').grid(sticky=NE, row=7, column=1, padx=7, pady=7)

        c = tk.Button(self.window, text="Close", command=self.sub_window_destroyed_callback,
                      background='white').grid(sticky=NW, row=7, column=0, padx=7, pady=7)



    def setMenuValue(self, Sy, F, T, a, h, w, l):
        self.input_Sy.set(Sy)
        self.input_F.set(F)
        self.input_T.set(T)
        self.input_alpha.set(a)
        self.input_h.set(h)
        self.input_w.set(w)
        self.input_l.set(l)



    def getManualEntryValues(self):
        try:
            digits = 2

            # Check for limits
            Sy = np.min([float(self.limit_yieldstress), np.max([float(0), float(self.input_Sy.get())])])
            Sy = round(Sy,digits)
            self.input_Sy.set(Sy)
            L = np.min([float(self.limit_load), np.max([float(-self.limit_load), float(self.input_F.get())])])
            L = round(L, digits)
            self.input_F.set(L)
            a = np.min([float(self.limit_angle), np.max([float(-self.limit_angle), float(self.input_alpha.get())])])
            a = round(a,digits)
            self.input_alpha.set(a)
            T = np.min([float(self.limit_torsion), np.max([float(-self.limit_torsion), float(self.input_T.get())])])
            T = round(T, digits)
            self.input_T.set(T)
            h = np.min([float(self.limit_wh), np.max([float(-self.limit_wh), float(self.input_h.get())])])
            h = round(h,digits)
            self.input_h.set(h)
            l = np.min([float(self.limit_l), np.max([float(-self.limit_l), float(self.input_l.get())])])
            l = round(l,digits)
            self.input_l.set(l)
            w = np.min([float(self.limit_wh), np.max([float(-self.limit_wh), float(self.input_w.get())])])
            w = round(w,digits)
            self.input_w.set(w)

            return [Sy, L, a, T, h, w, l]

        except ValueError:
            print("Something went wrong - invalid numbers")



    def createDetailsWindow(self, toplevel):

        self.window_details = Toplevel(toplevel)

        tk.Label(self.window_details, text="Principal stress", background='white').grid(sticky=NW, row=0, column=0)
        tk.Label(self.window_details, text="\u03C3_1 (N/mm^2)", background='white').grid(sticky=NW, row=0, column=1)
        tk.Label(self.window_details, text="\u03C3_2 (N/mm^2)", background='white').grid(sticky=NW, row=1, column=1)

        tk.Label(self.window_details, text="Component stress", background='white').grid(sticky=NW, row=2, column=0)
        tk.Label(self.window_details, text="\u03C3_z,x (N/mm^2)", background='white').grid(sticky=NW, row=2, column=1)
        tk.Label(self.window_details, text="\u03C3_z,y (N/mm^2)", background='white').grid(sticky=NW, row=3, column=1)
        tk.Label(self.window_details, text="\u03C3_z,max (N/mm^2)", background='white').grid(sticky=NW, row=4, column=1)
        tk.Label(self.window_details, text="\u03C4_xy (N/mm^2)", background='white').grid(sticky=NW, row=5, column=1)


        tk.Label(self.window_details, text="Second moment", background='white').grid(sticky=NW, row=6, column=0)
        tk.Label(self.window_details, text="Ixx (mm^4)", background='white').grid(sticky=NW, row=6, column=1)
        tk.Label(self.window_details, text="Iyy (mm^4)", background='white').grid(sticky=NW, row=7, column=1)
        tk.Label(self.window_details, text="Jp (mm^4)", background='white').grid(sticky=NW, row=8, column=1)

        Entry(self.window_details, textvariable=self.detail_s1, state='readonly').grid(sticky=NW, row=0, column=2)
        Entry(self.window_details, textvariable=self.detail_s2, state='readonly').grid(sticky=NW, row=1, column=2)
        Entry(self.window_details, textvariable=self.detail_s_yy, state='readonly').grid(sticky=NW, row=2, column=2)
        Entry(self.window_details, textvariable=self.detail_s_xx, state='readonly').grid(sticky=NW, row=3, column=2)
        Entry(self.window_details, textvariable=self.detail_s_max, state='readonly').grid(sticky=NW, row=4, column=2)
        Entry(self.window_details, textvariable=self.detail_t_xy, state='readonly').grid(sticky=NW, row=5, column=2)
        Entry(self.window_details, textvariable=self.detail_I_xx, state='readonly').grid(sticky=NW, row=6, column=2)
        Entry(self.window_details, textvariable=self.detail_I_yy, state='readonly').grid(sticky=NW, row=7, column=2)
        Entry(self.window_details, textvariable=self.detail_J_p, state='readonly').grid(sticky=NW, row=8, column=2)


        self.canvas = self.createLoadPlot( self.window_details, 9, 0)



        tk.Button(self.window_details, text="Close", command=self.detail_window_destroyed_callback,
                      background='white').grid(sticky=NW, row=12, column=0, padx=7, pady=7)


    def setDetails(self, s1, s2, sxx, syy, smax, txy, Ixx, Iyy, Jp):
        digits = 2
        self.detail_s1.set(str(round(s1, digits)))
        self.detail_s2.set(str(round(s2, digits)))
        self.detail_s_xx.set(str(round(sxx, digits)))
        self.detail_s_yy.set(str(round(syy, digits)))
        self.detail_t_xy.set(str(round(txy, digits)))
        self.detail_I_xx.set(str(round(Ixx, digits)))
        self.detail_I_yy.set(str(round(Iyy, digits)))
        self.detail_s_max.set(str(round(smax,2)))
        self.detail_J_p.set(str(round(Jp,2)))




    def detail_window_destroyed_callback(self):
        """
        Destroy the subwindow
        :return:
        """
        self.window_details.destroy()
        self.window_details = None


    def updateLoadPlot(self):

        if self.plot_init == 0:
            return

        plt.figure(2)

        self.area_plt.set_data([-self.width / 2, self.width / 2, self.width / 2, -self.width / 2, -self.width / 2],
                               [-self.height / 2, -self.height / 2, self.height / 2, self.height / 2, -self.height / 2])

        margin = 20
        #length = np.sqrt(self.width ** 2 + self.height ** 2) * 0.8
        length = np.max([float(self.width), float(self.height)]) / 2 * 0.8 + 10
        arrow = length * 0.2
        px = np.cos(np.deg2rad(self.alpha)) * length
        py = np.sin(np.deg2rad(self.alpha)) * length
        ax = np.cos(np.deg2rad(self.alpha - 35)) * arrow
        ay = np.sin(np.deg2rad(self.alpha - 35)) * arrow
        ax2 = np.cos(np.deg2rad(self.alpha + 35)) * arrow
        ay2 = np.sin(np.deg2rad(self.alpha + 35)) * arrow

        # draw arrow
        self.arrow[0].set_data([0, px], [0, py])
        self.arrow[1].set_data([0, ax], [0, ay])
        self.arrow[2].set_data([0, ax2], [0, ay2])

        plt.figure(2)

        lim = np.max([float(self.width), float(self.height)])
        plt.xlim(-lim / 2 - margin, lim / 2 + margin)
        plt.ylim(-lim / 2 - margin, lim / 2 + margin)

       # plt.xlim(-self.width / 2 - margin, self.width / 2 + margin)
        #plt.ylim(-self.height / 2 - margin, self.height / 2 + margin)

        self.canvas.draw_idle()


    def createLoadPlot(self, toplevel, row_, col_):
        self.plot_init = 1
        fig, ax = plt.subplots(figsize=(4, 4),num=2)
        plt.subplots_adjust(left=0.15, bottom=0.15)
        fig.set_size_inches(4, 4, forward=True)
        canvas = FigureCanvasTkAgg(fig, master=toplevel)  # A tk.DrawingArea.
        canvas.draw()

        # self.canvas = Canvas(self.window_details, width=300, height=300)
        canvas.get_tk_widget().grid(row=row_, column=col_, columnspan=3, rowspan=3,
                                         padx=5, sticky=E + W + S + N)
        toplevel.columnconfigure(col_, weight=1)  # first and last column can expand
        toplevel.columnconfigure(col_, pad=7)
        toplevel.rowconfigure(row_, weight=1)
        toplevel.rowconfigure(row_, pad=7)

        # draw area
        self.area_plt, = plt.plot([-self.width/2, self.width/2, self.width/2, -self.width/2 , -self.width / 2],
                                  [-self.height/2, -self.height/2, self.height/2, self.height/2, -self.height/2],
                                  'k-', color='black', lw=2)

        margin = 20
        #length = np.sqrt(self.width**2 + self.height**2) * 0.8
        length = np.max([float(self.width), float(self.height)])/2 * 0.8 + 10
        arrow = length * 0.2
        px = np.cos(np.deg2rad(self.alpha)) * length
        py = np.sin(np.deg2rad(self.alpha)) * length
        ax = np.cos(np.deg2rad(self.alpha - 35)) * arrow
        ay = np.sin(np.deg2rad(self.alpha - 35)) * arrow
        ax2 = np.cos(np.deg2rad(self.alpha + 35)) * arrow
        ay2 = np.sin(np.deg2rad(self.alpha + 35)) * arrow

        # draw arrow
        self.arrow[0], = plt.plot([0, px], [0, py], 'k-', color='red', lw=3, label='Load F')
        self.arrow[1], = plt.plot([0, ax], [0, ay], 'k-', color='red', lw=3)
        self.arrow[2], = plt.plot([0, ax2], [0, ay2], 'k-', color='red', lw=3)


        # coordinate axis
        plt.plot([0, -self.width/2 - 5], [0,0], color='black', lw=1)
        plt.plot([0, 0], [0, -self.height / 2 - 5], color='black', lw=1)
        plt.text(-self.width/2 - 5, 0.5, "X")
        plt.text(0.5, -self.height / 2 - 5, "Y")



        plt.grid()
        plt.xlabel(r'width $w\;\;\left(mm\right)$')
        plt.ylabel(r'height $h\;\;\left(mm\right)$')

        lim = np.max([float(self.width), float(self.height)])
        plt.xlim(-lim/2-margin, lim/2+margin)
        plt.ylim(-lim/2-margin, lim/2+margin)
        plt.legend(loc=2)


        return canvas


