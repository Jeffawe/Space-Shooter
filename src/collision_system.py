"""
Collision Detection System for Retro Space Shooter
Handles all collision detection and physics responses
"""
import pygame
import math
from constants import *

class CollisionSystem:
    def __init__(self):
        """Initialize the collision detection system"""
        self.collision_events = []  # Store collision events for processing
        
    def check_player_environment_collisions(self, player, enemies, asteroids, debris):
        """Check player collisions with environment objects"""
        collision_events = []
        
        # Check player vs enemies
        for enemy in enemies:
            if self.check_collision(player.rect, enemy.rect):
                collision_events.append({
                    'type': 'player_enemy',
                    'player': player,
                    'enemy': enemy,
                    'collision_point': self.get_collision_point(player.rect, enemy.rect)
                })
        
        # Check player vs asteroids
        for asteroid in asteroids:
            if self.check_collision(player.rect, asteroid.rect):
                collision_events.append({
                    'type': 'player_asteroid',
                    'player': player,
                    'asteroid': asteroid,
                    'collision_point': self.get_collision_point(player.rect, asteroid.rect)
                })
        
        # Check player vs debris
        for debris_piece in debris:
            if self.check_collision(player.rect, debris_piece.rect):
                collision_events.append({
                    'type': 'player_debris',
                    'player': player,
                    'debris': debris_piece,
                    'collision_point': self.get_collision_point(player.rect, debris_piece.rect)
                })
        
        return collision_events
    
    def check_projectile_collisions(self, projectiles, enemy_projectiles, enemies, asteroids, debris, player):
        """Check projectile collisions with various targets"""
        collision_events = []
        
        # Player projectiles vs enemies
        for projectile in projectiles:
            for enemy in enemies:
                if self.check_collision(projectile.rect, enemy.rect):
                    collision_events.append({
                        'type': 'projectile_enemy',
                        'projectile': projectile,
                        'enemy': enemy,
                        'collision_point': self.get_collision_point(projectile.rect, enemy.rect)
                    })
        
        # Player projectiles vs asteroids
        for projectile in projectiles:
            for asteroid in asteroids:
                if self.check_collision(projectile.rect, asteroid.rect):
                    collision_events.append({
                        'type': 'projectile_asteroid',
                        'projectile': projectile,
                        'asteroid': asteroid,
                        'collision_point': self.get_collision_point(projectile.rect, asteroid.rect)
                    })
        
        # Player projectiles vs debris
        for projectile in projectiles:
            for debris_piece in debris:
                if self.check_collision(projectile.rect, debris_piece.rect):
                    collision_events.append({
                        'type': 'projectile_debris',
                        'projectile': projectile,
                        'debris': debris_piece,
                        'collision_point': self.get_collision_point(projectile.rect, debris_piece.rect)
                    })
        
        # Enemy projectiles vs player
        for enemy_projectile in enemy_projectiles:
            if self.check_collision(enemy_projectile.rect, player.rect):
                collision_events.append({
                    'type': 'enemy_projectile_player',
                    'projectile': enemy_projectile,
                    'player': player,
                    'collision_point': self.get_collision_point(enemy_projectile.rect, player.rect)
                })
        
        return collision_events
    
    def check_collision(self, rect1, rect2):
        """Basic rectangle collision detection"""
        return rect1.colliderect(rect2)
    
    def get_collision_point(self, rect1, rect2):
        """Get the center point of collision between two rectangles"""
        # Find the overlapping area
        left = max(rect1.left, rect2.left)
        right = min(rect1.right, rect2.right)
        top = max(rect1.top, rect2.top)
        bottom = min(rect1.bottom, rect2.bottom)
        
        # Return center of overlap
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        return (center_x, center_y)
    
    def handle_player_environment_collision(self, collision_event):
        """Handle collision between player and environment objects"""
        collision_type = collision_event['type']
        player = collision_event['player']
        
        if collision_type == 'player_enemy':
            enemy = collision_event['enemy']
            self.handle_player_enemy_collision(player, enemy, collision_event['collision_point'])
            
        elif collision_type == 'player_asteroid':
            asteroid = collision_event['asteroid']
            self.handle_player_asteroid_collision(player, asteroid, collision_event['collision_point'])
            
        elif collision_type == 'player_debris':
            debris = collision_event['debris']
            self.handle_player_debris_collision(player, debris, collision_event['collision_point'])
    
    def handle_player_enemy_collision(self, player, enemy, collision_point):
        """Handle collision between player and enemy ship"""
        # Calculate separation vector
        dx = player.rect.centerx - enemy.rect.centerx
        dy = player.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and apply separation
            separation_force = 5  # Pixels to separate
            dx = (dx / distance) * separation_force
            dy = (dy / distance) * separation_force
            
            # Move player away from enemy
            player.rect.x += dx
            player.rect.y += dy
            
            # Keep player on screen
            player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            print(f"Player collided with {enemy.enemy_type}!")
            return True  # Collision handled
        
        return False
    
    def handle_player_asteroid_collision(self, player, asteroid, collision_point):
        """Handle collision between player and asteroid with physics response"""
        # Calculate collision vector
        dx = player.rect.centerx - asteroid.rect.centerx
        dy = player.rect.centery - asteroid.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Calculate player's current speed (approximate)
            player_speed = getattr(player, 'last_speed', 3)  # Default speed if not available
            
            # Physics-based knockback based on speed
            knockback_force = min(player_speed * 2, 10)  # Cap at 10 pixels
            
            # Normalize collision vector and apply knockback
            dx = (dx / distance) * knockback_force
            dy = (dy / distance) * knockback_force
            
            # Apply knockback to player
            player.rect.x += dx
            player.rect.y += dy
            
            # Keep player on screen
            player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add some rotation to asteroid from impact
            if hasattr(asteroid, 'rotation_speed'):
                asteroid.rotation_speed += knockback_force * 0.5
            
            print(f"Player hit asteroid! Knockback force: {knockback_force:.1f}")
            return True  # Collision handled
        
        return False
    
    def handle_player_debris_collision(self, player, debris, collision_point):
        """Handle collision between player and debris with lighter physics response"""
        # Calculate collision vector
        dx = player.rect.centerx - debris.rect.centerx
        dy = player.rect.centery - debris.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Lighter knockback for debris (smaller objects)
            player_speed = getattr(player, 'last_speed', 3)
            knockback_force = min(player_speed * 1.5, 7)  # Lighter than asteroids
            
            # Normalize and apply knockback
            dx = (dx / distance) * knockback_force
            dy = (dy / distance) * knockback_force
            
            # Apply knockback to player
            player.rect.x += dx
            player.rect.y += dy
            
            # Keep player on screen
            player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Debris might get pushed away too
            debris.rect.x -= dx * 0.3  # Debris moves less
            debris.rect.y -= dy * 0.3
            
            print(f"Player hit debris! Light knockback: {knockback_force:.1f}")
            return True  # Collision handled
        
        return False
    
    def handle_projectile_collision(self, collision_event):
        """Handle projectile collision events"""
        collision_type = collision_event['type']
        
        if collision_type == 'projectile_enemy':
            projectile = collision_event['projectile']
            enemy = collision_event['enemy']
            
            # Damage enemy
            if enemy.take_damage(1):
                enemy.kill()  # Enemy destroyed
                print(f"Enemy {enemy.enemy_type} destroyed!")
            
            # Remove projectile
            projectile.kill()
            return True
            
        elif collision_type == 'projectile_asteroid':
            projectile = collision_event['projectile']
            asteroid = collision_event['asteroid']
            
            # Damage asteroid
            if asteroid.take_damage(1):
                asteroid.kill()  # Asteroid destroyed
                print(f"Asteroid destroyed!")
            
            # Remove projectile
            projectile.kill()
            return True
            
        elif collision_type == 'projectile_debris':
            projectile = collision_event['projectile']
            debris = collision_event['debris']
            
            # Debris is always destroyed by projectiles
            debris.kill()
            projectile.kill()
            print("Debris destroyed!")
            return True
            
        elif collision_type == 'enemy_projectile_player':
            projectile = collision_event['projectile']
            player = collision_event['player']
            
            # TODO: Damage player when health system is implemented
            projectile.kill()
            print("Player hit by enemy projectile!")
            return True
        
        return False
    
    def process_all_collisions(self, player, enemies, asteroids, debris, projectiles, enemy_projectiles):
        """Process all collision detection and responses"""
        collision_results = {
            'player_collisions': 0,
            'projectile_hits': 0,
            'enemies_destroyed': 0,
            'asteroids_destroyed': 0,
            'debris_destroyed': 0
        }
        
        # Check player vs environment collisions
        env_collisions = self.check_player_environment_collisions(player, enemies, asteroids, debris)
        for collision in env_collisions:
            if self.handle_player_environment_collision(collision):
                collision_results['player_collisions'] += 1
        
        # Check projectile collisions
        proj_collisions = self.check_projectile_collisions(projectiles, enemy_projectiles, enemies, asteroids, debris, player)
        for collision in proj_collisions:
            if self.handle_projectile_collision(collision):
                collision_results['projectile_hits'] += 1
                
                # Count specific destruction types
                if collision['type'] == 'projectile_enemy':
                    collision_results['enemies_destroyed'] += 1
                elif collision['type'] == 'projectile_asteroid':
                    collision_results['asteroids_destroyed'] += 1
                elif collision['type'] == 'projectile_debris':
                    collision_results['debris_destroyed'] += 1
        
        return collision_results
