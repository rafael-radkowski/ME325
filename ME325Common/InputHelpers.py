import platform
import matplotlib
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Arc

# tkinter for the display
from tkinter import *
from tkinter import Canvas
from tkinter import Tk, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Scale, Checkbutton
import tkinter as tk






class DataEntryMenu():


    __toplevel_frame = 0
    __window  = 0

    __callback = None

    # dictionary for output data
    __dict = 0
    __entry_dict = 0

    def __init__(self, frame, callback):
        self.__toplevel_frame = frame
        self.__callback = callback
        self.__dict = dict()
        self.__entry_dict = dict()


    def create(self, title, items):

        self.__window = Toplevel(self.__toplevel_frame)

        tk.Label(self.__window, text=title, background='white', font="Helvetica 14 bold").grid(sticky=NW, row=0, column=0)
        n = len(items)

        for i in range(n):
            self.__dict[items[i]] = StringVar()
            tk.Label(self.__window, text=items[i], background='white').grid(sticky=NW, row=i+1, column=0)
            e = Entry(self.__window, textvariable=self.__dict[items[i]], width=15)
            e.grid(sticky=NW, row=i+1, column=1)
            self.__entry_dict[items[i]] = e

        tk.Button(self.__window, text="Close", command=self.__destroyed_callback,
                  background='white').grid(sticky=NW, row=n+1, column=0, padx=7, pady=7)

        tk.Button(self.__window, text="Use", command=self.__callback,
                  background='white').grid(sticky=NE, row=n + 1, column=1, padx=7, pady=7)


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


