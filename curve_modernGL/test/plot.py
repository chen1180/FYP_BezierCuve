import matplotlib.pyplot as plt
import numpy as np
plt.plot([0,0.002,0.006,0.010,0.014,0.018,0.02],[100,150,218,254,258,230,200],'ro')

t = np.arange(0., 0.021, 0.001)
plt.plot(t, -1e6*t*t+25000*t+100, 'g--')
plt.show()