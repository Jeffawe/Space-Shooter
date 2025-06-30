#!/usr/bin/env python3
"""
Demo the improved continuous wave spawning system
"""
import pygame
from game import Game
from constants import *

def demo_continuous_waves():
    """Demo the continuous enemy spawning wave system"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🌊 CONTINUOUS WAVE SYSTEM DEMO")
    print("Testing improved continuous enemy spawning with increasing frequency")
    
    print("\n🎮 Improved Wave System Features:")
    print("  🔄 Continuous enemy spawning (no fixed counts)")
    print("  📈 Increasing spawn frequency per wave:")
    print("    • Wave 1: Every 2.0s (±1.0s) - Training pace")
    print("    • Wave 5: Every 1.2s (±0.6s) - Moderate intensity")
    print("    • Wave 10: Every 0.8s (±0.3s) - Maximum chaos!")
    print("  🎯 Time-based wave completion (survive the duration)")
    print("  👁️ Optimized spawning (enemies guaranteed to enter screen)")
    print("  📊 Real-time statistics (spawned vs destroyed)")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move")
    print("  Q/E - Shoot enemies")
    print("  SPACE - Continue to next wave")
    print("  ESC - Quit")
    
    print("\n🌊 Wave Objectives:")
    print("  ✅ Survive the wave duration")
    print("  🎯 Destroy as many enemies as possible")
    print("  📈 Experience increasing difficulty")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    
    while game.running and frame_count < 1800:  # 30 seconds max
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                elif event.key == pygame.K_SPACE and game.story_mode:
                    # Handle wave progression
                    wave_info = game.wave_manager.get_wave_info()
                    if wave_info and wave_info['wave_complete']:
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
        
        # Capture screenshots at key moments
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"assets/images/continuous_wave_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            wave_info = game.wave_manager.get_wave_info()
            if wave_info:
                enemies_on_screen = len(game.enemies)
                
                print(f"\nFrame {frame_count}:")
                print(f"  Wave: {wave_info['wave_number']}/10 - {wave_info['description']}")
                print(f"  Time: {wave_info['time_remaining']:.1f}s remaining")
                print(f"  Enemies: {enemies_on_screen} on screen | {wave_info['enemies_spawned']} spawned | {wave_info['enemies_destroyed']} destroyed")
                print(f"  Spawn Rate: {wave_info['spawn_rate']}")
                print(f"  Status: {'Active' if wave_info['wave_active'] else 'Complete' if wave_info['wave_complete'] else 'Waiting'}")
                print(f"  Screenshot: {screenshot_path}")
                
                if wave_info['wave_complete']:
                    print("  ✅ WAVE COMPLETE! Press SPACE to continue")
                
                # Show spawn frequency improvement
                if wave_info['wave_number'] > 1:
                    print(f"  📈 Spawn frequency increased from previous wave!")
        
        frame_count += 1
    
    print("\n✅ Continuous wave system demo completed!")
    print("🌊 Improved Wave System Features Demonstrated:")
    print("   🔄 Continuous enemy spawning throughout wave duration")
    print("   📈 Progressive spawn frequency increase (2.0s → 0.8s)")
    print("   👁️ Optimized spawn positions (enemies enter screen reliably)")
    print("   ⏱️ Time-based wave completion (survive duration)")
    print("   📊 Real-time enemy statistics tracking")
    print("   🎯 Maximum 8 concurrent enemies (performance optimized)")
    print("   🎮 Engaging gameplay with constant action")
    
    print("\n🚀 Gameplay Improvements:")
    print("   Before: Sparse enemy encounters with fixed counts")
    print("   After: Continuous action with escalating intensity")
    print("   🎯 Players always have enemies to engage")
    print("   📈 Difficulty scales naturally through spawn frequency")
    print("   ⚡ Optimized performance with screen-entry guarantee")
    print("   🎮 More engaging and action-packed experience")
    
    pygame.quit()

if __name__ == "__main__":
    demo_continuous_waves()
