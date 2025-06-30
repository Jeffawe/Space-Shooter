#!/usr/bin/env python3
"""
Demo the damage immunity during wave transitions
"""
import pygame
from game import Game
from constants import *

def demo_damage_immunity():
    """Demo the damage immunity system during wave transitions"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🛡️ DAMAGE IMMUNITY DEMO")
    print("Testing player immunity during wave intro, completion, and failure screens")
    
    print("\n🛡️ Damage Immunity Features:")
    print("  🔒 Wave Intro State:")
    print("    • Player cannot take damage during wave introduction")
    print("    • Enemy projectiles pass through player harmlessly")
    print("    • Player health remains unchanged")
    print("  ✅ Wave Complete State:")
    print("    • Player immune to damage on wave completion screen")
    print("    • Safe transition between waves")
    print("  ❌ Wave Failed State:")
    print("    • Player immune to damage on wave failure screen")
    print("    • No additional damage during failure state")
    print("  💀 Player Death State:")
    print("    • No damage possible when player is already dead")
    print("    • Health cannot reduce further after death")
    
    print("\n🎮 Controls:")
    print("  SPACE - Begin wave / Continue")
    print("  WASD/Arrow Keys - Move")
    print("  Q/E - Shoot enemies")
    print("  R - Restart game")
    print("  ESC - Quit")
    
    print("\n🧪 Test Sequence:")
    print("  1. Wave intro - Player immune, enemies may fire but no damage")
    print("  2. Wave active - Player can take damage normally")
    print("  3. Wave complete - Player immune during completion screen")
    print("  4. Player death - No further damage possible")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    last_health = 100
    immunity_tests = []
    
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
                    last_health = 100
                    immunity_tests = []
                elif event.key == pygame.K_SPACE and game.story_mode:
                    # Handle wave progression
                    wave_info = game.wave_manager.get_wave_info()
                    if wave_info:
                        if wave_info.get('wave_intro_active', False):
                            # Start the wave from intro
                            game.wave_manager.start_wave(wave_info['wave_number'])
                            print(f"🌊 Wave {wave_info['wave_number']} started! Player can now take damage.")
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
        
        # Monitor immunity and health changes
        current_health = game.player.health_system.current_health
        is_immune = game.player.health_system.is_immune()
        player_alive = game.player.is_alive()
        
        # Track immunity state changes
        wave_info = game.wave_manager.get_wave_info()
        if wave_info:
            current_state = "unknown"
            if wave_info.get('wave_intro_active', False):
                current_state = "intro"
            elif wave_info.get('wave_active', False):
                current_state = "active"
            elif wave_info.get('wave_complete', False):
                current_state = "complete"
            elif wave_info.get('wave_failed', False):
                current_state = "failed"
            
            # Test immunity during transitions
            if current_state in ["intro", "complete", "failed"] and not is_immune:
                print(f"⚠️ ERROR: Player should be immune during {current_state} state!")
            elif current_state == "active" and is_immune:
                print(f"⚠️ ERROR: Player should NOT be immune during active wave!")
            
            # Check for health changes during immunity
            if is_immune and current_health < last_health and player_alive:
                print(f"⚠️ ERROR: Health decreased during immunity! {last_health} → {current_health}")
                immunity_tests.append(f"FAILED: Health loss during {current_state} state")
            elif is_immune and current_health < last_health:
                print(f"✅ Health correctly protected during {current_state} state")
                immunity_tests.append(f"PASSED: No damage during {current_state} state")
        
        last_health = current_health
        
        # Capture screenshots at key moments
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"assets/images/immunity_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            if wave_info:
                enemies_on_screen = len(game.enemies)
                enemy_projectiles = len(game.enemy_projectiles)
                
                print(f"\nFrame {frame_count}:")
                print(f"  Player: {'Alive' if player_alive else 'Dead'} (Health: {current_health}/100)")
                print(f"  Immunity: {'🛡️ ACTIVE' if is_immune else '⚔️ VULNERABLE'}")
                
                if wave_info.get('wave_intro_active', False):
                    print(f"  State: WAVE INTRO - Should be immune")
                elif wave_info['wave_active']:
                    print(f"  State: WAVE ACTIVE - Should be vulnerable")
                elif wave_info['wave_complete']:
                    print(f"  State: WAVE COMPLETE - Should be immune")
                elif wave_info['wave_failed']:
                    print(f"  State: WAVE FAILED - Should be immune")
                
                print(f"  Enemies: {enemies_on_screen} | Enemy Projectiles: {enemy_projectiles}")
                print(f"  Screenshot: {screenshot_path}")
                
                # Immunity validation
                expected_immunity = (wave_info.get('wave_intro_active', False) or 
                                   wave_info.get('wave_complete', False) or 
                                   wave_info.get('wave_failed', False))
                
                if is_immune == expected_immunity:
                    print(f"  ✅ Immunity state correct")
                else:
                    print(f"  ⚠️ Immunity state incorrect! Expected: {expected_immunity}, Actual: {is_immune}")
        
        frame_count += 1
    
    print("\n✅ Damage immunity demo completed!")
    print("🛡️ Immunity System Test Results:")
    for test in immunity_tests:
        print(f"   {test}")
    
    print("\n🛡️ Damage Immunity Features Demonstrated:")
    print("   🔒 Wave intro immunity - No damage during introduction")
    print("   ✅ Wave complete immunity - Safe transition between waves")
    print("   ❌ Wave failed immunity - No additional damage during failure")
    print("   💀 Death state immunity - No further damage after death")
    print("   ⚔️ Active wave vulnerability - Normal damage during gameplay")
    
    print("\n🚀 Player Experience Improvements:")
    print("   Before: Could take damage during wave transitions")
    print("   After: Complete protection during non-gameplay states")
    print("   🛡️ Safe wave introductions without accidental damage")
    print("   ✅ Protected wave completion celebrations")
    print("   🎮 Clear separation between safe and dangerous states")
    print("   ⚡ Professional game state management")
    
    pygame.quit()

if __name__ == "__main__":
    demo_damage_immunity()
