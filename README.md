# Anna AI Assistant

An advanced locally-running AI assistant for Windows 10/11 with **GUI and Voice Control**. Understands natural language, responds via voice, and executes system automation with "Hey Anna" wake word detection.

## ✨ Key Features

### 🎤 Voice Control (Core Feature)
- **Wake Word Detection**: Say "Hey Anna" anytime to activate
- **Continuous Listening**: Always ready in the background
- **Natural Speech**: Text-to-speech responses
- **Auto-Start**: Launches with Windows, ready immediately

### 🖥️ Modern GUI Interface
- **Dark Theme**: Easy on the eyes
- **Chat Display**: Visual conversation history
- **Real-time Status**: Live indicators for voice and actions
- **Dual Input**: Type or speak your commands

### 🤖 AI-Powered Automation
- **Natural Language**: Just talk naturally
- **Smart Actions**: Opens apps, manages files, controls system
- **Web Integration**: Search, browse, YouTube
- **Learning System**: Remembers what you teach it

### 🔒 Security Features
- **PIN Protection**: Dangerous actions require verification
- **Smart Detection**: Automatically identifies risky operations
- **Audit Logging**: Complete action history

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.11+
- Microphone for voice input
- Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

### Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

3. **Run Anna**:
   ```bash
   python main.py
   ```

4. **First Run Setup**:
   - Set your security PIN
   - Anna will launch with GUI
   - Voice listening starts automatically

5. **Enable Auto-Start** (Optional):
   ```bash
   python auto_start.py enable
   ```

## 💬 Usage

### Voice Commands

Just say **"Hey Anna"** followed by your command:

```
🎤 "Hey Anna"
   "Open Chrome"

🎤 "Hey Anna"  
   "Search Google for Python tutorials"

🎤 "Hey Anna"
   "What's the weather like?"

🎤 "Hey Anna"
   "Volume up"
```

### Text Commands

Type in the GUI input box:
- "Open Notepad"
- "Launch File Explorer"
- "Search YouTube for music"
- "Type hello world"
- "Turn up the volume"

### Teaching Anna

If Anna doesn't know an app:
```
You: Open MyApp
Anna: I don't know where MyApp is. Tell me the path.
You: C:\Program Files\MyApp\app.exe
Anna: Thanks! I'll remember that.
```

## 🎯 Available Actions

| Category | Examples |
|----------|----------|
| **Apps** | "Open Chrome", "Launch Steam" |
| **Files** | "Open Downloads folder", "Find test.txt" |
| **Web** | "Search Google for news", "Go to github.com" |
| **System** | "Volume up", "Brightness 70", "WiFi toggle" |
| **Input** | "Type hello", "Press Ctrl+C", "Click" |
| **Games** | "Launch Minecraft" (launch only, no control) |

## ⚙️ Configuration

### Auto-Start with Windows

```bash
# Enable auto-start
python auto_start.py enable

# Disable auto-start  
python auto_start.py disable

# Check status
python auto_start.py status
```

### Personality Modes

Edit `config/anna_config.json`:
```json
{
  "preferences": {
    "personality": "adaptive"
  }
}
```

Options: `adaptive`, `professional`, `friendly`, `jarvis`

### Voice Settings

Edit `.env`:
```
WAKE_WORD=hey anna
TTS_RATE=175
TTS_VOLUME=0.9
```

## 🔐 Security

### PIN-Protected Actions
These require PIN confirmation:
- Deleting files/folders
- System shutdown/restart
- Running scripts
- Modifying system files

### Logs
All actions logged to `logs/`:
- `actions.log` - Automation actions
- `errors.log` - Error tracking
- `audit.log` - Security events
- `debug.log` - Debug info

## 🛠️ Troubleshooting

### Voice Not Working
1. Check microphone is connected
2. Install PyAudio: `pip install pyaudio`
3. Grant microphone permissions in Windows

### "I'm not properly configured"
- Verify `GEMINI_API_KEY` in `.env`
- Get free API key: https://makersuite.google.com/app/apikey

### App Won't Launch
- Teach Anna the app path
- Use full name (e.g., "chrome.exe")

### GUI Won't Start
- Check tkinter installed: `python -m tkinter`
- Tkinter comes with Python by default

### PIN Forgotten
- Delete `config/anna_config.json`
- Restart Anna for setup wizard

## 📁 Project Structure

```
anna/
├── main.py                 # Main entry (GUI + Voice)
├── gui_interface.py        # Modern GUI
├── voice_interface.py      # Voice with wake word
├── anna_brain.py          # AI interpreter
├── automation_engine.py   # Action dispatcher
├── auto_start.py          # Windows startup manager
├── config.py              # Configuration
├── safety.py              # Security layer
├── [automation modules]   # App, file, web, system, input
└── requirements.txt       # Dependencies
```

## 🎨 Features Demo

### GUI Interface
- **Dark modern theme**
- **Color-coded messages** (You: Green, Anna: Cyan, Actions: Purple)
- **Status indicators** (Ready/Listening/Processing)
- **Voice toggle button** with visual feedback

### Voice Interface
- **Background listening** (runs continuously)
- **Wake word activation** ("Hey Anna")
- **Speech-to-text** for commands
- **Text-to-speech** for responses

## 🔄 Updates

### Version 1.0 (Current)
- ✅ GUI interface with dark theme
- ✅ Voice control with wake word
- ✅ Auto-start capability
- ✅ Full Windows automation
- ✅ PIN security system

### Roadmap
- [ ] Multi-monitor support
- [ ] Custom wake word training
- [ ] Plugin system
- [ ] Mobile companion app

## 📝 Notes

- **Game Control**: Anna launches games but doesn't send in-game inputs (as per original spec)
- **Admin Rights**: Some actions may require admin privileges
- **Network**: Internet required for Gemini API and web searches
- **Microphone**: Always listening when voice is enabled (privacy consideration)

## 🙏 Credits

- [Google Gemini](https://ai.google.dev/) - AI brain
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Automation
- [pyttsx3](https://pyttsx3.readthedocs.io/) - Text-to-speech
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice input

---

**Anna AI Assistant** - Your voice-activated Windows companion 🎤🤖

*Say "Hey Anna" and let the magic begin!*
