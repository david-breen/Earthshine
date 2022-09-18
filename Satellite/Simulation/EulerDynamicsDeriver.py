import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt
import matplotlib.animation as animation



def Euler_motion(w, M, Idiag, t):

    wdhold = np.matmul(M - np.cross(w, (np.multiply(Idiag, w))),
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
initial_velocity = np.array([1, 0, 0], float)
initial_attitude = np.array([0, 0, 0], float)
initial_inertial = np.array([[ 0, 0, 0], [ 0, 0, 0], [ 0, 0, 0]], float)

velocity_mat = np.empty((0, 3), float)
attitude_mat = np.empty((0, 3), float)
inertial_mat = np.empty((0, 3, 3), float)

velocity_mat = np.append(velocity_mat, [initial_velocity], axis=0)
attitude_mat = np.append(attitude_mat, [initial_attitude], axis=0)
inertial_mat = np.append(inertial_mat, [initial_inertial], axis=0)
#quat = np.quaternion(1, 0, 0, 0)
M = np.array([0, 0, 0])


print(RK45_step(velocity_mat, M, Itensor, time, dt))



for t in time:

    if t < 100:

        M = np.array([0, 0, 0])   # N*m
    else:

        M = np.array([-0.014, -0.2, -1])   # N*m

    velocity_mat = np.append(velocity_mat, [velocity_mat[-1] +
                             np.diag(RK45_step(velocity_mat[-1],
                                               M, Itensor, t, dt))], axis=0)

    attitude_mat = np.append(attitude_mat,
                             [velocity_mat[-1] * dt],
                             axis=0)

    ror = R.from_euler('xyz', (attitude_mat[-1]))

   

    inertial_mat = np.append(inertial_mat,
                             [ror.as_matrix()],
                             axis=0)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
plt.plot(time, (np.sin(velocity_mat[1:, 1])))
plt.show()

for i in range(len(time)):
    ax.quiver(0,0,0, inertial_mat[i, 0, 0], inertial_mat[i, 1, 0], inertial_mat[i, 2, 0])
    plt.draw()
    plt.pause(0.001)
    