from iohandler import *
from randomagents import *
from minmaxagents import *
from mctsagents import *
from os import system
import time


def main():
    (arena, ghosts, pacman) = IoHandler.ReadInputFile('test3.in')
    maxScore = len(arena) * len(arena[0])

    #PacmanAgent = RandomPacmanAgent(arena, pacman)
    #GhostsAgent = RandomGhostAgent(arena, ghosts)

    PacmanAgent = PacmanMinMaxAgent(arena, pacman, ghosts)
    #GhostsAgent = GhostMinMaxAgent(arena, pacman, ghosts)

    #PacmanAgent = PacmanMctsAgent(arena, pacman, ghosts)
    GhostsAgent = GhostMctsAgent(arena, pacman, ghosts)

    while pacman.isAlive():
        time.sleep(1)
        system('clear')
        IoHandler.PrintArena(arena)
        print(f'SCORE: {pacman.score}')
        PacmanAgent.move()
        GhostsAgent.move()

    print(f'pacman scored: {pacman.score}')

    if (pacman.score == maxScore):
        print('pacman wins!')
    else:
        print('ghosts win!')


if __name__ == "__main__":
    main()
