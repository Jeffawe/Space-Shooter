"""
Main Game class for Retro Space Shooter
"""
import pygame
from player import Player
from projectile import Projectile
from enemy import Enemy, Asteroid, Debris
from enemy_projectile import EnemyProjectile, Bomb
from enemy_spawner import EnemySpawner
from space_background import SpaceBackground
from constants import *

class Game:
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Space Shooter - Amazon Build Challenge")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create space background
        self.background = SpaceBackground()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.debris = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create enemy spawner
        self.enemy_spawner = EnemySpawner()
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_q:
                    # Primary weapon
                    shot_data = self.player.shoot("primary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        self.projectiles.add(projectile)
                        self.all_sprites.add(projectile)
                elif event.key == pygame.K_e:
                    # Secondary weapon
                    shot_data = self.player.shoot("secondary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        self.projectiles.add(projectile)
                        self.all_sprites.add(projectile)
    
    def update(self):
        """Update game state"""
        # Update all sprites
        self.all_sprites.update()
        
        # Update enemies with AI (pass player position)
        for enemy in self.enemies:
            actions = enemy.update(self.player.rect)
            if actions:
                for action in actions:
                    if isinstance(action, EnemyProjectile):
                        self.enemy_projectiles.add(action)
                        self.all_sprites.add(action)
                    elif isinstance(action, Bomb):
                        self.bombs.add(action)
                        self.all_sprites.add(action)
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Update background based on player position and key presses
        self.background.update(self.player.rect, keys)
        
        # Update enemy spawner
        self.enemy_spawner.update(self.enemies, self.asteroids, self.debris, self.all_sprites)
    
    def draw(self):
        """Draw everything to the screen"""
        # Draw background
        self.background.draw(self.screen)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        fps = self.clock.get_fps()
        fps_text = pygame.font.Font(None, 36).render(f"FPS: {int(fps)}", True, WHITE)
        self.screen.blit(fps_text, (10, 10))
        
        # Show scroll info
        scroll_progress = self.background.get_scroll_progress()
        scroll_text = pygame.font.Font(None, 24).render(f"Scroll: {scroll_progress:.1%}", True, WHITE)
        self.screen.blit(scroll_text, (10, 50))
        
        # Show instructions
        player_y = self.player.rect.centery
        if player_y < self.background.upper_scroll_zone:
            instruction_text = pygame.font.Font(None, 20).render("Hold W to scroll up!", True, YELLOW)
            self.screen.blit(instruction_text, (10, 80))
        elif player_y > self.background.lower_scroll_zone:
            instruction_text = pygame.font.Font(None, 20).render("Hold S to scroll down!", True, YELLOW)
            self.screen.blit(instruction_text, (10, 80))
        else:
            instruction_text = pygame.font.Font(None, 20).render("Q: Primary Fire | E: Secondary Fire", True, WHITE)
            self.screen.blit(instruction_text, (10, 80))
        
        # Show projectile count
        projectile_count = len(self.projectiles)
        proj_text = pygame.font.Font(None, 20).render(f"Projectiles: {projectile_count}", True, WHITE)
        self.screen.blit(proj_text, (10, 100))
        
        # Show enemy counts and AI status
        enemy_count = len(self.enemies)
        asteroid_count = len(self.asteroids)
        debris_count = len(self.debris)
        enemy_projectile_count = len(self.enemy_projectiles)
        bomb_count = len(self.bombs)
        
        enemy_text = pygame.font.Font(None, 20).render(f"Enemies: {enemy_count} | Asteroids: {asteroid_count} | Debris: {debris_count}", True, WHITE)
        self.screen.blit(enemy_text, (10, 120))
        
        ai_text = pygame.font.Font(None, 20).render(f"Enemy Shots: {enemy_projectile_count} | Bombs: {bomb_count}", True, YELLOW)
        self.screen.blit(ai_text, (10, 140))
        
        # Show shooting cooldown
        if self.player.shooting_cooldown > 0:
            cooldown_text = pygame.font.Font(None, 20).render(f"Cooldown: {self.player.shooting_cooldown}", True, RED)
            self.screen.blit(cooldown_text, (10, 160))
        
        # Draw scroll zone indicators (more subtle)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.upper_scroll_zone), (SCREEN_WIDTH, self.background.upper_scroll_zone), 1)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.lower_scroll_zone), (SCREEN_WIDTH, self.background.lower_scroll_zone), 1)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Retro Space Shooter!")
        print("Use ARROW KEYS or WASD to move")
        print("Press ESC to quit")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
