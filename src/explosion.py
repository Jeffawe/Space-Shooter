"""
Explosion animation system for Retro Space Shooter
Cuts and animates frames from Explosion02-Sheet
"""
import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, explosion_type="player"):
        """Initialize an explosion animation"""
        super().__init__()
        
        self.explosion_type = explosion_type
        self.animation_frames = []
        self.current_frame = 0
        self.animation_speed = 4  # Frames to wait between animation frames (slower for better visibility)
        self.frame_counter = 0
        
        # Load explosion frames from sheet
        self.load_explosion_frames()
        
        # Set initial frame
        if self.animation_frames:
            self.image = self.animation_frames[0]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
        
        print(f"Created {explosion_type} explosion at ({x}, {y}) with {len(self.animation_frames)} frames")
        
    def load_explosion_frames(self):
        """Load and cut explosion animation frames from Explosion02-Sheet"""
        try:
            explosion_sheet = pygame.image.load("/home/jeffawe/amazon-build/assets/images/Explosion02-Sheet.png").convert_alpha()
            
            # The sheet contains 10 explosion frames in a single row
            sheet_width = explosion_sheet.get_width()
            sheet_height = explosion_sheet.get_height()
            frame_width = sheet_width // 10  # 10 frames in the sheet
            
            print(f"Explosion sheet: {sheet_width}x{sheet_height}, frame size: {frame_width}x{sheet_height}")
            
            # Extract each frame from the sheet
            for i in range(10):
                x = i * frame_width
                frame_rect = pygame.Rect(x, 0, frame_width, sheet_height)
                
                # Extract the frame and convert to proper format
                frame = explosion_sheet.subsurface(frame_rect).copy()
                
                # Scale up the explosion for better visibility (2x size)
                if self.explosion_type == "player":
                    # Player explosions are larger
                    scaled_frame = pygame.transform.scale(frame, (frame_width * 2, sheet_height * 2))
                else:
                    # Enemy explosions are normal size
                    scaled_frame = pygame.transform.scale(frame, (frame_width * 1.5, int(sheet_height * 1.5)))
                
                self.animation_frames.append(scaled_frame)
            
            print(f"Loaded {len(self.animation_frames)} explosion frames")
            
        except pygame.error as e:
            print(f"Error loading explosion sheet: {e}")
            # Create a simple colored circle as fallback
            self.create_fallback_explosion()
    
    def create_fallback_explosion(self):
        """Create a simple fallback explosion if sheet loading fails"""
        for i in range(10):
            size = 10 + i * 5  # Growing circle
            surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color = (255, 255 - i * 20, 0, 255 - i * 25)  # Fading yellow to red
            pygame.draw.circle(surface, color, (size, size), size)
            self.animation_frames.append(surface)
        
        print("Created fallback explosion animation")
        
    def update(self):
        """Update explosion animation"""
        self.frame_counter += 1
        
        # Advance animation frame
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame += 1
            
            # Check if animation is complete
            if self.current_frame >= len(self.animation_frames):
                self.kill()  # Remove explosion when animation is done
                print(f"{self.explosion_type} explosion animation completed")
                return
            
            # Update image to current frame
            self.image = self.animation_frames[self.current_frame]
            
            # Keep the explosion centered on the original position
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
