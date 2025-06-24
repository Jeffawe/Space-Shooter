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
        
        # Wave timing
        self.wave_timer = 0
        self.wave_duration = 0  # Set per wave
        
        # Enemy tracking
        self.enemies_required = 0
        self.enemies_destroyed = 0
        self.enemies_spawned = 0
        self.max_enemies_on_screen = 8  # Limit concurrent enemies
        
        # Wave composition definitions
        self.wave_compositions = {
            1: {
                'enemies': ['fighter1'],
                'count': 8,
                'duration': 60,  # 60 seconds
                'description': "Training Wave - Basic Fighters"
            },
            2: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'count': 12,
                'duration': 75,
                'description': "Mixed Squadron"
            },
            3: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'count': 15,
                'duration': 80,
                'description': "Heavy Patrol"
            },
            4: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'count': 18,
                'duration': 85,
                'description': "Advanced Formation"
            },
            5: {
                'enemies': ['fighter1', 'fighter2', 'gunship'],
                'count': 20,
                'duration': 90,
                'description': "Elite Squadron"
            },
            6: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship'],
                'count': 22,
                'duration': 95,
                'description': "New Threat Detected"
            },
            7: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'count': 25,
                'duration': 100,
                'description': "Pirate Raid"
            },
            8: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'count': 28,
                'duration': 105,
                'description': "Full Assault"
            },
            9: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'count': 30,
                'duration': 110,
                'description': "Final Defense"
            },
            10: {
                'enemies': ['fighter1', 'fighter2', 'gunship', 'crabship', 'pirate'],
                'count': 35,
                'duration': 120,
                'description': "Last Stand"
            }
        }
        
        # Spawning control
        self.spawn_timer = 0
        self.spawn_interval = 90  # Base spawn interval (1.5 seconds)
        self.spawn_variance = 30  # Random variance in spawn timing
        
        print("🌊 Wave Manager initialized - Story Mode ready!")
        
    def start_wave(self, wave_number):
        """Start a specific wave"""
        if wave_number > self.max_waves:
            self.story_complete = True
            print("🏆 All waves completed! Boss battle time!")
            return False
            
        self.current_wave = wave_number
        wave_data = self.wave_compositions[wave_number]
        
        # Set wave parameters
        self.enemies_required = wave_data['count']
        self.wave_duration = wave_data['duration'] * 60  # Convert to frames (60 FPS)
        self.wave_timer = self.wave_duration
        
        # Reset counters
        self.enemies_destroyed = 0
        self.enemies_spawned = 0
        self.spawn_timer = 0
        
        # Set wave state
        self.wave_active = True
        self.wave_complete = False
        self.wave_failed = False
        
        # Adjust spawn rate based on wave difficulty
        base_interval = 90
        self.spawn_interval = max(30, base_interval - (wave_number * 5))  # Faster spawning in later waves
        
        print(f"🌊 Wave {wave_number} started: {wave_data['description']}")
        print(f"   Objective: Destroy {self.enemies_required} enemies in {wave_data['duration']} seconds")
        print(f"   Enemy types: {', '.join(wave_data['enemies'])}")
        
        return True
    
    def update(self, enemies_group, all_sprites_group):
        """Update wave state and enemy spawning"""
        if not self.wave_active:
            return
            
        # Update wave timer
        self.wave_timer -= 1
        
        # Check wave completion conditions
        if self.enemies_destroyed >= self.enemies_required:
            self.complete_wave()
            return
            
        # Check wave failure conditions
        if self.wave_timer <= 0:
            self.fail_wave()
            return
            
        # Handle enemy spawning
        self.update_enemy_spawning(enemies_group, all_sprites_group)
    
    def update_enemy_spawning(self, enemies_group, all_sprites_group):
        """Handle spawning enemies for the current wave"""
        # Don't spawn if we've spawned enough enemies or too many on screen
        current_enemies = len(enemies_group)
        if (self.enemies_spawned >= self.enemies_required or 
            current_enemies >= self.max_enemies_on_screen):
            return
            
        # Update spawn timer
        self.spawn_timer += 1
        
        # Check if it's time to spawn
        spawn_delay = self.spawn_interval + random.randint(-self.spawn_variance, self.spawn_variance)
        if self.spawn_timer >= spawn_delay:
            self.spawn_wave_enemy(enemies_group, all_sprites_group)
            self.spawn_timer = 0
    
    def spawn_wave_enemy(self, enemies_group, all_sprites_group):
        """Spawn an enemy based on current wave composition"""
        wave_data = self.wave_compositions[self.current_wave]
        enemy_types = wave_data['enemies']
        
        # Choose random enemy type from wave composition
        enemy_type = random.choice(enemy_types)
        
        # Choose spawn location and direction
        spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if spawn_side == 'top':
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = -50
            direction = 'down'
        elif spawn_side == 'bottom':
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = SCREEN_HEIGHT + 50
            direction = 'up'
        elif spawn_side == 'left':
            x = -50
            y = random.randint(50, SCREEN_HEIGHT - 50)
            direction = 'right'
        else:  # right
            x = SCREEN_WIDTH + 50
            y = random.randint(50, SCREEN_HEIGHT - 50)
            direction = 'left'
        
        # Create enemy
        from enemy import Enemy
        enemy = Enemy(enemy_type, x, y, direction)
        enemies_group.add(enemy)
        all_sprites_group.add(enemy)
        
        self.enemies_spawned += 1
        print(f"🚀 Spawned {enemy_type} for wave {self.current_wave} ({self.enemies_spawned}/{self.enemies_required})")
    
    def enemy_destroyed(self):
        """Call when an enemy is destroyed"""
        if self.wave_active:
            self.enemies_destroyed += 1
            print(f"💥 Enemy destroyed! Progress: {self.enemies_destroyed}/{self.enemies_required}")
    
    def complete_wave(self):
        """Complete the current wave"""
        self.wave_active = False
        self.wave_complete = True
        
        print(f"✅ Wave {self.current_wave} completed!")
        print(f"   Enemies destroyed: {self.enemies_destroyed}/{self.enemies_required}")
        print(f"   Time remaining: {self.wave_timer/60:.1f} seconds")
    
    def fail_wave(self):
        """Fail the current wave"""
        self.wave_active = False
        self.wave_failed = True
        
        print(f"❌ Wave {self.current_wave} failed!")
        print(f"   Time expired! Only destroyed {self.enemies_destroyed}/{self.enemies_required} enemies")
    
    def next_wave(self):
        """Advance to the next wave"""
        if self.wave_complete:
            next_wave = self.current_wave + 1
            if next_wave <= self.max_waves:
                return self.start_wave(next_wave)
            else:
                self.story_complete = True
                print("🏆 All waves completed! Prepare for boss battle!")
                return False
        return False
    
    def restart_wave(self):
        """Restart the current wave"""
        return self.start_wave(self.current_wave)
    
    def get_wave_info(self):
        """Get current wave information"""
        if self.current_wave in self.wave_compositions:
            wave_data = self.wave_compositions[self.current_wave]
            return {
                'wave_number': self.current_wave,
                'description': wave_data['description'],
                'enemies_destroyed': self.enemies_destroyed,
                'enemies_required': self.enemies_required,
                'time_remaining': max(0, self.wave_timer / 60.0),
                'wave_active': self.wave_active,
                'wave_complete': self.wave_complete,
                'wave_failed': self.wave_failed,
                'story_complete': self.story_complete
            }
        return None
    
    def get_progress_percentage(self):
        """Get wave progress as percentage"""
        if self.enemies_required > 0:
            return min(100, (self.enemies_destroyed / self.enemies_required) * 100)
        return 0
    
    def get_time_percentage(self):
        """Get time remaining as percentage"""
        if self.wave_duration > 0:
            return max(0, (self.wave_timer / self.wave_duration) * 100)
        return 0
