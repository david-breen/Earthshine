import numpy as np
from numpy.linalg import inv
from matplotlib import pyplot as plt


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
w = np.array([0, 1, 0], float)
O = np.array([0, 0, 0], float)
wdot = np.array([0, 0, 0])

thetadot = np.empty((0, 3), float)
theta = np.empty((0, 3), float)

print()

for t in time:

    if t < 100:

        M = np.array([0.008, 0.01, 0])   # N*m
    else:

        M = np.array([0, 0, 0])   # N*m

    w = w + np.diag(RK45_step(w, M, Itensor, t, dt))
    thetadot = np.append(thetadot, [w], axis=0)
    O = O + thetadot[-1] * dt
    theta = np.append(theta, [O], axis=0)
    


plt.plot(time, np.sin(theta[:, 0] * (np.pi / 2)))
plt.show()