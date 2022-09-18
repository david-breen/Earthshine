from cmath import cos
import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt
from EulerDynamicsDeriver import *

# Time stuff
dt = 0.1
time = np.arange(0, 100, dt)

# initial conditions
Itensor = np.array([[5, 0, 0], [0, 5, 0], [0, 0, 2]])  # kg*m^2
initial_velocity = np.array([1, 0, 1], float)
initial_attitude = np.array([0, 0, 0], float)
initial_inertial = np.array([[ 0, 0, 0], [ 0, 0, 0], [ 0, 0, 0]], float)
M = np.array([0, 0, 0])

# Matrix initalization
velocity_mat = np.empty((0, 3), float)
attitude_mat = np.empty((0, 3), float)
inertial_mat = np.empty((0, 3, 3), float)

velocity_mat = np.append(velocity_mat, [initial_velocity], axis=0)
attitude_mat = np.append(attitude_mat, [initial_attitude], axis=0)
inertial_mat = np.append(inertial_mat, [initial_inertial], axis=0)




for t in time:

    if t < 100:

        M = np.array([0, 0, 0])   # N*m
    else:

        M = np.array([-0.014, -0.2, -1])   # N*m

    velocity_mat = np.append(velocity_mat, [velocity_mat[-1] + 
						    (RK45_step(velocity_mat[-1], M, Itensor, t, dt))],
							 axis=0)

    attitude_mat = np.append(attitude_mat,
                             [velocity_mat[-1] * dt],
                             axis=0)

    #ror = R.from_euler('xyz', (attitude_mat[-1]))

   
'''
    inertial_mat = np.append(inertial_mat,
                             [ror.as_matrix()],
                             axis=0)
'''
w1 = np.multiply(-velocity_mat[:, 1], np.cos((1-Itensor[2][2]/Itensor[0][0])*velocity_mat[:, 2]))
w2 = np.multiply(velocity_mat[:, 1], np.sin((1-Itensor[2][2]/Itensor[0][0])*velocity_mat[:, 2]))
w3 = velocity_mat[:, 2]

time = np.append(time, time[-1] + dt)
print(len(time))

print(-velocity_mat[:, 1])

fig, ax = plt.subplots(3,2)
ax[0][0].plot(time, (velocity_mat[:, 0]))
ax[1][0].plot(time, (velocity_mat[:, 1]))
ax[2][0].plot(time, (velocity_mat[:, 2]))
ax[0][1].plot(time, w1)
ax[1][1].plot(time, w2)
ax[2][1].plot((velocity_mat[:, 1]), (velocity_mat[:, 0]))
fig.suptitle("Numerically integrated (left) Solved (right)")
plt.show()
'''
for i in range(len(time)):
    ax.quiver(0,0,0, attitude_mat[i, 0, 0], inertial_mat[i, 1, 0], inertial_mat[i, 2, 0])
    plt.draw()
    plt.pause(0.001)
'''