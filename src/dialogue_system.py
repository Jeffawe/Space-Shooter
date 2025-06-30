#!/usr/bin/env python3
"""
Dialogue System for Space Shooter
Handles story dialogue with professional presentation
"""
import pygame
from constants import *

class DialogueSystem:
    """Manages story dialogue with professional presentation"""
    
    def __init__(self):
        # Dialogue state
        self.active = False
        self.current_dialogue = None
        self.current_line_index = 0
        self.dialogue_complete = False
        self.auto_advance_timer = 0
        self.auto_advance_delay = 180  # 3 seconds at 60 FPS
        
        # Fonts
        self.font_large = pygame.font.Font(None, 28)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        # Dialogue box dimensions
        self.box_height = 120
        self.box_margin = 20
        self.text_margin = 15
        
        # Colors
        self.box_color = (0, 0, 0, 200)  # Semi-transparent black
        self.border_color = (100, 150, 255)  # Blue border
        self.text_color = WHITE
        self.speaker_color = CYAN
        self.continue_color = YELLOW
        
        # Character colors
        self.character_colors = {
            'operator': (150, 255, 150),  # Light green
            'pilot': (255, 255, 150),     # Light yellow
            'Duke': (255, 150, 150),      # Light red
        }
        
        # Dialogue definitions
        self.dialogues = {
            'game_start': [
                {'speaker': 'operator', 'text': 'Can you hear me Pilot?'},
                {'speaker': 'pilot', 'text': "I can! Loud and Clear. I'm in orbit outside Planet Juvar. Requesting permission to land"},
                {'speaker': 'operator', 'text': "Where's the rest of your crew"},
                {'speaker': 'pilot', 'text': "We were attacked just outside Welkor System. I'm the only one that made it out"},
                {'speaker': 'operator', 'text': 'Alright. Permi…. WHAT! No!'},
                {'speaker': 'pilot', 'text': "What's going on?"},
                {'speaker': 'operator', 'text': '…'},
                {'speaker': 'Duke', 'text': '…'},
                {'speaker': 'Duke', 'text': 'Pilot. Are you there'},
                {'speaker': 'pilot', 'text': 'Yes.'},
                {'speaker': 'Duke', 'text': "This is Duke Jennon. I'm in charge of the Manufacturing planet of Juvar!"},
                {'speaker': 'Duke', 'text': "An enemy fleet just made the jump into our orbit. It doesn't make sense how as we're light years away from the nearest enemy base"},
                {'speaker': 'pilot', 'text': "They did the same to my crew in the Welkor system. Caught us off guard. It's new technology"},
                {'speaker': 'Duke', 'text': '… …  *sigh* All of our home pilots are at the Jaftar system helping forces there'},
                {'speaker': 'pilot', 'text': 'What do you need me to do Duke?'},
                {'speaker': 'Duke', 'text': "We've made the call out for reinforcements but they'll take some time to come."},
                {'speaker': 'Duke', 'text': 'The enemy will sends ships to try and weaken the planet shield. We need … We need you to…'},
                {'speaker': 'pilot', 'text': 'I understand Duke.'},
                {'speaker': 'Duke', 'text': "We also have new technology. A ship. A one of a kind ship. Best that'll ever fly the 10 systems. Land at base station 5. I've arranged it to be moved there for you. It should make the battle a bit more even"},
                {'speaker': 'pilot', 'text': 'Ok Duke. Landing at Base Station 5'},
                {'speaker': 'Duke', 'text': 'Thank you Pilot! Juvar and the Empire owe you a lot'},
                {'speaker': 'pilot', 'text': "I'll do my best Duke. Take out as many ships as I can"},
                {'speaker': 'Duke', 'text': "We'll be sending out fuel cells to fuel up the ship and better the ship guns momentarily as well"}
            ],
            'after_wave_1': [
                {'speaker': 'Duke', 'text': 'PILOT!'},
                {'speaker': 'pilot', 'text': 'Hear you loud and clear'},
                {'speaker': 'Duke', 'text': "You're amazing!"},
                {'speaker': 'pilot', 'text': 'Just doing my job!'},
                {'speaker': 'Duke', 'text': "Seems like they have retreated. They'll want to regroup and come back Land at base station, let's get you back up to shape."},
                {'speaker': 'pilot', 'text': 'Alright!'}
            ],
            'after_wave_7': [
                {'speaker': 'Duke', 'text': 'Some of their fleet has moved out of our system. Reinforcements have met up with another force at Kuvirar. Seems like these ones are going to join that battle.'},
                {'speaker': 'pilot', 'text': 'Ok!'},
                {'speaker': 'Duke', 'text': "Finish the remaining ones off. We're winning this!"}
            ],
            'after_wave_10': [
                {'speaker': 'Duke', 'text': "I can't believe you really did this! There's one more. The last fleet sheep. It coming closer. You'll have to take care of it. Reinforcements are winning the battle at Kuvirar! Strength to the Empire. Fight the final battle!"}
            ],
            'wave_failed': [
                {'speaker': 'Duke', 'text': "They got through the defenses. The fleet is coming close. PILOT! You fought a good fight! but it wasn't enough. Fly away and live to fly another day. Juvar will be in the hands of the enemies by Dusk but the Empire will live on and fight. Fight forever. Goodbye Pilot. Take care of the ship!"}
            ]
        }
        
        # print("💬 Dialogue System initialized - Story mode ready!")
    
    def start_dialogue(self, dialogue_key):
        """Start a specific dialogue sequence"""
        if dialogue_key in self.dialogues:
            self.current_dialogue = self.dialogues[dialogue_key]
            self.current_line_index = 0
            self.active = True
            self.dialogue_complete = False
            self.auto_advance_timer = 0
            
            # print(f"💬 Starting dialogue: {dialogue_key}")
            # print(f"   Lines: {len(self.current_dialogue)}")
            return True
        else:
            # print(f"⚠️ Dialogue not found: {dialogue_key}")
            return False
    
    def advance_dialogue(self):
        """Advance to the next line of dialogue"""
        if not self.active or not self.current_dialogue:
            return False
            
        self.current_line_index += 1
        self.auto_advance_timer = 0
        
        if self.current_line_index >= len(self.current_dialogue):
            # Dialogue complete
            self.dialogue_complete = True
            # print("💬 Dialogue sequence completed")
            return False
        else:
            current_line = self.current_dialogue[self.current_line_index]
            # print(f"💬 {current_line['speaker']}: {current_line['text']}")
            return True
    
    def skip_dialogue(self):
        """Skip to the end of current dialogue"""
        if self.active and self.current_dialogue:
            self.current_line_index = len(self.current_dialogue) - 1
            self.dialogue_complete = True
            print("💬 Dialogue skipped")
    
    def close_dialogue(self):
        """Close the dialogue system"""
        self.active = False
        self.current_dialogue = None
        self.current_line_index = 0
        self.dialogue_complete = False
        self.auto_advance_timer = 0
        print("💬 Dialogue closed - ready for next game phase")
    
    def update(self):
        """Update dialogue system (auto-advance timer)"""
        if self.active and not self.dialogue_complete:
            self.auto_advance_timer += 1
            
            # Auto-advance after delay (for silent lines like "...")
            current_line = self.current_dialogue[self.current_line_index]
            if (current_line['text'] in ['…', '...'] and 
                self.auto_advance_timer >= self.auto_advance_delay // 3):  # Faster for silent lines
                self.advance_dialogue()
    
    def handle_input(self, event):
        """Handle input for dialogue progression"""
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.dialogue_complete:
                    self.close_dialogue()
                    return True
                else:
                    self.advance_dialogue()
                    return True
            elif event.key == pygame.K_ESCAPE:
                self.skip_dialogue()
                return True
        
        return False
    
    def draw(self, screen):
        """Draw the dialogue box and current dialogue"""
        if not self.active or not self.current_dialogue:
            return
            
        # Calculate dialogue box position
        box_y = SCREEN_HEIGHT - self.box_height - self.box_margin
        box_rect = pygame.Rect(self.box_margin, box_y, 
                              SCREEN_WIDTH - (self.box_margin * 2), self.box_height)
        
        # Create dialogue box surface with transparency
        dialogue_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        dialogue_surface.fill(self.box_color)
        
        # Draw border
        pygame.draw.rect(dialogue_surface, self.border_color, 
                        (0, 0, box_rect.width, box_rect.height), 3)
        
        # Get current dialogue line
        if self.current_line_index < len(self.current_dialogue):
            current_line = self.current_dialogue[self.current_line_index]
            speaker = current_line['speaker']
            text = current_line['text']
            
            # Speaker name
            speaker_color = self.character_colors.get(speaker, self.speaker_color)
            speaker_surface = self.font_medium.render(f"{speaker.upper()}:", True, speaker_color)
            dialogue_surface.blit(speaker_surface, (self.text_margin, self.text_margin))
            
            # Dialogue text (word wrap)
            text_y = self.text_margin + 30
            max_width = box_rect.width - (self.text_margin * 2)
            
            # Simple word wrapping
            words = text.split(' ')
            lines = []
            current_line_text = ""
            
            for word in words:
                test_line = current_line_text + word + " "
                test_surface = self.font_small.render(test_line, True, self.text_color)
                
                if test_surface.get_width() <= max_width:
                    current_line_text = test_line
                else:
                    if current_line_text:
                        lines.append(current_line_text.strip())
                        current_line_text = word + " "
                    else:
                        lines.append(word)
                        current_line_text = ""
            
            if current_line_text:
                lines.append(current_line_text.strip())
            
            # Draw text lines
            for i, line in enumerate(lines):
                if text_y + (i * 22) < box_rect.height - 30:  # Don't overflow box
                    text_surface = self.font_small.render(line, True, self.text_color)
                    dialogue_surface.blit(text_surface, (self.text_margin, text_y + (i * 22)))
        
        # Draw continue/close instruction
        if self.dialogue_complete:
            instruction = "Press SPACE to close dialogue"
        else:
            instruction = "Press SPACE to continue • ESC to skip"
        
        instruction_surface = self.font_small.render(instruction, True, self.continue_color)
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.bottomright = (box_rect.width - self.text_margin, box_rect.height - self.text_margin)
        dialogue_surface.blit(instruction_surface, instruction_rect)
        
        # Draw dialogue box to screen
        screen.blit(dialogue_surface, box_rect)
    
    def is_active(self):
        """Check if dialogue is currently active"""
        return self.active
    
    def is_complete(self):
        """Check if current dialogue sequence is complete"""
        return self.dialogue_complete
    
    def get_current_speaker(self):
        """Get the current speaker"""
        if (self.active and self.current_dialogue and 
            self.current_line_index < len(self.current_dialogue)):
            return self.current_dialogue[self.current_line_index]['speaker']
        return None
    
    def get_current_text(self):
        """Get the current dialogue text"""
        if (self.active and self.current_dialogue and 
            self.current_line_index < len(self.current_dialogue)):
            return self.current_dialogue[self.current_line_index]['text']
        return None
