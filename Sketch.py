'''
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun), Matt Firmin (firminm@bu.edu)
:version: 2021.2.1
:Changes (Matt Firmin)
 - Desinged an ant creature using ModelAnt.py
 - Changed functionality to allow overriding the regular select use to a custom multi-select use by using key: "m" to select/deselect
 - Changed default rotation feature to allow for opposible/reflected limbs
:Overall changes - there are a lot of unneeded Displayable/linkage files... if it's not used by ModelAnt.py, ignore

'''
import os
import wx
import time
import math
import random
import numpy as np

import ColorType
from Point import Point
import ColorType as CT
from ColorType import ColorType
from Quaternion import Quaternion
from Component import Component
# from DisplayableCube import DisplayableCube
from DisplayableHead import DisplayableHead
from CanvasBase import CanvasBase
from ModelLinkage import ModelLinkage
from ModelAxes import ModelAxes
from AntennaLinkage import AntennaLinkage
from HeadLinkage import HeadLinkage
from ArmLinkage import ArmLinkage
from BodyLinkage import BodyLinkage
from ModelLegs import ModelLegs
from ModelAnt import ModelAnt



try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
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


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    components = None
    select_obj_index = -1  # index in components
    multi_select = [] # index that new limbs are being appended to
    dft_obj_linkage = [[0], [1], [2], [3], [4], [5], [6], [7],
                       [8, 11], [9, 12], [10, 13], [11, 8], [12, 9], [13, 10],
                       [14], [15]]
    obj_linkage = dft_obj_linkage.copy()
    select_axis_index = -1  # index of select axis
    select_color = [ColorType(1, 0, 0), ColorType(0, 1, 0), ColorType(0, 0, 1)]
    multi_select_color = [ColorType(1, 0, 1), ColorType(0, 1, 1), ColorType(1, 1, 0)]
    pose = 0

    def __init__(self, parent):
        """
        Init everything. You should set your model here.
        """
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        self.context = glcanvas.GLContext(self)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]

        ##### TODO 3: Import Your Creature
        # You should instance your creature class here, and add it as self.topLevelComponent's Child

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural way
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.

        m1 = ModelAxes(self, Point((0, 0, 0)))  # coordinate system with x, y, z axes
        m2 = ModelAnt(self, Point((0, 0, 0)))
        # head = HeadLinkage(self, Point((0, 1, 0)))
        self.topLevelComponent.addChild(m1)
        self.topLevelComponent.addChild(m2)
        # self.topLevelComponent.addChild(head)

        self.components = m1.components + m2.components



    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        wheelChange = wheelRotation / abs(wheelRotation)  # normalize wheel change

        rotation_sign = 1
        if len(self.multi_select) > 0:
            for item in self.multi_select:
                self.components[item].rotate(wheelChange * 5 * rotation_sign,
                                             self.components[item].
                                             axisBucket[self.select_axis_index])

        elif len(self.components) > self.select_obj_index >= 0:
            for item in self.obj_linkage[self.select_obj_index]:
                self.components[item].rotate(wheelChange * 5 * rotation_sign,
                                             self.components[item].
                                             axisBucket[self.select_axis_index])
                if self.select_axis_index != 0: # change on z & y rotation
                    rotation_sign *= -1

        # if len(self.components) > self.select_obj_index >= 0:
        #     self.components[self.select_obj_index].rotate(wheelChange * 5,
        #                                                   self.components[self.select_obj_index].
        #                                                   axisBucket[self.select_axis_index])
        self.update()

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """
        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]
        mag = math.sqrt(dx * dx + dy * dy)
        axis = (dy / mag, -dx / mag, 0) if mag != 0 else (1, 0, 0)
        viewing_delta = 3.14159265358 / 180
        s = math.sin(0.5 * viewing_delta)
        c = math.cos(0.5 * viewing_delta)
        q = Quaternion(c, s * axis[0], s * axis[1], s * axis[2])
        self.viewing_quaternion = q.multiply(self.viewing_quaternion)
        self.viewing_quaternion.normalize()  # to correct round-off error caused by cos/sin
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.modelUpdate()

    def Interrupt_MouseMoving(self, x, y):
        ##### BONUS 2 (TODO 6 for CS680 student): Finishing touch - eyes!
        # Requirements:
        #   1. Add eyes to the creature model, for each it consists of an eyeball and pupil.
        #   2. Make eyes automatically follow the mouse position by rotating the eyeball.
        #   3. (extra credits) Use quaternion to implement the eyeball rotation
        pass

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """
        ##### TODO 5: Define creature poses and set interface to iterate through them
        # Requirements:
        #   1. Set 5 different poses of the creature.
        #   2. Add a keyboard interface "T" to cycle through the poses.
        #   3. Add multi-select feature to the interface, so you can change multiple joints at the same time. 

        if keycode in [wx.WXK_RETURN]:
            # enter component editing mode
            # iterate_loop = [[0],[1],[2],[3],[4],[1,3],[2,4]]
            # self.obj_iterate_index

            if len(self.components) > self.select_obj_index >= 0:
                for item in self.obj_linkage[self.select_obj_index]:
                    if len(self.multi_select) == 0:
                        self.components[item].reset("color")
                    elif item not in self.multi_select:
                        self.components[item].reset("color")
                # self.components[self.select_obj_index].reset("color")

            self.select_axis_index = 0
            if len(self.components) > 0:
                if self.select_obj_index < 0:
                    self.select_obj_index = 0
                else:
                    self.select_obj_index = (self.select_obj_index + 1) % len(self.components)

            if len(self.components) > self.select_obj_index >= 0:
                for item in self.obj_linkage[self.select_obj_index]:
                    if len(self.multi_select) == 0 or item not in self.multi_select:
                        self.components[item].setCurrentColor(self.select_color[self.select_axis_index])

                # self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis of this component
            self.select_axis_index = (self.select_axis_index - 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                if len(self.multi_select) == 0:
                    for item in self.obj_linkage[self.select_obj_index]:
                        self.components[item].setCurrentColor(self.select_color[self.select_axis_index])
                else:
                    for item in self.multi_select:
                        self.components[item].setCurrentColor(self.multi_select_color[self.select_axis_index])
                # self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis of this component
            self.select_axis_index = (self.select_axis_index + 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                if len(self.multi_select) == 0:
                    for item in self.obj_linkage[self.select_obj_index]:
                        self.components[item].setCurrentColor(self.select_color[self.select_axis_index])
                else:
                    for item in self.multi_select:
                        self.components[item].setCurrentColor(self.multi_select_color[self.select_axis_index])
                # self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            self.Interrupt_Scroll(1)
            self.update()
        if keycode in [wx.WXK_DOWN]:
            # Decrease rotation angle
            self.Interrupt_Scroll(-1)
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()
        if chr(keycode) in "r":
            # reset viewing angle only
            self.viewing_quaternion = Quaternion()
        if chr(keycode) in "R":
            # reset everything
            for c in self.components:
                c.reset()
            self.viewing_quaternion = Quaternion()
            self.select_obj_index = 0
            self.select_axis_index = 0
            self.multi_select.clear()
            self.pose = 0
            self.update()
        if chr(keycode) in "m":
            # Multi-Select toggle
            if len(self.components) > self.select_obj_index >= 0:
                if len(self.multi_select) > 0 and self.select_obj_index in self.multi_select:
                    self.multi_select.remove(self.select_obj_index)
                    self.components[self.select_obj_index].reset("color")
                else:
                    self.multi_select.append(self.select_obj_index)
                    self.components[self.select_obj_index].setCurrentColor(self.multi_select_color[self.select_axis_index])
            self.update()
        if chr(keycode) in "c":
            # clear multi-select
            for item in self.multi_select:
                self.components[item].reset("color")
            self.multi_select.clear()
            self.update()
        if chr(keycode) in "t":
            x = 0
            y = 1
            z = 2
            tr = None
            for c in self.components:
                c.reset()
            if self.pose == 0:
                tr = [
                    [1, 3, x], [2, -10, x], [3, 0, x], [5, -10, x], [8, -3, x] , [8, -7, y],
                    [14, -3, x], [15, 3, x], [11, -3, x], [11, 7, y]
                ]
            elif self.pose == 1:
                tr = [
                    [8, 3, x], [8, 12, y], [8, 1, z], [11, 3, x], [11, -12, y], [11, 1, z],
                    [1, 6, x], [2, -6, z], [3, 4, z], [4, -3, x], [5, -10, x], [5, -4, z], [6, -4, z],
                    [12, -40, y], [9, -40, y],
                    [14, -3, x], [15, 3, x]
                ]
            elif self.pose == 2:
                tr = [
                    [3, 20, z], [4, 10, z], [5, 50, x], [6, -20, z], [7, -10, z], [8, 50, x],
                    [9, 60, z], [11, 60, z]
                ]
            elif self.pose == 3:
                tr = [
                    [3, 20, z], [4, 15, z], [5, 50, x], [6, -20, z], [7, 30, z], [8, 50, x],
                    [9, 60, z], [11, -60, z]
                ]
            elif self.pose == 4:
                tr = [
                    [1, 3, x], [2, -15, x], [3, 0, x], [5, -5, x], [8, 3, x], [8, -7, y],
                    [14, -3, x], [15, 3, x], [11, -3, x], [11, 7, y],
                    [4, 10, z], [5, 50, x]
                ]
            if tr is not None:
                for item in tr:
                    self.components[item[0]].rotate(item[1] * 5,
                                                                  self.components[item[0]].
                                                                  axisBucket[item[2]])

            self.pose = (self.pose + 1) % 6
            self.update()



if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
