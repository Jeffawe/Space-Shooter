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
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update and draw game
        game.run()
        
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
