import numpy as np



def calcPrincipalStress(s_xx, s_yy, t_xy):
    """
    Calculate the principal stress
    :param s_xx: the stress component in z direction, around the xx axis
    :param s_yy: the stress component in z direction, around the yy axis
    :param t_xy: shear stress around z in the xy-plane
    :return:
    """

    h = round(np.sqrt( ( (s_xx - s_yy)/2.0)**2 + t_xy**2),6)
    a = round((s_xx + s_yy)/2,6)

    s1 = a + h
    s3 = a - h

    # swap so that s1 >= s3
    if(s1 < s3):
        t = s1
        s1 = s3
        s3 = t

    return [s1, s3]