#!/usr/bin/env python3
"""
Boss Battle System - Final wave enhancement with laser and missile attacks
"""
import pygame
import random
from constants import *

class BossLaser:
    def __init__(self, laser_type, position):
        """Initialize a boss laser attack"""
        self.type = laser_type  # 'horizontal' or 'vertical'
        self.warning_time = 60  # 1 second warning
        self.active_time = 120  # 2 seconds active
        self.total_time = self.warning_time + self.active_time
        self.timer = self.total_time
        
        if laser_type == 'horizontal':
            self.x = 0
            self.y = position
            self.width = SCREEN_WIDTH
            self.height = 20
        else:  # vertical
            self.x = position
            self.y = 0
            self.width = 20
            self.height = SCREEN_HEIGHT
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """Update laser state"""
        self.timer -= 1
        return self.timer > 0
    
    def is_warning(self):
        """Check if laser is in warning phase"""
        return self.timer > self.active_time
    
    def is_active(self):
        """Check if laser is actively damaging"""
        return 0 < self.timer <= self.active_time

class BossMissile:
    def __init__(self, start_x, start_y, direction):
        """Initialize a boss missile"""
        self.x = float(start_x)
        self.y = float(start_y)
        self.direction = direction  # 'horizontal' or 'vertical'
        self.speed = 4
        
        if direction == 'horizontal':
            self.dx = random.choice([-self.speed, self.speed])
            self.dy = 0
        else:  # vertical
            self.dx = 0
            self.dy = random.choice([-self.speed, self.speed])
        
        self.width = 16
        self.height = 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """Update missile position"""
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Remove if off screen
        return (0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT)

class PlayerMissile:
    def __init__(self, start_x, start_y):
        """Initialize player missile to boss"""
        self.x = start_x
        self.y = start_y
        self.speed = 10
        self.active = True
        
        # Load the actual missile sprite
        try:
            missile_image = pygame.image.load("/home/jeffawe/amazon-build/SpaceShooter/Enemies/Missile.png")
            self.image = missile_image.convert_alpha()
            # Scale if needed (keep original size for now)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            print(f"🚀 Loaded missile sprite: {self.width}x{self.height}")
        except Exception as e:
            print(f"⚠️ Could not load missile sprite: {e}")
            # Fallback: create simple rectangle
            self.width = 8
            self.height = 20
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 255, 255), (0, 0, self.width, self.height))
        
    def update(self):
        """Update missile movement"""
        self.y -= self.speed
        return self.y > -50  # Remove when off screen

class BossBattle:
    def __init__(self):
        """Initialize boss battle system"""
        self.active = False
        self.boss_health = 100
        self.max_boss_health = 100
        
        # Attack timers
        self.laser_cooldown = 0
        self.laser_cooldown_max = 300  # 5 seconds
        self.missile_cooldown = 0
        self.missile_cooldown_max = 180  # 3 seconds
        
        # Active attacks
        self.active_lasers = []
        self.active_missiles = []
        self.player_missiles = []  # Track player missiles to boss
        
        print("🏆 Boss Battle System initialized")
    
    def start_boss_battle(self):
        """Start the boss battle"""
        self.active = True
        self.boss_health = self.max_boss_health
        self.laser_cooldown = 120  # Start with 2 second delay
        self.missile_cooldown = 60   # Start with 1 second delay
        
        # Clear existing attacks
        self.active_lasers.clear()
        self.active_missiles.clear()
        self.player_missiles.clear()
        
        print("🏆 BOSS BATTLE STARTED!")
        print("   Dodge lasers and missiles while fighting enemies!")
    
    def update(self):
        """Update boss battle state"""
        if not self.active:
            return
        
        # Update attack cooldowns
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1
        
        # Fire attacks when ready
        if self.laser_cooldown <= 0:
            self.fire_laser()
            self.laser_cooldown = self.laser_cooldown_max + random.randint(-60, 60)
        
        if self.missile_cooldown <= 0:
            self.fire_missile()
            self.missile_cooldown = self.missile_cooldown_max + random.randint(-30, 30)
        
        # Update active attacks
        self.active_lasers = [laser for laser in self.active_lasers if laser.update()]
        self.active_missiles = [missile for missile in self.active_missiles if missile.update()]
        self.player_missiles = [missile for missile in self.player_missiles if missile.update()]
    
    def fire_laser(self):
        """Fire a laser attack"""
        laser_type = random.choice(['horizontal', 'vertical'])
        
        if laser_type == 'horizontal':
            position = random.randint(100, SCREEN_HEIGHT - 100)
        else:
            position = random.randint(100, SCREEN_WIDTH - 100)
        
        laser = BossLaser(laser_type, position)
        self.active_lasers.append(laser)
        print(f"🔴 Boss fired {laser_type} laser!")
    
    def fire_missile(self):
        """Fire a missile attack"""
        direction = random.choice(['horizontal', 'vertical'])
        
        if direction == 'horizontal':
            start_x = random.choice([0, SCREEN_WIDTH])
            start_y = random.randint(50, SCREEN_HEIGHT - 50)
        else:
            start_x = random.randint(50, SCREEN_WIDTH - 50)
            start_y = random.choice([0, SCREEN_HEIGHT])
        
        missile = BossMissile(start_x, start_y, direction)
        self.active_missiles.append(missile)
        print(f"🚀 Boss fired {direction} missile!")
    
    def check_laser_collision(self, player_rect):
        """Check if player collides with active lasers (only once per laser)"""
        for laser in self.active_lasers:
            if laser.is_active() and not hasattr(laser, 'hit_player'):
                if laser.rect.colliderect(player_rect):
                    laser.hit_player = True  # Mark as hit to prevent multiple hits
                    return True
        return False
    
    def check_missile_collision(self, player_rect):
        """Check if player collides with missiles"""
        for missile in self.active_missiles[:]:
            if missile.rect.colliderect(player_rect):
                self.active_missiles.remove(missile)
                return True
        return False
    
    def fire_player_missile(self, player_x, player_y):
        """Fire a player missile at the boss"""
        missile = PlayerMissile(player_x, player_y)
        self.player_missiles.append(missile)
        print("🚀 Player missile fired at boss!")
    
    def damage_boss(self, damage):
        """Damage the boss"""
        if self.active:
            self.boss_health -= damage
            self.boss_health = max(0, self.boss_health)
            print(f"🎯 Boss took {damage} damage! Health: {self.boss_health}/{self.max_boss_health}")
            
            if self.boss_health <= 0:
                self.active = False
                print("🏆 BOSS DEFEATED!")
                return True
        return False
    
    def draw(self, screen):
        """Draw boss battle elements"""
        # Draw lasers
        for laser in self.active_lasers:
            if laser.is_warning():
                # Warning phase - red outline
                color = (255, 100, 100)
                pygame.draw.rect(screen, color, laser.rect, 3)
            elif laser.is_active():
                # Active phase - solid red
                color = (255, 0, 0)
                pygame.draw.rect(screen, color, laser.rect)
        
        # Draw missiles
        for missile in self.active_missiles:
            color = (255, 150, 0)  # Orange
            pygame.draw.rect(screen, color, missile.rect)
        
        # Draw player missiles to boss
        for missile in self.player_missiles:
            # Draw the actual missile sprite
            screen.blit(missile.image, (missile.x - missile.width//2, missile.y))
        
        # Draw boss health bar
        if self.active:
            self.draw_boss_health(screen)
    
    def draw_boss_health(self, screen):
        """Draw boss health bar at bottom"""
        bar_width = SCREEN_WIDTH - 100
        bar_height = 20
        bar_x = 50
        bar_y = SCREEN_HEIGHT - 40
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health bar
        health_percentage = self.boss_health / self.max_boss_health
        health_width = int(bar_width * health_percentage)
        
        if health_percentage > 0.6:
            health_color = (255, 0, 0)
        elif health_percentage > 0.3:
            health_color = (255, 150, 0)
        else:
            health_color = (255, 255, 0)
        
        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Label
        font = pygame.font.Font(None, 24)
        label = font.render("BOSS", True, (255, 255, 255))
        screen.blit(label, (bar_x, bar_y - 25))
        
        # Health text
        health_text = font.render(f"{self.boss_health}/{self.max_boss_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(health_text, text_rect)
    
    def get_info(self):
        """Get boss battle info"""
        return {
            'active': self.active,
            'boss_health': self.boss_health,
            'max_boss_health': self.max_boss_health,
            'boss_defeated': self.boss_health <= 0,
            'active_lasers': len(self.active_lasers),
            'active_missiles': len(self.active_missiles)
        }
