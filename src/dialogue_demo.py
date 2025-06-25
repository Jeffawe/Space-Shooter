#!/usr/bin/env python3
"""
Demo the dialogue system
"""
import pygame
from game import Game
from constants import *

def demo_dialogue_system():
    """Demo the complete dialogue system"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("💬 DIALOGUE SYSTEM DEMO")
    print("Testing complete story dialogue integration")
    
    print("\n💬 Dialogue System Features:")
    print("  🎬 Opening Dialogue:")
    print("    • 23-line conversation between Operator, Pilot, and Duke")
    print("    • Sets up the story context and mission")
    print("    • Professional dialogue box at bottom of screen")
    print("  🌊 Wave-Based Dialogues:")
    print("    • After Wave 1: Victory celebration")
    print("    • After Wave 7: Strategic update")
    print("    • After Wave 10: Final battle preparation")
    print("  💀 Failure Dialogue:")
    print("    • Dramatic failure sequence if wave timer expires")
    print("    • Emotional farewell from Duke")
    
    print("\n🎮 Dialogue Controls:")
    print("  SPACE/ENTER - Advance dialogue")
    print("  ESC - Skip current dialogue")
    print("  Game controls disabled during dialogue")
    
    print("\n🎨 Visual Features:")
    print("  📦 Professional dialogue box at screen bottom")
    print("  🎭 Character-specific colors:")
    print("    • Operator: Light Green")
    print("    • Pilot: Light Yellow") 
    print("    • Duke: Light Red")
    print("  📝 Word-wrapped text with proper formatting")
    print("  ⏱️ Auto-advance for silent lines (...)")
    
    print("\n🎬 Story Sequence:")
    print("  1. Opening dialogue (23 lines)")
    print("  2. Wave 1 introduction")
    print("  3. Post-wave 1 dialogue")
    print("  4. Continue through waves...")
    print("  5. Epic finale dialogue after wave 10")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    dialogue_events = []
    
    while game.running and frame_count < 3600:  # 60 seconds max
        # Handle events
        game.handle_events()
        
        # Track dialogue events
        if game.dialogue_system.is_active():
            current_speaker = game.dialogue_system.get_current_speaker()
            current_text = game.dialogue_system.get_current_text()
            
            if current_speaker and current_text:
                event_key = f"{current_speaker}:{current_text[:20]}..."
                if event_key not in dialogue_events:
                    dialogue_events.append(event_key)
                    print(f"💬 {current_speaker.upper()}: {current_text}")
        
        game.update()
        game.draw()
        
        # Capture screenshots at key moments
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/dialogue_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            dialogue_active = game.dialogue_system.is_active()
            current_speaker = game.dialogue_system.get_current_speaker()
            
            print(f"\nFrame {frame_count}:")
            print(f"  Dialogue Active: {'Yes' if dialogue_active else 'No'}")
            if dialogue_active and current_speaker:
                print(f"  Current Speaker: {current_speaker}")
                print(f"  Line: {game.dialogue_system.current_line_index + 1}")
            
            wave_info = game.wave_manager.get_wave_info()
            if wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"  Game State: Wave {wave_info['wave_number']} Intro")
                elif wave_info.get('wave_active', False):
                    print(f"  Game State: Wave {wave_info['wave_number']} Active")
                elif wave_info.get('wave_complete', False):
                    print(f"  Game State: Wave {wave_info['wave_number']} Complete")
            else:
                print(f"  Game State: Pre-game (dialogue phase)")
            
            print(f"  Screenshot: {screenshot_path}")
        
        frame_count += 1
    
    print("\n✅ Dialogue system demo completed!")
    print(f"💬 Dialogue Events Captured: {len(dialogue_events)}")
    
    print("\n🎬 Dialogue System Features Demonstrated:")
    print("   💬 Professional dialogue box presentation")
    print("   🎭 Character-specific speaker colors")
    print("   📝 Word-wrapped text with proper formatting")
    print("   ⌨️ Intuitive dialogue progression controls")
    print("   🎮 Game control lockout during dialogue")
    print("   ⏱️ Auto-advance for dramatic pauses")
    print("   🌊 Wave-integrated story progression")
    
    print("\n🚀 Story Experience Transformation:")
    print("   Before: Pure arcade action without context")
    print("   After: Cinematic story-driven campaign")
    print("   🎬 Professional dialogue presentation")
    print("   📖 Rich narrative context and character development")
    print("   🎯 Clear mission objectives and story motivation")
    print("   ⚡ Seamless integration with wave progression")
    
    pygame.quit()

if __name__ == "__main__":
    demo_dialogue_system()
