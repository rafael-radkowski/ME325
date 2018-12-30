"""
Example for ME325 - Machine Component Design

Utility functions for stress calculations

Rafael Radkowski
Iowa State University
Jan 2017
rafael@iastate.edu

All rights reserved
"""


from pylab import *
import numpy as np;
import matplotlib.pyplot as plt


ee = 1E-12 # to prevent division by zero


def PrincipleStress(sigma, tau):
    """
    Computes the principle stresses
    in a 2-axis case:
    sigma  = (sx + sy)/2 +- sqrt[  ((sx-sy)/2)^2 + tau^2  ]

    :param sigma_x: the stress exerted along the x-axis in kpsi as scalar
    :param sigma_y: the stress exerted along the  y-axis in kpis as scalar
    :param tau_xy: the shear stress exerted around the xy-plane in kpsi as scalar
    :return: a vector of size [N+M,1] with N, the number of stress components and M, the number of angles.
                in a 2-axis case [s_1, s_2, a]
    """
    sigma_x = 0.0
    sigma_y = 0.0
    sigma_z = 0.0
    tau_xy = 0.0

    # get the number of components
    size = len(sigma);



    if size == 1:
        sigma_x = sigma[0]  # in 1-a, the principle stress is equal to the input stress
        tau_xy = tau[0]

        param1 = (sigma_x ) / 2.0;
        param2 = sqrt((sigma_x / 2.0) ** 2 + tau_xy ** 2);

        sigma_1 = param1 + param2;
        sigma_2 = param1 - param2;

        tan2phi = (2.0 * tau_xy) / (sigma_x)
        tan2phi = arctan(tan2phi)/2.0

        if sigma_x > 0.0:
            return [sigma_1, sigma_2, tan2phi]
        else:
            return [sigma_2, sigma_1, tan2phi]

    elif size == 2:
        sigma_x = sigma[0]
        sigma_y = sigma[1]
        tau_xy = tau[0]

        # compute the components and the streses
        param1 = (sigma_x + sigma_y) / 2.0;

        param2 = sqrt(((sigma_x - sigma_y) / 2.0)**2   + tau_xy**2 );

        sigma_1 = param1 + param2;
        sigma_2 = param1 - param2;


        tan2phi = (2.0 * tau_xy) / (sigma_x - sigma_y)
        tan2phi = arctan(tan2phi) / 2.0

        return [sigma_1, sigma_2, tan2phi]


    elif size == 3:
        sigma_x = sigma[0]
        sigma_y = sigma[1]
        sigma_z = sigma[3]
        tau_xy = tau[0]
        tau_yz = tau[1]
        tau_xz = tau[2]

        I1 = sigma_x + sigma_y + sigma_z
        I2 = sigma_x * sigma_y + sigma_y*sigma_z + sigma_z*sigma_z - tau_xy**2 - tau_yz**2 - tau_xz**2
        # To be continued




def vonMises(sigma, tau, principle_stress = False):
    """
    Computes the von Mises equivalent stress
    :param sigma:
    :param tau:
    :param principle_stress:
    :return:
    """

    size = len(sigma)

    if size == 1:
        s_x = sigma[0]
        s_y = 0.0
        tau = tau[0]

        s_vm = (s_x ** 2 - s_x * s_y + s_y ** 2 + 3.0 * (tau ** 2))**0.5

        return s_vm

    elif size == 2:
        s_x = sigma[0]
        s_y = sigma[1]
        tau = tau[0]

        s_vm = sqrt(s_x**2 - s_x*s_y + s_y**2 + 3.0 * tau**2)

        return s_vm




def tresca(sigma):
    """
    Computes the Tresca equivalent stress
    :param sigma:
    :return:
    """

    size = len(sigma)

    if size == 1:
        return (sigma[0] - 0.0)/(2.0)
    elif size == 2:
        return (sigma[0] - sigma[1]) / (2.0)




def FoS(sigma_x, sigma_y, Sut, Suc):
    """
    Helper function to compute the Factor of Safety (FoS) from the max and min stress components

    :param sigma_x: the first stress component as scalar
    :param sigma_y: the secdond stress component as scalar
    :param Sut: the ultimate tensile stress of a material as scalar
    :param Suc: the ultimate comporession stress of a material as scalar
    :return: the factor of safety as scalar
    """
    fs1 = 0.0; fs2 = 0.0;

    ## distinguish between compression and tensile stress
    if sigma_x > 0:
        fs1 = Sut / (sigma_x  + ee) # tensile
    else:
        fs1 = -Suc / (sigma_x + ee)  # compression

    ## distinguish between compression and tensile stress
    if sigma_y > 0:
        fs2 = Sut / (sigma_y + ee)  # tensile
    else:
        fs2 = - Suc / (sigma_y + ee)  # compression

    # return the smallest values
    if fs1 < fs2 and fs1 > 0.0:
        return fs1
    elif fs2 < fs1 and fs2 > 0.0:
        return fs2
    elif fs1 < 0.0 and fs2 > 0.0:
        return fs2
    else:
        return fs1 #both are equal




def brittle_coulumb_fos(s1, s3, Sut, Suc):
    """
    Computes the brittle coulumb factor of safety
    :param s1:  the first principle stress in kpsi
    :param s3:  the second principle stess in kpsi
    :param Sut: Ultimate tensile
    :param Suc: Ultimate compression
    :return:
    """

    if s1 >= 0 and s3 >= 0:
        n = Sut/s1
        return n
    elif s1 >= 0 and s3 < 0:
        n_inv = (s1/Sut) - (s3/Suc)
        n = 1/n_inv
        return n
    elif s1 < 0 and s3 < 0:
        n = -Suc/s3
        return n



def mnst_fos(s1, s3, Sut, Suc):

    if s1 >= 0 and s1 > s3:
        n = Sut / s1
        return n
    elif s3 >= 0 and s3 > s1:
        n = Suc / s3
        return abs(n)
    if s1 < 0 and s1 < s3:
        n = Suc / s1
        return abs(n)
    else:
        n = Suc / s3
        return abs(n)