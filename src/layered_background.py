"""
Layered Background system for Retro Space Shooter
Separates background sheets into background and foreground layers
"""
import pygame
from constants import *

class LayeredBackground:
    def __init__(self, background_sheet_path):
        """Initialize the layered background system"""
        # Load the background sheet
        self.original_sheet = pygame.image.load(background_sheet_path).convert_alpha()
        
        # Get sheet dimensions
        self.sheet_width = self.original_sheet.get_width()
        self.sheet_height = self.original_sheet.get_height()
        
        print(f"Background sheet loaded: {self.sheet_width}x{self.sheet_height}")
        
        # Scale to screen width if needed
        if self.sheet_width != SCREEN_WIDTH:
            scale_factor = SCREEN_WIDTH / self.sheet_width
            new_height = int(self.sheet_height * scale_factor)
            self.background_sheet = pygame.transform.scale(self.original_sheet, (SCREEN_WIDTH, new_height))
            self.sheet_height = new_height
        else:
            self.background_sheet = self.original_sheet
        
        # Split the sheet into layers
        self.split_layers()
        
        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll = max(0, self.bg_height - SCREEN_HEIGHT)
        
        print(f"Background layers created - BG: {self.bg_height}px, FG: {self.fg_height}px")
        print(f"Max scroll distance: {self.max_scroll}")
        
    def split_layers(self):
        """Split the background sheet into background and foreground layers"""
        # Analyze the image to find where to split
        # For now, let's assume the sheet is divided into thirds:
        # Top third: deep space (background)
        # Middle third: nebula clouds (foreground) 
        # Bottom third: more space (background)
        
        third_height = self.sheet_height // 3
        
        # Create background layer (deep space + bottom space)
        self.bg_height = self.sheet_height
        self.background_layer = pygame.Surface((SCREEN_WIDTH, self.bg_height), pygame.SRCALPHA)
        
        # Copy top section (deep space)
        top_section = self.background_sheet.subsurface((0, 0, SCREEN_WIDTH, third_height))
        self.background_layer.blit(top_section, (0, 0))
        
        # Copy bottom section (more space)
        bottom_section = self.background_sheet.subsurface((0, third_height * 2, SCREEN_WIDTH, third_height))
        self.background_layer.blit(bottom_section, (0, third_height * 2))
        
        # Fill middle section with deep space color to connect top and bottom
        middle_fill = pygame.Surface((SCREEN_WIDTH, third_height))
        middle_fill.fill((10, 10, 30))  # Dark space blue
        self.background_layer.blit(middle_fill, (0, third_height))
        
        # Create foreground layer (nebula clouds)
        self.fg_height = third_height
        self.foreground_layer = self.background_sheet.subsurface((0, third_height, SCREEN_WIDTH, third_height)).copy()
        
        # Make the foreground semi-transparent for better layering effect
        self.foreground_layer.set_alpha(180)  # 70% opacity
        
    def update(self, player_movement_y):
        """Update background scroll based on player movement"""
        if player_movement_y != 0:
            # Move background opposite to player movement
            self.scroll_y -= player_movement_y * BACKGROUND_SCROLL_SPEED
            
            # Clamp scroll position to boundaries
            self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
    
    def draw_background(self, screen):
        """Draw the background layer"""
        source_rect = pygame.Rect(0, self.scroll_y, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        if self.scroll_y + SCREEN_HEIGHT > self.bg_height:
            # At the bottom boundary
            source_rect.height = self.bg_height - self.scroll_y
            screen.blit(self.background_layer, (0, 0), source_rect)
            
            # Fill remaining space with deep space
            if source_rect.height < SCREEN_HEIGHT:
                remaining_height = SCREEN_HEIGHT - source_rect.height
                pygame.draw.rect(screen, (5, 5, 15), (0, source_rect.height, SCREEN_WIDTH, remaining_height))
        else:
            # Normal scrolling
            screen.blit(self.background_layer, (0, 0), source_rect)
    
    def draw_foreground(self, screen):
        """Draw the foreground layer (clouds) on top of everything"""
        # Calculate where the nebula clouds should appear based on scroll position
        # The clouds should appear when we're in the middle section of the background
        
        cloud_start_scroll = self.max_scroll * 0.3  # Clouds start appearing at 30% scroll
        cloud_end_scroll = self.max_scroll * 0.7    # Clouds end at 70% scroll
        
        if cloud_start_scroll <= self.scroll_y <= cloud_end_scroll:
            # Calculate cloud position and opacity based on scroll
            cloud_progress = (self.scroll_y - cloud_start_scroll) / (cloud_end_scroll - cloud_start_scroll)
            
            # Position clouds to scroll slower than background (parallax effect)
            cloud_y = -int(cloud_progress * self.fg_height * 0.5)
            
            # Draw the nebula clouds
            screen.blit(self.foreground_layer, (0, cloud_y))
    
    def get_scroll_progress(self):
        """Get scroll progress as a percentage"""
        if self.max_scroll == 0:
            return 0.0
        return self.scroll_y / self.max_scroll
    
    def is_at_top(self):
        """Check if at top boundary"""
        return self.scroll_y <= 0
    
    def is_at_bottom(self):
        """Check if at bottom boundary"""
        return self.scroll_y >= self.max_scroll
