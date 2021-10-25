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


class DisplayableAntenna(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    ##### TODO 1: Build Creature Parts
    # Build the class(es) of basic geometric objects/combination that could add up to be a part of your creature. 
    # E.g., you could write a cylinder class to be the trunk of your creature's limb. Or, you could 
    # write a two-sphere class to be the eye ball of your creature (one sphere for the eye ball and one sphere for the lens/iris).
    # The needed GLU functions for cylinder and sphere are mentioned in README.md



    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    r = 1
    height = 5
    top = 5
    _bufferData = None

    def __init__(self, parent, r, top, height, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.r = r
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale
        self.top = top
        self.height = height

    ##### BONUS 1: Texture your creature
    # Requirement: 1. Build the texture mapping that binds texture image to your objects. 

    def draw(self):
        gl.glCallList(self.callListHandle)

        # glu.gluCylinder(self.qd, self.edgeLength, self.edgeLength, self.edgeLength*2, 1, 16)
        # glu.gluCylinder(self.qd, self.r, 3, 16)



    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()
        gl.glScale(*self.scale)
        gl.glTranslate(0, self.r, 0)

        glu.gluSphere(self.qd, self.r, 5, 5)

        gl.glPushMatrix()
        gl.glRotatef(270, 1, 0, 0)
        glu.gluCylinder(self.qd, self.r, self.r, self.height, 5, 5)
        gl.glPopMatrix()

        gl.glPushMatrix()  # New joint rotate by 30 deg
        gl.glTranslate(0,self.height, 0)     # align middle of sphere with bottom cylinder to be created
        gl.glRotatef(15, 1, 0, 0)

        ''' 2nd sphere + cylinder '''
        gl.glPushMatrix()
        glu.gluSphere(self.qd, self.r, 5, 5)
        gl.glPopMatrix()


        gl.glPushMatrix()   # Enclosed Cylinder Transforms
        gl.glRotatef(270, 1, 0, 0)
        glu.gluCylinder(self.qd, self.r, self.r, self.height, 5, 5)
        gl.glPopMatrix()    # End enclosed cylinder transform

        ''' Topmost sphere + cylinder'''
        gl.glPushMatrix()   # Move up to prepare for appendage 2
        gl.glTranslate(0, self.height, 0)

        glu.gluSphere(self.qd, self.r, 5, 5)

        gl.glPushMatrix()   # Top appendage (cone)
        gl.glRotatef(300, 1, 0, 0)
        glu.gluCylinder(self.qd, self.r, 0, self.height + self.height / 2, 5, 5)
        gl.glPopMatrix()

        gl.glPopMatrix()    # Translations to prepare for appendage 2
        gl.glPopMatrix()    # second-cylinder 30 deg rotation



        gl.glPopMatrix()    # Scale Matrix
        gl.glEndList()






