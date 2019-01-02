import numpy as np





class UnitConversion():


    def __init__(self):

        return


    @staticmethod
    def Nmm2_to_psi(value):
        return value * 145.037738  # N/mm^2 -> psi


    @staticmethod
    def psi_to_Nmm2(value):
        return value * 0.00689475728  # psi -> N/mm^2