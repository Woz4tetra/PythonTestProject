import numpy as np  
import matplotlib.pyplot as plt  

SIZE = 50  
R1 = 0.5
R2 = 0.75

plt.ion()

fig = plt.figure(0)
fig.canvas.set_window_title('broken spiral')

A = []
B = []

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
line1, = ax1.plot([], [],'-k',label='black')
line2, = ax2.plot([], [],'-r',label='red')
ax1.legend()
ax2.legend()
for i in range(0, SIZE):
  A.append(R1 * i * np.sin(i))
  line1.set_xdata(range(len(A)))
  line1.set_ydata(A)
  ax1.relim()
  ax1.autoscale_view()
  
  B.append(R2 * i * np.cos(i))
  line2.set_xdata(range(len(B)))
  line2.set_ydata(B)
  ax2.relim()
  ax2.autoscale_view()
  
  fig.canvas.draw()
  plt.pause(0.005)
    
  
