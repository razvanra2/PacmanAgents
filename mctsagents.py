from copy import deepcopy
from math import sqrt
import random


class MctsBase:
    visited = {}

    @staticmethod
    def Mcts(pacman, ghosts, node, arena, depth, maximizing, branchingFactor):
        depth -= 1

        if depth == 0:
            g1Dist = sqrt((ghosts[0].x - pacman.x) * (ghosts[0].x - pacman.x) +
                          (ghosts[0].y - pacman.y) * (ghosts[0].y - pacman.y))
            g2Dist = sqrt((ghosts[1].x - pacman.x) * (ghosts[1].x - pacman.x) +
                          (ghosts[1].y - pacman.y) * (ghosts[1].y - pacman.y))
            return g1Dist + g2Dist

        if MctsBase.IsWinForGhosts(node):
            return 0  # equal to heuristic

        if MctsBase.IsWinForPacman(arena):
            # big enough to signal win to maximizing
            # that's what she said
            return len(arena) * len(arena[0])

        if maximizing:  # pacman
            # mark visited for pacman
            if node in MctsBase.visited:
                MctsBase.visited[node] = MctsBase.visited[node] + 1
            else:
                MctsBase.visited[node] = 1

            value = -999999
            neighbours = MctsBase.sortUCB(node.getNeighbours(arena), 2)

            for n in neighbours:
                newArena = deepcopy(arena)
                newNode = newArena[pacman.y][pacman.x]

                newArena[pacman.y][pacman.x].pacman = None
                pacman.y = n.y
                pacman.x = n.x
                newArena[pacman.y][pacman.x].pacman = pacman

                value = max(value, MctsBase.Mcts(
                    pacman, ghosts, newNode, newArena, depth, not maximizing, 2))

            return value

        else:  # ghosts
            value = +999999

            ghost1Cell = arena[ghosts[0].y][ghosts[0].x]
            ghost2Cell = arena[ghosts[1].y][ghosts[1].x]

            # mark visited for ghosts
            position = ghost1Cell, ghost2Cell
            if position in MctsBase.visited:
                MctsBase.visited[position] = MctsBase.visited[position] + 1
            else:
                MctsBase.visited[position] = 1

            g1Neighbours = ghost1Cell.getNeighbours(arena)
            g2Neighbours = ghost2Cell.getNeighbours(arena)

            # build neighbours combinations
            all_neighbours = []
            for n1 in g1Neighbours:
                for n2 in g2Neighbours:
                    if n1 != n2 and (n1, n2) not in all_neighbours and (n2, n1) not in all_neighbours:
                        all_neighbours.append((n1, n2))
            neighbours = MctsBase.sortUCB(all_neighbours, 2)

            for n in neighbours:
                (n1, n2) = n

                newArena = deepcopy(arena)
                newNode = newArena[pacman.y][pacman.x]

                newArena[ghosts[0].y][ghosts[0].x].ghost = None
                newArena[ghosts[1].y][ghosts[1].x].ghost = None

                ghosts[0].y = n1.y
                ghosts[0].x = n1.x

                ghosts[1].y = n2.y
                ghosts[1].x = n2.x

                newArena[ghosts[0].y][ghosts[0].x].ghost = ghosts[0]
                newArena[ghosts[1].y][ghosts[1].x].ghost = ghosts[1]

                value = min(value, MctsBase.Mcts(
                    pacman, ghosts, newNode, newArena, depth, not maximizing, 2))

            return value

    @staticmethod
    def IsWinForGhosts(node):
        if (node.ghost is not None and node.pacman is not None):
            return True

    @staticmethod
    def IsWinForPacman(arena):
        for line in arena:
            for cell in line:
                if cell.visited is False:
                    return False
        return True

    @staticmethod
    def sortUCB(neighbours, branching):
        nActions = len(neighbours)
        nsum = 0

        tosort = []

        for action in neighbours:
            if action in MctsBase.visited:
                nsum += MctsBase.visited[action]

        for action in neighbours:
            if action not in MctsBase.visited:
                v = +999999
            else:
                v = MctsBase.visited[action] + \
                    sqrt(2 * log(nsum) / MctsBase.visited[action])
            tosort.append((action, v))

        tosort.sort(key=lambda tup: tup[1], reverse=True)
        sortedNeighbours = []

        if branching > len(tosort):
            branching = len(tosort)

        for i in range(branching):
            sortedNeighbours.append(tosort[i][0])

        return sortedNeighbours


class PacmanMctsAgent:
    def __init__(self, arena, pacman, ghosts):
        self.arena = arena
        self.pacman = pacman
        self.ghosts = ghosts

    def move(self):
        neighbours = self.arena[self.pacman.y][self.pacman.x].getNeighbours(
            self.arena)

        newCell = None
        maxScore = -999999

        for n in neighbours:
            pacmanCopy = deepcopy(self.pacman)
            ghostsCopy = deepcopy(self.ghosts)
            arenaCopy = deepcopy(self.arena)

            arenaCopy[pacmanCopy.y][pacmanCopy.x].pacman = None
            pacmanCopy.x = n.x
            pacmanCopy.y = n.y
            arenaCopy[pacmanCopy.y][pacmanCopy.x].pacman = pacmanCopy
            cellCopy = arenaCopy[pacmanCopy.y][pacmanCopy.x]

            moveScore = MctsBase.Mcts(
                pacmanCopy, ghostsCopy, cellCopy, arenaCopy, 5, False, 2)

            print(f'{n.y, n.x} - score: {moveScore}')

            if (maxScore < moveScore):
                maxScore = moveScore
                newCell = n
            # favour unvisited cells
            elif (maxScore == moveScore and n.notVisited()):
                newCell = n

        self.arena[self.pacman.y][self.pacman.x].pacman = None

        if (newCell.notVisited()):
            self.pacman.score += 1

        newCell.pacman = self.pacman
        newCell.visited = True
        self.pacman.y = newCell.y
        self.pacman.x = newCell.x

        print(f'move to: {newCell.y, newCell.x}')

        self.checkAlive()

    def checkAlive(self):
        if (self.arena[self.pacman.y][self.pacman.x].ghost != None):
            self.pacman.alive = False


class GhostMctsAgent:
    def __init__(self, arena, pacman, ghosts):
        self.arena = arena
        self.pacman = pacman
        self.ghosts = ghosts

    def move(self):

        ghost1Cell = self.arena[self.ghosts[0].y][self.ghosts[0].x]
        ghost2Cell = self.arena[self.ghosts[1].y][self.ghosts[1].x]

        g1Neighbours = ghost1Cell.getNeighbours(self.arena)
        g2Neighbours = ghost2Cell.getNeighbours(self.arena)

        # build neighbours combinations
        neighbours = []
        for n1 in g1Neighbours:
            for n2 in g2Neighbours:
                if n1 != n2 and (n1, n2) not in neighbours and (n2, n1) not in neighbours:
                    neighbours.append((n1, n2))

        bestn1, bestn2 = None, None
        minScore = 999999

        for n1, n2 in neighbours:
            newArena = deepcopy(self.arena)
            newNode = newArena[self.pacman.y][self.pacman.x]
            newpacman = deepcopy(self.pacman)
            newghosts = deepcopy(self.ghosts)

            newArena[self.ghosts[0].y][self.ghosts[0].x].ghost = None
            newArena[self.ghosts[1].y][self.ghosts[1].x].ghost = None

            newghosts[0].y = n1.y
            newghosts[0].x = n1.x

            newghosts[1].y = n2.y
            newghosts[1].x = n2.x

            newArena[self.ghosts[0].y][self.ghosts[0].x].ghost = newghosts[0]
            newArena[self.ghosts[1].y][self.ghosts[1].x].ghost = newghosts[1]

            moveScore = MctsBase.Mcts(
                newpacman, newghosts, newNode, newArena, 3, True, 2)

            print(f'{n1.y, n1.x} ; {n2.y,n2.x} - score: {moveScore}')

            if (minScore > moveScore):
                minScore = moveScore
                bestn1, bestn2 = n1, n2

        ghost1Cell.ghost = None
        ghost2Cell.ghost = None

        bestn1.ghost = self.ghosts[0]
        bestn2.ghost = self.ghosts[1]

        self.ghosts[0].y = bestn1.y
        self.ghosts[0].x = bestn1.x

        self.ghosts[1].y = bestn2.y
        self.ghosts[1].x = bestn2.x

        print(f'move to: {bestn1.y, bestn1.x} ; {bestn2.y, bestn2.x}')

        aux = 0
