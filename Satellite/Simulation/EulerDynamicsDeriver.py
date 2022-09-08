import numpy as np
from numpy.linalg import inv
from matplotlib import pyplot as plt


def RK45_step(x, y, z, t, dt):
    k1 = G(x, t)
    k2 = G(x + 0.5*k1*dt, t + 0.5*dt)
    k3 = G(x + 0.5*k2*dt, t + 0.5*dt)
    k4 = G(y + k3*dt, t + dt)

    return dt * ((k1 + 2*k2 + 2*k3 + k4) / 6)


def Euler_motion():
    wd1 = (M1[0]-(I3[0]-I2[0])*w2[0]*w3[0]) / I1
    wd2 = (M2[0]-(I1[0]-I3[0])*w3[0]*w1[0]) / I2
    wd1 = (M3[0]-(I2[0]-I1[0])*w1[0]*w2[0]) / I3

    return [wd1, wd2, wd3]

# variables
t = 0
dt = 0.1

Itensor = np.array([[1, 0, 0],[0, 1, 0,],[0, 0, 1]])  #kg*m^2

w = np.array([[0], [0], [0]])
wdot = np.array([[0],[0],[0]])

I1 = Itensor[0, 0]
I2 = Itensor[1, 1]
I3 = Itensor[2, 2]

w1 = np.array([])   # rad/s
w2 = np.array([])
w3 = np.array([])

wd1 = np.array([])  # rad/s^2
wd2 = np.array([])
wd3 = np.array([])

M1 = np.array([])   # N*m
M2 = np.array([])
M3 = np.array([])





