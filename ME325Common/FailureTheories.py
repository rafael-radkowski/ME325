import numpy as np




def CalcVonMiesesEquivalentStress(sigma_A, sigma_B ):
    """
    Calculate the von Mises Equivalent stress for a planar (2D) situations
    using the principal stresses sigma_A and sigma_B, with sigma_A > sigma_B
    :param sigma_A:  the first principal stress
    :param sigma_B:  the second principal stress:
    :return: the von Mises equivalent stress
    """
    sigma_eq = sigma_A**2 - sigma_A * sigma_B + sigma_B**2
    sigma_eq = np.sqrt(sigma_eq)
    return sigma_eq

def CalcVonMiesesFoS(sigma_A, sigma_B, Sy):
    vonMisesEq = CalcVonMiesesEquivalentStress(sigma_A, sigma_B)
    if vonMisesEq == 0.0:
        vonMisesEq = 0.00000001
    FoS_vonMisesEq = Sy / vonMisesEq

    return [ vonMisesEq, FoS_vonMisesEq ]


def CalcTrescaEquicalentStress(sigma_A, sigma_B ):
    """
    \
    :param sigma_A:
    :param sigma_B:
    :return:
    """
    s1 = sigma_A
    s2 = sigma_B
    if sigma_B > sigma_A:
        s2 = sigma_A
        s1 = sigma_B

    stress = (s1 - s2)/2

    return stress


def CalcTrescaFoS(sigma_A, sigma_B, Sy ):

    s1 = sigma_A
    s2 = sigma_B
    if sigma_B > sigma_A:
        s2 = sigma_A
        s1 = sigma_B

    stress = CalcTrescaEquicalentStress(s1, s2)

    if stress == 0.0:
        stress = 0.00000001

    if s1 == 0.0:
        s1 = 0.00000001

    if s2 == 0.0:
        s2 = 0.00000001

    #FoS_TrescaEqStress = 0
    if s1 >= s2 and s1 >= 0 and s2 >= 0:
        FoS_TrescaEqStress = Sy / s1
    elif s1 >= 0 and s2 < 0:
        FoS_TrescaEqStress = Sy / 2 / stress
    elif s1 < 0 and s2  < s1:
        FoS_TrescaEqStress = -Sy / s2

    #FoS_TrescaEqStress = Sy/(stress)

    return [stress, FoS_TrescaEqStress]



def CalcPrincipalStressFos(sigma_A, sigma_B, Sy ):
    if sigma_A == 0.0:
        sigma_A = 0.00000001

    if sigma_B == 0.0:
        sigma_B = 0.00000001

    n1 = Sy / sigma_A
    n2 = Sy / sigma_B

    return min(n1,n2)



def CalcMNSTStressFoS(s1, s3, Sut, Suc):

    if s1 < 0.000001 and s1 > -0.000001:
        s1 = 0.0001

    if s3 < 0.000001 and s3 > -0.000001:
        s3 = 0.0001

    case = 0
    stress = 0
    n = 0
    if s1 >= 0 and s3 >= 0 and s1 >= s3:
        case = 1
        n = Sut / s1
        stress = s1
    elif s1 >= 0 and s3 >= 0 and s3 > s1:
        case = 2
        n = Sut / s3
        stress = s3
    elif s1 < 0 and s3 >= 0 and -Sut / Suc > s3 / s1:
        case = 3
        n = Sut / s3
        stress = s3
    elif s1 < 0 and s3 >= 0 and -Sut/Suc <= s3/s1:
        case = 4
        n = Suc / s1
        stress = s1
    elif s1 < 0 and s3 < 0 and -Suc/-Suc >= s3/s1:
        case = 5
        n = Suc / s1
        stress = s1
    elif s1 < 0 and s3 < 0 and -Suc/-Suc < s3/s1:
        case = 6
        n = Suc / s3
        stress = s3
    elif s1 >= 0 and s3 < 0 and -Suc / Sut > s3 / s1:
        case = 7
        n = Suc / s3
        stress = s3
    elif s1 >= 0 and s3 < 0 and -Suc / Sut < s3 / s1:
        case = 8
        n = Sut / s1
        stress = s1

   # print( -Suc / Sut, "  ",  s3 / s1, " ", case)

    return [stress, abs(round(n,2))]


def CalcMMStressFoS(s1, s3, Sut, Suc):

    # swap s1 and s3 so that s1 > s3
    if s1 < s3:
        t = s1
        s1 = s3
        s3  = t

    if s1 < 0.000001 and s1 > -0.000001:
        s1 = 0.0001

    if s3 < 0.000001 and s3 > -0.000001:
        s3 = 0.0001

    case  = 0
    s = 0
    FoS = 0
    if s1 >= s3 and s3 >= 0:
        FoS = Sut / s1
        s = s1
        case = 1
    elif s1 >= 0 and s3 < 0 and abs(s3/s1) <= 1.0:
        FoS = Sut / s1
        s = s1
        case = 2
    elif  s1 >= 0 and s3 < 0 and abs(s3/s1) > 1.0:
        n = ((Suc - Sut) * s1)/(Suc* Sut) - s3/Suc
        FoS = 1/n
        s = np.sqrt(s1**2 + s3**2)
        case = 3
    elif s1 <=0 and s3 < s1:
        FoS = -Suc/s3
        s = s3
        case = 4


    return [s, abs(round(FoS, 2))]



def CalcBCMStressFoS(s1, s3, Sut, Suc):
    # swap s1 and s3 so that s1 > s3
    if s1 < s3:
        t = s1
        s1 = s3
        s3 = t

    if s1 < 0.000001 and s1 > -0.000001:
        s1 = 0.0001

    if s3 < 0.000001 and s3 > -0.000001:
        s3 = 0.0001

    case = 0
    s = 0
    FoS = 0

    if s1 >= s3 and s3 >= 0:
        FoS = Sut/s1
        s = s1
    elif  s1 >= 0 and s3 <= 0:
        n = s1/Sut - s3/Suc
        FoS = 1/n
        s = np.sqrt(s1**2 + s3**2)
    elif s1 <= 0 and s3 <= 0:
        FoS = -Suc /s3
        s = s3

    return [s, abs(round(FoS, 2))]