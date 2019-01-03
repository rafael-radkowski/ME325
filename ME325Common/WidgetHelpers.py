# matplotlib
import platform
import matplotlib
import matplotlib.patches as mpatches
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import datetime
import os




class Arrow():

    px = 0
    py = 0
    dx = 0
    dy = 0
    ang = 0

    col = 'red'
    linewidth = 2
    arrowhead_angle = 35

    arrow = None
    head = None


    def __init__(self, px_, py_, dx_, dy_, ang_, linewidth_=2, color_='red'):
        self.px = px_
        self.py = py_
        self.dx = dx_
        self.dy = dy_
        self.ang = ang_
        self.col = color_
        self.linewidth = linewidth_

        self.__create_arrow()

    def set(self, px_, py_, dx_, dy_, ang_, flip_ = 1):
        self.px = px_
        self.py = py_
        self.dx = dx_
        self.dy = dy_
        self.ang = ang_
        px, py, ax, ay = self.__get_arrow_points(self.px, self.py, self.dx, self.dy, self.ang, flip_)
        self.arrow.set_data(px, py)
        self.head.set_data(ax, ay)



    def __create_arrow(self):
        px, py, ax, ay = self.__get_arrow_points(self.px, self.py, self.dx, self.dy, self.ang)
        self.arrow, = plt.plot(px, py, 'k-', color=self.col, lw=self.linewidth, alpha=0.8)
        self.head, = plt.plot(ax, ay, 'k-', color=self.col, lw=self.linewidth, alpha=0.8)



    def __get_arrow_points(self, p0x, p0y, d1x, d1y, angle, flip_head = 1):
        vx = (d1x + p0x) - p0x
        vy = (p0y + d1y) - p0y

        l = np.sqrt(vx** 2 + vy**2)
        l = np.max([1, l])

        #  cos  -sin
        #  sin  cos

        # arrow
        r1x = p0x * np.cos(np.deg2rad(angle)) - p0y * np.sin(np.deg2rad(angle))
        r1y = p0x * np.sin(np.deg2rad(angle)) + p0y * np.cos(np.deg2rad(angle))

        r2x = (p0x + d1x) * np.cos(np.deg2rad(angle)) - (p0y + d1y) * np.sin(np.deg2rad(angle))
        r2y = (p0x + d1x) * np.sin(np.deg2rad(angle)) + (p0y + d1y) * np.cos(np.deg2rad(angle))

        # arrow head
        ang = np.deg2rad(self.arrowhead_angle)
        avx = -vx * 0.2 * flip_head
        avy = -vy * 0.2 * flip_head
        avx1 = avx * np.cos(ang) - avy * np.sin(ang)
        avy1 = avx * np.sin(ang) + avy * np.cos(ang)
        ang = np.deg2rad(-self.arrowhead_angle)
        avx2 = avx * np.cos(ang) - avy * np.sin(ang)
        avy2 = avx * np.sin(ang) + avy * np.cos(ang)

        a1x = r2x
        a1y = r2y
        if  flip_head == -1: # set the start point for the arrow to the start of the line
            d1x = 0
            d1y = 0
            a1x = r1x
            a1y = r1y

        a2x = (p0x + d1x + avx1) * np.cos(np.deg2rad(angle)) - (p0y + d1y + avy1) * np.sin(np.deg2rad(angle))
        a2y = (p0x + d1x + avx1) * np.sin(np.deg2rad(angle)) + (p0y + d1y + avy1) * np.cos(np.deg2rad(angle))

        a3x = (p0x + d1x + avx2) * np.cos(np.deg2rad(angle)) - (p0y + d1y + avy2) * np.sin(np.deg2rad(angle))
        a3y = (p0x + d1x + avx2) * np.sin(np.deg2rad(angle)) + (p0y + d1y + avy2) * np.cos(np.deg2rad(angle))

        return [r1x, r2x], [r1y, r2y], [a2x, a1x, a3x], [a2y, a1y, a3y]