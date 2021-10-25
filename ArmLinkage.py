"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableArmJoint import DisplayableArmJoint
from DisplayablePinser import DisplayablePinser
from DisplayableCylinder import DisplayableCylinder



class ArmLinkage(Component):
    """
    Define our linkage model
    Basically an antenna but with a pinser (2-fingered hand) at end
    """
    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None, isFlipped=False):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        shrink = 0.5  # Set < 1 if want to flatten

        x = (0, 1 * shrink, .75 * shrink)

        joint1 = Component(Point((x[0], 0, 0)), DisplayableArmJoint(self.contextParent, 0.2, 1, [.5, 0.5, shrink]))
        joint1.setDefaultColor(Ct.DARKORANGE3)
        if isFlipped:
            joint1.setDefaultAngle(180, joint1.wAxis)

        joint2 = Component(Point((x[1], 0, 0)), DisplayableArmJoint(self.contextParent, 0.2, .75, [.5, 0.5, shrink]))
        joint2.setDefaultColor(Ct.DARKORANGE3)

        pinser = Component(Point((x[2], 0, 0)), DisplayablePinser(self.contextParent, 0.2, .75, [.5, 0.6, shrink]))
        pinser.setDefaultColor(Ct.DARKORANGE3)


        self.addChild(joint1)
        joint1.addChild(joint2)
        joint2.addChild(pinser)



        self.components = [joint1, joint2, pinser]
