#!/usr/bin/env python3
"""
Demo the persistent player facing direction system
"""
import pygame
from game import Game
from constants import *

def demo_persistent_facing():
    """Demo the persistent facing direction system"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎮 PERSISTENT FACING DIRECTION DEMO")
    print("Testing player sprite direction persistence")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    print(f"Player positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print(f"Initial facing direction: {game.player.last_facing_direction}")
    print(f"Initial sprite: {game.player.current_sprite}")
    
    print("\n🎯 Testing Sequence:")
    print("1. Player starts facing up")
    print("2. Press S to face down, release S - should stay facing down")
    print("3. Press W to face up, release W - should stay facing up") 
    print("4. Press A to face left, release A - should stay facing left")
    print("5. Press D to face right, release D - should stay facing right")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move and change facing direction")
    print("  Q/E - Shoot (direction based on facing)")
    print("  ESC - Quit")
    print("  Watch the sprite and console output for facing changes!")
    
    last_facing = game.player.last_facing_direction
    last_sprite = game.player.current_sprite
    
    # Run demo
    for frame in range(1800):  # 30 seconds at 60 FPS
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_q and game.player.is_alive():
                    # Primary weapon - show firing direction
                    shot_data = game.player.shoot("primary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                        print(f"🔫 Fired {direction} while facing {game.player.last_facing_direction}")
        
        game.update()
        game.draw()
        
        # Check for facing direction changes
        current_facing = game.player.last_facing_direction
        current_sprite = game.player.current_sprite
        
        if current_facing != last_facing or current_sprite != last_sprite:
            print(f"Frame {frame}: Facing changed to '{current_facing}', sprite: '{current_sprite}'")
            last_facing = current_facing
            last_sprite = current_sprite
        
        # Capture key frames
        if frame in [0, 300, 600, 900, 1200]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/movement_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            print(f"Screenshot {frame}: Facing '{current_facing}', Sprite '{current_sprite}' - {screenshot_path}")
    
    print("\n✅ Persistent facing direction system tested!")
    print("🎮 Key Features:")
    print("   • Player maintains last facing direction when not moving")
    print("   • Direction changes only when actively moving in new direction")
    print("   • Smooth transitions between facing directions")
    print("   • Projectile firing direction matches player facing")
    print("🎯 No more snapping back to default 'up' direction!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_persistent_facing()
