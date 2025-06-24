"""
Power-up system for Retro Space Shooter
HP Container: Increases player health
Energy Container: Enhances projectile destruction with area effects
"""
import pygame
import random
import math
from constants import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type, spawn_side="random"):
        """Initialize a power-up that floats from screen edges"""
        super().__init__()
        
        self.powerup_type = powerup_type
        self.spawn_side = spawn_side
        
        # Load power-up sprite
        self.load_sprite()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Floating movement - containers drift naturally across screen
        self.setup_floating_movement()
        
        # Lifetime - containers can drift off screen naturally
        self.lifetime = 1200  # 20 seconds - enough time to cross screen
        self.blink_timer = 0
        self.visible = True
        
        print(f"Spawned {powerup_type} power-up from {spawn_side} at ({x}, {y})")
        
    def setup_floating_movement(self):
        """Setup natural floating movement based on spawn side"""
        # Base floating animation
        self.float_amplitude = 15  # Gentle up/down floating
        self.float_speed = 0.05  # Slow floating rhythm
        self.float_offset = random.uniform(0, 6.28)  # Random start phase
        
        # Drift movement - containers float across screen
        if self.spawn_side == "left":
            # Spawn from left, drift right with slight upward/downward angle
            self.drift_x = random.uniform(0.5, 1.2)  # Rightward drift
            self.drift_y = random.uniform(-0.3, 0.3)  # Slight vertical drift
        elif self.spawn_side == "right":
            # Spawn from right, drift left with slight upward/downward angle
            self.drift_x = random.uniform(-1.2, -0.5)  # Leftward drift
            self.drift_y = random.uniform(-0.3, 0.3)  # Slight vertical drift
        elif self.spawn_side == "top":
            # Spawn from top, drift down with slight horizontal angle
            self.drift_x = random.uniform(-0.3, 0.3)  # Slight horizontal drift
            self.drift_y = random.uniform(0.5, 1.2)  # Downward drift
        elif self.spawn_side == "bottom":
            # Spawn from bottom, drift up with slight horizontal angle
            self.drift_x = random.uniform(-0.3, 0.3)  # Slight horizontal drift
            self.drift_y = random.uniform(-1.2, -0.5)  # Upward drift
        else:
            # Random drift direction
            angle = random.uniform(0, 6.28)  # Random angle
            speed = random.uniform(0.5, 1.0)
            self.drift_x = speed * math.cos(angle)
            self.drift_y = speed * math.sin(angle)
        
        # Store original position for floating calculation
        self.base_x = float(self.rect.centerx)
        self.base_y = float(self.rect.centery)
        
    def load_sprite(self):
        """Load the appropriate sprite for this power-up type"""
        try:
            if self.powerup_type == "health":
                self.image = pygame.image.load("/home/jeffawe/amazon-build/assets/images/HPContainer.png").convert_alpha()
            elif self.powerup_type == "energy":
                self.image = pygame.image.load("/home/jeffawe/amazon-build/assets/images/EnergyContainer.png").convert_alpha()
            else:
                # Fallback - create a colored square
                self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
                color = GREEN if self.powerup_type == "health" else BLUE
                pygame.draw.rect(self.image, color, (0, 0, 24, 24))
                
            print(f"Loaded {self.powerup_type} power-up sprite: {self.image.get_size()}")
            
        except pygame.error as e:
            print(f"Error loading {self.powerup_type} power-up sprite: {e}")
            # Create fallback sprite
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            color = GREEN if self.powerup_type == "health" else BLUE
            pygame.draw.rect(self.image, color, (0, 0, 24, 24))
    
    def update(self):
        """Update power-up floating movement and lifetime"""
        # Natural drift movement
        self.base_x += self.drift_x
        self.base_y += self.drift_y
        
        # Floating animation (gentle up/down bobbing)
        self.float_offset += self.float_speed
        import math
        float_offset_y = self.float_amplitude * math.sin(self.float_offset)
        
        # Apply both drift and floating
        self.rect.centerx = int(self.base_x)
        self.rect.centery = int(self.base_y + float_offset_y)
        
        # Update lifetime
        self.lifetime -= 1
        
        # Blinking effect when about to expire (last 3 seconds)
        if self.lifetime < 180:
            self.blink_timer += 1
            if self.blink_timer >= 10:  # Blink every 10 frames
                self.visible = not self.visible
                self.blink_timer = 0
        
        # Remove if expired or drifted off screen
        off_screen = (self.rect.right < -50 or self.rect.left > SCREEN_WIDTH + 50 or 
                     self.rect.bottom < -50 or self.rect.top > SCREEN_HEIGHT + 50)
        
        if self.lifetime <= 0 or off_screen:
            if off_screen:
                print(f"{self.powerup_type} power-up drifted off-screen")
            else:
                print(f"{self.powerup_type} power-up expired")
            self.kill()
    
    def draw(self, screen):
        """Draw power-up with blinking effect"""
        if self.visible:
            screen.blit(self.image, self.rect)

class EnergyEffect:
    """Manages the Energy power-up effect on the player"""
    def __init__(self, duration=300):  # 5 seconds at 60 FPS
        self.duration = duration
        self.remaining_time = duration
        self.active = True
        
        # Area effect patterns and their probabilities
        self.effect_patterns = {
            'horizontal': 40,    # 40% chance - clear horizontal line
            'vertical': 30,      # 30% chance - clear vertical line  
            'diagonal': 25,      # 25% chance - clear diagonal lines
            'screen_clear': 5    # 5% chance - clear entire screen (very rare!)
        }
        
        print(f"⚡ Energy effect activated! Duration: {duration/60:.1f} seconds")
        
    def update(self):
        """Update energy effect timer"""
        if self.active:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.active = False
                print("⚡ Energy effect wore off")
                return False
        return self.active
    
    def get_random_effect(self):
        """Get a random area effect pattern based on probabilities"""
        rand = random.randint(1, 100)
        
        if rand <= self.effect_patterns['screen_clear']:
            return 'screen_clear'
        elif rand <= self.effect_patterns['screen_clear'] + self.effect_patterns['diagonal']:
            return 'diagonal'
        elif rand <= self.effect_patterns['screen_clear'] + self.effect_patterns['diagonal'] + self.effect_patterns['vertical']:
            return 'vertical'
        else:
            return 'horizontal'
    
    def apply_area_effect(self, hit_enemy, all_enemies, explosions_list):
        """Apply area-of-effect destruction based on the hit enemy's position"""
        if not self.active:
            return []
        
        effect_type = self.get_random_effect()
        destroyed_enemies = []
        
        hit_x, hit_y = hit_enemy.rect.centerx, hit_enemy.rect.centery
        
        print(f"⚡ Energy effect triggered: {effect_type.upper()} at ({hit_x}, {hit_y})")
        
        if effect_type == 'horizontal':
            # Destroy all enemies in horizontal line (±50 pixels vertically)
            for enemy in all_enemies:
                if abs(enemy.rect.centery - hit_y) <= 50:
                    destroyed_enemies.append(enemy)
                    
        elif effect_type == 'vertical':
            # Destroy all enemies in vertical line (±50 pixels horizontally)
            for enemy in all_enemies:
                if abs(enemy.rect.centerx - hit_x) <= 50:
                    destroyed_enemies.append(enemy)
                    
        elif effect_type == 'diagonal':
            # Destroy enemies in both diagonal lines through the hit point
            for enemy in all_enemies:
                dx = abs(enemy.rect.centerx - hit_x)
                dy = abs(enemy.rect.centery - hit_y)
                # Check if enemy is on either diagonal (within tolerance)
                if abs(dx - dy) <= 30:  # Main diagonal
                    destroyed_enemies.append(enemy)
                elif abs(dx + dy - abs(hit_x - hit_y)) <= 30:  # Anti-diagonal
                    destroyed_enemies.append(enemy)
                    
        elif effect_type == 'screen_clear':
            # Destroy ALL enemies on screen (very rare!)
            destroyed_enemies = list(all_enemies)
            print("💥 SCREEN CLEAR! All enemies destroyed!")
        
        # Create explosions for all destroyed enemies
        for enemy in destroyed_enemies:
            from explosion import Explosion
            explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, "energy_blast")
            explosions_list.append(explosion)
            enemy.kill()
        
        print(f"⚡ Energy effect destroyed {len(destroyed_enemies)} enemies with {effect_type}")
        return destroyed_enemies
    
    def get_time_remaining(self):
        """Get remaining time in seconds"""
        return self.remaining_time / 60.0

class PowerUpSpawner:
    """Manages power-up spawning from screen edges"""
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = 360  # 6 seconds between spawns (increased from 10 seconds)
        self.spawn_chance = 0.6  # 60% chance to spawn when timer triggers (increased from 40%)
        
        # Power-up type probabilities (increased health chance)
        self.powerup_chances = {
            'health': 75,  # 75% chance for health (increased from 60%)
            'energy': 25   # 25% chance for energy (decreased from 40%)
        }
        
        # Spawn side probabilities
        self.spawn_sides = ['left', 'right', 'top', 'bottom']
        self.spawn_side_weights = [30, 30, 20, 20]  # Left/right more common
        
        print("🎁 Power-up spawner initialized - containers will float from screen edges")
    
    def update(self, powerups_group, all_sprites_group):
        """Update spawner and potentially create new power-ups"""
        self.spawn_timer += 1
        
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            
            # Check if we should spawn a power-up
            if random.random() < self.spawn_chance:
                self.spawn_powerup(powerups_group, all_sprites_group)
    
    def spawn_powerup(self, powerups_group, all_sprites_group):
        """Spawn a power-up from a random screen edge"""
        # Choose power-up type
        rand = random.randint(1, 100)
        if rand <= self.powerup_chances['health']:
            powerup_type = "health"
        else:
            powerup_type = "energy"
        
        # Choose spawn side (weighted random)
        spawn_side = random.choices(self.spawn_sides, weights=self.spawn_side_weights)[0]
        
        # Determine spawn position based on side
        if spawn_side == "left":
            x = -30  # Start off-screen left
            y = random.randint(50, SCREEN_HEIGHT - 50)
        elif spawn_side == "right":
            x = SCREEN_WIDTH + 30  # Start off-screen right
            y = random.randint(50, SCREEN_HEIGHT - 50)
        elif spawn_side == "top":
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = -30  # Start off-screen top
        else:  # bottom
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = SCREEN_HEIGHT + 30  # Start off-screen bottom
        
        # Create power-up
        powerup = PowerUp(x, y, powerup_type, spawn_side)
        powerups_group.add(powerup)
        all_sprites_group.add(powerup)
        
        print(f"🎁 Spawned {powerup_type} power-up from {spawn_side} edge at ({x}, {y})")
        return powerup
