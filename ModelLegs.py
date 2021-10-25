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
from DisplayableLeg import DisplayableLeg




class ModelLegs(Component):
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

        leg = Component(Point((0,0,0)), DisplayableLeg(self.contextParent, 1, 1, [.15, .5, .15]))
        leg.setDefaultColor(Ct.DARKORANGE3)

        # leg1 = Component(Point((.4, 0, 0)), DisplayableLeg(self.contextParent, 1, 1, [.15, .5, .15]))
        # leg1.setDefaultColor(Ct.DARKORANGE3)

        self.addChild(leg)
        # self.addChild(leg1)
        self.componenets = [leg]#, leg1]

        '''
        shrink = .5  # Set < 1 if want to flatten

        antenna1 = Component(Point((0, 0, 0)), DisplayableJoint(self.contextParent, 0.25, .75, [shrink, shrink, shrink]))
        antenna1.setDefaultColor(Ct.DARKORANGE3)
        if isFlipped:
            antenna1.setDefaultAngle(190, antenna1.wAxis)
        else:
            antenna1.setDefaultAngle(170, antenna1.wAxis)

        antenna2 = Component(Point((0, 3*shrink/4, 0)), DisplayableJoint(self.contextParent, 0.25, .75, [shrink, shrink, shrink]))
        antenna2.setDefaultColor(Ct.DARKORANGE3)
        # antenna2.setDefaultAngle(20, antenna2.uAxis)

        antenna3 = Component(Point((0, 3*shrink/4, 0)), DisplayableConeJoint(self.contextParent, 0.25, .4, [shrink, shrink, shrink]))
        antenna3.setDefaultColor(Ct.DARKORANGE3)
        # antenna3.setDefaultAngle(40, antenna3.uAxis)

        self.addChild(antenna1)
        antenna1.addChild(antenna2)
        antenna2.addChild(antenna3)

        self.components = [antenna1, antenna2, antenna3]
        '''

