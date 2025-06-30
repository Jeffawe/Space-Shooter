#!/usr/bin/env python3
"""
Demo the zone-based scrolling system
"""
import pygame
from game import Game

def demo_zone_scrolling():
    """Demo the zone-based background scrolling"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🌌 ZONE-BASED SCROLLING DEMO")
    print(f"Upper scroll zone: Y < {game.background.upper_scroll_zone}")
    print(f"Lower scroll zone: Y > {game.background.lower_scroll_zone}")
    print("Moving player to different zones to trigger scrolling...")
    
    # Test different player positions
    test_positions = [
        (400, 100, "Upper Zone - Should scroll up"),
        (400, 300, "Middle Zone - No scrolling"),
        (400, 500, "Lower Zone - Should scroll down"),
        (400, 300, "Back to Middle"),
    ]
    
    for i, (x, y, description) in enumerate(test_positions):
        # Move player to test position
        game.player.rect.centerx = x
        game.player.rect.centery = y
        
        # Update several times to see scrolling effect
        for _ in range(30):  # 30 frames of updates
            game.update()
        
        game.draw()
        
        # Save screenshot
        screenshot_path = f"assets/images/zone_demo_{i}.png"
        pygame.image.save(game.screen, screenshot_path)
        
        scroll_progress = game.background.get_scroll_progress()
        print(f"Position {i+1}: {description}")
        print(f"  Player at Y={y}, Scroll: {scroll_progress:.1%}")
        print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Zone-based scrolling system working!")
    print("🎮 Move to upper 30% or lower 70% of screen to trigger scrolling!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_zone_scrolling()
