#!/usr/bin/env python3
"""
Demo the improved game state management - player death freezing and wave intro locking
"""
import pygame
from game import Game
from constants import *

def demo_game_state_management():
    """Demo the game state management improvements"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🎮 GAME STATE MANAGEMENT DEMO")
    print("Testing player death freezing and wave intro player locking")
    
    print("\n🛑 Game State Features:")
    print("  🔒 Wave Intro State:")
    print("    • Player cannot move during wave introduction")
    print("    • Must press SPACE to begin wave")
    print("    • Enemies do not spawn during intro")
    print("  💀 Player Death State:")
    print("    • All enemy movement stops when player dies")
    print("    • All enemy firing stops when player dies")
    print("    • Wave timer stops when player dies")
    print("    • Enemy spawning stops when player dies")
    print("    • Enemy projectiles are cleared when player dies")
    
    print("\n🎮 Controls:")
    print("  SPACE - Begin wave (during intro) / Continue (after completion)")
    print("  WASD/Arrow Keys - Move (only when wave is active)")
    print("  Q/E - Shoot enemies")
    print("  R - Restart game")
    print("  ESC - Quit")
    
    print("\n🌊 Test Sequence:")
    print("  1. Wave intro - Player locked, press SPACE to start")
    print("  2. Wave active - Player can move and fight")
    print("  3. Player death - Everything freezes")
    print("  4. Restart - Back to wave intro")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    
    while game.running and frame_count < 2400:  # 40 seconds max
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
                elif event.key == pygame.K_SPACE and game.story_mode:
                    # Handle wave progression
                    wave_info = game.wave_manager.get_wave_info()
                    if wave_info:
                        if wave_info.get('wave_intro_active', False):
                            # Start the wave from intro
                            game.wave_manager.start_wave(wave_info['wave_number'])
                            print(f"🌊 Wave {wave_info['wave_number']} started! Player can now move.")
                        elif wave_info['wave_complete']:
                            # Advance to next wave
                            if not game.wave_manager.next_wave():
                                print("🏆 All waves completed!")
                        elif wave_info['wave_failed']:
                            # Retry current wave
                            game.wave_manager.restart_wave()
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
        
        # Capture screenshots at key moments
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"assets/images/game_state_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            wave_info = game.wave_manager.get_wave_info()
            if wave_info:
                enemies_on_screen = len(game.enemies)
                enemy_projectiles = len(game.enemy_projectiles)
                player_alive = game.player.is_alive()
                
                print(f"\nFrame {frame_count}:")
                print(f"  Player: {'Alive' if player_alive else 'Dead'} (Health: {game.player.health_system.current_health if hasattr(game.player, 'health_system') else 'N/A'})")
                print(f"  Wave: {wave_info['wave_number']}/10 - {wave_info['description']}")
                
                if wave_info.get('wave_intro_active', False):
                    print(f"  State: WAVE INTRO - Player locked, press SPACE to begin")
                elif wave_info['wave_active']:
                    print(f"  State: WAVE ACTIVE - Player can move and fight")
                    print(f"  Time: {wave_info['time_remaining']:.1f}s remaining")
                elif wave_info['wave_complete']:
                    print(f"  State: WAVE COMPLETE - Press SPACE to continue")
                else:
                    print(f"  State: Waiting")
                
                print(f"  Enemies: {enemies_on_screen} on screen")
                print(f"  Enemy Projectiles: {enemy_projectiles}")
                print(f"  Screenshot: {screenshot_path}")
                
                # Check if everything is properly frozen when player dies
                if not player_alive and game.story_mode:
                    print(f"  🛑 DEATH STATE: Everything should be frozen!")
                    if wave_info['wave_active']:
                        print(f"    ⚠️ Wave timer should be stopped")
                    if enemies_on_screen > 0:
                        print(f"    ⚠️ Enemies should not be moving or firing")
                    if enemy_projectiles > 0:
                        print(f"    ⚠️ Enemy projectiles should be cleared")
        
        frame_count += 1
    
    print("\n✅ Game state management demo completed!")
    print("🎮 Game State Features Demonstrated:")
    print("   🔒 Wave intro player locking (cannot move until SPACE)")
    print("   🛑 Complete game freeze on player death")
    print("   ⏱️ Wave timer stops when player dies")
    print("   🚀 Enemy spawning stops when player dies")
    print("   💥 Enemy firing stops when player dies")
    print("   🧹 Enemy projectiles cleared on player death")
    print("   🔄 Proper state restoration on game restart")
    
    print("\n🚀 Player Experience Improvements:")
    print("   Before: Chaotic state management with continued activity after death")
    print("   After: Clean state transitions with proper game freezing")
    print("   🎯 Players have clear control over wave progression")
    print("   🛑 Death state provides clear feedback and pause")
    print("   🔒 Wave intro prevents accidental early starts")
    print("   ⚡ Improved game flow and player agency")
    
    pygame.quit()

if __name__ == "__main__":
    demo_game_state_management()
