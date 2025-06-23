"""
Player class for Retro Space Shooter
"""
import pygame
import os
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Load and cut sprite sheet
        self.load_sprites()
        
        # Set initial sprite
        self.image = self.sprites['center']
        self.rect = self.image.get_rect()
        
        # Position player at bottom center of screen
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        
        # Movement
        self.speed = PLAYER_SPEED
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Animation
        self.current_sprite = 'center'
        
        # Shooting
        self.shooting_cooldown = 0
        
    def load_sprites(self):
        """Load and cut the player sprite sheet"""
        # Load the sprite sheet
        sprite_sheet_path = "/home/jeffawe/amazon-build/assets/images/Player01-Sheet.png"
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        # Get dimensions - the sheet appears to have 5 frames horizontally
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        frame_width = sheet_width // 5  # 5 frames
        frame_height = sheet_height
        
        # Cut out individual sprites
        self.sprites = {}
        
        # Frame 0: Left lean 2
        self.sprites['left2'] = sprite_sheet.subsurface((0, 0, frame_width, frame_height))
        
        # Frame 1: Left lean 1
        self.sprites['left1'] = sprite_sheet.subsurface((frame_width, 0, frame_width, frame_height))
        
        # Frame 2: Center (neutral)
        self.sprites['center'] = sprite_sheet.subsurface((frame_width * 2, 0, frame_width, frame_height))
        
        # Frame 3: Right lean 1
        self.sprites['right1'] = sprite_sheet.subsurface((frame_width * 3, 0, frame_width, frame_height))
        
        # Frame 4: Right lean 2
        self.sprites['right2'] = sprite_sheet.subsurface((frame_width * 4, 0, frame_width, frame_height))
        
        # Create up/down facing sprites by rotating the center sprite
        self.sprites['up'] = self.sprites['center']  # Center sprite already faces up
        self.sprites['down'] = pygame.transform.rotate(self.sprites['center'], 180)  # Rotate 180° for down facing
        
        print(f"Player sprites loaded: {frame_width}x{frame_height} each")
        print("Added up/down facing sprites")
        
    def update(self):
        """Update player state"""
        # Store previous position for speed calculation
        prev_x, prev_y = self.rect.x, self.rect.y
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Reset movement flags
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.moving_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.moving_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.moving_up = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.moving_down = True
            
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Calculate movement speed for collision physics
        dx = self.rect.x - prev_x
        dy = self.rect.y - prev_y
        self.last_speed = (dx*dx + dy*dy)**0.5  # Store speed for collision system
        
        # Update shooting cooldown
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
        
        # Update sprite based on movement
        self.update_sprite()
        
    def update_sprite(self):
        """Update sprite based on movement direction - prioritize vertical movement"""
        # Vertical movement takes priority over horizontal
        if self.moving_up and not self.moving_down:
            # Moving up - face up
            self.current_sprite = 'up'
        elif self.moving_down and not self.moving_up:
            # Moving down - face down
            self.current_sprite = 'down'
        elif self.moving_left and not self.moving_right:
            # Moving left only - use left lean sprite
            self.current_sprite = 'left1'
        elif self.moving_right and not self.moving_left:
            # Moving right only - use right lean sprite
            self.current_sprite = 'right1'
        else:
            # Not moving or moving in multiple directions - use center/up facing
            self.current_sprite = 'up'
            
        # Update the image
        self.image = self.sprites[self.current_sprite]
    
    def can_shoot(self):
        """Check if player can shoot (cooldown finished)"""
        return self.shooting_cooldown <= 0
    
    def shoot(self, projectile_type="primary"):
        """Create a projectile if cooldown allows"""
        if self.can_shoot():
            self.shooting_cooldown = SHOOTING_COOLDOWN
            
            # Determine firing direction based on player facing
            if self.current_sprite == 'down':
                # Player facing down - fire downward
                direction = "down"
                spawn_x = self.rect.centerx
                spawn_y = self.rect.bottom  # Spawn from bottom of ship
            else:
                # Player facing up or sideways - fire upward
                direction = "up"
                spawn_x = self.rect.centerx
                spawn_y = self.rect.top  # Spawn from top of ship
            
            return (spawn_x, spawn_y, projectile_type, direction)
        return None
