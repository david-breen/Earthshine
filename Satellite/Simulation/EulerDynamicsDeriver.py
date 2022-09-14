import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import quaternion


def Euler_motion(w, M, Idiag, t):

    wdhold = np.multiply(M - np.cross(w, (np.multiply(Idiag, w))),
                         np.linalg.inv(Idiag))
    return wdhold


def RK45_step(w, M, Idiag, time, deltat):

    k1 = Euler_motion(w, M, Idiag, time)
    k2 = Euler_motion(w+0.5*k1, M, Idiag, time + 0.5*deltat)
    k3 = Euler_motion(w + 0.5*k2, M, Idiag, time + 0.5*deltat)
    k4 = Euler_motion(w + k3*dt, M, Idiag, time + deltat)

    return deltat * ((k1 + 2*k2 + 2*k3 + k4) / 6)


# variables
dt = 0.1
time = np.arange(0, 100, dt)

Itensor = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # kg*m^2
initial_velocity = np.array([0, 1, 0], float)
initial_attitude = np.array([0, 0, 0], float)
velocity_mat = np.empty((0, 3), float)
attitude_mat = np.empty((0, 3), float)
velocity_mat = np.append(velocity_mat, [initial_velocity], axis=0)
attitude_mat = np.append(attitude_mat, [initial_attitude], axis=0)
quat = np.quaternion(1, 0, 0, 0)


for t in time:

    if t < 50:

        M = np.array([0.008, 0.01, 0])   # N*m
    else:

        M = np.array([-0.014, -0.02, -1])   # N*m

    velocity_mat = np.append(velocity_mat, [velocity_mat[-1] +
                             np.diag(RK45_step(velocity_mat[-1],
                                               M, Itensor, t, dt))], axis=0)
    attitude_mat = np.append(attitude_mat,
                             [attitude_mat[-1] + velocity_mat[-1] * dt],
                             axis=0)


fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.set_rmin(0)
ax.set_rmax(1)

ax.quiver(0,0,0,1, color='black', angles="xy", scale_units='xy', scale=1.)
#plt.plot(time, (attitude_mat[1:, 0] % (np.pi * 2)))
plt.show()
