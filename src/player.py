"""
Player class for Retro Space Shooter
"""
import pygame
import os
from health_system import PlayerHealth
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
        self.last_facing_direction = 'up'  # Remember last facing direction
        
        # Shooting
        self.shooting_cooldown = 0
        
        # Health system
        self.health_system = PlayerHealth(max_health=100)
        
        # Track last speed for collision physics
        self.last_speed = 0
        
        # Power-up effects
        self.energy_effect = None  # Energy power-up effect
        
        print("🚀 Player initialized with power-up support")
        
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
        # Don't update if player is dead
        if not self.is_alive():
            # Update health system even when dead (for invulnerability timer)
            self.health_system.update()
            return
        
        # Store previous position for speed calculation
        prev_x, prev_y = self.rect.x, self.rect.y
        
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Reset movement flags
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Handle movement (only if alive)
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
        
        # Update health system
        self.health_system.update()
        
        # Update power-up effects
        self.update_powerup_effects()
        
        # Update sprite based on movement
        self.update_sprite()
        
    def update_sprite(self):
        """Update sprite based on movement direction - preserve vertical orientation during horizontal movement"""
        
        # Priority 1: Pure vertical movement (up/down only)
        if self.moving_up and not self.moving_down and not self.moving_left and not self.moving_right:
            # Moving up only - face up
            self.current_sprite = 'up'
            self.last_facing_direction = 'up'
            
        elif self.moving_down and not self.moving_up and not self.moving_left and not self.moving_right:
            # Moving down only - face down
            self.current_sprite = 'down'
            self.last_facing_direction = 'down'
            
        # Priority 2: Horizontal movement - preserve vertical orientation
        elif self.moving_left and not self.moving_right:
            # Moving left - check current vertical orientation
            if self.last_facing_direction == 'down' or (self.moving_down and not self.moving_up):
                # Was facing down or currently moving down - use down-left
                self.current_sprite = 'left1'  # Left lean while maintaining down orientation
                self.last_facing_direction = 'down'  # Remember we were oriented down
            else:
                # Was facing up or default - use up-left  
                self.current_sprite = 'left1'  # Left lean while maintaining up orientation
                self.last_facing_direction = 'up'  # Remember we were oriented up
                
        elif self.moving_right and not self.moving_left:
            # Moving right - check current vertical orientation
            if self.last_facing_direction == 'down' or (self.moving_down and not self.moving_up):
                # Was facing down or currently moving down - use down-right
                self.current_sprite = 'right1'  # Right lean while maintaining down orientation
                self.last_facing_direction = 'down'  # Remember we were oriented down
            else:
                # Was facing up or default - use up-right
                self.current_sprite = 'right1'  # Right lean while maintaining up orientation
                self.last_facing_direction = 'up'  # Remember we were oriented up
                
        # Priority 3: Diagonal movement - vertical takes precedence
        elif self.moving_up and not self.moving_down:
            # Moving up (with possible horizontal) - face up
            self.current_sprite = 'up'
            self.last_facing_direction = 'up'
            
        elif self.moving_down and not self.moving_up:
            # Moving down (with possible horizontal) - face down
            self.current_sprite = 'down'
            self.last_facing_direction = 'down'
            
        else:
            # Not moving or complex movement - maintain last facing direction
            if self.last_facing_direction == 'down':
                self.current_sprite = 'down'
            else:  # 'up' or default
                self.current_sprite = 'up'
            
        # Update the image
        self.image = self.sprites[self.current_sprite]
    
    def collect_powerup(self, powerup_type):
        """Handle power-up collection"""
        if powerup_type == "health":
            # HP Container - restore health
            heal_amount = 50  # Increased from 30 to 50 HP
            old_health = self.health_system.current_health
            self.health_system.heal(heal_amount)
            new_health = self.health_system.current_health
            actual_heal = new_health - old_health
            
            print(f"💖 HP Container collected! Healed {actual_heal} HP ({old_health} → {new_health})")
            return f"Health +{actual_heal}"
            
        elif powerup_type == "energy":
            # Energy Container - activate energy effect
            from powerup import EnergyEffect
            self.energy_effect = EnergyEffect(duration=300)  # 5 seconds
            
            print(f"⚡ Energy Container collected! Enhanced projectiles for {self.energy_effect.duration/60:.1f} seconds")
            return "Energy Boost!"
        
        return "Power-up collected!"
    
    def update_powerup_effects(self):
        """Update active power-up effects"""
        if self.energy_effect:
            if not self.energy_effect.update():
                self.energy_effect = None  # Effect expired
    
    def has_energy_effect(self):
        """Check if energy effect is active"""
        return self.energy_effect is not None and self.energy_effect.active
    
    def get_energy_time_remaining(self):
        """Get remaining energy effect time"""
        if self.has_energy_effect():
            return self.energy_effect.get_time_remaining()
        return 0
    
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
    
    def take_damage(self, damage, damage_source="unknown"):
        """Take damage and return True if player dies"""
        return self.health_system.take_damage(damage, damage_source)
    
    def heal(self, amount):
        """Heal the player"""
        self.health_system.heal(amount)
    
    def is_alive(self):
        """Check if player is alive"""
        return self.health_system.is_alive
    
    def is_invulnerable(self):
        """Check if player is invulnerable"""
        return self.health_system.is_invulnerable()
    
    def get_health_percentage(self):
        """Get health as percentage"""
        return self.health_system.get_health_percentage()
    
    def draw_health(self, screen):
        """Draw player health bar"""
        self.health_system.draw(screen)
    
    def draw(self, screen):
        """Draw player sprite only if alive"""
        if self.is_alive():
            screen.blit(self.image, self.rect)
