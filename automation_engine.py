"""
Anna AI Assistant - Automation Engine
Main dispatcher that routes JSON action commands to appropriate handlers
"""

import json
from logger import logger
from app_launcher import app_launcher
from file_operations import file_ops
from web_handler import web_handler
from system_control import system_control
from input_automation import input_automation


class AutomationEngine:
    """Main automation dispatcher"""
    
    def __init__(self):
        self.handlers = {
            "open_app": self._handle_open_app,
            "open_file": self._handle_open_file,
            "open_folder": self._handle_open_folder,
            "launch_game": self._handle_launch_game,
            "web_search": self._handle_web_search,
            "open_url": self._handle_open_url,
            "run_cmd": self._handle_run_cmd,
            "type_text": self._handle_type_text,
            "press_key": self._handle_press_key,
            "move_mouse": self._handle_move_mouse,
            "click": self._handle_click,
            "system_control": self._handle_system_control,
            "read_file": self._handle_read_file,
            "write_file": self._handle_write_file,
            "search_files": self._handle_search_files,
            "dangerous_action": self._handle_dangerous_action,
            "none": self._handle_none,
        }
    
    def execute(self, action_data):
        """Execute an action from JSON data"""
        try:
            # Parse if string
            if isinstance(action_data, str):
                action_data = json.loads(action_data)
            
            action = action_data.get("action", "none")
            
            # Get handler
            handler = self.handlers.get(action, self._handle_unknown)
            
            # Execute
            result = handler(action_data)
            
            return result
            
        except json.JSONDecodeError as e:
            logger.log_error("JSON_PARSE", str(e), str(action_data))
            return {"success": False, "message": "Invalid action format"}
        except Exception as e:
            logger.log_error("EXECUTE_ACTION", str(e), str(action_data))
            return {"success": False, "message": f"Error executing action: {str(e)}"}
    
    # Action Handlers
    
    def _handle_open_app(self, data):
        """Open application"""
        target = data.get("target", "")
        return app_launcher.open_app(target)
    
    def _handle_open_file(self, data):
        """Open file"""
        target = data.get("target", "")
        return file_ops.open_file(target)
    
    def _handle_open_folder(self, data):
        """Open folder"""
        target = data.get("target", "")
        return file_ops.open_folder(target)
    
    def _handle_launch_game(self, data):
        """Launch game"""
        target = data.get("target", "")
        return app_launcher.launch_game(target)
    
    def _handle_web_search(self, data):
        """Web search"""
        query = data.get("query", "")
        engine = data.get("engine", "google")
        return web_handler.web_search(query, engine)
    
    def _handle_open_url(self, data):
        """Open URL"""
        url = data.get("url", data.get("target", ""))
        return web_handler.open_url(url)
    
    def _handle_run_cmd(self, data):
        """Run command"""
        command = data.get("command", data.get("target", ""))
        return system_control.run_command(command)
    
    def _handle_type_text(self, data):
        """Type text"""
        text = data.get("text", data.get("target", ""))
        return input_automation.type_text(text)
    
    def _handle_press_key(self, data):
        """Press key"""
        key = data.get("key", data.get("target", ""))
        return input_automation.press_key(key)
    
    def _handle_move_mouse(self, data):
        """Move mouse"""
        x = data.get("x", 0)
        y = data.get("y", 0)
        return input_automation.move_mouse(x, y)
    
    def _handle_click(self, data):
        """Click mouse"""
        x = data.get("x")
        y = data.get("y")
        button = data.get("button", "left")
        return input_automation.click(x, y, button)
    
    def _handle_system_control(self, data):
        """System control actions"""
        target = data.get("target", "").lower()
        
        if target == "volume_up":
            return system_control.volume_up()
        elif target == "volume_down":
            return system_control.volume_down()
        elif target == "volume_mute" or target == "mute":
            return system_control.volume_mute()
        elif target.startswith("brightness"):
            # Extract level from target
            try:
                level = int(data.get("level", 50))
                return system_control.set_brightness(level)
            except:
                return {"success": False, "message": "Invalid brightness level"}
        elif target == "wifi_toggle":
            return system_control.wifi_toggle()
        else:
            return {"success": False, "message": f"Unknown system control: {target}"}
    
    def _handle_read_file(self, data):
        """Read file"""
        target = data.get("target", "")
        return file_ops.read_file(target)
    
    def _handle_write_file(self, data):
        """Write file (dangerous)"""
        target = data.get("target", "")
        content = data.get("content", "")
        return file_ops.write_file(target, content)
    
    def _handle_search_files(self, data):
        """Search files"""
        query = data.get("query", data.get("target", ""))
        path = data.get("path")
        return file_ops.search_files(query, path)
    
    def _handle_dangerous_action(self, data):
        """Handle dangerous action after PIN verification"""
        # This is called after PIN is verified
        actual_action = data.get("actual_action", "none")
        if actual_action in self.handlers:
            return self.handlers[actual_action](data)
        return {"success": False, "message": "Invalid dangerous action"}
    
    def _handle_none(self, data):
        """No action required"""
        return {"success": True, "message": "No action required"}
    
    def _handle_unknown(self, data):
        """Unknown action"""
        action = data.get("action", "unknown")
        logger.log_error("UNKNOWN_ACTION", f"Unknown action: {action}", str(data))
        return {"success": False, "message": f"Unknown action: {action}"}


# Global automation engine instance
automation_engine = AutomationEngine()
