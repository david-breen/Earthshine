from cmath import cos
from math import atan2
import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from EulerDynamicsDeriver import *


def quaternion_rotation(quat0, quat1):

    w0, x0, y0, z0 = quat0
    w1, x1, y1, z1 = (-quat1)
    # this is just the hamiltonian product
    r0, r1, r2, r3 = np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)
    # find the vector and angle to rotate about
    normal = np.linalg.norm([r1,r2,r3])
    r_vector = np.divide([r1, r2, r3], normal)
    theta = atan2(normal, r0)
    return np.append(theta, r_vector)



if(__name__ == "__main__"):

  # Time stuff
  run_time = 10
  dt = 0.1

  # initial conditions
  Itensor = np.array([5,
                        5,
                          2])  # kg*m^2
  initial_velocity = [1, 1, -1]
  initial_attitude = [1, 0, 0, 0] # this will eventually be cube verticies
  moments = [0, 0, 0]

  velocity_mat, attitude_mat = simulate_dynamics(Itensor, initial_velocity,
                                                initial_attitude, moments,
                                                run_time, dt, just_last=False)

  bigO = ((Itensor[2]-Itensor[0])/Itensor[0])*2

  time = np.arange(1, (run_time), dt)
  errorx = np.empty((0,2), float)
  errory = np.empty((0,2), float)

  for t in range(len(time)):

    errorx = np.append(errorx, [3*np.cos(bigO * time[t])-velocity_mat[t][0]])
    errory = np.append(errory, [3*np.sin(bigO * time[t])-velocity_mat[t][1]])
    #print("quat")
    #print(attitude_mat[t][0], attitude_mat[t][3])
    #print("angle")
    #print(np.arccos(attitude_mat[t][0])*2 - np.arccos(attitude_mat[t-1][0])*2, np.arcsin(attitude_mat[t][3])*2 - np.arcsin(attitude_mat[t-1][3])*2)
    print("rotation")
    print(quaternion_rotation(attitude_mat[t-1],attitude_mat[t]))
  
'''
  fig, ax = plt.subplots(3, 2)
  ax[0][0].plot(time, velocity_mat[:, 0])
  ax[0][0].set_title("Numerical integration")
  ax[1][0].plot(time, velocity_mat[:, 1])
  ax[2][0].plot(time, velocity_mat[:, 3])
  ax[2][0].set_title("w3 Velocity")

  ax[0][1].plot(time, 3 * np.cos(bigO * time))
  ax[0][1].set_title("Analytical integration")
  ax[1][1].plot(time, 3 * np.sin(bigO * time) )

  ax[2][1].plot(velocity_mat[:, 0], velocity_mat[:, 1])
  ax[2][1].plot(3 * np.cos(bigO * time), 3 * np.sin(bigO * time))
  ax[2][1].set_title("f(w1,w2,t)")

  fig.suptitle("Numerically integrated vs Analytical Solutions for λ1=λ2 > λ3")
  plt.show()
'''