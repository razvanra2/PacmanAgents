import random


class RandomPacmanAgent:
    def __init__(self, arena, pacman):
        self.arena = arena
        self.pacman = pacman

    def move(self):
        neighbours = self.arena[self.pacman.y][self.pacman.x].getNeighbours(
            self.arena)
        newCell = random.choice(neighbours)
        self.arena[self.pacman.y][self.pacman.x].pacman = None

        if (newCell.notVisited()):
            self.pacman.score += 1

        newCell.pacman = self.pacman
        newCell.visited = True
        self.pacman.y = newCell.y
        self.pacman.x = newCell.x


        self.checkAlive()

    def checkAlive(self):
        if (self.arena[self.pacman.y][self.pacman.x].ghost != None):
            self.pacman.alive = False


class RandomGhostAgent:
    def __init__(self, arena, ghosts):
        self.arena = arena
        self.ghosts = ghosts

    def move(self):
        for ghost in self.ghosts:

            newCell = self.arena[ghost.y][ghost.x]
            while newCell.ghost is not None:
                neighbours = self.arena[ghost.y][ghost.x].getNeighbours(
                    self.arena)
                newCell = random.choice(neighbours)

            self.arena[ghost.y][ghost.x].ghost = None

            newCell.ghost = ghost
            ghost.y = newCell.y
            ghost.x = newCell.x
