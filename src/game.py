from src.settings import *
from src.utils.color import *
from src.utils.board import *
from src.utils.pawn import *
from src.player.human import *
from src.action.pawn_move import *
from src.action.fence_placing import *
from src.path import *

import random


class Game:
    DefaultColorForPlayer = [
        Color.BLACK,
        Color.BLUE,
        Color.GREEN,
        Color.TURQUOISE
    ]

    DefaultNameForPlayer = [
        "1",
        "2",
        "3",
        "4"
    ]

    def __init__(self, players, cols=9, rows=9, totalFenceCount=20,
                 squareSize=40, innerSize=None):
        if innerSize is None:
            innerSize = int(squareSize / 8)
        self.totalFenceCount = totalFenceCount
        # TODO = CREAR INSTANCIA DE AREA
        board = Board(self, cols, rows, squareSize, innerSize)

        playerCount = min(int(len(players) / 2) * 2, 4)
        self.players = []

        for num_player in range(playerCount):

            # TODO = Seteamos a los jugaodres en caso no tengan nombre
            if players[num_player].name is None:
                players[num_player].name = Game.DefaultNameForPlayer[num_player]
            if players[num_player].color is None:
                players[num_player].color = Game.DefaultColorForPlayer[
                    num_player]

            # TODO = Inicializamos jugador
            players[num_player].pawn = Pawn(board, players[num_player])

            # TODO = Definimos inicio de posiciones
            players[num_player].startPosition = board.startPosition(num_player)
            players[num_player].endPositions = board.endPositions(num_player)
            self.players.append(players[num_player])
        self.board = board

    def start(self, roundCount=1):

        roundNumberZeroFill = len(str(roundCount))
        # TODO = Por cada vuelta
        for roundNumber in range(1, roundCount + 1):
            # TODO = Resetear area y dibujar movimientos del jugador

            self.board.initStoredValidActions()
            self.board.draw()
            print("RONDA #%s: " % str(roundNumber).zfill(roundNumberZeroFill),
                  end="")
            playerCount = len(self.players)
            # TODO = Compartir cercas entrea los jugadores

            playerFenceCount = int(self.totalFenceCount / playerCount)
            self.board.fences, self.board.pawns = [], []
            # TODO = Por cada jugador
            for i in range(playerCount):
                player = self.players[i]
                # TODO = Posicion del jugador en el inicio

                player.pawn.place(player.startPosition)
                for j in range(playerFenceCount):
                    player.fences.append(Fence(self.board, player))

            # TODO = Definir aleatoriamente el primer jugador
            currentPlayerIndex = random.randrange(playerCount)
            finished = False

            while not finished:
                player = self.players[currentPlayerIndex]
                # TODO = El jugador comienza a jugar, puede ser tú mismo o el bot

                action = player.play(self.board)
                if isinstance(action, PawnMove):
                    player.movePawn(action.toCoord)
                    # TODO = Chequear si el jugador ha alcanzado uno de los
                    #  objetivos del jugador
                    if player.hasWon():
                        finished = True
                        print("Jugador %s gana" % player.name)
                        player.score += 1
                elif isinstance(action, FencePlacing):
                    player.placeFence(action.coord, action.direction)
                elif isinstance(action, Quit):
                    finished = True
                    print("Player %s se fue" % player.name)
                currentPlayerIndex = (currentPlayerIndex + 1) % playerCount
                if INTERFACE:
                    time.sleep(TEMPO_SEC)

        print("RESULTADOS FINALES: ")

        bestPlayer = self.players[0]
        for player in self.players:
            print("- %s: %d" % (str(player), player.score))
            if player.score > bestPlayer.score:
                bestPlayer = player
        print("Jugador %s gana con %d victorias!" % (
            bestPlayer.name, bestPlayer.score))

    def end(self):
        if INTERFACE:
            self.board.window.close()
