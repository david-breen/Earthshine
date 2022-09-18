import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt


def Euler_motion(w, M, Idiag, t):

	wdhold = np.matmul((M - np.cross(w,(np.matmul(Idiag, w)))),
	                    np.linalg.inv(Idiag))

	return wdhold


def RK45_step(w, M, Idiag, time, deltat):

    k1 = Euler_motion(w, M, Idiag, time)
    k2 = Euler_motion(w + 0.5*k1, M, Idiag, time + 0.5*deltat)
    k3 = Euler_motion(w + 0.5*k2, M, Idiag, time + 0.5*deltat)
    k4 = Euler_motion(w + k3, M, Idiag, time + deltat)

    return deltat * ((k1 + 2*k2 + 2*k3 + k4) / 6)
