"""
Anna AI Assistant - Voice Interface (CORE)
Speech recognition with wake word detection and text-to-speech
"""

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    pyttsx3 = None

import threading
import time
import os
from logger import logger


class VoiceInterface:
    """Voice interface with wake word detection"""
    
    def __init__(self, callback=None):
        # Initialize basic attributes first (always needed)
        self.wake_word = os.getenv("WAKE_WORD", "hey anna").lower()
        self.is_listening = False
        self.listening_thread = None
        self.callback = callback
        self.running = False
        self.awaiting_command = False
        self.available = False
        
        # Check if dependencies are available
        if not SPEECH_RECOGNITION_AVAILABLE or not TTS_AVAILABLE:
            logger.log_error("VOICE_INIT", "Voice dependencies not available", 
                           "Install PyAudio for voice support")
            return
        
        # Speech recognition
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        except Exception as e:
            logger.log_error("VOICE_INIT", "PyAudio not available", str(e))
            return
        
        # Text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Mark as available if we got here
        self.available = True
    
    def setup_tts(self):
        """Configure text-to-speech engine"""
        # Set properties
        self.tts_engine.setProperty('rate', 175)  # Speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0-1)
        
        # Try to set a female voice
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        """Text-to-speech output"""
        if not self.available:
            return  # Silently skip if voice not available
        
        try:
            logger.log_action("tts_speak", text[:50], True)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.log_error("TTS_SPEAK", str(e), text)
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        logger.log_action("wake_word_listening", "started", True)
        
        with self.microphone as source:
            # Adjust for ambient noise once
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while self.running:
            # Skip if we're waiting for a command after wake word
            if self.awaiting_command:
                time.sleep(0.1)
                continue
                
            try:
                with self.microphone as source:
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio).lower()
                    logger.log_debug(f"Heard: {text}")
                    
                    # Check for wake word
                    if self.wake_word in text:
                        logger.log_action("wake_word_detected", text, True)
                        self.on_wake_word_detected()
                    
                except sr.UnknownValueError:
                    # Couldn't understand - ignore
                    pass
                except sr.RequestError as e:
                    logger.log_error("SPEECH_API", str(e))
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                # Timeout - continue listening
                continue
            except Exception as e:
                logger.log_error("WAKE_WORD_LISTEN", str(e))
                time.sleep(1)
    
    def on_wake_word_detected(self):
        """Handle wake word detection"""
        self.speak("Yes?")
        self.awaiting_command = True
        
        # Listen for command
        command = self.listen_for_command()
        
        if command:
            logger.log_action("voice_command", command, True)
            # Call callback with command
            if self.callback:
                self.callback(command)
        
        self.awaiting_command = False
    
    def listen_for_command(self, timeout=5):
        """Listen for a voice command after wake word"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            try:
                command = self.recognizer.recognize_google(audio)
                logger.log_action("command_recognized", command, True)
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return None
            except sr.RequestError as e:
                logger.log_error("COMMAND_RECOGNIZE", str(e))
                self.speak("Sorry, I'm having trouble with my speech recognition.")
                return None
                
        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything.")
            return None
        except Exception as e:
            logger.log_error("LISTEN_COMMAND", str(e))
            return None
    
    def start(self):
        """Start voice interface in background"""
        if not self.available:
            logger.log_error("VOICE_START", "Voice not available", "Missing PyAudio")
            return False
        
        if not self.running:
            self.running = True
            self.listening_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
            self.listening_thread.start()
            logger.log_action("voice_interface", "started", True)
            return True
        return False
    
    def stop(self):
        """Stop voice interface"""
        self.running = False
        if self.listening_thread:
            self.listening_thread.join(timeout=2)
        logger.log_action("voice_interface", "stopped", True)
    
    def is_running(self):
        """Check if voice interface is running"""
        if not self.available:
            return False
        return self.running


# Global voice interface instance
voice_interface = None

def initialize_voice(callback=None):
    """Initialize voice interface"""
    global voice_interface
    try:
        voice_interface = VoiceInterface(callback)
        return voice_interface
    except Exception as e:
        logger.log_error("VOICE_INIT", str(e))
        return None
