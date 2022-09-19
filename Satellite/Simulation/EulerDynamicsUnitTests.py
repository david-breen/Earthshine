from cmath import cos
import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from EulerDynamicsDeriver import *


# Time stuff
dt = 0.1
time = np.arange(0, 100, dt)

# initial conditions
Itensor = np.array([[5, 0, 0], [0, 5, 0], [0, 0, 2]])  # kg*m^2
initial_velocity = np.array([3, 0, 2], float)
initial_attitude = np.array([0, 0, 0, 1], float)
M = np.array([0, 0, 0])

# Matrix initalization

velocity_mat = np.empty((0, 3), float)
attitude_mat = np.empty((0, 4), float)

velocity_mat = np.append(velocity_mat, [initial_velocity], axis=0)
attitude_mat = np.append(attitude_mat, [initial_attitude], axis=0)

display_vect = [1, 0, 0]


for t in time:
    
    #print(RK45_step(state_mat[-1][0], M, Itensor, t, dt, state_mat[-1][1]))

    w_hold, Q_hold = RK45_step(velocity_mat[-1], M, Itensor, t, dt,
                                attitude_mat[-1])

    velocity_mat = np.append(velocity_mat, [w_hold] , axis=0)
    attitude_mat = np.append(attitude_mat, [Q_hold], axis=0)


bigO = ((Itensor[2][2]-Itensor[0][0])/Itensor[0][0])*2

time = np.append(time, time[-1] + dt)


fig, ax = plt.subplots(3, 2)
ax[0][0].plot(time, velocity_mat[:, 0])
ax[1][0].plot(time, velocity_mat[:, 1])
ax[2][0].plot(time, velocity_mat[:, 2])

ax[0][1].plot(time, 3 * np.cos(bigO * time))
ax[1][1].plot(time, 3 * np.sin(bigO * time) )
ax[2][1].plot(velocity_mat[:, 0], velocity_mat[:, 1])
ax[2][1].plot(3 * np.cos(bigO * time), 3 * np.sin(bigO * time))

fig.suptitle("Numerically integrated (left) Solved (right)")
plt.show()
