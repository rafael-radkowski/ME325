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
        return g_plot_number


    @staticmethod
    def SaveFigure( fig, path_and_file):
        """
        Save the figure
        :param fig: reference to the figure
        :param path_and_file: string with the relative or absolute path and filename.
                    Note that the ending needs to be .png or .jpg, the file type to save.
        :return:
        """
        fig.savefig(path_and_file)