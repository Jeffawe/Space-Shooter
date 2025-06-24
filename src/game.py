"""
Main Game class for Retro Space Shooter
"""
import pygame
from player import Player
from projectile import Projectile
from enemy import Enemy, Asteroid, Debris
from enemy_projectile import EnemyProjectile, Bomb
from enemy_spawner import EnemySpawner
from collision_system import CollisionSystem
from explosion import Explosion
from wave_manager import WaveManager
from wave_ui import WaveUI
from space_background import SpaceBackground
from constants import *

CYAN = (0, 255, 255)        # R-G-B
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

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
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Power-ups group
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create enemy spawner
        self.enemy_spawner = EnemySpawner()
        
        # Create power-up spawner
        from powerup import PowerUpSpawner
        self.powerup_spawner = PowerUpSpawner()
        
        # Create wave management system
        self.wave_manager = WaveManager()
        self.wave_ui = WaveUI()
        
        # Game mode
        self.story_mode = True  # True for story mode, False for endless mode
        self.wave_intro_timer = 0  # Timer for wave introduction screen
        
        # Create collision system
        self.collision_system = CollisionSystem()
        
        # Collision statistics
        self.collision_stats = {
            'player_collisions': 0,
            'projectile_hits': 0,
            'enemies_destroyed': 0,
            'asteroids_destroyed': 0,
            'debris_destroyed': 0,
            'bomb_explosions': 0,
            'powerups_collected': 0,
            'bombs_shot': 0,
            'waves_completed': 0
        }
        
        # Game state
        self.game_over = False
        self.player_death_timer = 0  # Timer for player death animation
        
        # Start story mode
        if self.story_mode:
            self.wave_intro_timer = 0  # No automatic timer, wait for SPACE
            self.wave_manager.start_wave_intro(1)  # Start with wave 1 intro
            print("🎮 Story Mode initialized - Press SPACE to begin Wave 1!")
        else:
            print("🎮 Endless Mode initialized")
        
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over and self.player_death_timer <= 0:
                    # Restart game
                    self.restart_game()
                elif event.key == pygame.K_SPACE and self.story_mode:
                    # Handle wave progression
                    wave_info = self.wave_manager.get_wave_info()
                    if wave_info:
                        if wave_info.get('wave_intro_active', False):
                            # Start the wave from intro
                            self.wave_manager.start_wave(wave_info['wave_number'])
                        elif wave_info['wave_complete']:
                            # Advance to next wave
                            if not self.wave_manager.next_wave():
                                # All waves completed - boss battle time!
                                print("🏆 Prepare for boss battle!")
                        elif wave_info['wave_failed']:
                            # Retry current wave
                            self.wave_manager.restart_wave()
                        elif wave_info['story_complete']:
                            # Start boss battle (TODO: implement boss)
                            print("🏆 Boss battle would start here!")
                elif event.key == pygame.K_r and self.story_mode:
                    # Retry wave in story mode
                    wave_info = self.wave_manager.get_wave_info()
                    if wave_info and wave_info['wave_failed']:
                        self.wave_manager.restart_wave()
                elif event.key == pygame.K_q and self.player.is_alive():
                    # Primary weapon (only if player is alive)
                    shot_data = self.player.shoot("primary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        self.projectiles.add(projectile)
                        self.all_sprites.add(projectile)
                elif event.key == pygame.K_e and self.player.is_alive():
                    # Secondary weapon (only if player is alive)
                    shot_data = self.player.shoot("secondary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        self.projectiles.add(projectile)
                        self.all_sprites.add(projectile)
    
    def update(self):
        """Update game state"""
        # Update game objects only if player is alive or in endless mode
        if self.player.is_alive() or not self.story_mode:
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
            
            # Update enemy spawner
            if self.story_mode:
                # Story mode: Wave-based spawning (only if player alive)
                self.wave_manager.update(self.enemies, self.all_sprites, self.player.is_alive())
            else:
                # Endless mode: Traditional spawning
                self.enemy_spawner.update(self.enemies, self.asteroids, self.debris, self.all_sprites)
            
            # Update power-up spawner (only if player alive)
            if self.player.is_alive():
                self.powerup_spawner.update(self.powerups, self.all_sprites)
        else:
            # Player is dead in story mode - only update explosions and UI
            # Remove any remaining enemy projectiles and bombs when player dies
            if self.player_death_timer == 180:  # First frame of death
                print("🛑 Player died - stopping all enemy activity")
                for projectile in self.enemy_projectiles:
                    projectile.kill()
                for bomb in self.bombs:
                    bomb.kill()
        
        # Always update explosions
        self.explosions.update()
        
        # Get current key states and update background
        keys = pygame.key.get_pressed()
        
        # Update background based on player position and key presses
        if self.player.is_alive():
            wave_info = self.wave_manager.get_wave_info() if self.story_mode else None
            # Allow movement only if not in wave intro
            if not self.story_mode or not (wave_info and wave_info.get('wave_intro_active', False)):
                self.background.update(self.player.rect, keys)
            # If in wave intro, don't update background (player can't move)
        
        # Update enemy spawner
        if self.story_mode:
            # Story mode: Wave-based spawning
            self.wave_manager.update(self.enemies, self.all_sprites)
        else:
            # Endless mode: Traditional spawning
            self.enemy_spawner.update(self.enemies, self.asteroids, self.debris, self.all_sprites)
        
        # Update power-up spawner
        self.powerup_spawner.update(self.powerups, self.all_sprites)
        
        # Process all collisions (only if player is alive)
        if self.player.is_alive():
            collision_results = self.collision_system.process_all_collisions(
                self.player, self.enemies, self.asteroids, self.debris, 
                self.projectiles, self.enemy_projectiles, self.bombs, self.powerups
            )
            
            # Update collision statistics
            for key, value in collision_results.items():
                if key == 'explosions':
                    # Add explosions to game
                    for explosion in value:
                        self.explosions.add(explosion)
                        self.all_sprites.add(explosion)
                        
                        # Check if player died
                        if explosion.explosion_type == "player":
                            self.game_over = True
                            self.player_death_timer = 180  # 3 seconds at 60 FPS
                elif key == 'powerup_messages':
                    # Handle power-up collection messages (could display them)
                    for message in value:
                        print(f"🎁 {message}")
                elif key in self.collision_stats:
                    # Update collision statistics
                    self.collision_stats[key] += value
                    
                    # Notify wave manager of enemy destruction
                    if key == 'enemies_destroyed' and self.story_mode:
                        for _ in range(value):
                            self.wave_manager.enemy_destroyed()
        else:
            # Player is dead, update death timer
            if self.player_death_timer > 0:
                self.player_death_timer -= 1
    
    def draw(self):
        """Draw everything to the screen"""
        # Draw background
        self.background.draw(self.screen)
        
        # Draw all sprites except player (we'll draw player separately)
        for sprite in self.all_sprites:
            if sprite != self.player:
                self.screen.blit(sprite.image, sprite.rect)
        
        # Draw player only if alive (explosion will show if dead)
        self.player.draw(self.screen)
        
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
        
        # Show collision statistics
        collision_text = pygame.font.Font(None, 20).render(
            f"Collisions: {self.collision_stats['player_collisions']} | Hits: {self.collision_stats['projectile_hits']} | Destroyed: {self.collision_stats['enemies_destroyed']}",
            True, GREEN
        )
        self.screen.blit(collision_text, (10, 160))
        
        # Show power-up statistics
        if self.collision_stats['powerups_collected'] > 0:
            powerup_text = pygame.font.Font(None, 20).render(
                f"🎁 Power-ups: {self.collision_stats['powerups_collected']}", 
                True, YELLOW
            )
            self.screen.blit(powerup_text, (10, 200))
        
        # Show energy effect status
        if self.player.has_energy_effect():
            energy_time = self.player.get_energy_time_remaining()
            energy_text = pygame.font.Font(None, 24).render(
                f"⚡ ENERGY BOOST: {energy_time:.1f}s", 
                True, CYAN
            )
            self.screen.blit(energy_text, (10, 220))
        
        # Show bombs shot statistics
        if self.collision_stats['bombs_shot'] > 0:
            bombs_shot_text = pygame.font.Font(None, 20).render(
                f"🎯 Bombs Shot: {self.collision_stats['bombs_shot']}", 
                True, ORANGE
            )
            self.screen.blit(bombs_shot_text, (10, 240))
        
        # Show shooting cooldown
        if self.player.shooting_cooldown > 0:
            cooldown_text = pygame.font.Font(None, 20).render(f"Cooldown: {self.player.shooting_cooldown}", True, RED)
            self.screen.blit(cooldown_text, (10, 260))
        
        # Draw player health bar
        self.player.draw_health(self.screen)
        
        # Draw enemy health bars
        for enemy in self.enemies:
            enemy.draw_health(self.screen)
        
        # Draw game over screen if player is dead
        if self.game_over:
            self.draw_game_over_screen()
        
        # Draw wave UI in story mode
        if self.story_mode:
            self.draw_wave_ui()
        
        # Draw scroll zone indicators (more subtle)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.upper_scroll_zone), (SCREEN_WIDTH, self.background.upper_scroll_zone), 1)
        pygame.draw.line(self.screen, (100, 100, 0), (0, self.background.lower_scroll_zone), (SCREEN_WIDTH, self.background.lower_scroll_zone), 1)
        
        pygame.display.flip()
    
    def draw_game_over_screen(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Statistics
        stats_text = font_medium.render(f"Enemies Destroyed: {self.collision_stats['enemies_destroyed']}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(stats_text, stats_rect)
        
        hits_text = font_medium.render(f"Total Hits: {self.collision_stats['projectile_hits']}", True, WHITE)
        hits_rect = hits_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(hits_text, hits_rect)
        
        # Restart instruction
        if self.player_death_timer <= 0:
            restart_text = font_small.render("Press R to Restart or ESC to Quit", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
            self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the game"""
        # Clear all sprite groups
        self.all_sprites.empty()
        self.projectiles.empty()
        self.enemy_projectiles.empty()
        self.bombs.empty()
        self.enemies.empty()
        self.asteroids.empty()
        self.debris.empty()
        self.explosions.empty()
        self.powerups.empty()
        
        # Reset player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Reset game state
        self.game_over = False
        self.player_death_timer = 0
        
        # Reset collision statistics
        self.collision_stats = {
            'player_collisions': 0,
            'projectile_hits': 0,
            'enemies_destroyed': 0,
            'asteroids_destroyed': 0,
            'debris_destroyed': 0,
            'bomb_explosions': 0,
            'powerups_collected': 0,
            'bombs_shot': 0,
            'waves_completed': 0
        }
        
        # Reset wave system for story mode
        if self.story_mode:
            self.wave_manager = WaveManager()
            self.wave_manager.start_wave_intro(1)  # Start with wave 1 intro
        
        print("Game restarted!")
    
    def draw_wave_ui(self):
        """Draw wave-related UI elements"""
        wave_info = self.wave_manager.get_wave_info()
        if not wave_info:
            return
            
        # Draw wave introduction screen
        if wave_info.get('wave_intro_active', False):
            self.wave_ui.draw_wave_intro(self.screen, wave_info)
            return
        
        # Draw main wave UI during active gameplay
        if wave_info['wave_active']:
            self.wave_ui.draw_wave_info(self.screen, self.wave_manager)
            self.wave_ui.draw_progress_bars(self.screen, self.wave_manager)
        
        # Draw wave status screens
        self.wave_ui.draw_wave_status(self.screen, self.wave_manager)
    
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
