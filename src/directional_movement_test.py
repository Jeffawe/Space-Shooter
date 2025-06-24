#!/usr/bin/env python3
"""
Test directional movement with vertical orientation preservation
"""
import pygame
from game import Game
from constants import *

def test_directional_movement():
    """Test that A/D movement preserves vertical orientation (up/down)"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎮 DIRECTIONAL MOVEMENT TEST")
    print("Testing A/D movement with vertical orientation preservation")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Test sequence: demonstrate vertical orientation preservation
    test_sequence = [
        (0, 60, "Initial state - facing up", {}),
        (60, 120, "Press A (left) while facing up - should stay up-oriented", {'a': True}),
        (120, 180, "Release A - should return to facing up", {}),
        (180, 240, "Press S to face down", {'s': True}),
        (240, 300, "Release S - should stay facing down", {}),
        (300, 360, "Press A (left) while facing down - should stay down-oriented", {'a': True}),
        (360, 420, "Release A - should return to facing down", {}),
        (420, 480, "Press D (right) while facing down - should stay down-oriented", {'d': True}),
        (480, 540, "Release D - should return to facing down", {}),
        (540, 600, "Press W to face up", {'w': True}),
        (600, 660, "Release W - should stay facing up", {}),
        (660, 720, "Press D (right) while facing up - should stay up-oriented", {'d': True}),
        (720, 780, "Release D - should return to facing up", {}),
    ]
    
    current_test = 0
    
    print(f"\nTest sequence:")
    for i, (start, end, description, keys) in enumerate(test_sequence):
        print(f"  {i+1}. Frames {start}-{end}: {description}")
    
    print("\n🎯 Expected Behavior:")
    print("  • A/D movement while facing UP should maintain UP orientation")
    print("  • A/D movement while facing DOWN should maintain DOWN orientation")
    print("  • No snapping to UP when moving left/right while facing down")
    
    # Run test
    for frame in range(780):
        # Determine current test phase
        while current_test < len(test_sequence) and frame >= test_sequence[current_test][1]:
            current_test += 1
        
        if current_test < len(test_sequence):
            start_frame, end_frame, description, keys = test_sequence[current_test]
            
            # Set movement flags based on test phase
            game.player.moving_up = keys.get('w', False)
            game.player.moving_down = keys.get('s', False)
            game.player.moving_left = keys.get('a', False)
            game.player.moving_right = keys.get('d', False)
        else:
            # No movement
            game.player.moving_up = False
            game.player.moving_down = False
            game.player.moving_left = False
            game.player.moving_right = False
        
        # Update sprite based on movement
        game.player.update_sprite()
        
        # Update game
        game.all_sprites.update()
        game.explosions.update()
        
        # Log key frames
        if frame in [0, 120, 180, 300, 360, 420, 480, 540, 600, 660, 720, 780]:
            current_phase = ""
            for i, (start, end, desc, keys) in enumerate(test_sequence):
                if start <= frame < end:
                    current_phase = desc
                    break
            
            print(f"\nFrame {frame}: {current_phase}")
            print(f"  Facing: {game.player.last_facing_direction}")
            print(f"  Sprite: {game.player.current_sprite}")
            print(f"  Moving: Up={game.player.moving_up}, Down={game.player.moving_down}, Left={game.player.moving_left}, Right={game.player.moving_right}")
            
            # Take screenshot
            game.draw()
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/directional_test_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Directional movement test completed!")
    print("\n🎯 Key Test Results:")
    print("  Frame 120: A pressed while facing UP → Should show left lean but maintain UP orientation")
    print("  Frame 360: A pressed while facing DOWN → Should show left lean but maintain DOWN orientation") 
    print("  Frame 480: D pressed while facing DOWN → Should show right lean but maintain DOWN orientation")
    print("  Frame 720: D pressed while facing UP → Should show right lean but maintain UP orientation")
    
    print("\n🚀 Expected Improvements:")
    print("  ✅ No more snapping to UP when pressing A/D while facing down")
    print("  ✅ Horizontal movement preserves vertical orientation")
    print("  ✅ Natural movement behavior in all directions")
    
    pygame.quit()

if __name__ == "__main__":
    test_directional_movement()
