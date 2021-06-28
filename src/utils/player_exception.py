from src.player.IPlayer import *
from src.action.fence_placing import *


class PlayerPathObstructedException(Exception):

    # TODO = En caso de un error no reportado, lanzamos una excepcion

    def __init__(self, player: IPlayer, fencePlacing: FencePlacing = None):
        self.message = "Jugador %s tiene error" % (player)
        if fencePlacing is not None:
            self.message += "by %s" % (fencePlacing)
