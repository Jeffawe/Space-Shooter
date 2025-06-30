"""
Enemy projectile and bomb system for Retro Space Shooter
"""
import pygame
import random
import math
from constants import *

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, projectile_type="laser"):
        """Initialize an enemy projectile"""
        super().__init__()
        
        self.projectile_type = projectile_type
        
        # Load projectile sprite (use Projectile03 for all enemy projectiles)
        if projectile_type == "laser":
            self.image = pygame.image.load("assets/images/Projectile03.png").convert_alpha()
            # Rotate to face the target direction
            angle = math.atan2(target_y - y, target_x - x)
            self.image = pygame.transform.rotate(self.image, math.degrees(angle) - 90)
            self.speed = 4
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Calculate movement direction toward target
        distance = math.sqrt((target_x - x)**2 + (target_y - y)**2)
        if distance > 0:
            self.velocity_x = (target_x - x) / distance * self.speed
            self.velocity_y = (target_y - y) / distance * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = self.speed
        
    def update(self):
        """Update projectile position"""
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Remove if off screen
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Initialize a bomb"""
        super().__init__()
        
        # Load bomb sprite from sheet
        self.load_bomb_sprite()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Bombs are stationary but can have slight drift
        self.velocity_x = random.uniform(-0.5, 0.5)
        self.velocity_y = random.uniform(-0.5, 0.5)
        
        # Bomb properties
        self.lifetime = 300  # 5 seconds at 60 FPS
        self.damage = 2
        self.explosion_radius = 50
        
        # Visual effects
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
    def load_bomb_sprite(self):
        """Load individual bomb sprite from sheet"""
        bomb_sheet = pygame.image.load("assets/images/Bombe-Sheet.png").convert_alpha()
        
        # The sheet contains 5 bomb sprites in a single row
        sheet_width = bomb_sheet.get_width()
        sheet_height = bomb_sheet.get_height()
        bomb_width = sheet_width // 5  # 5 bombs in the sheet
        
        # Choose a random bomb sprite
        bomb_index = random.randint(0, 4)
        
        # Cut out the specific bomb
        x = bomb_index * bomb_width
        bomb_rect = pygame.Rect(x, 0, bomb_width, sheet_height)
        self.original_image = bomb_sheet.subsurface(bomb_rect).copy()
        self.image = self.original_image
        
        print(f"Loaded bomb sprite (index {bomb_index})")
        
    def update(self):
        """Update bomb position and lifetime"""
        # Slight drift movement
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Rotate for visual effect
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
            
        # Apply rotation
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Countdown lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            # TODO: Create explosion effect here
            self.kill()
    
    def explode(self):
        """Explode the bomb (called by collision detection)"""
        # TODO: Create explosion animation and damage
        self.kill()
        return self.explosion_radius, self.damage
