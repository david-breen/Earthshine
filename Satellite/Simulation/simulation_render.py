from math import atan2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R
from euler_dynamics import *


# Initial physical conditions to generate the verticies

Itensor = np.array([2, 5, 2])  # kg*m^2
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


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    #Initialize the display
    gluPerspective(20, (display[0]/display[1]), 0.1, 70.0)
    glTranslate(0.0, 0.0, -60)
    glRotatef(0, 0, 0, 0)

    # Time stuff
    run_time = 0.1
    dt = 0.001

    # initial conditions
    initial_velocity = [1, 0, 0]    # rad/s
    initial_attitude = [1, 0, 0, 0] # Unit quaternion orientation [s, i, j, k]
    moments = [0, 0, 0]     # Moments applied to the spacecraft in the B frame

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            

        velocity_mat, attitude_mat = simulate_dynamics(Itensor,
                                                   initial_velocity,
                                                   initial_attitude,
                                                   moments,
                                                   run_time,
                                                   dt,
                                                   just_last=True)
        
        O, x, y ,z = quaternion_rotation(initial_attitude, attitude_mat)
        initial_attitude = attitude_mat
        initial_velocity = velocity_mat
        
        glRotatef(O, x, y, z)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        space_craft()
        pygame.display.flip()
        pygame.time.wait(10)


main()