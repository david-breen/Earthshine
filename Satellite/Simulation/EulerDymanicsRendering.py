from math import atan2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R
from EulerDynamicsDeriver import *


# Initial physical conditions to generate the verticies

Itensor = np.array([2, 2, 5])  # kg*m^2
trans_mat = np.diag(Itensor)

verticies = np.reshape(np.mgrid[-1:2:2,-1:2:2,-1:2:2].T, (8,3))

verticies = np.matmul(verticies, trans_mat)


# Connections between the verticies
edges = (

    (0,1), (0,2), (0,4), (3,2),
    (3,7), (3,1), (5,7), (5,4),
    (5,1), (6,4), (6,7), (6,2)

)

# spacecraft function for drawing the new spacecraft
def space_craft():

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()

#function to rotate the verticies by the new quat value
# Q0-1 = Q0 * -Q1
def quaternion_rotation(quat0, quat1):
    
    print(np.linalg.norm(quat1))
    if (quat1[0]*quat0[0]) < 0:
        quat0[1], quat0[2], quat0[3] = -quat0[1], -quat0[2], -quat0[3]

    a1, b1, c1, d1 = quat0
    b1, c1, d1 = -b1, -c1, -d1
    a2, b2, c2, d2 = quat1

   

    # this is just the hamiltonian product
    r0, r1, r2, r3 = np.array([a1*a2 - b1*b2 - c1*c2 - d1*d2,
                               a1*b2 + b1*a2 + c1*d2 - d1*c2,
                               a1*c2 - b1*d2 + c1*a2 + d1*b2,
                               d1*a2 + b1*c2 - c1*b2 + d1*a2
                              ], dtype=np.float64)
    
    # find the vector and angle to rotate about
    normal = np.linalg.norm([r1,r2,r3])
    r_vector = np.divide([r1, r2, r3], normal)
    theta = np.degrees(2* np.arccos(r0))

    return np.append(theta, r_vector)


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslate(0.0, 0.0, -20)
    glRotatef(0, 0, 0, 0)

    # Time stuff
    run_time = 10 
    dt = 0.01

    # initial conditions
    initial_velocity = [0, 0, 2]    # rad/s
    initial_attitude = [1, 0, 0, 0] # Unit quaternion orientation
    moments = [0, 0, 0]     # Moments applied to the spacecraft in the B frame


    velocity_mat, attitude_mat = simulate_dynamics(Itensor,
                                                   initial_velocity,
                                                   initial_attitude,
                                                   moments,
                                                   run_time,
                                                   dt,
                                                   just_last=False)


    for t in  np.arange(1,1001):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN & event.type == pygame.KEYUP:
                               
                if event.mod & pygame.K_w:
                    print('Left shift was in a pressed state when this event '
                            'occurred.')
                
        # function for simulating the dynamics at a time stepw

        
        O, x, y ,z = quaternion_rotation(attitude_mat[t-1],attitude_mat[t])
        #print([O, x, y, z])
        glRotatef(O, x, y, z)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        space_craft()
        pygame.display.flip()
        pygame.time.wait(10)


main()