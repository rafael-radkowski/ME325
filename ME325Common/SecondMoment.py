"""
Implementing second moments of area from

https://en.wikipedia.org/wiki/List_of_second_moments_of_area


"""
import numpy as np


class SecondMoment():

    def __init__(self):
        return

    @staticmethod
    def RectArea(b, h):
        """
                /\ y
                |
             b  |
            ---------
            |       |
            |       |
            |       |  h --->x
            |       |
            ---------
        :param b: width
        :param h: heigth
        :return: The second moments of area [Ixx, Iyy]
        """

        return [ (b*h**3 )/12, (b**3*h)/12 ]

    @staticmethod
    def PolarRectArea(b, h):
        """
             /\ y
                |
             b  |
            ---------
            |       |
            |       |
            |       |  h --->x
            |       |
            ---------

        :param b:
        :param h:
        :return:

        """
        # from  https://www.engineersedge.com/polar-moment-inertia.htm
        return (b * h*(b**2 + h**2))/12
