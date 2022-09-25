from math import atan2
import numpy as np
from matplotlib import pyplot as plt
from EulerDynamicsDeriver import *
import unittest




def quaternion_rotation(quat0, quat1):

    a1, b1, c1, d1 = np.conjugate(quat0)
    #b1, c1, d1 = -b1, -c1, -d1
    a2, b2, c2, d2 = quat1

    print([a1, b1, c1, d1])

    # this is just the hamiltonian product
    r0, r1, r2, r3 = np.array([a1*a2 - b1*b2 - c1*c2 - d1*d2,
                               a1*b2 + b1*a2 + c1*d2 - d1*c2,
                               a1*c2 - b1*d2 + c1*a2 + d1*b2,
                               d1*a2 + b1*c2 - c1*b2 + d1*a2
                              ], dtype=np.float64)
    
    # find the vector and angle to rotate about
    theta = np.degrees(np.arccos(r0))
    normal = np.linalg.norm([r1, r2, r3])
    theta2 = np.arctan2(normal, r0)
    if r1 == r2 == r3 == 0:
        r_vector = [0, 0, 0]
    else:
      r_vector = np.divide([r1, r2, r3], np.sin(theta))

    

    return np.append(2*theta, r_vector)


class TestDynamics(unittest.TestCase):
  
  def test_full_rotation(self):
      rotation = quaternion_rotation([1,0,0,0],[0,0,0,1])



if(__name__ == "__main__"):


  print(quaternion_rotation([1,0,0,0],[0,0,0,1]))



  '''
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



