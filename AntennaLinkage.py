"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableJoint import DisplayableJoint
from DisplayableConeJoint import DisplayableConeJoint




class AntennaLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature.

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None, isFlipped=False):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        yrot = 20
        zrot = 10

        shrink = .5  # Set < 1 if want to flatten

        antenna1 = Component(Point((0, 0, 0)), DisplayableJoint(self.contextParent,0.2, .75, [shrink, shrink, shrink]))
        antenna1.setDefaultColor(Ct.DARKORANGE3)
        # if isFlipped:
            # antenna1.setDefaultAngle(-zrot, antenna1.wAxis)
        # else:
        #     antenna1.setDefaultAngle(zrot, antenna1.wAxis)

        antenna2 = Component(Point((0, .75 * shrink, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna2.setDefaultColor(Ct.DARKORANGE3)
        # antenna2.setDefaultAngle(yrot, antenna2.uAxis)

        antenna3 = Component(Point((0, .75 * shrink, 0)), DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        antenna3.setDefaultColor(Ct.DARKORANGE3)
        # antenna3.setDefaultAngle(yrot, antenna3.uAxis)

        self.addChild(antenna1)
        antenna1.addChild(antenna2)
        antenna2.addChild(antenna3)

        self.components = [antenna1, antenna2, antenna3]



        # antenna4 = Component(Point((.5, -.2*shrink, 0)), DisplayableJoint(self.contextParent,0.2, .75, [shrink, shrink, shrink]))
        # antenna4.setDefaultColor(Ct.DARKORANGE3)
        #
        # antenna5 = Component(Point((.5, -.2*shrink, 0)), DisplayableJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        # antenna5.setDefaultColor(Ct.DARKORANGE3)
        #
        # antenna6 = Component(Point((.5, -.2*shrink, 0)), DisplayableConeJoint(self.contextParent, 0.2, .75, [shrink, shrink, shrink]))
        # antenna6.setDefaultColor(Ct.DARKORANGE3)
        #
        # antenna1.addChild(antenna4)
        # antenna2.addChild(antenna5)
        # antenna3.addChild(antenna6)
        # self.components = [antenna1, antenna2, antenna3, antenna4, antenna5, antenna6]


