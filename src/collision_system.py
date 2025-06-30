"""
Collision Detection System for Retro Space Shooter
Handles all collision detection and physics responses with health system
"""
import pygame
import math
from explosion import Explosion
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
    
    def check_player_bomb_collisions(self, player, bombs):
        """Check for collisions between player and bombs"""
        collision_events = []
        
        # Check player vs bombs
        for bomb in bombs:
            if self.check_collision(player.rect, bomb.rect):
                collision_events.append({
                    'type': 'player_bomb',
                    'player': player,
                    'bomb': bomb,
                    'collision_point': self.get_collision_point(player.rect, bomb.rect)
                })
        
        return collision_events
    
    def check_player_powerup_collisions(self, player, powerups):
        """Check for collisions between player and power-ups"""
        collision_events = []
        
        # Check player vs power-ups
        for powerup in powerups:
            if self.check_collision(player.rect, powerup.rect):
                collision_events.append({
                    'type': 'player_powerup',
                    'player': player,
                    'powerup': powerup,
                    'collision_point': self.get_collision_point(player.rect, powerup.rect)
                })
        
        return collision_events
    
    def check_projectile_bomb_collisions(self, projectiles, bombs):
        """Check for collisions between projectiles and bombs"""
        collision_events = []
        
        # Check projectiles vs bombs
        for projectile in projectiles:
            for bomb in bombs:
                if self.check_collision(projectile.rect, bomb.rect):
                    collision_events.append({
                        'type': 'projectile_bomb',
                        'projectile': projectile,
                        'bomb': bomb,
                        'collision_point': self.get_collision_point(projectile.rect, bomb.rect)
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
        explosion = None
        
        if collision_type == 'player_enemy':
            enemy = collision_event['enemy']
            explosion = self.handle_player_enemy_collision(player, enemy, collision_event['collision_point'])
            
        elif collision_type == 'player_asteroid':
            asteroid = collision_event['asteroid']
            explosion = self.handle_player_asteroid_collision(player, asteroid, collision_event['collision_point'])
            
        elif collision_type == 'player_debris':
            debris = collision_event['debris']
            explosion = self.handle_player_debris_collision(player, debris, collision_event['collision_point'])
        
        return explosion
    
    def handle_player_bomb_collision(self, player, bomb, collision_point):
        """Handle collision between player and bomb with massive damage and explosion"""
        # Calculate 40% of max health as damage
        max_health = player.health_system.max_health
        bomb_damage = int(max_health * 0.4)  # 40% damage
        
        # Player takes massive damage from bomb
        player_died = player.take_damage(bomb_damage, "bomb explosion")
        
        # Create explosion at bomb location (bombs always explode on contact)
        bomb_explosion = Explosion(bomb.rect.centerx, bomb.rect.centery, "bomb")
        
        # Remove the bomb (it exploded)
        bomb.kill()
        
        # print(f"💣 BOMB EXPLOSION! Player took {bomb_damage} damage ({bomb_damage/max_health*100:.0f}% of max health)")
        
        # If player died from bomb, create player explosion too
        if player_died:
            player_explosion = Explosion(player.rect.centerx, player.rect.centery, "player")
            # print("💥 Player killed by bomb explosion!")
            return [bomb_explosion, player_explosion]  # Return both explosions
        
        return [bomb_explosion]  # Return just bomb explosion
    
    def handle_player_powerup_collision(self, player, powerup):
        """Handle collision between player and power-up"""
        # Player collects the power-up
        message = player.collect_powerup(powerup.powerup_type)
        
        # Remove the power-up
        powerup.kill()
        
        # print(f"🎁 Player collected {powerup.powerup_type} power-up: {message}")
        return message
    
    def handle_projectile_bomb_collision(self, projectile, bomb):
        """Handle collision between projectile and bomb - bomb explodes"""
        from explosion import Explosion
        
        # Create bomb explosion at bomb location
        bomb_explosion = Explosion(bomb.rect.centerx, bomb.rect.centery, "bomb")
        
        # Remove both projectile and bomb
        projectile.kill()
        bomb.kill()
        
        # print(f"💥 Projectile hit bomb! Bomb destroyed by player shot at ({bomb.rect.centerx}, {bomb.rect.centery})")
        return bomb_explosion
    
    def handle_player_enemy_collision(self, player, enemy, collision_point):
        """Handle collision between player and enemy ship"""
        # Player takes damage from collision
        player_died = player.take_damage(20, f"collision with {enemy.enemy_type}")
        
        # Calculate separation vector
        dx = player.rect.centerx - enemy.rect.centerx
        dy = player.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and apply separation
            separation_force = 5  # Pixels to separate
            dx = (dx / distance) * separation_force
            dy = (dy / distance) * separation_force
            
            # Move player away from enemy (only if alive)
            if player.is_alive():
                player.rect.x += dx
                player.rect.y += dy
                
                # Keep player on screen
                player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # print(f"Player collided with {enemy.enemy_type}! Took 20 damage")
            
            # Return explosion if player died
            if player_died:
                return Explosion(player.rect.centerx, player.rect.centery, "player")
            
            return None  # No explosion if player survived
        
        return None
    
    def handle_player_asteroid_collision(self, player, asteroid, collision_point):
        """Handle collision between player and asteroid with physics response"""
        # Player takes damage from collision
        player_died = player.take_damage(10, "asteroid collision")
        
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
            
            # Apply knockback to player (only if alive)
            if player.is_alive():
                player.rect.x += dx
                player.rect.y += dy
                
                # Keep player on screen
                player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Add some rotation to asteroid from impact
            if hasattr(asteroid, 'rotation_speed'):
                asteroid.rotation_speed += knockback_force * 0.5
            
            # print(f"Player hit asteroid! Took 10 damage, knockback: {knockback_force:.1f}")
            
            # Return explosion if player died
            if player_died:
                return Explosion(player.rect.centerx, player.rect.centery, "player")
            
            return None  # No explosion if player survived
        
        return None
    
    def handle_player_debris_collision(self, player, debris, collision_point):
        """Handle collision between player and debris with lighter physics response"""
        # Player takes light damage from debris
        player_died = player.take_damage(5, "debris collision")
        
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
            
            # Apply knockback to player (only if alive)
            if player.is_alive():
                player.rect.x += dx
                player.rect.y += dy
                
                # Keep player on screen
                player.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Debris might get pushed away too
            debris.rect.x -= dx * 0.3  # Debris moves less
            debris.rect.y -= dy * 0.3
            
            # print(f"Player hit debris! Took 5 damage, knockback: {knockback_force:.1f}")
            
            # Return explosion if player died
            if player_died:
                return Explosion(player.rect.centerx, player.rect.centery, "player")
            
            return None  # No explosion if player survived
        
        return None
    
    def handle_projectile_collision(self, collision_event, player=None):
        """Handle projectile collision events with energy effect support"""
        collision_type = collision_event['type']
        
        if collision_type == 'projectile_enemy':
            projectile = collision_event['projectile']
            enemy = collision_event['enemy']
            
            # Check for energy effect before destroying enemy
            energy_destroyed = []
            if player and player.has_energy_effect():
                # Apply energy area effect
                all_enemies = enemy.groups()[0] if enemy.groups() else []
                explosions_list = []
                energy_destroyed = player.energy_effect.apply_area_effect(enemy, all_enemies, explosions_list)
                
                # Return all explosions from energy effect
                if energy_destroyed:
                    projectile.kill()
                    return explosions_list
            
            # Normal enemy damage
            if enemy.take_damage(1):
                # Enemy destroyed - create explosion
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, "enemy")
                enemy.kill()  # Enemy destroyed
                # print(f"Enemy {enemy.enemy_type} destroyed!")
                
                # Remove projectile
                projectile.kill()
                return explosion  # Return explosion to be added to game
            
            # Enemy survived - just remove projectile
            projectile.kill()
            return None
            
        elif collision_type == 'projectile_asteroid':
            projectile = collision_event['projectile']
            asteroid = collision_event['asteroid']
            
            # Damage asteroid
            if asteroid.take_damage(1):
                # Asteroid destroyed - create explosion
                explosion = Explosion(asteroid.rect.centerx, asteroid.rect.centery, "asteroid")
                asteroid.kill()  # Asteroid destroyed
                # print(f"Asteroid destroyed!")
                
                # Remove projectile
                projectile.kill()
                return explosion  # Return explosion to be added to game
            
            # Asteroid survived - just remove projectile
            projectile.kill()
            return None
            
        elif collision_type == 'projectile_debris':
            projectile = collision_event['projectile']
            debris = collision_event['debris']
            
            # Debris is always destroyed by projectiles - create small explosion
            explosion = Explosion(debris.rect.centerx, debris.rect.centery, "debris")
            debris.kill()
            projectile.kill()
            # print("Debris destroyed!")
            return explosion  # Return explosion to be added to game
            
        elif collision_type == 'enemy_projectile_player':
            projectile = collision_event['projectile']
            player = collision_event['player']
            
            # Player takes damage from enemy projectile
            player_died = player.take_damage(15, "enemy projectile")
            projectile.kill()
            
            # print("Player hit by enemy projectile! Took 15 damage")
            
            # Return explosion if player died
            if player_died:
                return Explosion(player.rect.centerx, player.rect.centery, "player")
            
            return None  # No explosion if player survived
        
        return None
    
    def process_safe_collisions(self, player, powerups=None):
        """Process only safe collisions (power-ups) - no damage to player"""
        collision_results = {
            'player_collisions': 0,
            'projectile_hits': 0,
            'enemies_destroyed': 0,
            'explosions': [],
            'powerup_messages': [],
            'powerups_collected': 0,
            'bombs_shot': 0
        }
        
        # Only process power-up collections (safe)
        if powerups:
            for powerup in powerups:
                if self.check_collision(player.rect, powerup.rect):
                    # Player collected power-up
                    result = player.collect_powerup(powerup.powerup_type)
                    if result:
                        collision_results['powerup_messages'].append(result)
                        collision_results['powerups_collected'] += 1
                        powerup.kill()  # Remove power-up
        
        return collision_results
    
    def process_all_collisions(self, player, enemies, asteroids, debris, projectiles, enemy_projectiles, bombs=None, powerups=None):
        """Process all collision detection and responses"""
        collision_results = {
            'player_collisions': 0,
            'projectile_hits': 0,
            'enemies_destroyed': 0,
            'asteroids_destroyed': 0,
            'debris_destroyed': 0,
            'bomb_explosions': 0,
            'powerups_collected': 0,
            'bombs_shot': 0,  # New stat for bombs destroyed by projectiles
            'explosions': [],  # List of explosions to add to game
            'powerup_messages': []  # List of power-up collection messages
        }
        
        # Check player vs environment collisions
        env_collisions = self.check_player_environment_collisions(player, enemies, asteroids, debris)
        for collision in env_collisions:
            explosion = self.handle_player_environment_collision(collision)
            if explosion:
                collision_results['explosions'].append(explosion)
            
            # Always count as a collision regardless of explosion
            collision_results['player_collisions'] += 1
        
        # Check player vs bomb collisions
        if bombs:
            bomb_collisions = self.check_player_bomb_collisions(player, bombs)
            for collision in bomb_collisions:
                explosions = self.handle_player_bomb_collision(
                    collision['player'], 
                    collision['bomb'], 
                    collision['collision_point']
                )
                
                # Add all explosions (bomb explosion + possible player explosion)
                if explosions:
                    for explosion in explosions:
                        collision_results['explosions'].append(explosion)
                
                collision_results['bomb_explosions'] += 1
                collision_results['player_collisions'] += 1
        
        # Check player vs power-up collisions
        if powerups:
            powerup_collisions = self.check_player_powerup_collisions(player, powerups)
            for collision in powerup_collisions:
                message = self.handle_player_powerup_collision(
                    collision['player'], 
                    collision['powerup']
                )
                
                collision_results['powerups_collected'] += 1
                collision_results['powerup_messages'].append(message)
        
        # Check projectile vs bomb collisions
        if bombs:
            projectile_bomb_collisions = self.check_projectile_bomb_collisions(projectiles, bombs)
            for collision in projectile_bomb_collisions:
                explosion = self.handle_projectile_bomb_collision(
                    collision['projectile'], 
                    collision['bomb']
                )
                
                collision_results['bombs_shot'] += 1
                collision_results['explosions'].append(explosion)
        
        # Check projectile collisions
        proj_collisions = self.check_projectile_collisions(projectiles, enemy_projectiles, enemies, asteroids, debris, player)
        for collision in proj_collisions:
            explosion = self.handle_projectile_collision(collision, player)
            if explosion:
                if isinstance(explosion, list):
                    # Multiple explosions from energy effect
                    collision_results['explosions'].extend(explosion)
                else:
                    # Single explosion
                    collision_results['explosions'].append(explosion)
            
            # Always count as a hit regardless of explosion
            collision_results['projectile_hits'] += 1
            
            # Count specific destruction types
            if collision['type'] == 'projectile_enemy':
                collision_results['enemies_destroyed'] += 1
            elif collision['type'] == 'projectile_asteroid':
                collision_results['asteroids_destroyed'] += 1
            elif collision['type'] == 'projectile_debris':
                collision_results['debris_destroyed'] += 1
        
        return collision_results
