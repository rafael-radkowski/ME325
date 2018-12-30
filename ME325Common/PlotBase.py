"""
Base class for plots
Maintains a plot number on  a global level so that single matplotlib plots
are easily distinguishable.

Rafael Radkowski
Iowa State University
rafael@iastate.edu
Dec 27, 2018

All copyright reserved
"""

g_plot_number = 0


class PlotBase():


    @staticmethod
    def GetPlotNumber():
        """
        Get a plot number
        :return: integer with the plot no.
        """
        global g_plot_number
        g_plot_number = g_plot_number + 1
        print(g_plot_number)
        return g_plot_number

