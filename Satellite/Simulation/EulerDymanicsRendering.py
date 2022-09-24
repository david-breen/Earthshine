import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R
from EulerDynamicsDeriver import *



Itensor = np.array([2, 2, 5])  # kg*m^2
trans_mat = np.diag(Itensor)


verticies = np.reshape(np.mgrid[-1:2:2,-1:2:2,-1:2:2].T, (8,3))
print(verticies)

verticies = np.matmul(verticies, trans_mat)



edges = (

    (0,1), (0,2), (0,4), (3,2),
    (3,7), (3,1), (5,7), (5,4),
    (5,1), (6,4), (6,7), (6,2)

)


def space_craft():

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])

    glEnd()


def quaternion_rotation(quat0, quat1):

    w0, x0, y0, z0 = quat0
    w1, x1, y1, z1 = (-quat1)
    
    
    
    r0, r1, r2, r3 = np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                     x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                     -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                     x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)

    normal = np.linalg.norm([r1,r2,r3])
    r_vector = np.divide([r1, r2, r3], normal)
    theta = 2* np.arctan2(normal, r0)
    return np.append(theta, r_vector)


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslate(0.0, 0.0, -20)

    glRotatef(0, 0, 0, 0)


    # Time stuff
    run_time = 0.1
    dt = 0.001

    # initial conditions
    Itensor = np.array([5,
                          5,
                            2])  # kg*m^2
    initial_velocity = [1, 0, 2]
    initial_attitude = [1, 0, 0, 0] # this will eventually be cube verticies
    moments = [0, 0, 0]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        velocity_mat, attitude_mat = simulate_dynamics(Itensor, initial_velocity,
                                                initial_attitude, moments,
                                                run_time, dt, just_last=True)
        O, x, y ,z = quaternion_rotation(initial_attitude,attitude_mat)
        glRotatef(O, x, y, z)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        space_craft()
        pygame.display.flip()
        pygame.time.wait(10)


main()