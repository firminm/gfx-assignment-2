'''
A test object which defines a primitive shape for rendering
All primitive shapes must inherit from Displayable class
First version in 10/21/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1
'''
from math import pi
import os
import numpy as np
import string

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Displayable import Displayable


class DisplayableJoint(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """
    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    r = 1
    height = 5
    _bufferData = None

    def __init__(self, parent, radius, height, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.r = radius
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale
        self.height = height

    ##### BONUS 1: Texture your creature
    # Requirement: 1. Build the texture mapping that binds texture image to your objects.

    def draw(self):
        gl.glCallList(self.callListHandle)



    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()
        gl.glScale(*self.scale)

        # Results in middle of joint at y=0
        glu.gluSphere(self.qd, self.r, 8, 8)

        gl.glPushMatrix()
        gl.glRotatef(270, 1, 0, 0)
        glu.gluCylinder(self.qd, self.r, self.r, self.height, 5, 5)
        gl.glPopMatrix()

        gl.glPopMatrix()    # Scale Matrix
        gl.glEndList()






