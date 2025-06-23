"""
Scrolling Background system for Retro Space Shooter
"""
import pygame
from constants import *

class ScrollingBackground:
    def __init__(self, background_image_path):
        """Initialize the scrolling background"""
        # Load the background image
        self.original_bg = pygame.image.load(background_image_path).convert()
        
        # Get background dimensions
        self.bg_width = self.original_bg.get_width()
        self.bg_height = self.original_bg.get_height()
        
        # Scale background to fit screen width if needed
        if self.bg_width != SCREEN_WIDTH:
            scale_factor = SCREEN_WIDTH / self.bg_width
            new_height = int(self.bg_height * scale_factor)
            self.background = pygame.transform.scale(self.original_bg, (SCREEN_WIDTH, new_height))
            self.bg_height = new_height
        else:
            self.background = self.original_bg
        
        # Background scrolling variables
        self.scroll_y = 0
        self.max_scroll = max(0, self.bg_height - SCREEN_HEIGHT)  # Maximum scroll distance
        
        print(f"Background loaded: {self.bg_width}x{self.bg_height}")
        print(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"Max scroll distance: {self.max_scroll}")
        
    def update(self, player_movement_y):
        """Update background scroll based on player movement"""
        if player_movement_y != 0:
            # Move background opposite to player movement for parallax effect
            self.scroll_y -= player_movement_y * BACKGROUND_SCROLL_SPEED
            
            # Clamp scroll position to boundaries
            self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
    
    def draw(self, screen):
        """Draw the background to the screen"""
        # Calculate the source rectangle from the background image
        source_rect = pygame.Rect(0, self.scroll_y, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Make sure we don't go beyond the background image bounds
        if self.scroll_y + SCREEN_HEIGHT > self.bg_height:
            # We're at the bottom, adjust the source rectangle
            source_rect.height = self.bg_height - self.scroll_y
            screen.blit(self.background, (0, 0), source_rect)
            
            # Fill the remaining space with black (deep space)
            if source_rect.height < SCREEN_HEIGHT:
                remaining_height = SCREEN_HEIGHT - source_rect.height
                pygame.draw.rect(screen, BLACK, (0, source_rect.height, SCREEN_WIDTH, remaining_height))
        else:
            # Normal scrolling
            screen.blit(self.background, (0, 0), source_rect)
    
    def get_scroll_progress(self):
        """Get scroll progress as a percentage (0.0 to 1.0)"""
        if self.max_scroll == 0:
            return 0.0
        return self.scroll_y / self.max_scroll
    
    def is_at_top(self):
        """Check if background is at the top"""
        return self.scroll_y <= 0
    
    def is_at_bottom(self):
        """Check if background is at the bottom"""
        return self.scroll_y >= self.max_scroll
