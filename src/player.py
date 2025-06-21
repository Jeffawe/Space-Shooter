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
        
        # Animation
        self.current_sprite = 'center'
        
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
        
        print(f"Player sprites loaded: {frame_width}x{frame_height} each")
        
    def update(self):
        """Update player state"""
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Reset movement flags
        self.moving_left = False
        self.moving_right = False
        
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.moving_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.moving_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Update sprite based on movement
        self.update_sprite()
        
    def update_sprite(self):
        """Update sprite based on movement direction"""
        if self.moving_left and not self.moving_right:
            # Moving left - use left lean sprite
            self.current_sprite = 'left1'
        elif self.moving_right and not self.moving_left:
            # Moving right - use right lean sprite
            self.current_sprite = 'right1'
        else:
            # Not moving horizontally or moving both ways - use center
            self.current_sprite = 'center'
            
        # Update the image
        self.image = self.sprites[self.current_sprite]
