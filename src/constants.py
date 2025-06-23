"""
Game constants for Retro Space Shooter
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 32  # Assuming 32x32 sprites

# Background settings
BACKGROUND_SCROLL_SPEED = 2  # Pixels per frame for background scrolling

# Projectile settings
PROJECTILE_PRIMARY_SPEED = 8    # Speed of primary projectile (Q key)
PROJECTILE_SECONDARY_SPEED = 6  # Speed of secondary projectile (E key)
SHOOTING_COOLDOWN = 10          # Frames between shots (prevents spam)

# Enemy settings
ENEMY_SPAWN_RATE = 120          # Base frames between enemy spawns
ASTEROID_SPAWN_RATE = 180       # Base frames between asteroid spawns
DEBRIS_SPAWN_RATE = 240         # Base frames between debris spawns

# Asset paths
ASSETS_DIR = "../assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
