# VR Language Learning System
- An immersive language learning application that uses speech recognition and AI-driven avatars to create realistic conversation scenarios.
- Practice your language skills in interactive environments like restaurants, job interviews, and shopping scenarios.

## Features

- **Real-time Speech Recognition**: Converts your speech to text using Google Speech Recognition
- **Text-to-Speech AI Responses**: AI characters respond with natural voice synthesis
- **Interactive Scenarios**: 
  - Restaurant ordering in a French setting
  - Job interview practice
  - Shopping conversations
- **Progress Tracking**: Monitor your grammar, vocabulary, fluency, and contextual appropriateness
- **Instant Feedback**: Get real-time evaluation of your language skills
- **Two Implementations**: Both a Python desktop app and a web browser version


## Requirements
### Python Version
- Python 3.7 or higher
- Windows/macOS/Linux support

### Dependencies
```bash
pip install pygame speechrecognition pyttsx3 pyaudio
```

### Additional Requirements
- **Microphone**: Required for speech input
- **Internet Connection**: Needed for Google Speech Recognition API
- **Audio Output**: Speakers or headphones for AI responses

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/vr-language-learning.git
   cd vr-language-learning
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyAudio** (if installation fails):
   
   **Windows**:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```
   
   **macOS**:
   ```bash
   brew install portaudio
   pip install pyaudio
   ```
   
   **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt-get install python3-pyaudio
   ```

4. **Set up microphone permissions**:
   - **Windows**: Settings > Privacy > Microphone > Allow apps to access microphone
   - **macOS**: System Preferences > Security & Privacy > Microphone
   - **Linux**: Ensure your user is in the audio group

## Usage

### Python Desktop Application

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Choose a scenario**:
   - Press `R` for Restaurant scenario
   - Press `J` for Job Interview scenario
   - Press `S` for Shopping scenario

3. **Start conversing**:
   - Listen to the AI character's initial prompt
   - Press `SPACE` to start speaking
   - Speak clearly into your microphone
   - Receive instant feedback and AI responses

4. **Controls**:
   - `SPACE` - Start listening/responding
   - `R` - Restaurant scenario
   - `J` - Job interview scenario
   - `S` - Shopping scenario
   - `Q` - Quit application

### Web Browser Version

1. **Open `index.html`** in a modern web browser (Chrome, Edge, Firefox)

2. **Grant microphone permissions** when prompted

3. **Use the same controls** as the desktop version

## Scenarios

### Restaurant Scenario
- **Setting**: French restaurant in Paris
- **Character**: Marie - Friendly Waitress
- **Skills**: Ordering food, asking about menu items, polite conversation
- **Vocabulary**: Food, drinks, ordering, payment terms

### Job Interview Scenario
- **Setting**: Marketing position interview
- **Character**: Mr. Johnson - HR Manager
- **Skills**: Professional communication, describing experience, asking questions
- **Vocabulary**: Professional terms, skills, experience, career goals

### Shopping Scenario
- **Setting**: Clothing boutique
- **Character**: Sofia - Shop Assistant
- **Skills**: Shopping conversations, describing preferences, making purchases
- **Vocabulary**: Clothing, sizes, colors, prices, preferences

## Evaluation System

The system evaluates your responses based on:

- **Grammar Score** (0-100%): Sentence structure and grammatical correctness
- **Vocabulary Usage** (0-100%): Variety and appropriateness of words used
- **Fluency** (0-100%): Natural flow and length of responses
- **Context Appropriateness** (0-100%): Relevance to the conversation scenario

### Feedback Examples
- "Good use of complete sentences!"
- "Great use of polite language!"
- "Try to use more detailed responses."
- "Try to respond with phrases relevant to the conversation."

## Troubleshooting

### Speech Recognition Issues

**"Could not understand audio"**:
- Speak more clearly and closer to the microphone
- Reduce background noise
- Check microphone levels in system settings

**"No speech detected"**:
- Ensure the microphone is properly connected
- Check microphone permissions
- Speak within 15 seconds after pressing SPACE

**"Speech recognition service error"**:
- Check internet connection
- Verify Google Speech Recognition API access
- Try restarting the application

### Microphone Setup Issues

**"Microphone not available"**:
- Check the microphone connection
- Verify microphone permissions
- Try selecting a different microphone device

**"Available microphones: 0"**:
- Install audio drivers
- Check Windows audio services
- Restart the audio system

### Performance Issues
**Slow response times**:
- Check internet connection speed
- Close other audio applications
- Reduce system load

**Audio feedback/echo**:
- Use headphones instead of speakers
- Adjust microphone sensitivity
- Increase the distance between the microphone and the speakers

## File Structure

```
vr-language-learning/
├── main.py                 # Python desktop application
├── index.html             # Web browser version
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── screenshots/           # Application screenshots
└── docs/                  # Additional documentation
```

## Technical Details
### Speech Recognition
- Uses Google Speech Recognition API
- Supports multiple languages (configured for English)
- 15-second timeout for speech input
- Automatic ambient noise calibration

### Text-to-Speech
- Python: pyttsx3 engine
- Web: Browser's built-in SpeechSynthesis API
- Configurable speech rate and volume
- Character-specific voice settings

### Conversation Flow
- State-based conversation management
- Context-aware AI responses
- Keyword matching for natural interactions
- Progress tracking across sessions

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-scenario`)
3. Commit your changes (`git commit -am 'Add new scenario'`)
4. Push to the branch (`git push origin feature/new-scenario`)
5. Create a Pull Request

### Adding New Scenarios

To add a new conversation scenario:

1. **Define the scenario** in `main.py` or `index.html`
2. **Add states and responses** following the existing pattern
3. **Include appropriate keywords** for natural conversation flow
4. **Test thoroughly** with various user inputs


## License
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Speech recognition powered by Google Speech Recognition
- Text-to-speech using pyttsx3 and Web Speech API
- UI framework: Pygame for desktop, vanilla JavaScript for web
- Inspired by modern language learning methodologies

---

**Note**: This application requires microphone access and internet connectivity for optimal performance. Ensure your system meets all requirements before installation.
