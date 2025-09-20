import pygame
import speech_recognition as sr
import pyttsx3
import json
import random
import threading
from datetime import datetime
import time
from typing import Dict, List, Optional

class LanguageLearningVR:
    def __init__(self):
        # Initialize pygame for basic graphics
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("VR Language Learning - Interactive Conversation")
        
        # Initialize speech components with better error handling
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS engine
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Initialize microphone with error handling
        self.setup_microphone()
        
        # Conversation state
        self.current_scenario = None
        self.conversation_history = []
        self.user_progress = {"correct_responses": 0, "total_interactions": 0}
        self.is_listening = False
        self.listening_thread = None
        
        # Colors for UI
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 150, 255)
        self.GREEN = (100, 255, 150)
        self.RED = (255, 100, 100)
        self.YELLOW = (255, 255, 100)
        self.PURPLE = (200, 100, 255)
        
        # Font setup
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Load scenarios
        self.scenarios = self.load_scenarios()
        
        # Status messages
        self.status_message = "Ready to start! Press R, J, or S to choose a scenario."
        self.last_user_input = ""
        
    def setup_microphone(self):
        """Setup microphone with proper error handling"""
        try:
            # List available microphones
            mic_list = sr.Microphone.list_microphone_names()
            print(f"Available microphones: {len(mic_list)}")
            for i, name in enumerate(mic_list[:5]):  # Show first 5
                print(f"  {i}: {name}")
            
            # Try to use default microphone
            self.microphone = sr.Microphone()
            
            # Test microphone access
            with self.microphone as source:
                print("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone setup complete!")
                
        except Exception as e:
            print(f"Microphone setup error: {e}")
            print("Please check your microphone permissions and connection.")
            self.microphone = None
        
    def load_scenarios(self) -> Dict:
        """Load predefined conversation scenarios"""
        return {
            "restaurant": {
                "name": "French Restaurant",
                "setting": "You are dining at a French restaurant in Paris",
                "ai_character": "Marie - Friendly Waitress",
                "initial_prompt": "Bonjour! Welcome to Le Petit Café. How may I help you today?",
                "responses": {
                    "menu": "We have excellent pasta dishes, fresh salads, and our famous coq au vin. What would you like to try?",
                    "order": "Excellent choice! Would you like anything to drink with that?",
                    "drink": "Perfect! I'll bring that right out. Anything else for you?",
                    "bill": "Of course! Your total comes to 45 euros. Will you pay by card or cash?",
                    "default": "I see. Is there anything else I can help you with today?"
                }
            },
            "job_interview": {
                "name": "Job Interview",
                "setting": "You are in a job interview for a marketing position",
                "ai_character": "Mr. Johnson - HR Manager",
                "initial_prompt": "Good morning! Please, have a seat. Tell me about yourself.",
                "responses": {
                    "experience": "That's impressive! How do you think that experience would help you in this role?",
                    "skills": "Those are valuable skills. Can you give me a specific example of when you used them?",
                    "company": "Great question! We're a growing company focused on innovation. What interests you most about working here?",
                    "salary": "We offer competitive compensation. What are your salary expectations?",
                    "default": "Interesting. Tell me more about that."
                }
            },
            "shopping": {
                "name": "Clothing Store",
                "setting": "You are shopping for clothes in a boutique",
                "ai_character": "Sofia - Shop Assistant",
                "initial_prompt": "Hello! Looking for anything specific today?",
                "responses": {
                    "looking": "Great! What size are you looking for? We have some beautiful new arrivals.",
                    "size": "Perfect! Would you like to try it on? The fitting room is right over there.",
                    "color": "That color would look lovely on you! We also have it in blue and black.",
                    "price": "This one is 89 euros, but we have a 20% discount today!",
                    "default": "Of course! Let me know if you need any help."
                }
            }
        }
    
    def start_scenario(self, scenario_name: str):
        """Initialize a learning scenario"""
        if scenario_name not in self.scenarios:
            self.status_message = f"Scenario '{scenario_name}' not found!"
            return
        
        self.current_scenario = self.scenarios[scenario_name]
        self.conversation_history = []
        
        # AI speaks the initial prompt
        initial_prompt = self.current_scenario["initial_prompt"]
        self.ai_speak(initial_prompt)
        self.conversation_history.append({
            "speaker": "AI",
            "text": initial_prompt,
            "timestamp": datetime.now()
        })
        
        self.status_message = f"Started {self.current_scenario['name']} scenario. Press SPACE to respond!"
        
    def listen_to_user(self) -> Optional[str]:
        """Capture and transcribe user speech with better error handling"""
        if not self.microphone:
            self.status_message = "Microphone not available. Please check your microphone setup."
            return None
            
        try:
            self.status_message = "🎤 Listening... Please speak clearly!"
            self.is_listening = True
            
            with self.microphone as source:
                print("Listening... Please speak.")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio with longer timeout
                audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=10)
            
            self.status_message = "🔄 Processing speech..."
            self.is_listening = False
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(audio, language='en-US')
                print(f"✅ You said: {text}")
                self.last_user_input = text
                self.status_message = f"You said: {text}"
                return text
            except sr.UnknownValueError:
                # Try with different language
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"✅ You said: {text}")
                    self.last_user_input = text
                    self.status_message = f"You said: {text}"
                    return text
                except:
                    pass
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout - no speech detected")
            self.status_message = "No speech detected. Press SPACE to try again."
        except sr.UnknownValueError:
            print("❌ Could not understand audio - please speak more clearly")
            self.status_message = "Could not understand. Please speak more clearly and try again."
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            self.status_message = "Speech recognition service error. Check internet connection."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.status_message = f"Error: {str(e)}"
        
        self.is_listening = False
        return None
    
    def ai_speak(self, text: str):
        """Convert text to speech for AI responses"""
        print(f"🤖 AI: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def generate_ai_response(self, user_input: str) -> str:
        """Generate contextual AI response"""
        if not self.current_scenario:
            return "Please start a scenario first."
        
        user_input_lower = user_input.lower()
        responses = self.current_scenario["responses"]
        
        # Check for keywords and return appropriate responses
        for keyword, response in responses.items():
            if keyword != "default" and keyword in user_input_lower:
                return response
        
        # Return default response if no keywords match
        return responses["default"]
    
    def evaluate_response(self, user_input: str) -> Dict:
        """Evaluate user's language learning progress"""
        evaluation = {
            "grammar_score": min(95, 70 + len(user_input.split()) * 2),
            "vocabulary_usage": min(90, 60 + len(set(user_input.lower().split())) * 3),
            "fluency": min(85, 65 + (20 if len(user_input) > 20 else 10)),
            "context_appropriateness": random.randint(75, 95),
            "feedback": []
        }
        
        # Add feedback based on input
        if len(user_input.split()) >= 5:
            evaluation["feedback"].append("Good use of complete sentences!")
        if any(word in user_input.lower() for word in ["please", "thank", "sorry", "excuse"]):
            evaluation["feedback"].append("Great use of polite language!")
        if len(user_input) < 10:
            evaluation["feedback"].append("Try to use more detailed responses")
            
        return evaluation
    
    def draw_ui(self):
        """Draw the improved user interface"""
        self.screen.fill(self.WHITE)
        
        # Title with better styling
        title_text = self.large_font.render("🎧 VR Language Learning", True, self.PURPLE)
        title_rect = title_text.get_rect(center=(600, 40))
        self.screen.blit(title_text, title_rect)
        
        # Status message with color coding
        status_color = self.GREEN if "You said:" in self.status_message else self.BLUE
        if "error" in self.status_message.lower() or "could not" in self.status_message.lower():
            status_color = self.RED
        elif self.is_listening:
            status_color = self.YELLOW
            
        status_text = self.font.render(self.status_message, True, status_color)
        status_rect = status_text.get_rect(center=(600, 80))
        self.screen.blit(status_text, status_rect)
        
        # Current scenario info
        if self.current_scenario:
            pygame.draw.rect(self.screen, (240, 248, 255), (50, 120, 500, 80), 0)
            pygame.draw.rect(self.screen, self.BLUE, (50, 120, 500, 80), 2)
            
            scenario_text = self.small_font.render(f"📍 {self.current_scenario['setting']}", True, self.BLACK)
            character_text = self.small_font.render(f"👤 {self.current_scenario['ai_character']}", True, self.BLACK)
            self.screen.blit(scenario_text, (60, 130))
            self.screen.blit(character_text, (60, 160))
        
        # Conversation history with better formatting
        conversation_rect = pygame.Rect(50, 220, 700, 350)
        pygame.draw.rect(self.screen, (248, 248, 248), conversation_rect, 0)
        pygame.draw.rect(self.screen, self.BLACK, conversation_rect, 2)
        
        y_offset = 230
        for entry in self.conversation_history[-10:]:  # Show last 10 messages
            if y_offset > 550:  # Don't overflow
                break
                
            speaker_color = self.GREEN if entry["speaker"] == "You" else self.BLUE
            icon = "🗣️" if entry["speaker"] == "You" else "🤖"
            
            speaker_text = self.small_font.render(f"{icon} {entry['speaker']}:", True, speaker_color)
            self.screen.blit(speaker_text, (60, y_offset))
            
            # Word wrap for long messages
            words = entry['text'].split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if self.small_font.size(test_line)[0] < 620:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            if current_line:
                lines.append(' '.join(current_line))
            
            for line in lines[:2]:  # Max 2 lines per message
                y_offset += 25
                message_text = self.small_font.render(line, True, self.BLACK)
                self.screen.blit(message_text, (80, y_offset))
            
            y_offset += 35
        
        # Progress and evaluation
        progress_rect = pygame.Rect(50, 590, 700, 120)
        pygame.draw.rect(self.screen, (240, 255, 240), progress_rect, 0)
        pygame.draw.rect(self.screen, self.GREEN, progress_rect, 2)
        
        progress_text = self.font.render(f"📊 Progress: {self.user_progress['correct_responses']}/{self.user_progress['total_interactions']} interactions", True, self.BLACK)
        self.screen.blit(progress_text, (60, 600))
        
        if self.last_user_input:
            evaluation = self.evaluate_response(self.last_user_input)
            scores_text = self.small_font.render(f"Grammar: {evaluation['grammar_score']}%  Vocabulary: {evaluation['vocabulary_usage']}%  Fluency: {evaluation['fluency']}%", True, self.BLACK)
            self.screen.blit(scores_text, (60, 640))
            
            if evaluation['feedback']:
                feedback_text = self.small_font.render(f"💡 {evaluation['feedback'][0]}", True, self.GREEN)
                self.screen.blit(feedback_text, (60, 670))
        
        # Control instructions with better layout
        controls_rect = pygame.Rect(780, 120, 400, 450)
        pygame.draw.rect(self.screen, (255, 248, 240), controls_rect, 0)
        pygame.draw.rect(self.screen, self.RED, controls_rect, 2)
        
        controls_title = self.font.render("🎮 Controls", True, self.RED)
        self.screen.blit(controls_title, (790, 130))
        
        instructions = [
            "🎤 SPACE - Start Speaking",
            "🍽️ R - Restaurant Scenario",
            "💼 J - Job Interview",
            "🛍️ S - Shopping Scenario",
            "❌ Q - Quit",
            "",
            "📋 Instructions:",
            "1. Choose a scenario (R/J/S)",
            "2. Listen to AI character",
            "3. Press SPACE to respond",
            "4. Speak clearly into mic",
            "5. Get instant feedback!",
            "",
            "🎯 Tips:",
            "• Speak slowly and clearly",
            "• Use complete sentences",
            "• Be polite and contextual",
            "• Practice regularly!"
        ]
        
        y_pos = 170
        for instruction in instructions:
            color = self.RED if instruction.startswith(("🎤", "🍽️", "💼", "🛍️", "❌")) else self.BLACK
            if instruction == "":
                y_pos += 10
                continue
            inst_text = self.small_font.render(instruction, True, color)
            self.screen.blit(inst_text, (790, y_pos))
            y_pos += 25
        
        # Listening indicator
        if self.is_listening:
            pygame.draw.circle(self.screen, self.RED, (600, 150), 20)
            mic_text = self.font.render("🎤", True, self.WHITE)
            mic_rect = mic_text.get_rect(center=(600, 150))
            self.screen.blit(mic_text, mic_rect)
        
        pygame.display.flip()
    
    def conversation_loop(self):
        """Main conversation interaction loop - runs in separate thread"""
        if not self.current_scenario:
            self.status_message = "Please start a scenario first! (Press R, J, or S)"
            return
        
        user_input = self.listen_to_user()
        if user_input:
            # Add user input to history
            self.conversation_history.append({
                "speaker": "You",
                "text": user_input,
                "timestamp": datetime.now()
            })
            
            # Generate and speak AI response
            ai_response = self.generate_ai_response(user_input)
            
            # Add AI response to history
            self.conversation_history.append({
                "speaker": "AI",
                "text": ai_response,
                "timestamp": datetime.now()
            })
            
            # Speak AI response in separate thread so UI doesn't freeze
            def speak_response():
                self.ai_speak(ai_response)
                self.status_message = "Response complete. Press SPACE to continue conversation."
            
            threading.Thread(target=speak_response, daemon=True).start()
            
            # Update progress
            self.user_progress["total_interactions"] += 1
            evaluation = self.evaluate_response(user_input)
            if evaluation["grammar_score"] > 80:
                self.user_progress["correct_responses"] += 1
    
    def run(self):
        """Main application loop with improved event handling"""
        clock = pygame.time.Clock()
        running = True
        
        print("🎧 VR Language Learning System Started!")
        print("🎯 Choose a scenario to begin learning:")
        print("   R - Restaurant Scenario")
        print("   J - Job Interview Scenario") 
        print("   S - Shopping Scenario")
        print("   SPACE - Start speaking (after choosing scenario)")
        print("   Q - Quit")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("👋 Goodbye! Thanks for learning with us!")
                        running = False
                        
                    elif event.key == pygame.K_r:
                        print("🍽️ Starting Restaurant scenario...")
                        self.start_scenario("restaurant")
                        
                    elif event.key == pygame.K_j:
                        print("💼 Starting Job Interview scenario...")
                        self.start_scenario("job_interview")
                        
                    elif event.key == pygame.K_s:
                        print("🛍️ Starting Shopping scenario...")
                        self.start_scenario("shopping")
                        
                    elif event.key == pygame.K_SPACE:
                        if self.current_scenario and not self.is_listening:
                            # Start conversation in separate thread so UI doesn't freeze
                            if self.listening_thread is None or not self.listening_thread.is_alive():
                                self.listening_thread = threading.Thread(target=self.conversation_loop, daemon=True)
                                self.listening_thread.start()
                        elif not self.current_scenario:
                            self.status_message = "Please choose a scenario first! (Press R, J, or S)"
                        elif self.is_listening:
                            self.status_message = "Already listening... Please speak!"
            
            self.draw_ui()
            clock.tick(60)
        
        pygame.quit()

# Usage example with better error handling
if __name__ == "__main__":
    print("🚀 Starting VR Language Learning System...")
    print("📋 Required packages: pygame, speechrecognition, pyttsx3, pyaudio")
    print("🎤 Make sure your microphone is connected and permissions are granted!")
    
    try:
        app = LanguageLearningVR()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Try installing missing packages: pip install pygame speechrecognition pyttsx3 pyaudio")
        input("Press Enter to exit...")