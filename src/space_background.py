"""
Space Background system for Retro Space Shooter
Starfield background with key-press triggered scrolling
"""
import pygame
from constants import *

class SpaceBackground:
    def __init__(self):
        """Initialize the space background"""
        # Load the background image
        bg_path = "assets/images/Space_01-Sheet.png"
        self.original_bg = pygame.image.load(bg_path).convert()
        
        # Get original dimensions
        self.original_width = self.original_bg.get_width()
        self.original_height = self.original_bg.get_height()
        
        # Extract only the starfield sections (skip blue and nebula sections)
        self.create_starfield_background()
        
        # Background scroll position
        self.scroll_y = 0
        self.max_scroll = max(0, self.bg_height - SCREEN_HEIGHT)
        
        # Scrolling zones (when player reaches these areas AND presses keys, scrolling happens)
        self.upper_scroll_zone = SCREEN_HEIGHT * 0.3  # Upper 30% of screen
        self.lower_scroll_zone = SCREEN_HEIGHT * 0.7  # Lower 70% of screen
        
        print(f"Original background: {self.original_width}x{self.original_height}")
        print(f"Starfield background: {SCREEN_WIDTH}x{self.bg_height}")
        print(f"Max scroll: {self.max_scroll} pixels")
        print(f"Scroll zones: Upper={self.upper_scroll_zone}, Lower={self.lower_scroll_zone}")
        
    def create_starfield_background(self):
        """Create background using only starfield sections"""
        # The background has 3 sections - we want only the bottom starfield section
        section_height = self.original_height // 3
        
        # Extract the bottom starfield section (the one with scattered white stars)
        starfield_section = self.original_bg.subsurface((0, section_height * 2, self.original_width, section_height))
        
        # Create a taller background by repeating the starfield
        # Make it about 3x screen height for good scrolling range
        self.bg_height = SCREEN_HEIGHT * 3
        self.background = pygame.Surface((SCREEN_WIDTH, self.bg_height))
        
        # Scale the starfield section to screen width
        scale_factor = SCREEN_WIDTH / self.original_width
        scaled_section_height = int(section_height * scale_factor)
        scaled_starfield = pygame.transform.scale(starfield_section, (SCREEN_WIDTH, scaled_section_height))
        
        # Tile the starfield to fill the background
        y_pos = 0
        while y_pos < self.bg_height:
            self.background.blit(scaled_starfield, (0, y_pos))
            y_pos += scaled_section_height
            
        print(f"Created starfield background by tiling {SCREEN_WIDTH}x{scaled_section_height} section")
        
    def update(self, player_rect, keys_pressed):
        """Update background based on player position AND key presses"""
        player_center_y = player_rect.centery
        
        # Only scroll if player is in zone AND pressing the correct key
        
        # Upper zone + W key pressed - scroll background down (reveal upper stars)
        if (player_center_y < self.upper_scroll_zone and 
            (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and 
            self.scroll_y > 0):
            self.scroll_y -= BACKGROUND_SCROLL_SPEED
            if self.scroll_y < 0:
                self.scroll_y = 0
                
        # Lower zone + S key pressed - scroll background up (reveal lower stars)  
        elif (player_center_y > self.lower_scroll_zone and 
              (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) and 
              self.scroll_y < self.max_scroll):
            self.scroll_y += BACKGROUND_SCROLL_SPEED
            if self.scroll_y > self.max_scroll:
                self.scroll_y = self.max_scroll
    
    def draw(self, screen):
        """Draw the background"""
        # Calculate source rectangle from background
        source_rect = pygame.Rect(0, int(self.scroll_y), SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Handle edge cases
        if self.scroll_y + SCREEN_HEIGHT > self.bg_height:
            # At bottom of background
            available_height = self.bg_height - self.scroll_y
            if available_height > 0:
                partial_rect = pygame.Rect(0, int(self.scroll_y), SCREEN_WIDTH, int(available_height))
                screen.blit(self.background, (0, 0), partial_rect)
                
                # Fill remaining space with black
                if available_height < SCREEN_HEIGHT:
                    remaining_height = SCREEN_HEIGHT - available_height
                    pygame.draw.rect(screen, BLACK, (0, available_height, SCREEN_WIDTH, remaining_height))
            else:
                screen.fill(BLACK)
        else:
            # Normal drawing
            screen.blit(self.background, (0, 0), source_rect)
    
    def get_scroll_progress(self):
        """Get scroll progress as percentage"""
        if self.max_scroll == 0:
            return 0.0
        return self.scroll_y / self.max_scroll
    
    def is_at_top(self):
        """Check if at top of background"""
        return self.scroll_y <= 0
    
    def is_at_bottom(self):
        """Check if at bottom of background"""
        return self.scroll_y >= self.max_scroll
