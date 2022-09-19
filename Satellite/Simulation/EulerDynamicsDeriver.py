import numpy as np
import math
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt


def Euler_motion(w, M, Idiag, t):

	wdhold = np.matmul((M - np.cross(w,(np.matmul(Idiag, w)))),
	                    np.linalg.inv(Idiag))

	return wdhold


def RK45_step(w, M, Idiag, time, deltat, quat):

    kq1 = deltat * w_to_Qdot(w, quat)
    kw1 = deltat * Euler_motion(w, M, Idiag, time)

    kq2 = deltat * w_to_Qdot(w + kw1, quat + .5*kq1)
    kw2 = deltat * Euler_motion(w + 0.5*kw1, M, Idiag, time + 0.5*deltat)

    kq3 = deltat * w_to_Qdot(w + kw2, quat + .5*kq2)
    kw3 = deltat * Euler_motion(w + 0.5*kw2, M, Idiag, time + 0.5*deltat)

    kq4 = deltat * w_to_Qdot(w + kw3, quat + kq3)
    kw4 = deltat * Euler_motion(w + kw3, M, Idiag, time + deltat)

    new_w = w + ((kw1 + 2*kw2 + 2*kw3 + kw4) / 6)
    new_Q = quat + ((kq1 + 2*kq2 + 2*kq3 + kq4) / 6)
    new_Q = np.divide(new_Q, np.linalg.norm(new_Q))
    
    return new_w, new_Q


def w_to_Qdot(w, quat):

    rot = R.from_quat(quat)
    rot = rot.as_matrix()
    Qdot = rot * w
    rot = R.from_matrix(Qdot)
    Qdot = rot.as_quat()

    return Qdot
