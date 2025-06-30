#!/usr/bin/env python3
"""
Demo the complete Wave Management System for Story Mode
"""
import pygame
from game import Game
from constants import *

def demo_wave_system():
    """Demo the wave management system with story mode progression"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🌊 WAVE SYSTEM DEMO - STORY MODE")
    print("Testing complete wave progression with timers and enemy quotas")
    
    print("\n🎮 Wave System Features:")
    print("  📊 Wave 1: 8 Fighters, 60 seconds")
    print("  📊 Waves 2-5: Fighter + Fighter2 + Gunship (12-20 enemies)")
    print("  📊 Wave 6: + Crabship (22 enemies)")
    print("  📊 Waves 7-10: + Pirate (25-35 enemies)")
    print("  ⏱️ Time limits: 60-120 seconds per wave")
    print("  🎯 Enemy quotas: Must destroy all enemies to advance")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move")
    print("  Q/E - Shoot enemies")
    print("  SPACE - Continue to next wave (when wave complete)")
    print("  R - Retry wave (when wave failed)")
    print("  ESC - Quit")
    
    print("\n🌊 Wave Progression:")
    print("  ✅ Complete wave → Press SPACE for next wave")
    print("  ❌ Fail wave → Press R to retry or ESC to quit")
    print("  🏆 Complete all 10 waves → Boss battle!")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    
    while game.running:
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
                        if wave_info['wave_complete']:
                            # Advance to next wave
                            if not game.wave_manager.next_wave():
                                # All waves completed - boss battle time!
                                print("🏆 All waves completed! Boss battle would start here!")
                        elif wave_info['wave_failed']:
                            # Retry current wave
                            game.wave_manager.restart_wave()
                        elif wave_info['story_complete']:
                            # Start boss battle (TODO: implement boss)
                            print("🏆 Boss battle would start here!")
                elif event.key == pygame.K_r and game.story_mode:
                    # Retry wave in story mode
                    wave_info = game.wave_manager.get_wave_info()
                    if wave_info and wave_info['wave_failed']:
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
            screenshot_path = f"assets/images/wave_demo_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            wave_info = game.wave_manager.get_wave_info()
            if wave_info:
                print(f"\nFrame {frame_count}:")
                print(f"  Wave: {wave_info['wave_number']}/10 - {wave_info['description']}")
                print(f"  Progress: {wave_info['enemies_destroyed']}/{wave_info['enemies_required']} enemies")
                print(f"  Time: {wave_info['time_remaining']:.1f}s remaining")
                print(f"  Status: {'Active' if wave_info['wave_active'] else 'Complete' if wave_info['wave_complete'] else 'Failed' if wave_info['wave_failed'] else 'Waiting'}")
                print(f"  Screenshot: {screenshot_path}")
                
                if wave_info['wave_complete']:
                    print("  ✅ WAVE COMPLETE! Press SPACE to continue")
                elif wave_info['wave_failed']:
                    print("  ❌ WAVE FAILED! Press R to retry")
                elif wave_info['story_complete']:
                    print("  🏆 STORY COMPLETE! Boss battle ready!")
        
        frame_count += 1
        
        # Auto-quit after reasonable demo time
        if frame_count > 3600:  # 1 minute
            break
    
    print("\n✅ Wave system demo completed!")
    print("🌊 Wave Management Features Demonstrated:")
    print("   📊 Progressive wave composition (1-10 waves)")
    print("   ⏱️ Time-based wave challenges (60-120 seconds)")
    print("   🎯 Enemy quota system (8-35 enemies per wave)")
    print("   📈 Escalating difficulty with more enemy types")
    print("   🎮 Wave completion/failure states")
    print("   🔄 Wave retry functionality")
    print("   📱 Professional UI with progress bars and timers")
    print("   🏆 Story completion leading to boss battle")
    
    print("\n🚀 Story Mode Transformation:")
    print("   Before: Endless arcade gameplay")
    print("   After: Structured campaign with clear objectives")
    print("   🎯 Players now have specific goals per wave")
    print("   ⏱️ Time pressure creates urgency and challenge")
    print("   📈 Progressive difficulty keeps engagement high")
    print("   🏆 Clear end goal (boss battle) provides motivation")
    
    pygame.quit()

if __name__ == "__main__":
    demo_wave_system()
