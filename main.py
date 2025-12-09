"""
Anna AI Assistant - Main Entry Point (GUI + Voice)
Orchestrates GUI and voice interface with automation
"""

import sys
import threading
from gui_interface import initialize_gui
from voice_interface import initialize_voice
from anna_brain import anna_brain
from automation_engine import automation_engine
from safety import safety
from config import config
from memory import memory
from logger import logger


class Anna:
    """Main Anna orchestrator with GUI and Voice"""
    
    def __init__(self):
        self.gui = None
        self.voice = None
        self.awaiting_pin = False
        self.running = False
    
    def setup_first_run(self):
        """Setup wizard for first run"""
        import tkinter as tk
        from tkinter import simpledialog, messagebox
        
        # Create temporary window for setup
        root = tk.Tk()
        root.withdraw()
        
        messagebox.showinfo(
            "Anna First Run Setup",
            "Welcome to Anna! Let's set up your security PIN.\n\n"
            "This PIN will be required for dangerous actions like:\n"
            "- Deleting files\n"
            "- System shutdown\n"
            "- Modifying system settings"
        )
        
        while True:
            pin1 = simpledialog.askstring("Set PIN", "Enter a security PIN (min 4 characters):", show='*')
            if not pin1 or len(pin1) < 4:
                messagebox.showerror("Error", "PIN must be at least 4 characters")
                continue
            
            pin2 = simpledialog.askstring("Confirm PIN", "Confirm your PIN:", show='*')
            
            if pin1 == pin2:
                config.set_pin(pin1)
                messagebox.showinfo("Success", "PIN set successfully!")
                break
            else:
                messagebox.showerror("Error", "PINs don't match. Try again.")
        
        # API Key check
        if not config.gemini_api_key:
            messagebox.showwarning(
                "API Key Missing",
                "No Gemini API key found in .env file.\n\n"
                "Please add your GEMINI_API_KEY to the .env file.\n"
                "Get a key from: https://makersuite.google.com/app/apikey"
            )
        
        root.destroy()
    
    def start(self):
        """Start Anna with GUI and Voice"""
        # First run setup
        if config.is_first_run():
            self.setup_first_run()
        
        # Initialize GUI
        self.gui = initialize_gui(callback=self.handle_user_input)
        
        # Initialize and start voice interface
        self.voice = initialize_voice(callback=self.handle_voice_command)
        if self.voice and self.voice.start():
            self.gui.update_status("Voice active - Say 'Hey Anna' anytime", 'listening')
            self.gui.voice_active = True
            self.gui.voice_button.config(bg='#4caf50', text="🎤 Listening...")
        else:
            self.gui.update_status("Voice unavailable - Install PyAudio for voice control", 'normal')
            self.gui.voice_button.config(state='disabled', text="🎤 Voice N/A")
            self.gui.add_message("System", 
                               "Voice input not available. Install PyAudio to enable 'Hey Anna' wake word.", 
                               'system')
        
        self.running = True
        
        # Run GUI (blocking)
        logger.log_action("anna_started", "GUI+Voice", True)
        self.gui.run()
    
    def handle_user_input(self, user_input):
        """Handle text input from GUI"""
        try:
            # Handle file upload
            if user_input.startswith("UPLOAD_FILE:"):
                file_path = user_input.replace("UPLOAD_FILE:", "")
                self.handle_file_upload(file_path)
                return
            
            # Handle special commands
            if self.handle_special_commands(user_input):
                return
            
            # Handle PIN input if awaiting
            if self.awaiting_pin:
                self.handle_pin_input(user_input)
                return
            
            # Update status
            self.gui.update_status("Processing...", 'processing')
            
            # Process with Anna's brain
            result = anna_brain.process(user_input)
            
            # Display Anna's response
            if result["response"]:
                self.gui.add_message("Anna", result["response"], 'anna')
                # Also speak if voice is active and available
                if self.voice and hasattr(self.voice, 'available') and self.voice.available:
                    threading.Thread(target=self.voice.speak, args=(result["response"],), daemon=True).start()
            
            # Execute action if present
            if result["action"] and result["action"].get("action") != "none":
                self.execute_action(user_input, result["action"], result["needs_pin"])
            
            # Check if user provided a file path (auto-learning)
            self._check_and_save_path(user_input, result["response"])
            
            # Save to memory
            memory.add_exchange(user_input, result["response"], result["action"])
            
            # Reset status
            self.gui.update_status("Ready to assist", 'normal')
            
        except Exception as e:
            self.gui.add_message("System", f"Error: {str(e)}", 'error')
            logger.log_error("HANDLE_INPUT", str(e), user_input)
            self.gui.update_status("Error occurred", 'error')
    
    def _check_and_save_path(self, user_input, anna_response):
        """Check if user provided a path and save it automatically"""
        import os
        from app_launcher import app_launcher
        
        # Check if input looks like a file path
        if ':\\' in user_input or user_input.endswith('.exe'):
            # Extract app name from history if Anna just said she doesn't know where something is
            recent = memory.get_recent_context(2)
            if recent and len(recent) >= 1:
                last_interaction = recent[-1]
                anna_msg = last_interaction.get('anna', '').lower()
                
                # Check if Anna said she doesn't know where an app is
                if "don't know where" in anna_msg or "tell me the path" in anna_msg:
                    # Try to extract app name from Anna's message
                    # Example: "I don't know where chrome is"
                    import re
                    match = re.search(r"where\s+(\w+)\s+is", anna_msg)
                    if match:
                        app_name = match.group(1)
                        
                        # Verify the path exists
                        if os.path.exists(user_input):
                            # Save the app
                            from config import config
                            config.learn_app(app_name, user_input)
                            logger.log_action("auto_learn_app", f"{app_name}: {user_input}", True)
                            self.gui.add_message("System", f"✓ Saved {app_name} path for future use", 'system')
    
    def handle_file_upload(self, file_path):
        """Handle file upload and document processing"""
        from document_processor import document_processor
        
        try:
            self.gui.update_status(f"Processing document...", 'processing')
            
            # Process the document
            result = document_processor.process_file(file_path)
            
            if result["success"]:
                # Save to memory
                memory.add_document(result["data"])
                
                # Show summary
                doc_data = result["data"]
                filename = doc_data["filename"]
                summary = doc_data["summary"]
                
                self.gui.add_message("System", f"✓ Learned from {filename}", 'system')
                self.gui.add_message("Anna", f"I've read and learned from {filename}. Here's what I understand:\\n\\n{summary}", 'anna')
                
                # Speak if voice available
                if self.voice and hasattr(self.voice, 'available') and self.voice.available:
                    threading.Thread(target=self.voice.speak, args=(f"I've learned from {filename}",), daemon=True).start()
                
                logger.log_action("document_learned", filename, True)
            else:
                self.gui.add_message("System", f"✗ {result['message']}", 'error')
            
            self.gui.update_status("Ready to assist", 'normal')
            
        except Exception as e:
            self.gui.add_message("System", f"✗ Error processing file: {str(e)}", 'error')
            logger.log_error("FILE_UPLOAD", str(e), file_path)
            self.gui.update_status("Error occurred", 'error')
    
    def handle_voice_command(self, voice_input):
        """Handle voice command"""
        # Display voice command in GUI
        self.gui.add_message("You", f"🎤 {voice_input}", 'user')
        
        # Process same as text input
        self.handle_user_input(voice_input)
    
    def execute_action(self, user_input, action_data, needs_pin):
        """Execute an action"""
        try:
            # Check if PIN required
            if needs_pin:
                self.gui.add_message("System", "⚠️ This action requires PIN confirmation", 'system')
                if self.voice:
                    self.voice.speak("This action requires your PIN for confirmation")
                
                safety.request_pin_confirmation(user_input, action_data)
                self.awaiting_pin = True
                
                # Get PIN via dialog
                import tkinter as tk
                from tkinter import simpledialog
                pin = simpledialog.askstring("PIN Required", "Enter your PIN:", show='*')
                if pin:
                    self.handle_pin_input(pin)
                else:
                    self.gui.add_message("System", "Action cancelled", 'system')
                    safety.clear_pending_action()
                    self.awaiting_pin = False
                return
            
            # Display action
            action_type = action_data.get("action", "unknown")
            target = action_data.get("target", "")
            self.gui.add_action(action_type, target)
            
            # Execute
            result = automation_engine.execute(action_data)
            
            # Display result
            if result:
                self.gui.add_result(result.get("success", False), result.get("message", ""))
            
        except Exception as e:
            self.gui.add_message("System", f"Error: {str(e)}", 'error')
            logger.log_error("EXECUTE_ACTION", str(e), str(action_data))
    
    def handle_pin_input(self, pin_input):
        """Handle PIN verification"""
        pin_result = safety.verify_pin(pin_input)
        
        if pin_result == "LOCKED":
            self.gui.add_message("System", "❌ Too many failed attempts. Action cancelled.", 'error')
            if self.voice:
                self.voice.speak("Too many failed attempts. Action cancelled.")
            safety.clear_pending_action()
            self.awaiting_pin = False
            return
        
        if not pin_result:
            self.gui.add_message("System", "❌ Incorrect PIN", 'error')
            return
        
        # PIN correct
        self.gui.add_message("System", "✓ PIN verified", 'system')
        if self.voice:
            self.voice.speak("PIN verified")
        
        pending = safety.get_pending_action()
        if pending:
            action_data = pending["action"]
            action_type = action_data.get("action", "unknown")
            target = action_data.get("target", "")
            self.gui.add_action(action_type, target)
            
            result = automation_engine.execute(action_data)
            if result:
                self.gui.add_result(result.get("success", False), result.get("message", ""))
        
        self.awaiting_pin = False
    
    def handle_special_commands(self, user_input):
        """Handle special commands"""
        cmd = user_input.lower().strip()
        
        if cmd in ["exit", "quit", "close"]:
            self.gui.add_message("Anna", "Goodbye! Have a great day!", 'anna')
            if self.voice:
                self.voice.speak("Goodbye!")
                self.voice.stop()
            self.gui.quit()
            return True
        
        elif cmd == "status":
            status_text = (
                f"API Key: {'✓' if config.gemini_api_key else '✗'}\n"
                f"Voice: {'✓ Active' if self.voice and self.voice.is_running() else '✗ Inactive'}\n"
                f"Learned Apps: {len(config.settings.get('learned_apps', {}))}\n"
                f"Learned Games: {len(config.settings.get('learned_games', {}))}"
            )
            self.gui.add_message("System", status_text, 'system')
            return True
        
        elif cmd == "clear":
            # Can't clear in this GUI, but acknowledge
            self.gui.add_message("System", "Chat history is persistent in this session", 'system')
            return True
        
        return False


def main():
    """Main entry point"""
    try:
        anna = Anna()
        anna.start()
    except Exception as e:
        print(f"Fatal error: {e}")
        logger.log_error("FATAL", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
