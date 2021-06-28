from src.player.random_bot import *
from src.utils.player_exception import *
from src.player.IBot import *
from src.path import *


class BuilderBot(RandomBot):
    def computeFencePlacingImpacts(self, board):

        fencePlacingImpacts = {}

        for fencePlacing in board.storedValidFencePlacings:
            try:
                impact = board.getFencePlacingImpactOnPaths(fencePlacing)

            except PlayerPathObstructedException as e:
                continue

            globalImpact = 0
            for playerName in impact:
                globalImpact += (-1 if playerName == self.name else 1) * impact[
                    playerName]
            fencePlacingImpacts[fencePlacing] = globalImpact
        return fencePlacingImpacts

    def getFencePlacingWithTheHighestImpact(self, fencePlacingImpacts):
        return max(fencePlacingImpacts, key=fencePlacingImpacts.get)

    def play(self, board) -> IAction:
        # TODO = Si no hay muro, se puede mover el jugador
        if self.remainingFences() < 1 or len(
                board.storedValidFencePlacings) < 1:
            return self.moveRandomly(board)
        fencePlacingImpacts = self.computeFencePlacingImpacts(board)
        # TODO = Si no es válido el lugar de la cerca, el jugador se puede mover
        if len(fencePlacingImpacts) < 1:
            return self.moveRandomly(board)
        # TODO = Escoger lugar de la cerca con el mayor impacto
        bestFencePlacing = self.getFencePlacingWithTheHighestImpact(
            fencePlacingImpacts)

        # TODO = Si el impacto no es positivo, el jugador se mueve
        if fencePlacingImpacts[bestFencePlacing] < 1:
            return self.moveRandomly(board)
        return bestFencePlacing


class RunnerBot(IBot):
    def moveAlongTheShortestPath(self, board) -> IAction:
        print('Solo BFS AQUI ')
        path = Path.BreadthFirstSearch(board, self.pawn.coord,
                                       self.endPositions, ignorePawns=False)
        if path is None:
            path = Path.BreadthFirstSearch(board, self.pawn.coord,
                                           self.endPositions, ignorePawns=True)
            print(path.firstMove())
            firstMove = path.firstMove()
            if not board.isValidPawnMove(firstMove.fromCoord, firstMove.toCoord,
                                         ignorePawns=False):
                return None
        return path.firstMove()

    def play(self, board) -> IAction:
        return self.moveAlongTheShortestPath(board)


class BuildAndRunBot(BuilderBot, RunnerBot):
    def play(self, board) -> IAction:
        # If no fence left, move pawn
        if self.remainingFences() < 1 or len(
                board.storedValidFencePlacings) < 1:
            return self.moveAlongTheShortestPath(board)
        fencePlacingImpacts = self.computeFencePlacingImpacts(board)
        # If no valid fence placing, move pawn
        if len(fencePlacingImpacts) < 1:
            return self.moveAlongTheShortestPath(board)
        # Choose fence placing with the greatest impact
        bestFencePlacing = self.getFencePlacingWithTheHighestImpact(
            fencePlacingImpacts)
        # If impact is not positive, move pawn
        if fencePlacingImpacts[bestFencePlacing] < 1:
            return self.moveAlongTheShortestPath(board)
        return bestFencePlacing
