import numpy as np





class DMaterialData():
    Sut = 1     # ultimate tensile strength
    Sy = 1      # yield strength
    Se = 1      # endurance strength


    def __init__(self, sut_, sy_, se_ ):
        self.Sut = sut_
        self.Sy = sy_
        self.Se = se_


    def set(self,sut_, sy_, se_):
        self.Sut = sut_
        self.Sy = sy_
        self.Se = se_


class BMaterialData():
    Sut = 1     # ultimate tensile strength
    Suc = 1      # ultimate compression strength


    def __init__(self, sut_, suc_):
        self.Sut = sut_
        self.Suc = suc_


    def set(self,sut_, suc_):
        self.Sut = sut_
        self.Suc = suc_
