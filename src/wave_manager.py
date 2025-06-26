"""
Wave Management System for Story Mode
Handles wave progression, enemy composition, timers, and quotas
"""
import pygame
import random
from constants import *

class WaveManager:
    def __init__(self):
        """Initialize the wave management system"""
        self.current_wave = 1
        self.max_waves = 10
        self.wave_active = False
        self.wave_complete = False
        self.wave_failed = False
        self.story_complete = False
        self.wave_intro_active = False  # New state for wave introduction
        
        # Wave timing
        self.wave_timer = 0
        self.wave_duration = 0  # Set per wave
        
        # Enemy tracking - continuous spawning, no fixed count
        self.enemies_spawned = 0
        self.enemies_destroyed = 0  # Track for statistics only
        self.max_enemies_on_screen = 10  # Increased from 8 for more action
        
        # Wave composition definitions - continuous spawning with increasing frequency
        self.wave_compositions = {
            1: {
                'enemies': ['fighter1'],
                'spawn_interval': 120,  # 2 seconds between spawns
                'spawn_variance': 60,   # ±1 second variance
                'duration': 60,  # 60 seconds
                'description': "Training Wave - Basic Fighters"
            },
            2: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'spawn_interval': 90,   # 1.5 seconds between spawns (faster)
                'spawn_variance': 45,
                'duration': 75,
                'description': "Mixed Squadron"
            },
            3: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'spawn_interval': 80,   # 1.33 seconds between spawns
                'spawn_variance': 40,
                'duration': 80,
                'description': "Heavy Patrol"
            },
            4: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'spawn_interval': 70,   # 1.17 seconds between spawns
                'spawn_variance': 35,
                'duration': 85,
                'description': "Advanced Formation"
            },
            5: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'spawn_interval': 60,   # 1.0 seconds between spawns
                'spawn_variance': 30,
                'duration': 90,
                'description': "Elite Squadron"
            },
            6: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship'],
                'spawn_interval': 65,   # 1.08 seconds between spawns
                'spawn_variance': 30,
                'duration': 95,
                'description': "New Threat Detected"
            },
            7: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'spawn_interval': 60,   # 1 second between spawns
                'spawn_variance': 30,
                'duration': 100,
                'description': "Pirate Raid"
            },
            8: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'spawn_interval': 55,   # 0.92 seconds between spawns
                'spawn_variance': 25,
                'duration': 105,
                'description': "Full Assault"
            },
            9: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'spawn_interval': 50,   # 0.83 seconds between spawns
                'spawn_variance': 25,
                'duration': 110,
                'description': "Final Defense"
            },
            10: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'spawn_interval': 45,   # 0.75 seconds between spawns
                'spawn_variance': 20,
                'duration': 120,
                'description': "Last Stand"
            }
        }
        
        # Spawning control
        self.spawn_timer = 0
        self.spawn_interval = 90  # Base spawn interval (1.5 seconds)
        self.spawn_variance = 30  # Random variance in spawn timing
        
        print("🌊 Wave Manager initialized - Story Mode ready!")
        
    def start_wave_intro(self, wave_number):
        """Start wave introduction (player can't move yet)"""
        if wave_number > self.max_waves:
            self.story_complete = True
            print("🏆 All waves completed! Boss battle time!")
            return False
            
        self.current_wave = wave_number
        self.wave_intro_active = True
        self.wave_active = False
        self.wave_complete = False
        self.wave_failed = False
        
        print(f"🌊 Wave {wave_number} introduction - Press SPACE to begin!")
        return True
    
    def start_wave(self, wave_number):
        """Start a specific wave (called after intro)"""
        if wave_number > self.max_waves:
            self.story_complete = True
            print("🏆 All waves completed! Boss battle time!")
            return False
            
        self.current_wave = wave_number
        wave_data = self.wave_compositions[wave_number]
        
        # Set wave parameters
        self.wave_duration = wave_data['duration'] * 60  # Convert to frames (60 FPS)
        self.wave_timer = self.wave_duration
        
        # Reset counters
        self.enemies_destroyed = 0
        self.enemies_spawned = 0
        self.spawn_timer = 0
        
        # Set wave state
        self.wave_intro_active = False
        self.wave_active = True
        self.wave_complete = False
        self.wave_failed = False
        
        # Set spawn parameters from wave data
        self.spawn_interval = wave_data['spawn_interval']
        self.spawn_variance = wave_data['spawn_variance']
        
        print(f"🌊 Wave {wave_number} started: {wave_data['description']}")
        print(f"   Duration: {wave_data['duration']} seconds")
        print(f"   Enemy types: {', '.join(wave_data['enemies'])}")
        print(f"   Spawn rate: Every {wave_data['spawn_interval']/60:.1f}s (±{wave_data['spawn_variance']/60:.1f}s)")
        
        return True
    
    def update(self, enemies_group, all_sprites_group, player_alive=True):
        """Update wave state and enemy spawning"""
        if not self.wave_active:
            return
            
        # Stop everything if player is dead - INCLUDING TIMER
        if not player_alive:
            print("🛑 Player dead - wave timer and spawning stopped")
            return
            
        # Update wave timer only if player is alive
        self.wave_timer -= 1
        
        # Check wave completion - time-based only
        if self.wave_timer <= 0:
            self.complete_wave()
            return
            
        # Handle continuous enemy spawning only if player is alive
        self.update_enemy_spawning(enemies_group, all_sprites_group)
    
    def update_enemy_spawning(self, enemies_group, all_sprites_group):
        """Handle continuous enemy spawning for the current wave"""
        # Don't spawn if too many enemies on screen
        current_enemies = len(enemies_group)
        if current_enemies >= self.max_enemies_on_screen:
            return
            
        # Update spawn timer
        self.spawn_timer += 1
        
        # Check if it's time to spawn
        spawn_delay = self.spawn_interval + random.randint(-self.spawn_variance, self.spawn_variance)
        if self.spawn_timer >= spawn_delay:
            self.spawn_wave_enemy(enemies_group, all_sprites_group)
            self.spawn_timer = 0
    
    def spawn_wave_enemy(self, enemies_group, all_sprites_group):
        """Spawn an enemy that will enter the player's view"""
        wave_data = self.wave_compositions[self.current_wave]
        enemy_types = wave_data['enemies']
        
        # Choose random enemy type from wave composition
        enemy_type = random.choice(enemy_types)
        
        # Choose spawn location ensuring enemy enters screen
        spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
        
        # Spawn positions that guarantee screen entry
        if spawn_side == 'top':
            x = random.randint(100, SCREEN_WIDTH - 100)  # Avoid extreme edges
            y = -60  # Start above screen
            direction = 'down'
        elif spawn_side == 'bottom':
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = SCREEN_HEIGHT + 60  # Start below screen
            direction = 'up'
        elif spawn_side == 'left':
            x = -60  # Start left of screen
            y = random.randint(100, SCREEN_HEIGHT - 100)  # Avoid extreme edges
            direction = 'right'
        else:  # right
            x = SCREEN_WIDTH + 60  # Start right of screen
            y = random.randint(100, SCREEN_HEIGHT - 100)
            direction = 'left'
        
        # Create enemy
        from enemy import Enemy
        enemy = Enemy(enemy_type, x, y, direction)
        enemies_group.add(enemy)
        all_sprites_group.add(enemy)
        
        self.enemies_spawned += 1
        print(f"🚀 Spawned {enemy_type} for wave {self.current_wave} (#{self.enemies_spawned}) from {spawn_side}")
    
    def enemy_destroyed(self):
        """Call when an enemy is destroyed"""
        if self.wave_active:
            self.enemies_destroyed += 1
    
    def complete_wave(self):
        """Complete the current wave"""
        self.wave_active = False
        self.wave_complete = True
        
        print(f"✅ Wave {self.current_wave} completed!")
        print(f"   Duration: {self.wave_compositions[self.current_wave]['duration']} seconds")
        print(f"   Enemies spawned: {self.enemies_spawned}")
        print(f"   Enemies destroyed: {self.enemies_destroyed}")
    
    def fail_wave(self):
        """Fail the current wave (not used in continuous mode, but kept for compatibility)"""
        self.wave_active = False
        self.wave_failed = True
        
        print(f"❌ Wave {self.current_wave} failed!")
        print(f"   Enemies destroyed: {self.enemies_destroyed}")
    
    def next_wave(self):
        """Advance to the next wave"""
        if self.wave_complete:
            next_wave = self.current_wave + 1
            if next_wave <= self.max_waves:
                return self.start_wave_intro(next_wave)
            else:
                self.story_complete = True
                print("🏆 All waves completed! Prepare for boss battle!")
                return False
        return False
    
    def restart_wave(self):
        """Restart the current wave"""
        return self.start_wave_intro(self.current_wave)
    
    def get_wave_info(self):
        """Get current wave information"""
        if self.current_wave in self.wave_compositions:
            wave_data = self.wave_compositions[self.current_wave]
            return {
                'wave_number': self.current_wave,
                'description': wave_data['description'],
                'enemies_spawned': self.enemies_spawned,
                'enemies_destroyed': self.enemies_destroyed,
                'time_remaining': max(0, self.wave_timer / 60.0),
                'wave_duration': wave_data['duration'],
                'wave_active': self.wave_active,
                'wave_complete': self.wave_complete,
                'wave_failed': self.wave_failed,
                'wave_intro_active': self.wave_intro_active,
                'story_complete': self.story_complete,
                'spawn_rate': f"Every {wave_data['spawn_interval']/60:.1f}s"
            }
        return None
    
    def get_progress_percentage(self):
        """Get wave progress as percentage (time-based)"""
        if hasattr(self, 'wave_duration') and self.wave_duration > 0:
            time_elapsed = self.wave_duration - self.wave_timer
            return min(100, (time_elapsed / self.wave_duration) * 100)
        return 0
    
    def get_time_percentage(self):
        """Get time remaining as percentage"""
        if self.wave_duration > 0:
            return max(0, (self.wave_timer / self.wave_duration) * 100)
        return 0
