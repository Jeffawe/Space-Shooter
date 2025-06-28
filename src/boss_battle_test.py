#!/usr/bin/env python3
"""
Boss Battle Test - Exact same as Wave 10 + Boss attacks
"""
import pygame
import sys
from game import Game
from boss_battle import BossBattle
from constants import *

def main():
    """Test boss battle using exact main game systems"""
    pygame.init()
    
    print("🏆 BOSS BATTLE TEST")
    print("Same as Wave 10 + Boss laser/missile attacks")
    print("Controls: WASD/Arrows=Move, Space=Shoot, Q=Bomb, ESC=Quit")
    print("")
    
    # Create normal game instance
    game = Game()
    
    # Add boss battle system
    game.boss_battle = BossBattle()
    
    # Set up for Wave 10 equivalent with easier settings for testing
    game.dialogue_system.active = False
    game.game_started = True
    
    # Configure wave manager for Wave 10 settings
    game.wave_manager.current_wave = 10
    game.wave_manager.wave_active = True
    game.wave_manager.wave_complete = False
    game.wave_manager.story_complete = False
    
    # Set Wave 10 parameters manually (easier for testing)
    game.wave_manager.wave_timer = 3600  # 60 seconds
    game.wave_manager.max_enemies = 8   # Reduced from 12 for easier testing
    game.wave_manager.spawn_interval = 60  # Slower spawn rate (1 second instead of 0.5)
    game.wave_manager.spawn_timer = 0
    
    # Start boss battle
    game.boss_battle.start_boss_battle()
    
    # Force player to be vulnerable but with more health for testing
    game.player.health_system.set_immunity(False)
    game.player.health_system.current_health = 200  # Double health for testing
    game.player.health_system.max_health = 200
    
    # Ensure player has shooting cooldown attribute
    if not hasattr(game.player, 'shooting_cooldown'):
        game.player.shooting_cooldown = 0
    
    # Enemy kill counter for boss damage
    enemies_killed = 0
    last_enemy_count = 0
    missile_ready = False  # Track if player has earned a missile
    
    print("🎯 Wave 10 + Boss Battle active!")
    print("🔴 Dodge red lasers and orange missiles!")
    print("💥 Destroy 10 enemies to earn a missile shot!")
    
    clock = pygame.time.Clock()
    
    while game.running:
        # Handle events - same as main game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                elif event.key == pygame.K_SPACE and missile_ready:
                    # Fire missile at boss with visual effect
                    game.boss_battle.fire_player_missile(game.player.rect.centerx, game.player.rect.top)
                    game.boss_battle.damage_boss(10)
                    missile_ready = False
                    enemies_killed = 0  # Reset counter
                    print("🚀 MISSILE FIRED AT BOSS!")
        
        # Track enemy kills for boss damage
        current_enemy_count = len(game.enemies)
        if current_enemy_count < last_enemy_count:
            enemies_destroyed = last_enemy_count - current_enemy_count
            enemies_killed += enemies_destroyed
            
            # Check if player earned a missile
            if enemies_killed >= 10 and not missile_ready:
                missile_ready = True
                print("🚀 MISSILE READY! Press SPACE to fire at boss!")
        
        last_enemy_count = current_enemy_count
        
        # Update game - EXACT same as main game
        keys = pygame.key.get_pressed()
        
        # Update player (handle input properly like main game)
        game.player.update(movement_disabled=False)
        
        # Handle player shooting manually (since main game handles this in event loop)
        if keys[pygame.K_SPACE]:
            if game.player.shooting_cooldown <= 0:
                # Create projectile
                from projectile import Projectile
                projectile = Projectile(
                    game.player.rect.centerx, 
                    game.player.rect.top, 
                    game.player.facing_direction
                )
                game.projectiles.add(projectile)
                game.all_sprites.add(projectile)
                game.player.shooting_cooldown = 10  # Set cooldown
        
        # Update shooting cooldown
        if game.player.shooting_cooldown > 0:
            game.player.shooting_cooldown -= 1
        
        # Update all sprites
        game.all_sprites.update()
        
        # Update enemies with AI - FIXED to handle projectiles properly
        for enemy in game.enemies:
            actions = enemy.update(game.player.rect)
            if actions:
                for action in actions:
                    if hasattr(action, 'rect'):  # It's a projectile
                        game.enemy_projectiles.add(action)
                        game.all_sprites.add(action)
        
        # Update projectiles
        game.projectiles.update()
        game.enemy_projectiles.update()
        game.bombs.update()
        game.explosions.update()
        
        # Update wave manager (for enemy spawning like Wave 10)
        game.wave_manager.update(game.enemies, game.all_sprites, game.player.is_alive())
        
        # Update boss battle
        game.boss_battle.update()
        
        # Update power-ups
        game.powerup_spawner.update(game.powerups, game.all_sprites)
        
        # Update background
        game.background.update(game.player.rect, keys)
        
        # Process collisions - EXACT same as main game
        if game.player.is_alive():
            collision_results = game.collision_system.process_all_collisions(
                game.player, game.enemies, game.asteroids, game.debris, 
                game.projectiles, game.enemy_projectiles, game.bombs, game.powerups
            )
            
            # Boss battle collisions
            if game.boss_battle.active:
                # Laser collisions (light damage)
                if game.boss_battle.check_laser_collision(game.player.rect):
                    game.player.health_system.take_damage(5)
                    print(f"⚡ Hit by laser! Health: {game.player.health_system.current_health}/100")
                
                # Missile collisions (heavy damage)
                if game.boss_battle.check_missile_collision(game.player.rect):
                    game.player.health_system.take_damage(25)
                    print(f"🚀 Hit by missile! Health: {game.player.health_system.current_health}/100")
            
            # Handle collision results
            for key, value in collision_results.items():
                if key == 'explosions':
                    for explosion in value:
                        game.explosions.add(explosion)
                        game.all_sprites.add(explosion)
        
        # Draw everything - EXACT same as main game
        game.screen.fill((0, 0, 0))
        game.background.draw(game.screen)
        
        # Draw all sprites except player
        for sprite in game.all_sprites:
            if sprite != game.player:
                game.screen.blit(sprite.image, sprite.rect)
        
        # Draw player
        game.player.draw(game.screen)
        
        # Draw boss battle elements
        game.boss_battle.draw(game.screen)
        
        # Draw missile ready message above boss health bar
        if missile_ready:
            font_large = pygame.font.Font(None, 36)
            missile_msg = font_large.render("MISSILE READY! Press SPACE to fire!", True, (255, 255, 0))
            msg_rect = missile_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
            
            # Draw background for message
            bg_rect = pygame.Rect(msg_rect.x - 10, msg_rect.y - 5, msg_rect.width + 20, msg_rect.height + 10)
            pygame.draw.rect(game.screen, (0, 0, 0), bg_rect)
            pygame.draw.rect(game.screen, (255, 255, 0), bg_rect, 2)
            
            game.screen.blit(missile_msg, msg_rect)
        
        # Draw UI
        font = pygame.font.Font(None, 24)
        
        # Player health (show out of 200 for testing)
        health_color = (0, 255, 0) if game.player.health_system.current_health > 100 else (255, 255, 0) if game.player.health_system.current_health > 50 else (255, 0, 0)
        health_text = font.render(f"Health: {game.player.health_system.current_health}/200", True, health_color)
        game.screen.blit(health_text, (10, 10))
        
        # Wave info
        wave_text = font.render(f"Wave 10 + Boss Battle", True, (255, 255, 255))
        game.screen.blit(wave_text, (10, 40))
        
        # Enemy count and missile progress
        enemy_text = font.render(f"Enemies: {len(game.enemies)}", True, (255, 255, 255))
        game.screen.blit(enemy_text, (10, 70))
        
        # Missile progress
        if missile_ready:
            progress_text = font.render(f"MISSILE READY! Press SPACE!", True, (255, 255, 0))
        else:
            kills_needed = 10 - enemies_killed
            progress_text = font.render(f"Kills for missile: {kills_needed}/10", True, (255, 255, 255))
        game.screen.blit(progress_text, (10, 100))
        
        # Boss attacks info
        boss_info = game.boss_battle.get_info()
        if boss_info['active']:
            attacks_text = font.render(f"Boss Attacks: {boss_info['active_lasers']} lasers, {boss_info['active_missiles']} missiles", True, (255, 200, 200))
            game.screen.blit(attacks_text, (10, 100))
        
        # Instructions
        font_small = pygame.font.Font(None, 20)
        instructions = [
            "🔴 Red lasers: 5 damage",
            "🚀 Orange missiles: 25 damage", 
            "💥 Kill 10 enemies = missile ready",
            "🚀 Press SPACE to fire missile at boss",
            "🎁 Collect power-ups like normal"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, (200, 200, 200))
            game.screen.blit(text, (SCREEN_WIDTH - 250, 10 + i * 20))
        
        pygame.display.flip()
        
        # Check win/lose conditions
        if boss_info['boss_defeated']:
            print("🏆 BOSS DEFEATED! Victory!")
            break
        
        if not game.player.is_alive():
            print("💀 Defeated! Press ESC to quit")
            # Could add restart logic here
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
