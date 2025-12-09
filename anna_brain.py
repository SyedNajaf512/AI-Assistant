"""
Anna AI Assistant - Brain (Command Interpreter)
Natural language processing via Gemini API
"""

import json
import google.generativeai as genai
from config import config
from memory import memory
from safety import safety
from logger import logger


class AnnaBrain:
    """Anna's AI brain for natural language understanding"""
    
    def __init__(self):
        # Configure Gemini
        if config.gemini_api_key:
            genai.configure(api_key=config.gemini_api_key)
            # Use gemini-2.5-flash (confirmed available)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            logger.log_error("GEMINI_CONFIG", "No API key found", "Check .env file")
        
        # Personality modes
        self.personality_prompts = {
            "adaptive": "You adapt your tone: professional for work, friendly for chat, Jarvis-like for system actions.",
            "professional": "You are professional and business-like in all responses.",
            "friendly": "You are warm, friendly, and casual in all responses.",
            "jarvis": "You are like Jarvis from Iron Man - formal, intelligent, and efficient."
        }
    
    def _build_system_prompt(self):
        """Build the system prompt for Anna"""
        personality = config.settings.get("preferences", {}).get("personality", "adaptive")
        personality_style = self.personality_prompts.get(personality, self.personality_prompts["adaptive"])
        
        prompt = f"""You are Anna, an advanced AI assistant running locally on Windows 10/11.

PERSONALITY:
{personality_style}

YOUR TASK:
1. Understand the user's natural language command
2. Decide if it requires an ACTION or is just CONVERSATION
3. Output structured JSON for executable actions, OR respond naturally for conversation

AVAILABLE ACTIONS:
- open_app: Open software (target: app name)
- launch_game: Launch games (target: game name)  
- open_file: Open file (target: file path)
- open_folder: Open folder (target: folder path)
- web_search: Search web (query: search terms, engine: google/youtube/bing)
- open_url: Open URL (url: web address)
- run_cmd: Run command (command: cmd string)
- type_text: Type text (text: string to type)
- press_key: Press key(s) (key: key name or combo like "ctrl+c")
- click: Click mouse (x, y, button: left/right)
- move_mouse: Move mouse (x, y)
- system_control: System settings (target: volume_up/volume_down/volume_mute/wifi_toggle/brightness, level: 0-100 for brightness)
- read_file: Read file (target: file path)
- write_file: Write file (target: file path, content: text)
- search_files: Search files (query: search term, path: optional search path)
- none: No action needed (for conversation)

IMPORTANT RULES:
1. Games: ONLY launch games, NEVER control them with keyboard/mouse
2. For conversation, use action "none" and respond naturally
3. If user says "Anna" treat it as activation
4. If you don't know an app path, ask user to teach you
5. For ambiguous requests, ask ONE clarifying question
6. ALWAYS output valid JSON for actions

OUTPUT FORMAT:
For actions:
{{
  "action": "action_name",
  "target": "target_value",
  "additional_params": "if_needed"
}}

After JSON, optionally add a brief natural response.

For conversation only:
{{
  "action": "none"
}}
Then provide your conversational response.

CONTEXT:
{memory.build_context_string()}
"""
        return prompt
    
    def process(self, user_input):
        """Process user input and return response + action"""
        try:
            # Check if model is configured
            if not self.model:
                return {
                    "response": "I'm not properly configured. Please set your GEMINI_API_KEY in the .env file.",
                    "action": None,
                    "needs_pin": False
                }
            
            # Build prompt
            system_prompt = self._build_system_prompt()
            full_prompt = f"{system_prompt}\n\nUser: {user_input}\n\nAnna:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            response_text = response.text.strip()
            
            # Extract JSON if present
            action_data = self._extract_json(response_text)
            
            # Get natural language response (text after JSON or full text if no JSON)
            natural_response = self._extract_natural_response(response_text)
            
            # Check if dangerous
            needs_pin = False
            if action_data and action_data.get("action") != "none":
                action_type = action_data.get("action")
                needs_pin = safety.requires_pin(user_input, action_type)
                
                if needs_pin:
                    logger.log_audit("DANGEROUS_DETECTED", user_input, str(action_data), False)
            
            return {
                "response": natural_response,
                "action": action_data,
                "needs_pin": needs_pin
            }
            
        except Exception as e:
            logger.log_error("BRAIN_PROCESS", str(e), user_input)
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "action": None,
                "needs_pin": False
            }
    
    def _extract_json(self, text):
        """Extract JSON from response text"""
        try:
            # Look for JSON between curly braces
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            
            return None
        except:
            return None
    
    def _extract_natural_response(self, text):
        """Extract natural language response (text after JSON)"""
        # Remove JSON if present
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            # Get text after JSON
            after_json = text[end:].strip()
            if after_json:
                return after_json
            # Get text before JSON
            before_json = text[:start].strip()
            if before_json:
                return before_json
        
        # No JSON found, return full text
        return text
    
    def generate_simple_response(self, user_input):
        """Generate a simple conversational response without actions"""
        try:
            if not self.model:
                return "I'm not properly configured. Please set your GEMINI_API_KEY."
            
            prompt = f"""You are Anna, a helpful AI assistant. Respond naturally and conversationally.

Context:
{memory.build_context_string()}

User: {user_input}
Anna:"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.log_error("SIMPLE_RESPONSE", str(e), user_input)
            return f"Sorry, I encountered an error: {str(e)}"


# Global brain instance
anna_brain = AnnaBrain()
