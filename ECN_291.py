"""
When i code in python..it's just like a pro
"""

import numpy as np
import matplotlib.pyplot as plt

"""
Everything is in SI units
"""

"""
Vconst = 5000 * Is * exp(Vdc/Vt)
Vout Vcc - Vconst * exp(Vac/Vt)
"""

Vconst = 7
Vcc = 15
Vt = 0.026
t = np.arange(0, 20, 0.2)
Vac = (0.005 * np.sin(t))/0.026
Vac1 = Vconst * np.exp(Vac)
Vfinal = 15 - Vac1

"""
To get DC offset of the Vout
VoutDC = 15 - Vconst = 8

To just get AC signal of the signal
Vfinal - VoutDC

Vamp is the max of the amplitude taken which is below 
x Axis in this case
"""

VoutDC = 8
Vamp = 1.4843038

"""
Multiplied by -1 to reverse the graph
"""

plt.plot(t,  -1 * (Vfinal - VoutDC)/Vamp, 'r')

"""
For general plotting of sin function Normalized
"""
plt.plot(t, np.sin(t), 'b')

plt.title('Bjt Equation')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True, which='both')
plt.axhline(y=0, color='g')
plt.show()
