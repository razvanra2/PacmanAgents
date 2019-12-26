from iohandler import *
import randomghostagent
import randompacmanagent

def main():
    (arena, ghosts, pacman) = IoHandler.ReadInputFile('test1.in')
    
    randomPacmanAgent = RandomPacmanAgent(arena, pacman)
    randomGhostAgent = RandomGhostAgent(arena, ghosts)
    
    while pacman.isAlive():
        randomPacmanAgent.movePacman()
        randomGhostAgent.moveGhosts()

        IoHandler.PrintArena(arena)

        
if __name__ == "__main__":
    main()
