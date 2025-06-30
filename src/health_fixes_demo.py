#!/usr/bin/env python3
"""
Demo the health and timer fixes
"""
import pygame
from game import Game
from constants import *

def demo_health_fixes():
    """Demo the health system and timer fixes"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🏥 HEALTH & TIMER FIXES DEMO")
    print("Testing timer freeze on death, health clamping, and improved HP boosts")
    
    print("\n🛑 Critical Fixes:")
    print("  ⏱️ Wave timer stops completely when player dies")
    print("  🏥 Health cannot go below 0 (properly clamped)")
    print("  💊 HP boost increased from 30 to 50 HP")
    print("  🎁 HP power-ups spawn more frequently:")
    print("    • Spawn interval: 6 seconds (was 10 seconds)")
    print("    • Spawn chance: 60% (was 40%)")
    print("    • HP power-up preference: 75% (was 60%)")
    
    print("\n🎮 Controls:")
    print("  SPACE - Begin wave / Continue")
    print("  WASD/Arrow Keys - Move")
    print("  Q/E - Shoot enemies")
    print("  R - Restart game")
    print("  ESC - Quit")
    
    print("\n🧪 Test Sequence:")
    print("  1. Start wave and take damage")
    print("  2. Observe timer behavior when player dies")
    print("  3. Check health doesn't go below 0")
    print("  4. Test improved HP power-up system")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    last_timer_value = None
    death_frame = None
    
    while game.running and frame_count < 1800:  # 30 seconds max
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                elif event.key == pygame.K_r and game.game_over and game.player_death_timer <= 0:
                    # Restart game
                    game.restart_game()
                    death_frame = None
                    last_timer_value = None
                elif event.key == pygame.K_SPACE and game.story_mode:
                    # Handle wave progression
                    wave_info = game.wave_manager.get_wave_info()
                    if wave_info:
                        if wave_info.get('wave_intro_active', False):
                            # Start the wave from intro
                            game.wave_manager.start_wave(wave_info['wave_number'])
                            print(f"🌊 Wave {wave_info['wave_number']} started!")
                        elif wave_info['wave_complete']:
                            # Advance to next wave
                            if not game.wave_manager.next_wave():
                                print("🏆 All waves completed!")
                elif event.key == pygame.K_q and game.player.is_alive():
                    # Primary weapon
                    shot_data = game.player.shoot("primary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                elif event.key == pygame.K_e and game.player.is_alive():
                    # Secondary weapon
                    shot_data = game.player.shoot("secondary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
        
        game.update()
        game.draw()
        
        # Track timer behavior and player death
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info['wave_active']:
            current_timer = wave_info['time_remaining']
            player_alive = game.player.is_alive()
            current_health = game.player.health_system.current_health
            
            # Detect player death
            if not player_alive and death_frame is None:
                death_frame = frame_count
                last_timer_value = current_timer
                print(f"💀 PLAYER DIED at frame {death_frame}")
                print(f"   Timer value at death: {last_timer_value:.1f}s")
                print(f"   Health at death: {current_health}")
            
            # Check if timer is frozen after death
            if death_frame is not None and not player_alive:
                if abs(current_timer - last_timer_value) > 0.1:  # Timer changed
                    print(f"⚠️ ERROR: Timer still running after death! {current_timer:.1f}s (was {last_timer_value:.1f}s)")
                else:
                    if frame_count % 60 == 0:  # Every second
                        print(f"✅ Timer correctly frozen at {current_timer:.1f}s (death frame: {death_frame})")
        
        # Capture screenshots at key moments
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"assets/images/health_fixes_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            if wave_info:
                enemies_on_screen = len(game.enemies)
                powerups_on_screen = len(game.powerups)
                player_alive = game.player.is_alive()
                current_health = game.player.health_system.current_health
                
                print(f"\nFrame {frame_count}:")
                print(f"  Player: {'Alive' if player_alive else 'Dead'} (Health: {current_health}/100)")
                
                if wave_info.get('wave_intro_active', False):
                    print(f"  State: WAVE INTRO")
                elif wave_info['wave_active']:
                    print(f"  State: WAVE ACTIVE")
                    print(f"  Timer: {wave_info['time_remaining']:.1f}s remaining")
                    if death_frame is not None:
                        print(f"  🛑 Timer should be FROZEN (death at frame {death_frame})")
                elif wave_info['wave_complete']:
                    print(f"  State: WAVE COMPLETE")
                
                print(f"  Enemies: {enemies_on_screen} | Power-ups: {powerups_on_screen}")
                print(f"  Screenshot: {screenshot_path}")
                
                # Health system checks
                if current_health < 0:
                    print(f"  ⚠️ ERROR: Health below 0! ({current_health})")
                elif current_health == 0 and player_alive:
                    print(f"  ⚠️ ERROR: Player alive with 0 health!")
                elif current_health == 0 and not player_alive:
                    print(f"  ✅ Health correctly clamped to 0 on death")
        
        frame_count += 1
    
    print("\n✅ Health and timer fixes demo completed!")
    print("🏥 Health System Improvements:")
    print("   ⏱️ Wave timer completely stops when player dies")
    print("   🏥 Health properly clamped to minimum 0")
    print("   💊 HP boost increased to 50 HP (was 30 HP)")
    print("   🎁 HP power-ups spawn every 6 seconds (was 10 seconds)")
    print("   📈 HP power-up spawn chance: 60% (was 40%)")
    print("   🎯 HP power-up preference: 75% (was 60%)")
    
    print("\n🚀 Player Experience Improvements:")
    print("   Before: Timer continued after death, health went negative")
    print("   After: Clean death state with proper value clamping")
    print("   🛑 Death provides clear pause with frozen timer")
    print("   🏥 Health system behaves predictably")
    print("   💊 More frequent and effective healing opportunities")
    print("   ⚡ Better survival chances with improved power-up system")
    
    pygame.quit()

if __name__ == "__main__":
    demo_health_fixes()
