"""
Enemy system with AI for Retro Space Shooter
"""
import pygame
import random
import math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, x, y, direction="down"):
        """Initialize an enemy with AI"""
        super().__init__()
        
        self.enemy_type = enemy_type
        self.direction = direction  # "up", "down"
        self.health = 1
        self.score_value = 10
        
        # Load enemy sprite based on type
        self.load_enemy_sprite()
        
        # Rotate sprite based on direction
        self.apply_direction_rotation()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Set movement properties based on enemy type
        self.set_movement_properties()
        
        # AI properties - Different detection ranges for different ship types
        self.set_ai_properties()
        self.ai_state = "patrol"     # "patrol", "pursue", "attack", "position"
        self.target_x = None
        self.target_y = None
        self.last_shot_time = 0
        
        # Movement variables
        self.move_timer = 0
        self.ai_timer = 0
        
        # Positioning behavior
        self.preferred_distance = 100  # Preferred distance from player
        
    def set_ai_properties(self):
        """Set AI detection ranges based on enemy type"""
        if self.enemy_type == "fighter1":
            # Fast, agile fighter - medium detection range
            self.detection_radius = 200  # Was 150, now 200
            self.attack_radius = 150     # Was 120, now 150
            
        elif self.enemy_type == "fighter2":
            # Tactical fighter - good detection range
            self.detection_radius = 220  # Was 150, now 220
            self.attack_radius = 160     # Was 120, now 160
            
        elif self.enemy_type == "crabship":
            # Defensive ship - shorter detection but wide attack
            self.detection_radius = 180  # Was 150, now 180
            self.attack_radius = 140     # Was 120, now 140
            
        elif self.enemy_type == "gunship":
            # Artillery ship - longest detection and attack range
            self.detection_radius = 280  # Was 150, now 280 (longest range)
            self.attack_radius = 220     # Was 180, now 220 (longest attack)
            
        elif self.enemy_type == "pirate":
            # Chaotic ship - very good detection for unpredictable attacks
            self.detection_radius = 250  # Was 150, now 250
            self.attack_radius = 180     # Was 120, now 180
        
    def load_enemy_sprite(self):
        """Load the appropriate sprite for this enemy type"""
        enemy_sprites = {
            "fighter1": "/home/jeffawe/amazon-build/assets/images/fighter1.png",
            "fighter2": "/home/jeffawe/amazon-build/assets/images/fighter2.png", 
            "crabship": "/home/jeffawe/amazon-build/assets/images/CrabShip.png",
            "gunship": "/home/jeffawe/amazon-build/assets/images/Gunship.png",
            "pirate": "/home/jeffawe/amazon-build/assets/images/Pirate_Fighter.png"
        }
        
        sprite_path = enemy_sprites.get(self.enemy_type, enemy_sprites["fighter1"])
        self.original_image = pygame.image.load(sprite_path).convert_alpha()
        
    def apply_direction_rotation(self):
        """Rotate sprite to face UP or DOWN only"""
        if self.direction == "down":
            # Default orientation (facing down)
            self.image = self.original_image
        elif self.direction == "up":
            # Rotate 180 degrees to face up
            self.image = pygame.transform.rotate(self.original_image, 180)
        
    def set_movement_properties(self):
        """Set movement properties based on enemy type"""
        if self.enemy_type == "fighter1":
            # Fast, agile fighter - aggressive AI (slowed down)
            self.base_speed = 2  # Was 3, now 2
            self.movement_pattern = "aggressive"
            self.health = 1
            self.score_value = 10
            self.shot_cooldown = 45
            self.can_drop_bombs = False
            
        elif self.enemy_type == "fighter2":
            # Medium speed with weaving - tactical AI (slowed down)
            self.base_speed = 1.5  # Was 2, now 1.5
            self.movement_pattern = "tactical"
            self.health = 1
            self.score_value = 15
            self.shot_cooldown = 60
            self.can_drop_bombs = False
            
        elif self.enemy_type == "crabship":
            # Slow but tough - defensive AI with bombs (slowed down)
            self.base_speed = 0.8  # Was 1, now 0.8
            self.movement_pattern = "defensive"
            self.health = 2
            self.score_value = 25
            self.shot_cooldown = 90
            self.can_drop_bombs = True
            self.bomb_drop_chance = 0.02  # 2% chance per frame when in range
            
        elif self.enemy_type == "gunship":
            # Heavy, slow, tough - artillery AI (slowed down)
            self.base_speed = 0.7  # Was 1, now 0.7
            self.movement_pattern = "artillery"
            self.health = 3
            self.score_value = 30
            self.shot_cooldown = 40  # Fast shooting
            self.can_drop_bombs = False
            
        elif self.enemy_type == "pirate":
            # Fast and unpredictable - chaotic AI with bombs (slowed down)
            self.base_speed = 1.2  # Was 2, now 1.2
            self.movement_pattern = "chaotic"
            self.health = 2
            self.score_value = 20
            self.shot_cooldown = 75
            self.can_drop_bombs = True
            self.bomb_drop_chance = 0.015  # 1.5% chance per frame
        
        # Set AI properties after movement properties
        self.set_ai_properties()
        
    def distance_to_player(self, player_rect):
        """Calculate distance to player"""
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        return math.sqrt(dx*dx + dy*dy)
    
    def can_see_player(self, player_rect):
        """Check if player is within detection radius"""
        return self.distance_to_player(player_rect) <= self.detection_radius
    
    def can_attack_player(self, player_rect):
        """Check if player is within attack radius"""
        return self.distance_to_player(player_rect) <= self.attack_radius
    
    def get_position_target(self, player_rect):
        """Calculate where enemy should position to attack player vertically"""
        player_x = player_rect.centerx
        player_y = player_rect.centery
        
        # Try to get in front or behind player for vertical attack
        if self.direction == "down":
            # Position above player to attack downward
            target_x = player_x + random.randint(-50, 50)  # Some randomness
            target_y = player_y - self.preferred_distance
        else:  # direction == "up"
            # Position below player to attack upward
            target_x = player_x + random.randint(-50, 50)
            target_y = player_y + self.preferred_distance
        
        # Keep within screen bounds
        target_x = max(50, min(SCREEN_WIDTH - 50, target_x))
        target_y = max(50, min(SCREEN_HEIGHT - 50, target_y))
        
        return target_x, target_y
    
    def update_ai(self, player_rect):
        """Update AI behavior based on player position"""
        self.ai_timer += 1
        distance = self.distance_to_player(player_rect)
        
        # State machine for AI behavior
        if not self.can_see_player(player_rect):
            self.ai_state = "patrol"
        elif self.can_attack_player(player_rect):
            self.ai_state = "attack"
        else:
            self.ai_state = "position"
        
        # Execute AI behavior based on state
        actions = []
        
        if self.ai_state == "patrol":
            self.patrol_behavior()
        elif self.ai_state == "position":
            self.position_behavior(player_rect)
        elif self.ai_state == "attack":
            action = self.attack_behavior(player_rect)
            if action:
                actions.append(action)
        
        return actions
    
    def patrol_behavior(self):
        """Default patrol movement"""
        # Continue with original movement pattern
        self.execute_movement_pattern()
    
    def position_behavior(self, player_rect):
        """Move to get in position to attack player"""
        target_x, target_y = self.get_position_target(player_rect)
        
        # Move toward target position
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 10:  # Don't micro-adjust
            move_x = (dx / distance) * self.base_speed * 0.7  # Slower positioning
            move_y = (dy / distance) * self.base_speed * 0.7
            
            self.rect.x += move_x
            self.rect.y += move_y
    
    def attack_behavior(self, player_rect):
        """Attack the player"""
        # Try to maintain position and shoot
        if self.ai_timer - self.last_shot_time >= self.shot_cooldown:
            self.last_shot_time = self.ai_timer
            return self.create_projectile(player_rect)
        
        # Drop bombs if capable
        if (self.can_drop_bombs and 
            random.random() < self.bomb_drop_chance):
            return self.create_bomb()
        
        return None
    
    def create_projectile(self, player_rect):
        """Create a projectile aimed at the player"""
        from enemy_projectile import EnemyProjectile
        
        # Shoot from the front of the ship
        if self.direction == "down":
            shoot_x = self.rect.centerx
            shoot_y = self.rect.bottom
        else:  # up
            shoot_x = self.rect.centerx
            shoot_y = self.rect.top
        
        # Aim at player with some prediction
        target_x = player_rect.centerx
        target_y = player_rect.centery
        
        projectile = EnemyProjectile(shoot_x, shoot_y, target_x, target_y, "laser")
        print(f"{self.enemy_type} fired at player!")
        return projectile
    
    def create_bomb(self):
        """Create a bomb at current position"""
        from enemy_projectile import Bomb
        
        bomb = Bomb(self.rect.centerx, self.rect.centery)
        print(f"{self.enemy_type} dropped a bomb!")
        return bomb
    
    def execute_movement_pattern(self):
        """Execute the enemy's movement pattern - simplified for better gameplay"""
        # Base vertical movement
        if self.direction == "down":
            base_y = self.base_speed
        else:
            base_y = -self.base_speed
        
        # Apply movement pattern modifications (simplified)
        if self.movement_pattern == "aggressive":
            # Direct forward movement
            self.rect.y += base_y
            
        elif self.movement_pattern == "tactical":
            # Slight weaving movement
            self.rect.x += math.sin(self.move_timer * 0.05) * 1  # Reduced weaving
            self.rect.y += base_y
            
        elif self.movement_pattern == "defensive":
            # Slow, steady movement
            self.rect.y += base_y * 0.8  # Even slower
            
        elif self.movement_pattern == "artillery":
            # Very slow movement, focus on positioning
            self.rect.y += base_y * 0.6  # Much slower
            
        elif self.movement_pattern == "chaotic":
            # Slight unpredictable movement
            if self.move_timer % 90 < 45:  # Slower zigzag
                self.rect.x += 1
            else:
                self.rect.x -= 1
            self.rect.y += base_y
    
    def update(self, player_rect=None):
        """Update enemy position and AI behavior"""
        self.move_timer += 1
        
        # Update AI if player is provided
        if player_rect:
            actions = self.update_ai(player_rect)
            if actions:
                return actions  # Return list of projectiles/bombs to be added to game
        else:
            # No player reference, just patrol
            self.execute_movement_pattern()
        
        # Remove enemy if it goes off screen
        if (self.rect.top > SCREEN_HEIGHT + 100 or 
            self.rect.bottom < -100 or
            self.rect.right < -100 or 
            self.rect.left > SCREEN_WIDTH + 100):
            self.kill()
        
        return []
    
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed"""
        self.health -= damage
        if self.health <= 0:
            return True
        return False


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, size="medium"):
        """Initialize an asteroid"""
        super().__init__()
        
        self.size = size
        self.rotation = 0
        self.rotation_speed = random.uniform(-1, 1)  # Slower rotation
        
        # Load asteroid sprite from sheet
        self.load_asteroid_sprite()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Set movement (much slower)
        self.speed_y = random.uniform(0.2, 0.6)  # Slower downward drift
        self.speed_x = random.uniform(-0.2, 0.2)  # Slower horizontal drift
        
        # Health based on size
        self.health = {"small": 1, "medium": 2, "large": 3}[size]
        self.score_value = {"small": 5, "medium": 10, "large": 15}[size]
        
    def load_asteroid_sprite(self):
        """Load individual asteroid sprite from sheet"""
        asteroid_sheet = pygame.image.load("/home/jeffawe/amazon-build/assets/images/Asteroids-Sheet.png").convert_alpha()
        
        # The sheet contains 12 asteroids in a single row
        sheet_width = asteroid_sheet.get_width()
        sheet_height = asteroid_sheet.get_height()
        asteroid_width = sheet_width // 12  # 12 asteroids in the sheet
        
        # Choose asteroid based on size
        if self.size == "small":
            # Use asteroids 8-11 (smaller ones on the right)
            asteroid_index = random.randint(8, 11)
        elif self.size == "medium":
            # Use asteroids 4-7 (medium ones in middle)
            asteroid_index = random.randint(4, 7)
        else:  # large
            # Use asteroids 0-3 (larger ones on the left)
            asteroid_index = random.randint(0, 3)
        
        # Cut out the specific asteroid
        x = asteroid_index * asteroid_width
        asteroid_rect = pygame.Rect(x, 0, asteroid_width, sheet_height)
        self.original_image = asteroid_sheet.subsurface(asteroid_rect).copy()
        self.image = self.original_image
        
        print(f"Loaded {self.size} asteroid (index {asteroid_index})")
        
    def update(self):
        """Update asteroid position and rotation"""
        # Move slowly
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Slow rotation
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
            
        # Apply rotation to image
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Remove if off screen
        if (self.rect.top > SCREEN_HEIGHT + 50 or 
            self.rect.right < -50 or 
            self.rect.left > SCREEN_WIDTH + 50):
            self.kill()
    
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed"""
        self.health -= damage
        if self.health <= 0:
            return True
        return False


class Debris(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """Initialize debris"""
        super().__init__()
        
        self.rotation = 0
        self.rotation_speed = random.uniform(-1.5, 1.5)  # Slower rotation
        
        # Load debris sprite from sheet
        self.load_debris_sprite()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Set movement (very slow drift)
        self.speed_y = random.uniform(0.1, 0.4)  # Much slower downward drift
        self.speed_x = random.uniform(-0.15, 0.15)  # Much slower horizontal drift
        
        # Debris is fragile
        self.health = 1
        self.score_value = 2
        
    def load_debris_sprite(self):
        """Load individual debris sprite from sheet"""
        debris_sheet = pygame.image.load("/home/jeffawe/amazon-build/assets/images/Debris-Sheet.png").convert_alpha()
        
        # The sheet contains 6 debris pieces in a single row
        sheet_width = debris_sheet.get_width()
        sheet_height = debris_sheet.get_height()
        debris_width = sheet_width // 6  # 6 debris pieces in the sheet
        
        # Choose a random debris piece
        debris_index = random.randint(0, 5)
        
        # Cut out the specific debris piece
        x = debris_index * debris_width
        debris_rect = pygame.Rect(x, 0, debris_width, sheet_height)
        self.original_image = debris_sheet.subsurface(debris_rect).copy()
        self.image = self.original_image
        
        print(f"Loaded debris piece (index {debris_index})")
        
    def update(self):
        """Update debris position and rotation"""
        # Very slow drift movement
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Slow rotation
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
        
        # Remove if off screen
        if (self.rect.top > SCREEN_HEIGHT + 50 or 
            self.rect.right < -50 or 
            self.rect.left > SCREEN_WIDTH + 50):
            self.kill()
    
    def take_damage(self, damage=1):
        """Debris is destroyed in one hit"""
        return True
