"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableHead import DisplayableHead
from DisplayableEye import DisplayableEye
from DisplayableConeJoint import DisplayableConeJoint
from DisplayableJoint import DisplayableJoint
from AntennaLinkage import AntennaLinkage



class HeadLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature.

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        shrink = .5
        scale = .5  # Set < 1 if want to flatten
        r = scale

        head = Component(Point((0, 0, 0)), DisplayableHead(self.contextParent, 1, [r, r*1.1, r]))
        head.setDefaultColor(Ct.DARKORANGE2)

        eye1 = Component(Point((r/2, r/10, r - r/3)), DisplayableEye(self.contextParent, .55, 1, [r/2, r/2, r/2]))
        eye2 = Component(Point((r/(-2), r/10, r - r/3)), DisplayableEye(self.contextParent, .55, 1, [r/2, r/2, r/2]))

        antenna1 = Component(Point((-.25, .4, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna1.setDefaultColor(Ct.DARKORANGE3)
        antenna2 = Component(Point((0, .75 * shrink, 0)),
                             DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna2.setDefaultColor(Ct.DARKORANGE3)
        antenna3 = Component(Point((0, .75 * shrink, 0)),
                             DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna3.setDefaultColor(Ct.DARKORANGE3)

        antenna4 = Component(Point((.25, .4, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna4.setDefaultColor(Ct.DARKORANGE3)
        antenna5 = Component(Point((0, .75 * shrink, 0)),
                             DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna5.setDefaultColor(Ct.DARKORANGE3)
        antenna6 = Component(Point((0, .75 * shrink, 0)),
                             DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna6.setDefaultColor(Ct.DARKORANGE3)

        self.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)

        head.addChild(antenna1)
        antenna1.addChild(antenna2)
        antenna2.addChild(antenna3)

        head.addChild(antenna4)
        antenna4.addChild(antenna5)
        antenna5.addChild(antenna6)

        self.components = [head, antenna1, antenna2, antenna3, antenna4, antenna5, antenna6]



