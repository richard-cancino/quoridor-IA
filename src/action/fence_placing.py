from src.action.IAction import *
from src.utils.fence import *

class FencePlacing(IAction):
    """
    Funciones predeterminadas como interfaces de las clases equivalentes
    """

    def __init__(self, coord, direction):
        self.coord = coord
        self.direction = direction

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.coord == other.coord and self.direction == other.direction
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.coord, self.direction))

    def __str__(self):
        vertical = (self.direction == Fence.DIRECTION.VERTICAL)
        return "%s-cerca en el punto %s" % ("Vertical" if vertical else "Horizontal", self.coord)
