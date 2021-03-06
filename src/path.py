import datetime
import math

from src.settings import *
from src.action.pawn_move import *


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Path:
    """
        Aquí definiremos los algoritmos utilizados en las funciones
    """

    def __init__(self, moves, parent=None, position=None):
        self.moves = moves
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def length(self):
        return len(self.moves)

    def startCoord(self):
        return self.moves[0].fromCoord

    def endCoord(self):
        return self.moves[-1].toCoord

    def firstMove(self):
        return self.moves[0]

    # TODO = Función predeterminada en Python, enfoca al objeto de manera string

    def __str__(self):
        return "[%s] -> %s" % (str(self.startCoord()), " -> ".join(
            map(lambda move: str(move.toCoord), self.moves)))

    def ManhattanDistance(fromCoord, toCoord):
        return abs(toCoord.col - fromCoord.col) + abs(
            toCoord.row - fromCoord.row)

    def ManhattanDistanceMulti(fromCoord, toCoords):

        minManhattanDistance = math.inf  # 3.5
        for toCoord in toCoords:
            manhattanDistance = Path.ManhattanDistance(fromCoord, toCoord)
            if manhattanDistance < minManhattanDistance:
                minManhattanDistance = manhattanDistance
        return minManhattanDistance

    def BreadthFirstSearch(board, startCoord, endCoords, ignorePawns=False):
        """
        1ER ALGORITMO USADO === BFS

        Hecho por: Elio

        Es un algoritmo de búsqueda no informada utilizado para recorrer o buscar
        elementos en un grafo (usado frecuentemente sobre árboles).
        Intuitivamente, se comienza en la raíz (eligiendo algún nodo como
        elemento raíz en el caso de un grafo) y se exploran todos los vecinos
        de este nodo. A continuación para cada uno de los vecinos se exploran
        sus respectivos vecinos adyacentes, y así hasta que se recorra
        todo el árbol.
        """
        global TRACE
        TRACE["Path.BreadthFirstSearch"] += 1

        print("Esta utilizando BFS en este movimiento")
        time_start = datetime.datetime.now()
        root = PawnMove(None, startCoord)

        previousMoves = {startCoord: root}
        nextMoves = [root]
        validPawnMoves = board.storedValidPawnMovesIgnoringPawns if ignorePawns else board.storedValidPawnMoves
        while nextMoves:
            move = nextMoves.pop(0)
            for endCoord in endCoords:
                if move.toCoord == endCoord:
                    pathMoves = [move]
                    while move.fromCoord is not None:
                        move = previousMoves[move.fromCoord]
                        pathMoves.append(move)
                    pathMoves.reverse()
                    time_end = datetime.datetime.now()
                    duration = time_end - time_start
                    print('Se demoró alrededor de ' + str(duration.microseconds) + ' microsegundos')
                    return Path(pathMoves[1:])
            validMoves = validPawnMoves[move.toCoord]
            sorted(validMoves,
                   key=lambda validMove: Path.ManhattanDistanceMulti(
                       validMove.toCoord, endCoords))
            for validMove in validMoves:
                if validMove.toCoord not in previousMoves:
                    previousMoves[validMove.toCoord] = validMove
                    nextMoves.append(validMove)
        return None

    def Dijkstra(board, startCoord, endCoords, moveScore=lambda move, step: 1,
                 ignorePawns=False):
        """
        2do ALGORITMO USADO === Dijkstra

        Hecho por Richard

        El algoritmo de Dijkstra, también llamado algoritmo de caminos mínimos,
        es un algoritmo para la determinación del camino más corto, dado un
        vértice origen, hacia el resto de los vértices en un grafo que tiene
        pesos en cada arista. La idea subyacente en este algoritmo consiste en
        ir explorando todos los caminos más cortos que parten del vértice
        origen y que llevan a todos los demás vértices; cuando se obtiene el
        camino más corto desde el vértice origen hasta el resto de los vértices
         que componen el grafo, el algoritmo se detiene.
        """
        global TRACE
        TRACE["Path.Dijkstra"] += 1
        time_start = datetime.datetime.now()
        root = PawnMove(None, startCoord)
        i = 0
        previousMoves = {startCoord: (0, root)}
        nextMoves = [(0, 0, root)]
        validPawnMoves = board.storedValidPawnMovesIgnoringPawns \
            if ignorePawns else board.storedValidPawnMoves
        while nextMoves:
            i = i + 1
            sorted(nextMoves,
                   key=lambda nextMove: nextMove[1])
            (step, score, move) = nextMoves.pop(0)
            for endCoord in endCoords:
                if move.toCoord == endCoord:
                    pathMoves = [move]
                    while move.fromCoord is not None:
                        move = previousMoves[move.fromCoord][1]
                        pathMoves.append(move)
                    pathMoves.reverse()
                    time_end = datetime.datetime.now()
                    if i > 61:
                        print('Esta utilizando BFS en este movimiento')
                        duration = time_end - time_start
                        print('Se demoró alrededor de ' + str(duration.microseconds) + ' microsegundos')
                    return Path(pathMoves[1:])
            validMoves = validPawnMoves[move.toCoord]
            sorted(validMoves,
                   key=lambda validMove: Path.ManhattanDistanceMulti(
                       validMove.toCoord, endCoords))
            for validMove in validMoves:
                validMoveScore = score + moveScore(validMove, step + 1)
                if validMove.toCoord not in previousMoves:
                    previousMoves[validMove.toCoord] = (
                        validMoveScore, validMove)
                    nextMoves.append((step + 1, validMoveScore, validMove))
                if validMoveScore < previousMoves[validMove.toCoord][0]:
                    previousMoves[validMove.toCoord] = (
                        validMoveScore, validMove)
        return None


# TODO = Algoritmo requerido por el curso, se implementó A-start para cumplir
#  los requisitos del curso

def Astar(maze, start, end):
    """
    Así, el algoritmo A* representa el valor
    heurístico del nodo a evaluar desde el actual, n, hasta el final, y
    la otra funcion, el coste real del camino
    recorrido para llegar a dicho nodo, n, desde el nodo inicial. A* mantiene
    dos estructuras de datos auxiliares, que podemos denominar abiertos,
    implementado como una cola de prioridad (ordenada por el valor
    {\displaystyle f(n)}{\displaystyle f(n)} de cada nodo), y cerrados, donde
    se guarda la información de los nodos que ya han sido visitados. En cada
    paso del algoritmo, se expande el nodo que esté primero en abiertos, y en
    caso de que no sea un nodo objetivo, calcula la
    {\displaystyle f(n)}{\displaystyle f(n)} de todos sus hijos, los inserta
    en abiertos, y pasa el nodo evaluado a cerrados.

    El algoritmo es una combinación entre búsquedas del tipo primero en anchura
    con primero en profundidad: mientras que {\displaystyle h'(n)}{\displaystyle h'(n)}
    tiende a primero en profundidad, {\displaystyle g(n)}{\displaystyle g(n)} tiende
    a primero en anchura. De este modo, se cambia de camino de búsqueda
    cada vez que existen nodos más prometedores.
    """
    global TRACE
    TRACE["Path.AStar"] += 1

    print("Esta utilizando AStar en este movimiento")
    time_start = datetime.datetime.now()

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1),
                             (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or \
                    node_position[1] > (len(maze[len(maze) - 1]) - 1) or \
                    node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    print('Esta utilizando Astar en este movimiento')
    duration = time_end - time_start
    print('Se demoró alrededor de ' + str(duration.microseconds) + ' microsegundos')
