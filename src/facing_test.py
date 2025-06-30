#!/usr/bin/env python3
"""
Test persistent facing direction by simulating key presses
"""
import pygame
from game import Game
from constants import *

def test_persistent_facing():
    """Test persistent facing direction with simulated key presses"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎮 PERSISTENT FACING DIRECTION TEST")
    print("Simulating key presses to test facing direction persistence")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Test sequence: simulate different key press patterns
    test_sequence = [
        (0, 60, "Initial state - facing up"),
        (60, 120, "Press S (down) for 1 second"),
        (120, 180, "Release S - should stay facing down"),
        (180, 240, "Press W (up) for 1 second"),
        (240, 300, "Release W - should stay facing up"),
        (300, 360, "Press A (left) for 1 second"),
        (360, 420, "Release A - should stay facing left"),
        (420, 480, "Press D (right) for 1 second"),
        (480, 540, "Release D - should stay facing right"),
        (540, 600, "Final state - should maintain last direction"),
    ]
    
    current_test = 0
    
    print(f"\nStarting test sequence:")
    for i, (start, end, description) in enumerate(test_sequence):
        print(f"  {i+1}. Frames {start}-{end}: {description}")
    
    # Run test
    for frame in range(600):
        # Determine current test phase
        while current_test < len(test_sequence) and frame >= test_sequence[current_test][1]:
            current_test += 1
        
        if current_test < len(test_sequence):
            start_frame, end_frame, description = test_sequence[current_test]
            
            # Simulate key presses based on test phase
            keys_pressed = {}
            if start_frame <= frame < end_frame:
                if "Press S" in description:
                    keys_pressed[pygame.K_s] = True
                elif "Press W" in description:
                    keys_pressed[pygame.K_w] = True
                elif "Press A" in description:
                    keys_pressed[pygame.K_a] = True
                elif "Press D" in description:
                    keys_pressed[pygame.K_d] = True
        
        # Manually set key states for testing
        if keys_pressed:
            # Simulate the key press by directly setting movement flags
            game.player.moving_up = keys_pressed.get(pygame.K_w, False)
            game.player.moving_down = keys_pressed.get(pygame.K_s, False)
            game.player.moving_left = keys_pressed.get(pygame.K_a, False)
            game.player.moving_right = keys_pressed.get(pygame.K_d, False)
        else:
            # No keys pressed - reset movement flags
            game.player.moving_up = False
            game.player.moving_down = False
            game.player.moving_left = False
            game.player.moving_right = False
        
        # Update sprite based on movement
        game.player.update_sprite()
        
        # Update game (but skip normal input handling)
        game.all_sprites.update()
        game.explosions.update()
        
        # Log facing direction changes
        if frame in [0, 60, 120, 180, 240, 300, 360, 420, 480, 540]:
            current_phase = ""
            for i, (start, end, desc) in enumerate(test_sequence):
                if start <= frame < end:
                    current_phase = desc
                    break
            
            print(f"Frame {frame}: {current_phase}")
            print(f"  Facing: {game.player.last_facing_direction}")
            print(f"  Sprite: {game.player.current_sprite}")
            print(f"  Moving: Up={game.player.moving_up}, Down={game.player.moving_down}, Left={game.player.moving_left}, Right={game.player.moving_right}")
            
            # Take screenshot
            game.draw()
            screenshot_path = f"assets/images/facing_test_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            print(f"  Screenshot: {screenshot_path}\n")
    
    print("✅ Persistent facing direction test completed!")
    print("\n🎯 Expected Results:")
    print("  • Frame 0: Facing 'up', Sprite 'up' (initial)")
    print("  • Frame 120: Facing 'down', Sprite 'down' (after pressing S)")
    print("  • Frame 180: Facing 'down', Sprite 'down' (maintained after releasing S)")
    print("  • Frame 240: Facing 'up', Sprite 'up' (after pressing W)")
    print("  • Frame 300: Facing 'up', Sprite 'up' (maintained after releasing W)")
    print("  • Frame 360: Facing 'left', Sprite 'left1' (after pressing A)")
    print("  • Frame 420: Facing 'left', Sprite 'left1' (maintained after releasing A)")
    print("  • Frame 480: Facing 'right', Sprite 'right1' (after pressing D)")
    print("  • Frame 540: Facing 'right', Sprite 'right1' (maintained after releasing D)")
    
    pygame.quit()

if __name__ == "__main__":
    test_persistent_facing()
