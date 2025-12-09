"""
Anna AI Assistant - Configuration Management
Handles user settings, PIN storage, app paths, and preferences
"""

import json
import hashlib
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Anna configuration manager"""
    
    def __init__(self):
        load_dotenv()
        
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / "anna_config.json"
        self.settings = self._load_config()
        
        # Environment variables
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.enable_voice = os.getenv("ENABLE_VOICE", "false").lower() == "true"
        self.enable_debug = os.getenv("ENABLE_DEBUG_MODE", "false").lower() == "true"
        self.enable_logging = os.getenv("ENABLE_ACTION_LOGGING", "true").lower() == "true"
        self.default_personality = os.getenv("DEFAULT_PERSONALITY", "adaptive")
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self._default_config()
    
    def _default_config(self):
        """Return default configuration"""
        return {
            "pin_hash": "",
            "first_run": True,
            "learned_apps": {
                # Common Windows apps
                "notepad": "notepad.exe",
                "chrome": "chrome.exe",
                "edge": "msedge.exe",
                "firefox": "firefox.exe",
                "explorer": "explorer.exe",
                "calculator": "calc.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
            },
            "learned_games": {},
            "learned_documents": {},
            "preferences": {
                "personality": "adaptive",
                "voice_enabled": False,
                "auto_confirm_safe_actions": True,
            },
            "memory": {
                "conversation_history": [],
                "user_context": {}
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def hash_pin(self, pin):
        """Hash PIN using SHA-256"""
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def set_pin(self, pin):
        """Set user PIN (hashed)"""
        self.settings["pin_hash"] = self.hash_pin(pin)
        self.settings["first_run"] = False
        self.save_config()
    
    def verify_pin(self, pin):
        """Verify PIN against stored hash"""
        if not self.settings["pin_hash"]:
            return False
        return self.hash_pin(pin) == self.settings["pin_hash"]
    
    def is_first_run(self):
        """Check if this is the first run"""
        return self.settings.get("first_run", True)
    
    def learn_app(self, name, path):
        """Learn new application path"""
        self.settings["learned_apps"][name.lower()] = path
        self.save_config()
    
    def learn_game(self, name, path):
        """Learn new game path"""
        self.settings["learned_games"][name.lower()] = path
        self.save_config()
    
    def get_app_path(self, name):
        """Get application path by name"""
        return self.settings["learned_apps"].get(name.lower())
    
    def get_game_path(self, name):
        """Get game path by name"""
        return self.settings["learned_games"].get(name.lower())
    
    def add_to_history(self, user_input, anna_response):
        """Add conversation to history"""
        self.settings["memory"]["conversation_history"].append({
            "user": user_input,
            "anna": anna_response
        })
        # Keep only last 50 conversations
        if len(self.settings["memory"]["conversation_history"]) > 50:
            self.settings["memory"]["conversation_history"] = \
                self.settings["memory"]["conversation_history"][-50:]
        self.save_config()
    
    def get_history(self, count=10):
        """Get recent conversation history"""
        history = self.settings["memory"]["conversation_history"]
        return history[-count:] if history else []
    
    def update_context(self, key, value):
        """Update user context"""
        self.settings["memory"]["user_context"][key] = value
        self.save_config()
    
    def get_context(self, key, default=None):
        """Get user context value"""
        return self.settings["memory"]["user_context"].get(key, default)
    
    def save_document(self, name, doc_data):
        """Save a document to learned documents"""
        self.settings["learned_documents"][name] = doc_data
        self.save_config()
    
    def get_document(self, name):
        """Get a document by name"""
        return self.settings["learned_documents"].get(name)
    
    def list_all_documents(self):
        """List all document names"""
        return list(self.settings["learned_documents"].keys())


# Global config instance
config = Config()
