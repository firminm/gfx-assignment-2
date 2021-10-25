"""
Create a x, y, z coordinate on canvas
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from ModelAxes import ModelAxes
from AntennaLinkage import AntennaLinkage
from HeadLinkage import HeadLinkage
from ArmLinkage import ArmLinkage
from BodyLinkage import BodyLinkage
from ModelLegs import ModelLegs
from DisplayableEye import DisplayableEye
from DisplayableConeJoint import DisplayableConeJoint
from DisplayableJoint import DisplayableJoint
from DisplayableHead import DisplayableHead
from DisplayableArmJoint import DisplayableArmJoint
from DisplayablePinser import DisplayablePinser
from DisplayableLeg import DisplayableLeg

class ModelAnt(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        shrink = .5
        scale = .5  # Set < 1 if want to flatten
        r = scale

        # build full head (face + eyes + antenna)
        head = Component(Point((0, 1, 0)), DisplayableHead(self.contextParent, 1, [r, r * 1.1, r]))
        head.setDefaultColor(Ct.DARKORANGE2)
        head.setRotateExtent(head.uAxis, -30, 15)
        head.setRotateExtent(head.vAxis, -30, 30)
        head.setRotateExtent(head.wAxis, -10, 10)

        eye1 = Component(Point((r / 2, r / 10, r - r / 3)), DisplayableEye(self.contextParent, .55, 1, [r / 2, r / 2, r / 2]))
        eye2 = Component(Point((r / (-2), r / 10, r - r / 3)), DisplayableEye(self.contextParent, .55, 1, [r / 2, r / 2, r / 2]))

        antenna1 = Component(Point((-.25, .4, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna1.setDefaultColor(Ct.DARKORANGE3)
        antenna2 = Component(Point((0, .75 * shrink, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna2.setDefaultColor(Ct.DARKORANGE3)
        antenna3 = Component(Point((0, .75 * shrink, 0)), DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna3.setDefaultColor(Ct.DARKORANGE3)
        antenna4 = Component(Point((.25, .4, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna4.setDefaultColor(Ct.DARKORANGE3)
        antenna5 = Component(Point((0, .75 * shrink, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna5.setDefaultColor(Ct.DARKORANGE3)
        antenna6 = Component(Point((0, .75 * shrink, 0)), DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna6.setDefaultColor(Ct.DARKORANGE3)
        # Set Extents
        antenna1.setRotateExtent(antenna1.uAxis, -50, 50)
        antenna1.setRotateExtent(antenna1.vAxis, -10, 10)
        antenna1.setRotateExtent(antenna1.wAxis, -20, 20)
        antenna4.setRotateExtent(antenna2.uAxis, -50, 50)
        antenna4.setRotateExtent(antenna1.vAxis, -10, 10)
        antenna4.setRotateExtent(antenna1.wAxis, -20, 20)

        antenna2.setRotateExtent(antenna1.uAxis, -60, 60)
        antenna2.setRotateExtent(antenna1.vAxis, -10, 10)
        antenna2.setRotateExtent(antenna1.wAxis, -20, 20)
        antenna5.setRotateExtent(antenna1.uAxis, -60, 60)
        antenna5.setRotateExtent(antenna1.vAxis, -10, 10)
        antenna5.setRotateExtent(antenna1.wAxis, -20, 20)
        antenna3.setRotateExtent(antenna1.uAxis, -60, 60)
        antenna3.setRotateExtent(antenna1.vAxis, -10, 10)
        antenna3.setRotateExtent(antenna1.wAxis, -60, 60)
        antenna6.setRotateExtent(antenna1.uAxis, -60, 60)
        antenna6.setRotateExtent(antenna1.vAxis, -25, 25)
        antenna6.setRotateExtent(antenna1.wAxis, -20, 20)

        # Build the body
        scale = .4  # Set < 1 if want to flatten
        r = scale
        body = Component(Point((0, -.2, 0)), DisplayableHead(self.contextParent, 1, [r, r + r, r]))
        body.setDefaultColor(Ct.DARKORANGE2)
        body.setRotateExtent(antenna1.uAxis, -180, 180)
        body.setRotateExtent(antenna1.vAxis, -180, 180)
        body.setRotateExtent(antenna1.wAxis, -180, 180)

        # Build the arms
        shrink = 0.5  # Set < 1 if want to flatten
        x = (0, 1 * shrink, .75 * shrink)

        joint1 = Component(Point((-.4, .1, 0)), DisplayableArmJoint(self.contextParent, 0.2, 1, [.5, 0.5, shrink]))
        joint1.setDefaultColor(Ct.DARKORANGE3)
        joint1.setDefaultAngle(180, joint1.wAxis)
        joint2 = Component(Point((x[1], 0, 0)), DisplayableArmJoint(self.contextParent, 0.2, .75, [.5, 0.5, shrink]))
        joint2.setDefaultColor(Ct.DARKORANGE3)
        # joint2.setDefaultAngle(180, joint1.uAxis)
        pinser = Component(Point((x[2], 0, 0)), DisplayablePinser(self.contextParent, 0.2, .75, [.5, 0.6, shrink]))
        pinser.setDefaultColor(Ct.DARKORANGE3)
        joint3 = Component(Point((.4, 0.1, 0)), DisplayableArmJoint(self.contextParent, 0.2, 1, [.5, 0.5, shrink]))
        joint3.setDefaultColor(Ct.DARKORANGE3)
        joint4 = Component(Point((x[1], 0, 0)), DisplayableArmJoint(self.contextParent, 0.2, .75, [.5, 0.5, shrink]))
        joint4.setDefaultColor(Ct.DARKORANGE3)
        pinser2 = Component(Point((x[2], 0, 0)), DisplayablePinser(self.contextParent, 0.2, .75, [.5, 0.6, shrink]))
        pinser2.setDefaultColor(Ct.DARKORANGE3)

        # swap v axis extrema
        joint1.setRotateExtent(antenna1.uAxis, -15, 15)         # u = z axis
        joint1.setRotateExtent(antenna1.vAxis, -35, 95)         # w = x axis
        joint1.setRotateExtent(antenna1.wAxis, 120, 240)            # w = z axis
        joint3.setRotateExtent(antenna1.uAxis, -15, 15)
        joint3.setRotateExtent(antenna1.vAxis, -95, 35)
        joint3.setRotateExtent(antenna1.wAxis, -60, 60)
        joint2.setRotateExtent(antenna1.uAxis, -10, 10)
        joint2.setRotateExtent(antenna1.vAxis, -60, 10)
        joint2.setRotateExtent(antenna1.wAxis, -60, 60)
        joint4.setRotateExtent(antenna1.uAxis, -10, 10)
        joint4.setRotateExtent(antenna1.vAxis, -60, 10)
        joint4.setRotateExtent(antenna1.wAxis, -60, 60)
        pinser.setRotateExtent(antenna1.uAxis, -30, 30)
        pinser.setRotateExtent(antenna1.vAxis, -15, 45)
        pinser.setRotateExtent(antenna1.wAxis, -60, 60)
        pinser2.setRotateExtent(antenna1.uAxis, -10, 10)
        pinser2.setRotateExtent(antenna1.vAxis, -45, 15)
        pinser2.setRotateExtent(antenna1.wAxis, -60, 60)


        # Make Legs
        # leg1 = ModelLegs(self, Point((-.2, -1, 0)))
        # leg2 = ModelLegs(self, Point((0.2, -1, 0)))
        leg1 = Component(Point((-0.2, -1, 0)), DisplayableLeg(self.contextParent, 1, 1, [.15, .5, .15]))
        leg1.setDefaultColor(Ct.DARKORANGE3)
        leg1.setRotateExtent(leg1.uAxis, -10, 10)
        leg1.setRotateExtent(leg1.uAxis, -15, 15)
        leg1.setRotateExtent(leg1.wAxis, -5, 0)

        leg2 = Component(Point((0.2, -1, 0)), DisplayableLeg(self.contextParent, 1, 1, [.15, .5, .15]))
        leg2.setDefaultColor(Ct.DARKORANGE3)
        leg2.setRotateExtent(leg2.uAxis, -15, 15)
        leg2.setRotateExtent(leg2.uAxis, -15, 15)
        leg2.setRotateExtent(leg2.wAxis, 0, 5)


        # Begin Linking
        self.addChild(body)
        body.addChild(joint1)
        joint1.addChild(joint2)
        joint2.addChild(pinser)
        body.addChild(joint3)
        joint3.addChild(joint4)
        joint4.addChild(pinser2)

        body.addChild(leg1)
        body.addChild(leg2)

        body.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)

        head.addChild(antenna1)
        antenna1.addChild(antenna2)
        antenna2.addChild(antenna3)

        head.addChild(antenna4)
        antenna4.addChild(antenna5)
        antenna5.addChild(antenna6)

        self.components = [body, head, antenna1, antenna2, antenna3, antenna4, antenna5, antenna6,
                           joint1, joint2, pinser, joint3, joint4, pinser2,
                           leg1, leg2]
        # [[0], [1], [2], [3], [4], [5], [6], [7],
        # [8, 11], [9, 12], [10, 13], [11, 8], [12, 9], [13, 10],
        # [14], [15]]
