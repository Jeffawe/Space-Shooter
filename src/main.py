#!/usr/bin/env python3
"""
Retro Space Shooter - Amazon Build Challenge
Main game entry point
"""
import pygame
import sys
from game import Game

def main():
    """Main game function"""
    # Initialize pygame
    pygame.init()
    
    # Create and run the game
    game = Game()
    game.run()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
