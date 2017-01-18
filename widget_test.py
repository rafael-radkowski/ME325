from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt
from pylab import *




def func(a, b, t):
    return sin( a * t) + b


t = linspace(0,10,50)


k = func(0.2, 0.5, t)
plt.plot(t,k)
plt.show()




