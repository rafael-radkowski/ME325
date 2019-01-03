import numpy as np

import platform
import matplotlib
if platform.system() == 'Darwin':
    matplotlib.use("TkAgg")


from typing import NamedTuple

from ME325Common.PlotHelpers import *

class SNData():
    Sut = 1     # ultimate tensile strength
    Sy = 1      # yield strength
    Se = 1      # endurance strength
    Nlow = 1    # low cycle fatigue limit
    Nend = 1    # endurance limit


    def __init__(self, sut_, sy_, se_, nlow_, nend_ ):
        self.Sut = sut_
        self.Sy = sy_
        self.Se = se_
        self.Nlow = nlow_
        self.Nend = nend_


    def set(self,sut_, sy_, se_, nlow_, nend_):
        self.Sut = sut_
        self.Sy = sy_
        self.Se = se_
        self.Nlow = nlow_
        self.Nend = nend_

class SNDiagram():
    """
    Calculation to be applied on an SN-Diagram.
    """


    def __init__(self):
        return

    @staticmethod
    def ComputeFatigueStrength(target_itrerations, sndata):
        """
        Calculate the maximal fatigue strength for a given target iterations.
        Iterations given -> search for fatigue strength.
        :param target_itrerations: the target iterations
        :param sndata: SN diagram data as defined in class SNData
        :return: the maximum fatigue strength Sf
        """

        if target_itrerations >= 0.0 and target_itrerations < sndata.Nlow:
            a = (sndata.Sut - sndata.Sy) / (np.log(1) - np.log(sndata.Nlow))
            b = sndata.Sy - a * np.log(sndata.Nlow)
            f = a * np.log(target_itrerations) + b
            return f

        elif target_itrerations >= sndata.Nlow and target_itrerations < sndata.Nend:
            a = (sndata.Sy - sndata.Se) / (np.log(sndata.Nlow) - np.log(sndata.Nend))
            b = sndata.Se - a * np.log(sndata.Nend)
            f = a * np.log(target_itrerations) + b
            return f

        else:
            return sndata.Se


    @staticmethod
    def ComputeMaxIterations(target_Sf, sndata):
        """
        Compute the maximum number of iterations for given fatigue strength Sf
        or: Sf given -> iterations searched.
        :param target_Sf: the target fatigue strength
        :param sndata:  SN diagram data as defined in class SNData
        :return: the maximum number of iterations for the given fatigue strength.
        """
        if target_Sf <= sndata.Se:
            return sndata.Nend
        elif target_Sf < sndata.Sy and target_Sf > sndata.Se:
            a = (sndata.Sy - sndata.Se) / (np.log(sndata.Nlow) - np.log(sndata.Nend))
            b = sndata.Se - a * np.log(sndata.Nend)
            e = (target_Sf - b) / a
            itr = np.exp(e)
            return itr
        else:
            a = (sndata.Sut - sndata.Sy) / (np.log(1) - np.log(sndata.Nlow))
            b = sndata.Sy - a * np.log(sndata.Nlow)
            e = (target_Sf - b) / a
            itr = np.exp(e)
            return itr


class FatigueDiagram():

    def __init__(self):
        pass


    @staticmethod
    def calc_mod_Goodman_FoS(Sa, Sm, Se, Sut ):
        f = 0.00000001 # prevent division by 0
        return 1 / ( Sa/(Se+f) + Sm/(Sut+f) + f)


    @staticmethod
    def calc_Sonderberg_FoS(Sa, Sm, Se, Sy):
        f = 0.00000001  # prevent division by 0
        return 1 / (Sa / (Se + f) + Sm / (Sy + f) + f)


    @staticmethod
    def calc_Gerber_FoS(Sa, Sm, Se, Sut):
        f = 0.000000001
        a = (Sm / (Sut+f)) ** 2
        b = (Sa / (Se+f))
        c = - 1.0

        p = b / (a+f)
        q = c / (a+f)

        n = - (p / 2.0) + np.sqrt((p / 2.0) ** 2 - q)
        n2 = - (p / 2.0) - np.sqrt((p / 2.0) ** 2 - q)

        return n