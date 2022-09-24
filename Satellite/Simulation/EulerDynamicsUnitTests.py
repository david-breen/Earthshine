from cmath import cos
import numpy as np
from scipy.spatial.transform import Rotation as R
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from EulerDynamicsDeriver import *



if(__name__ == "__main__"):

  # Time stuff
  run_time = 1
  dt = 0.01

  # initial conditions
  Itensor = np.array([1,
                        1,
                          1])  # kg*m^2
  initial_velocity = [0, 0, (2*np.pi)/8]
  initial_attitude = [1, 0, 0, 0] # this will eventually be cube verticies
  moments = [0, 0, 0]


  velocity_mat, attitude_mat = simulate_dynamics(Itensor, initial_velocity,
                                                initial_attitude, moments,
                                                run_time, dt, just_last=False)
  '''
  moments = [0, 0, 0]

  velocity_mat2, attitude_mat2 = simulate_dynamics(Itensor, velocity_mat[-1],
                                                attitude_mat[-1], moments,
                                                run_time, dt, just_last=False)


  velocity_mat = np.append(velocity_mat, velocity_mat2, axis=0)
  '''

  bigO = ((Itensor[2]-Itensor[0])/Itensor[0])*2


  time = np.arange(0, (run_time + dt), dt)
  errorx = np.empty((0,2), float)
  errory = np.empty((0,2), float)

  for t in range(len(time)):

    errorx = np.append(errorx, [3*np.cos(bigO * time[t])-velocity_mat[t][0]])
    errory = np.append(errory, [3*np.sin(bigO * time[t])-velocity_mat[t][1]])
  
  print(attitude_mat[-1])

  fig, ax = plt.subplots(3, 2)
  ax[0][0].plot(time, velocity_mat[:, 0])
  ax[0][0].set_title("Numerical integration")
  ax[1][0].plot(time, velocity_mat[:, 1])
  ax[2][0].plot(errorx, errory)
  ax[2][0].set_title("w3 Velocity")

  ax[0][1].plot(time, 3 * np.cos(bigO * time))
  ax[0][1].set_title("Analytical integration")
  ax[1][1].plot(time, 3 * np.sin(bigO * time) )

  ax[2][1].plot(velocity_mat[:, 0], velocity_mat[:, 1])
  ax[2][1].plot(3 * np.cos(bigO * time), 3 * np.sin(bigO * time))
  ax[2][1].set_title("f(w1,w2,t)")

  fig.suptitle("Numerically integrated vs Analytical Solutions for λ1=λ2 > λ3")
  plt.show()
