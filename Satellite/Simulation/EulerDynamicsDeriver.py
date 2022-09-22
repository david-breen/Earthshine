import numpy as np
from scipy.spatial.transform import Rotation as R


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


def simulate_dynamics(I_diag, init_velo, attitude, moments, run_time, dt,
                      just_last=True):

    # Time stuff
    time = np.arange(0, run_time, dt)

    # initial conditions
    initial_velocity = np.array([3, 0, 2], float)
    initial_attitude = np.array([0, 1, 0, 0], float) # this will eventually be cube verticies
    Itensor = np.array([[I_diag[0], 0, 0], [0, I_diag[1], 0], [0, 0, I_diag[2]]])  # kg*m^2
    initial_velocity = np.array(init_velo, float)
    initial_attitude = np.array(attitude, float)
    M = np.array(moments)

    # Matrix initalization

    velocity_mat = np.empty((0, 3), float)
    attitude_mat = np.empty((0, 4), float)

    velocity_mat = np.append(velocity_mat, [initial_velocity], axis=0)
    attitude_mat = np.append(attitude_mat, [initial_attitude], axis=0)

    for t in time:

        w_hold, Q_hold = RK45_step(velocity_mat[-1], M, Itensor, time, dt,
                                   attitude_mat[-1])

        velocity_mat = np.append(velocity_mat, [w_hold] , axis=0)
        attitude_mat = np.append(attitude_mat, [Q_hold], axis=0)

    if(just_last == False):
        return velocity_mat, attitude_mat
    else:
        return velocity_mat[-1], attitude_mat[-1]


if __name__ == "__main__":

    print("testing")
