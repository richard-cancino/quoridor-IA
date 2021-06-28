from src.settings import INTERFACE
from src.player.IPlayer import *
from src.action.IAction import *
from src.action.quit import *


class Human(IPlayer):
    def play(self, board) -> IAction:
        if not INTERFACE:
            raise Exception("")
        while True:
            # TODO = CAPTURA DE TECLA
            key = board.window.getKey()
            if key == ' ' or key == 'space':
                validPawnMoves = board.storedValidPawnMoves[self.pawn.coord]
                print(self.pawn.coord)
                board.displayValidPawnMoves(self, validPawnMoves)
                click = board.window.getMouse()
                pawnMove = board.getPawnMoveFromMousePosition(self.pawn,
                                                              click.x, click.y)
                clickOnValidTarget = (pawnMove is not None)
                board.hideValidPawnMoves(self, validPawnMoves)
                if clickOnValidTarget:
                    return pawnMove
            if key == "f" or key == "F" and self.remainingFences() > 0:
                # TODO = Podemos colocar en la otra pantalla si activo para
                #  las cercas
                click = board.window.getMouse()
                fencePlacing = board.getFencePlacingFromMousePosition(click.x,
                                                                      click.y)
                clickOnValidTarget = (fencePlacing is not None)
                if clickOnValidTarget:
                    return fencePlacing

