# Space Shooter - Amazon Build Challenge

A retro-style space shooter game built with Python and Pygame for the Amazon Build Challenge.

## 🎮 Game Features

- **Player Movement**: Smooth 8-directional movement with tilt animations
- **Sprite Animation**: Dynamic player ship tilting based on movement direction
- **Retro Graphics**: Classic pixel art style space shooter aesthetics
- **Responsive Controls**: WASD or Arrow Keys for movement

## 🚀 Current Status

✅ **Player System Complete**
- Sprite sheet cutting and animation system
- Smooth movement with screen boundaries
- Dynamic tilt animations (left/center/right)

🔄 **In Development**
- Player shooting mechanics
- Enemy ships and AI
- Collision detection
- Sound effects and music
- Background scrolling

## 📁 Project Structure

```
Space-Shooter/
├── src/                 # Source code
│   ├── main.py         # Game entry point
│   ├── game.py         # Main game class
│   ├── player.py       # Player class with animations
│   └── constants.py    # Game constants
├── assets/             # Game assets
│   ├── images/         # Sprites, backgrounds, UI elements
│   ├── sounds/         # Sound effects and music
│   └── fonts/          # Custom fonts
├── SpaceShooter/       # Original asset collection
├── docs/               # Documentation
├── tests/              # Test files
└── README.md           # This file
```

## 🛠️ Getting Started

### Prerequisites
- Python 3.12+
- pygame 2.5.2+

### Installation
```bash
# Clone the repository
git clone https://github.com/Jeffawe/Space-Shooter.git
cd Space-Shooter

# Install pygame (if not already installed)
pip3 install pygame

# Run the game
cd src
python3 main.py
```

### Controls
- **Movement**: Arrow Keys or WASD
- **Quit**: ESC key

## 🏆 Amazon Build Challenge

This project is being developed as part of the Amazon Build Challenge, showcasing:
- Clean code architecture
- Game development with Python/Pygame
- Asset management and sprite animation
- Version control with Git/GitHub

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Amazon Build Challenge**
