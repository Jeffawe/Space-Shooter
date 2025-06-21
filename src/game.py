"""
Main Game class for Retro Space Shooter
"""
import pygame
from player import Player
from constants import *

class Game:
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Space Shooter - Amazon Build Challenge")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        self.all_sprites.update()
    
    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # Draw FPS counter
        fps = self.clock.get_fps()
        fps_text = pygame.font.Font(None, 36).render(f"FPS: {int(fps)}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Retro Space Shooter!")
        print("Use ARROW KEYS or WASD to move")
        print("Press ESC to quit")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
