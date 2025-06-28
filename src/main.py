#!/usr/bin/env python3
"""
Retro Space Shooter - Amazon Build Challenge
Main game entry point
"""
import pygame
import sys
from game import Game
import asyncio

async def main():
    """Main game function"""
    # Initialize pygame
    pygame.init()
    
    clock = pygame.time.Clock()
    running = True
    game = Game()
    
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

        # Essential for pygbag - must be called every frame
        await asyncio.sleep(0)
        
        # Control frame rate
        clock.tick(60)
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
