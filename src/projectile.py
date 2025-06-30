"""
Projectile system for Retro Space Shooter
"""
import pygame
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, projectile_type="primary", direction="up"):
        """Initialize a projectile"""
        super().__init__()
        
        self.projectile_type = projectile_type
        self.direction = direction
        
        # Load appropriate projectile image
        if projectile_type == "primary":
            # Q key - Blue laser (Projectile01)
            self.original_image = pygame.image.load("assets/images/Projectile01.png").convert_alpha()
            self.speed = PROJECTILE_PRIMARY_SPEED
        elif projectile_type == "secondary":
            # E key - Different projectile (Projectile03)
            self.original_image = pygame.image.load("assets/images/Projectile03.png").convert_alpha()
            self.speed = PROJECTILE_SECONDARY_SPEED
        
        # Rotate projectile based on direction
        if direction == "down":
            self.image = pygame.transform.rotate(self.original_image, 180)  # Rotate 180° for downward
            self.velocity_y = self.speed  # Move downward (positive Y)
        else:  # direction == "up"
            self.image = self.original_image  # Keep original orientation for upward
            self.velocity_y = -self.speed  # Move upward (negative Y)
        
        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        
        # Position based on direction
        if direction == "down":
            self.rect.top = y  # Spawn from bottom of player when firing down
        else:
            self.rect.bottom = y  # Spawn from top of player when firing up
        
    def update(self):
        """Update projectile position"""
        self.rect.y += self.velocity_y
        
        # Remove projectile if it goes off screen (either direction)
        if self.direction == "up" and self.rect.bottom < 0:
            self.kill()  # Went off top of screen
        elif self.direction == "down" and self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Went off bottom of screen
    
    def draw(self, screen):
        """Draw the projectile"""
        screen.blit(self.image, self.rect)
