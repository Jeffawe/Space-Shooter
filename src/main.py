#!/usr/bin/env python3
"""
Retro Space Shooter - Amazon Build Challenge
Main game entry point
"""
import pygame
import sys
from game import Game
import asyncio

pygame.init()
    
clock = pygame.time.Clock()
running = True
game = Game()

async def main():
    """Main game function"""
    # Initialize pygame
    global running, game, clock
    
    while running:
        # Handle events, update and draw game
        game.handle_events()
        game.update()
        game.draw()

        # game.run()

        # Check if game wants to quit
        if not game.running:
            running = False
        
        # Update display
        pygame.display.flip()
        pygame.display.update()

        # Control frame rate
        clock.tick(60)

        await asyncio.sleep(0)

asyncio.run(main())
