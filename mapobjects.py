NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
PICKUP = "Pickup"
DROPOFF = "Dropoff"
arena = None

class Pacman:
    def __init__(self,
        newStarty, newStartx):
        self.x = newStartx
        self.y = newStarty
        self.score = 0
        self.alive = True

    def isAlive(self):
        return self.alive


class Ghost:
    def __init__(self,
                 newStarty, newStartx):
        self.x = newStartx
        self.y = newStarty
        self.alive = True

    def isAlive(self):
        return self.alive

class Cell:
    def __init__(self, posx, posy):
        self.x = posx
        self.y = posy
 
        self.pacman = None
        self.ghost = None

        self.directions = []

        self.visited = False

    def __lt__(ob1, ob2):
        return False    
    
    def notVisited(self):
        return not self.visited

    def getNeighbours(self, arena):
        neighbours = []
        
        if NORTH in self.directions:
            neighbours.append(arena[self.y - 1][self.x])
        if SOUTH in self.directions:
            neighbours.append(arena[self.y + 1][self.x])
        if EAST in self.directions:
            neighbours.append(arena[self.y][self.x + 1])
        if WEST in self.directions:
            neighbours.append(arena[self.y][self.x - 1])
        
        return neighbours
    
    def hasGhost(self):
        return ghost != None
    
    def hasPacman(self, clientId):
        return pacman != None
