from mapobjects import *
from os import system
import time
import copy
#import emoji

class IoHandler:
    @staticmethod
    def ReadInputFile(filename):
        fileReader = open(filename, "r")

        line = fileReader.readline()
        height = int(line.split(" ")[0])
        width = int(line.split(" ")[1])
        arena = []
        for i in range(height):
            arenaLine = []
            for j in range(width):
                arenaLine.append(Cell(j, i))
            arena.append(arenaLine)

        line = fileReader.readline()
        pacy = int(line.split(" ")[0])
        pacx = int(line.split(" ")[1])
        pacman = Pacman(pacx,pacy)
        arena[pacy][pacx].pacman = pacman

        ghosts = []
        ghostsCount = int(fileReader.readline())

        for i in range(ghostsCount):
            ghostLineToks = fileReader.readline().split(" ")
            starty = int(ghostLineToks[0])
            startx = int(ghostLineToks[1])

            newGhost = Ghost(startx, starty)

            ghosts.append(newGhost)

            arena[starty][startx].ghost = newGhost

        fileReader.readline()
        for i in range(height):
            line = fileReader.readline().rstrip('\n')
            separators = line.split(' ')

            for j in range(width):
                westSeparator = separators[j]
                eastSeparator = separators[j + 1]

                if (i != 0):
                    arena[i][j].directions.append(NORTH)
                if (i != height - 1):
                    arena[i][j].directions.append(SOUTH)
                if (westSeparator == ':'):
                    arena[i][j].directions.append(WEST)
                if (eastSeparator == ':'):
                    arena[i][j].directions.append(EAST)
        fileReader.close()
        return (arena, ghosts, pacman)
        
    @staticmethod
    def PrintOutput(strategy, time, states, cost, solution,test):
        fileWriter = open(f'output/{strategy}_output_{test}.txt', "w")

        fileWriter.write(f'{strategy}\n')
        fileWriter.write(f'{time}\n')
        fileWriter.write(f'{states}\n')
        fileWriter.write(f'{cost}\n')
        fileWriter.write(f'{solution}\n')

        fileWriter.close()

    @staticmethod
    def GetArenaChar(cell):
        if (cell.pacman != None):
            #return emoji.emojize(':oncoming_taxi:')
            return 'P'
        elif (cell.ghost != None):
            #return emoji.emojize(':thumbs_up:')
            return 'G'

        return ' '

    @staticmethod
    def PrintArena(arena):
        height = len(arena)
        width = len(arena[0])

        topBottomLine = '+'
        for _ in range(2*width - 1):
            topBottomLine += '-'
        topBottomLine += '+'

        print(topBottomLine)
        for i in range(height):
            lineString = ''
            for j in range(width):
                if (WEST in arena[i][j].directions and j != width - 1):
                    lineString += (f':{IoHandler.GetArenaChar(arena[i][j])}')
                elif (WEST not in arena[i][j].directions and j != width - 1):
                    lineString += (f'|{IoHandler.GetArenaChar(arena[i][j])}')
                elif (WEST in arena[i][j].directions and j == width - 1):
                    lineString += (f':{IoHandler.GetArenaChar(arena[i][j])}|')
                elif (j == width - 1):
                    lineString += (f'|{IoHandler.GetArenaChar(arena[i][j])}|')
            print(lineString)
        print(topBottomLine)

    @staticmethod
    def PrintAnalysis(text):
        fileWriter = open(f'output/out.csv', "w")
        fileWriter.write(text)
        fileWriter.close()
