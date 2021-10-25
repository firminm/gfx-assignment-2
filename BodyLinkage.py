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



class BodyLinkage(Component):
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

        scale = .4  # Set < 1 if want to flatten
        r = scale

        body = Component(Point((0, 0, 0)), DisplayableHead(self.contextParent, 1, [r, r + r, r]))
        body.setDefaultColor(Ct.DARKORANGE2)

        self.addChild(body)

        self.components = [body]



