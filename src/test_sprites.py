#!/usr/bin/env python3
"""
Test script to verify sprite cutting
"""
import pygame
import os
from constants import *

def test_sprite_cutting():
    """Test the sprite cutting functionality"""
    pygame.init()
    
    # Create a dummy display to initialize pygame properly
    pygame.display.set_mode((100, 100))
    
    # Load the sprite sheet
    sprite_sheet_path = "/home/jeffawe/amazon-build/assets/images/Player01-Sheet.png"
    
    try:
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return
    
    print(f"Original sprite sheet size: {sprite_sheet.get_size()}")
    
    # Get dimensions
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()
    frame_width = sheet_width // 5
    frame_height = sheet_height
    
    print(f"Frame size: {frame_width}x{frame_height}")
    
    # Cut and save individual sprites for verification
    sprites = {}
    sprite_names = ['left2', 'left1', 'center', 'right1', 'right2']
    
    for i, name in enumerate(sprite_names):
        sprite = sprite_sheet.subsurface((frame_width * i, 0, frame_width, frame_height))
        sprites[name] = sprite
        
        # Save individual sprite for verification
        output_path = f"/home/jeffawe/amazon-build/assets/images/player_{name}.png"
        pygame.image.save(sprite, output_path)
        print(f"Saved {name} sprite to {output_path}")
    
    print("Sprite cutting test completed!")
    pygame.quit()

if __name__ == "__main__":
    test_sprite_cutting()
