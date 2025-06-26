#!/usr/bin/env python3
"""
Debug enemy spawning and movement patterns
"""
import pygame
from game import Game
from constants import *

def debug_enemy_spawning():
    """Debug enemy spawning positions and movement"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🐛 ENEMY SPAWN DEBUG")
    print("Testing enemy spawn positions and movement patterns")
    
    print("\n🎯 Issues to Debug:")
    print("  1. Enemies spawning outside screen boundaries")
    print("  2. Enemies not entering screen properly")
    print("  3. Spawn frequency not escalating correctly")
    print("  4. Enemies staying off-screen (left/right)")
    
    # Fast-forward to Wave 2 for testing
    print("\n⏩ Fast-forwarding to Wave 2...")
    frame_count = 0
    wave_2_started = False
    enemy_spawn_log = []
    
    while game.running and frame_count < 3000:  # 50 seconds max
        # Keep player alive
        if game.player.health_system.current_health < 50:
            game.player.health_system.current_health = 100
            game.player.health_system.health_bar.current_health = 100
        
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 20 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info:
            if wave_info.get('wave_intro_active', False) and frame_count % 30 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
            elif wave_info.get('wave_complete', False) and frame_count % 30 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
        
        # Handle events
        game.handle_events()
        
        # Track enemy spawns before update
        enemies_before = len(game.enemies)
        
        game.update()
        game.draw()
        
        # Track enemy spawns after update
        enemies_after = len(game.enemies)
        
        # Log new spawns
        if enemies_after > enemies_before:
            for enemy in game.enemies:
                enemy_info = {
                    'frame': frame_count,
                    'type': enemy.enemy_type,
                    'position': (enemy.rect.x, enemy.rect.y),
                    'direction': enemy.direction,
                    'on_screen': (0 <= enemy.rect.x <= SCREEN_WIDTH and 0 <= enemy.rect.y <= SCREEN_HEIGHT)
                }
                if enemy_info not in enemy_spawn_log:
                    enemy_spawn_log.append(enemy_info)
        
        # Track Wave 2 specifically
        if wave_info and wave_info['wave_number'] == 2:
            if not wave_2_started and wave_info.get('wave_active', False):
                wave_2_started = True
                print(f"\n🌊 WAVE 2 STARTED at frame {frame_count}")
                print(f"   Spawn interval: {game.wave_manager.spawn_interval} frames ({game.wave_manager.spawn_interval/60:.2f}s)")
                print(f"   Spawn variance: ±{getattr(game.wave_manager, 'spawn_variance', 0)} frames")
                print(f"   Max enemies: {game.wave_manager.max_enemies_on_screen}")
            
            if wave_2_started and wave_info.get('wave_active', False):
                # Monitor enemy positions every 3 seconds
                if frame_count % 180 == 0:
                    current_enemies = len(game.enemies)
                    time_remaining = wave_info.get('time_remaining', 0)
                    
                    print(f"\n📊 Wave 2 Status - {time_remaining:.1f}s left:")
                    print(f"   Enemies on screen: {current_enemies}")
                    print(f"   Total spawned: {game.wave_manager.enemies_spawned}")
                    
                    # Check enemy positions
                    on_screen_count = 0
                    off_screen_enemies = []
                    
                    for enemy in game.enemies:
                        if 0 <= enemy.rect.x <= SCREEN_WIDTH and 0 <= enemy.rect.y <= SCREEN_HEIGHT:
                            on_screen_count += 1
                        else:
                            off_screen_enemies.append({
                                'type': enemy.enemy_type,
                                'pos': (enemy.rect.x, enemy.rect.y),
                                'direction': enemy.direction
                            })
                    
                    print(f"   On screen: {on_screen_count}, Off screen: {len(off_screen_enemies)}")
                    
                    if off_screen_enemies:
                        print(f"   🚨 OFF-SCREEN ENEMIES:")
                        for enemy in off_screen_enemies[:5]:  # Show first 5
                            print(f"     {enemy['type']} at {enemy['pos']} moving {enemy['direction']}")
            
            # Wave 2 completed
            if wave_2_started and wave_info.get('wave_complete', False):
                print(f"\n✅ WAVE 2 COMPLETED at frame {frame_count}")
                break
        
        frame_count += 1
    
    print(f"\n🐛 ENEMY SPAWN DEBUG RESULTS:")
    print(f"Total enemy spawns logged: {len(enemy_spawn_log)}")
    
    if enemy_spawn_log:
        print(f"\n📍 Spawn Position Analysis:")
        spawn_sides = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        off_screen_spawns = 0
        
        for spawn in enemy_spawn_log[-20:]:  # Analyze last 20 spawns
            x, y = spawn['position']
            direction = spawn['direction']
            
            # Determine spawn side
            if x < 0:
                spawn_sides['left'] += 1
            elif x > SCREEN_WIDTH:
                spawn_sides['right'] += 1
            elif y < 0:
                spawn_sides['top'] += 1
            elif y > SCREEN_HEIGHT:
                spawn_sides['bottom'] += 1
            
            if not spawn['on_screen']:
                off_screen_spawns += 1
            
            print(f"   {spawn['type']} at ({x}, {y}) moving {direction} - {'ON' if spawn['on_screen'] else 'OFF'} screen")
        
        print(f"\n📊 Spawn Distribution:")
        for side, count in spawn_sides.items():
            print(f"   {side.capitalize()}: {count} spawns")
        
        print(f"\n⚠️ Issues Found:")
        print(f"   Off-screen spawns: {off_screen_spawns}/{len(enemy_spawn_log[-20:])}")
        
        if off_screen_spawns > 0:
            print(f"   🔧 SPAWN POSITION ISSUE DETECTED!")
            print(f"   Enemies are spawning outside screen boundaries")
        else:
            print(f"   ✅ Spawn positions look correct")
    
    print(f"\n🔧 Spawn Frequency Analysis:")
    wave_data = game.wave_manager.wave_compositions
    print(f"   Wave progression (spawn intervals in seconds):")
    for wave_num in range(1, 6):
        interval = wave_data[wave_num]['spawn_interval'] / 60
        print(f"     Wave {wave_num}: {interval:.2f}s between spawns")
    
    pygame.quit()

if __name__ == "__main__":
    debug_enemy_spawning()
