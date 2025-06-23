"""
Main Game class for Retro Space Shooter
"""
import pygame
from player import Player
from space_background import SpaceBackground
from constants import *

class Game:
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Space Shooter - Amazon Build Challenge")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create space background
        self.background = SpaceBackground()
        
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
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Update background based on player position and key presses
        self.background.update(self.player.rect, keys)
    
    def draw(self):
        """Draw everything to the screen"""
        # Draw background
        self.background.draw(self.screen)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        fps = self.clock.get_fps()
        fps_text = pygame.font.Font(None, 36).render(f"FPS: {int(fps)}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        # Show scroll info
        scroll_progress = self.background.get_scroll_progress()
        scroll_text = pygame.font.Font(None, 24).render(f"Scroll: {scroll_progress:.1%}", True, WHITE)
        self.screen.blit(scroll_text, (10, 50))
        
        # Show instructions
        player_y = self.player.rect.centery
        if player_y < self.background.upper_scroll_zone:
            instruction_text = pygame.font.Font(None, 20).render("Hold W to scroll up!", True, YELLOW)
            self.screen.blit(instruction_text, (10, 80))
        elif player_y > self.background.lower_scroll_zone:
            instruction_text = pygame.font.Font(None, 20).render("Hold S to scroll down!", True, YELLOW)
            self.screen.blit(instruction_text, (10, 80))
        else:
            instruction_text = pygame.font.Font(None, 20).render("Move to zones to scroll", True, WHITE)
            self.screen.blit(instruction_text, (10, 80))
        
        # Draw scroll zone indicators (more subtle)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.upper_scroll_zone), (SCREEN_WIDTH, self.background.upper_scroll_zone), 1)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.lower_scroll_zone), (SCREEN_WIDTH, self.background.lower_scroll_zone), 1)
        
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
