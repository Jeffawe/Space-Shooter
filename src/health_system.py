"""
Health system for Retro Space Shooter
Handles player and enemy health with visual health bars
"""
import pygame
from constants import *

class HealthBar:
    def __init__(self, max_health, x, y, width=100, height=10, show_text=True):
        """Initialize a health bar"""
        self.max_health = max_health
        self.current_health = max_health
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.show_text = show_text
        
        # Colors for health bar
        self.bg_color = (60, 60, 60)      # Dark gray background
        self.health_color = (0, 255, 0)   # Green for healthy
        self.warning_color = (255, 255, 0) # Yellow for warning
        self.danger_color = (255, 0, 0)   # Red for danger
        self.border_color = (255, 255, 255) # White border
        
    def take_damage(self, damage):
        """Take damage and return True if health reaches 0"""
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        return self.current_health <= 0
    
    def heal(self, amount):
        """Heal by amount (up to max health)"""
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
    
    def get_health_percentage(self):
        """Get health as percentage (0.0 to 1.0)"""
        return self.current_health / self.max_health if self.max_health > 0 else 0
    
    def get_health_color(self):
        """Get color based on current health percentage"""
        percentage = self.get_health_percentage()
        if percentage > 0.6:
            return self.health_color  # Green
        elif percentage > 0.3:
            return self.warning_color  # Yellow
        else:
            return self.danger_color  # Red
    
    def draw(self, screen):
        """Draw the health bar"""
        # Draw background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect)
        
        # Draw health fill
        health_width = int(self.width * self.get_health_percentage())
        if health_width > 0:
            health_rect = pygame.Rect(self.x, self.y, health_width, self.height)
            pygame.draw.rect(screen, self.get_health_color(), health_rect)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, bg_rect, 1)
        
        # Draw text if enabled
        if self.show_text:
            font = pygame.font.Font(None, 20)
            text = f"{self.current_health}/{self.max_health}"
            text_surface = font.render(text, True, WHITE)
            text_x = self.x + self.width + 5
            text_y = self.y - 2
            screen.blit(text_surface, (text_x, text_y))


class PlayerHealth:
    def __init__(self, max_health=100):
        """Initialize player health system"""
        self.max_health = max_health
        self.current_health = max_health
        self.is_alive = True
        self.invulnerable_time = 0  # Frames of invulnerability after taking damage
        self.max_invulnerable_time = 60  # 1 second at 60 FPS
        self.immune_to_damage = False  # Complete immunity during wave transitions
        
        # Create health bar in bottom left
        self.health_bar = HealthBar(max_health, 10, SCREEN_HEIGHT - 30, 150, 15, True)
        
        print(f"Player health system initialized: {max_health} HP")
        
    def take_damage(self, damage, damage_source="unknown"):
        """Take damage if not invulnerable or immune"""
        if not self.is_alive or self.invulnerable_time > 0 or self.immune_to_damage:
            return False  # No damage taken
        
        self.current_health -= damage
        self.health_bar.current_health = self.current_health
        
        # Set invulnerability period
        self.invulnerable_time = self.max_invulnerable_time
        
        # print(f"Player took {damage} damage from {damage_source}! Health: {self.current_health}/{self.max_health}")
        
        # Check if player died
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            print("Player died!")
            return True  # Player died
        
        return False  # Player survived
    
    def heal(self, amount):
        """Heal the player"""
        if not self.is_alive:
            return
        
        old_health = self.current_health
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        
        self.health_bar.current_health = self.current_health
        
    
    def update(self):
        """Update health system"""
        # Update invulnerability timer
        if self.invulnerable_time > 0:
            self.invulnerable_time -= 1
    
    def set_immunity(self, immune):
        """Set damage immunity state (for wave transitions)"""
        self.immune_to_damage = immune
    
    def is_immune(self):
        """Check if player is immune to damage"""
        return self.immune_to_damage
    
    def is_invulnerable(self):
        """Check if player is currently invulnerable"""
        return self.invulnerable_time > 0
    
    def get_health_percentage(self):
        """Get health as percentage"""
        return self.current_health / self.max_health if self.max_health > 0 else 0
    
    def draw(self, screen):
        """Draw player health bar"""
        # Draw "HEALTH" label
        font = pygame.font.Font(None, 24)
        label = font.render("HEALTH", True, WHITE)
        screen.blit(label, (10, SCREEN_HEIGHT - 55))
        
        # Draw health bar
        self.health_bar.draw(screen)
        
        # Draw invulnerability indicator
        if self.is_invulnerable():
            inv_text = pygame.font.Font(None, 16).render("INVULNERABLE", True, YELLOW)
            screen.blit(inv_text, (10, SCREEN_HEIGHT - 75))


class EnemyHealth:
    def __init__(self, enemy, max_health=1):
        """Initialize enemy health system"""
        self.enemy = enemy
        self.max_health = max_health
        self.current_health = max_health
        self.is_alive = True
        
        # Create small health bar above enemy (only if health > 1)
        if max_health > 1:
            self.health_bar = HealthBar(max_health, 0, 0, 30, 4, False)
            self.show_health_bar = True
        else:
            self.health_bar = None
            self.show_health_bar = False
    
    def take_damage(self, damage):
        """Take damage and return True if enemy dies"""
        if not self.is_alive:
            return False
        
        self.current_health -= damage
        if self.health_bar:
            self.health_bar.current_health = self.current_health
        
        # print(f"{self.enemy.enemy_type} took {damage} damage! Health: {self.current_health}/{self.max_health}")
        
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            print(f"{self.enemy.enemy_type} destroyed!")
            return True  # Enemy died
        
        return False  # Enemy survived
    
    def update(self):
        """Update enemy health system"""
        # Update health bar position to follow enemy
        if self.health_bar and self.show_health_bar:
            self.health_bar.x = self.enemy.rect.centerx - 15
            self.health_bar.y = self.enemy.rect.top - 8
    
    def draw(self, screen):
        """Draw enemy health bar if applicable"""
        if self.health_bar and self.show_health_bar and self.is_alive:
            # Only show health bar if enemy is damaged
            if self.current_health < self.max_health:
                self.health_bar.draw(screen)
