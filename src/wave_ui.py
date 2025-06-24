"""
Wave UI System - Displays wave information, timers, and progress
"""
import pygame
from constants import *

class WaveUI:
    def __init__(self):
        """Initialize the wave UI system"""
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
        # UI positioning
        self.wave_info_x = SCREEN_WIDTH - 250
        self.wave_info_y = 10
        
        # Colors
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black
        self.border_color = WHITE
        self.progress_bg_color = (50, 50, 50)
        self.progress_fill_color = GREEN
        self.timer_normal_color = WHITE
        self.timer_warning_color = YELLOW
        self.timer_critical_color = RED
        
        print("🎮 Wave UI system initialized")
    
    def draw_wave_info(self, screen, wave_manager):
        """Draw the main wave information panel"""
        wave_info = wave_manager.get_wave_info()
        if not wave_info:
            return
            
        # Create semi-transparent background
        panel_width = 240
        panel_height = 120
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        
        # Draw border
        pygame.draw.rect(panel_surface, self.border_color, (0, 0, panel_width, panel_height), 2)
        
        # Wave number and description
        wave_text = self.font_large.render(f"WAVE {wave_info['wave_number']}", True, WHITE)
        panel_surface.blit(wave_text, (10, 10))
        
        desc_text = self.font_small.render(wave_info['description'], True, YELLOW)
        panel_surface.blit(desc_text, (10, 40))
        
        # Enemy progress
        progress_text = f"{wave_info['enemies_destroyed']}/{wave_info['enemies_required']} Enemies"
        progress_surface = self.font_medium.render(progress_text, True, WHITE)
        panel_surface.blit(progress_surface, (10, 65))
        
        # Timer
        time_remaining = wave_info['time_remaining']
        timer_color = self.get_timer_color(time_remaining)
        timer_text = f"Time: {time_remaining:.1f}s"
        timer_surface = self.font_medium.render(timer_text, True, timer_color)
        panel_surface.blit(timer_surface, (10, 90))
        
        # Blit panel to screen
        screen.blit(panel_surface, (self.wave_info_x, self.wave_info_y))
    
    def draw_progress_bars(self, screen, wave_manager):
        """Draw progress bars for enemy destruction and time"""
        wave_info = wave_manager.get_wave_info()
        if not wave_info or not wave_info['wave_active']:
            return
            
        bar_x = self.wave_info_x + 10
        bar_width = 220
        bar_height = 8
        
        # Enemy progress bar
        enemy_bar_y = self.wave_info_y + 135
        enemy_progress = wave_manager.get_progress_percentage()
        
        # Background
        pygame.draw.rect(screen, self.progress_bg_color, (bar_x, enemy_bar_y, bar_width, bar_height))
        # Progress fill
        fill_width = int((enemy_progress / 100) * bar_width)
        pygame.draw.rect(screen, self.progress_fill_color, (bar_x, enemy_bar_y, fill_width, bar_height))
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, enemy_bar_y, bar_width, bar_height), 1)
        
        # Label
        label = self.font_small.render("Enemy Progress", True, WHITE)
        screen.blit(label, (bar_x, enemy_bar_y - 20))
        
        # Time progress bar
        time_bar_y = enemy_bar_y + 30
        time_progress = wave_manager.get_time_percentage()
        time_color = self.get_timer_color(wave_info['time_remaining'])
        
        # Background
        pygame.draw.rect(screen, self.progress_bg_color, (bar_x, time_bar_y, bar_width, bar_height))
        # Progress fill
        time_fill_width = int((time_progress / 100) * bar_width)
        pygame.draw.rect(screen, time_color, (bar_x, time_bar_y, time_fill_width, bar_height))
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, time_bar_y, bar_width, bar_height), 1)
        
        # Label
        time_label = self.font_small.render("Time Remaining", True, WHITE)
        screen.blit(time_label, (bar_x, time_bar_y - 20))
    
    def draw_wave_status(self, screen, wave_manager):
        """Draw wave completion/failure status"""
        wave_info = wave_manager.get_wave_info()
        if not wave_info:
            return
            
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        if wave_info['wave_complete']:
            self.draw_wave_complete_screen(screen, wave_info, center_x, center_y)
        elif wave_info['wave_failed']:
            self.draw_wave_failed_screen(screen, wave_info, center_x, center_y)
        elif wave_info['story_complete']:
            self.draw_story_complete_screen(screen, center_x, center_y)
    
    def draw_wave_complete_screen(self, screen, wave_info, center_x, center_y):
        """Draw wave completion screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Success message
        success_text = self.font_large.render("WAVE COMPLETE!", True, GREEN)
        success_rect = success_text.get_rect(center=(center_x, center_y - 60))
        screen.blit(success_text, success_rect)
        
        # Wave info
        wave_text = self.font_medium.render(f"Wave {wave_info['wave_number']}: {wave_info['description']}", True, WHITE)
        wave_rect = wave_text.get_rect(center=(center_x, center_y - 20))
        screen.blit(wave_text, wave_rect)
        
        # Stats
        stats_text = f"Enemies Destroyed: {wave_info['enemies_destroyed']}/{wave_info['enemies_required']}"
        stats_surface = self.font_small.render(stats_text, True, YELLOW)
        stats_rect = stats_surface.get_rect(center=(center_x, center_y + 10))
        screen.blit(stats_surface, stats_rect)
        
        # Continue instruction
        continue_text = self.font_small.render("Press SPACE to continue to next wave", True, WHITE)
        continue_rect = continue_text.get_rect(center=(center_x, center_y + 50))
        screen.blit(continue_text, continue_rect)
    
    def draw_wave_failed_screen(self, screen, wave_info, center_x, center_y):
        """Draw wave failure screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Failure message
        fail_text = self.font_large.render("WAVE FAILED!", True, RED)
        fail_rect = fail_text.get_rect(center=(center_x, center_y - 60))
        screen.blit(fail_text, fail_rect)
        
        # Wave info
        wave_text = self.font_medium.render(f"Wave {wave_info['wave_number']}: {wave_info['description']}", True, WHITE)
        wave_rect = wave_text.get_rect(center=(center_x, center_y - 20))
        screen.blit(wave_text, wave_rect)
        
        # Stats
        stats_text = f"Only destroyed {wave_info['enemies_destroyed']}/{wave_info['enemies_required']} enemies"
        stats_surface = self.font_small.render(stats_text, True, YELLOW)
        stats_rect = stats_surface.get_rect(center=(center_x, center_y + 10))
        screen.blit(stats_surface, stats_rect)
        
        # Retry instruction
        retry_text = self.font_small.render("Press R to retry wave or ESC to quit", True, WHITE)
        retry_rect = retry_text.get_rect(center=(center_x, center_y + 50))
        screen.blit(retry_text, retry_rect)
    
    def draw_story_complete_screen(self, screen, center_x, center_y):
        """Draw story completion screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Victory message
        victory_text = self.font_large.render("ALL WAVES COMPLETE!", True, GOLD)
        victory_rect = victory_text.get_rect(center=(center_x, center_y - 60))
        screen.blit(victory_text, victory_rect)
        
        # Boss battle message
        boss_text = self.font_medium.render("Prepare for the final boss battle!", True, WHITE)
        boss_rect = boss_text.get_rect(center=(center_x, center_y - 20))
        screen.blit(boss_text, boss_rect)
        
        # Continue instruction
        continue_text = self.font_small.render("Press SPACE to begin boss battle", True, WHITE)
        continue_rect = continue_text.get_rect(center=(center_x, center_y + 50))
        screen.blit(continue_text, continue_rect)
    
    def draw_wave_intro(self, screen, wave_info):
        """Draw wave introduction screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Wave announcement
        wave_text = self.font_large.render(f"WAVE {wave_info['wave_number']}", True, CYAN)
        wave_rect = wave_text.get_rect(center=(center_x, center_y - 80))
        screen.blit(wave_text, wave_rect)
        
        # Description
        desc_text = self.font_medium.render(wave_info['description'], True, YELLOW)
        desc_rect = desc_text.get_rect(center=(center_x, center_y - 40))
        screen.blit(desc_text, desc_rect)
        
        # Objective
        obj_text = f"Destroy {wave_info['enemies_required']} enemies"
        obj_surface = self.font_small.render(obj_text, True, WHITE)
        obj_rect = obj_surface.get_rect(center=(center_x, center_y))
        screen.blit(obj_surface, obj_rect)
        
        # Time limit
        time_text = f"Time limit: {wave_info['time_remaining']:.0f} seconds"
        time_surface = self.font_small.render(time_text, True, WHITE)
        time_rect = time_surface.get_rect(center=(center_x, center_y + 30))
        screen.blit(time_surface, time_rect)
        
        # Start instruction
        start_text = self.font_small.render("Press SPACE to begin wave", True, GREEN)
        start_rect = start_text.get_rect(center=(center_x, center_y + 80))
        screen.blit(start_text, start_rect)
    
    def get_timer_color(self, time_remaining):
        """Get appropriate color for timer based on time remaining"""
        if time_remaining > 30:
            return self.timer_normal_color
        elif time_remaining > 10:
            return self.timer_warning_color
        else:
            return self.timer_critical_color
