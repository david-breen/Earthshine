import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R


verticies = np.reshape(np.mgrid[-1:2:2,-1:2:2,-1:2:2].T, (8,3))

edges = (

    (0,1), (0,3), (0,4), (2,1),
    (2,3), (2,7), (6,3), (6,4), 
    (6,7), (5,1), (5,4), (5,7)
)


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

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslate(0.0, 0.0, -5)

    glRotatef(0, 0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        glRotatef(1, 0, 2, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        space_craft()
        pygame.display.flip()
        pygame.time.wait(10)


main()