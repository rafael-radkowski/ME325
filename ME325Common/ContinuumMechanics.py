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


def calcPrincipalAngles(s_xx, s_yy, t_xy):

    tau21 = np.arctan(2*t_xy/(s_xx-s_yy+0.000001))
    tau22 = tau21 + np.deg2rad(180.0)

    return np.rad2deg(tau21)/2, np.rad2deg(tau22)/2,



def calcMaxShearStress(s_xx, s_yy, t_xy):

    s = round(np.sqrt(((s_xx - s_yy) / 2.0) ** 2 + t_xy ** 2), 6)

    return s, -s
