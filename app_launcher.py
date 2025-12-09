"""
Anna AI Assistant - Application Launcher
Handles launching, closing, and managing Windows applications
"""

import subprocess
import os
import psutil
from pathlib import Path
from logger import logger
from config import config


class AppLauncher:
    """Manages Windows application launching and control"""
    
    def __init__(self):
        # Common app locations
        self.common_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"C:\Windows\System32",
            os.path.expanduser("~\\AppData\\Local"),
            os.path.expanduser("~\\AppData\\Roaming"),
        ]
    
    def open_app(self, app_name):
        """Open an application by name"""
        try:
            # Check if we know this app
            app_path = config.get_app_path(app_name.lower())
            
            if app_path:
                # Try to launch known app
                result = self._launch(app_path)
                if result:
                    logger.log_action("open_app", app_name, True)
                    return {"success": True, "message": f"Opened {app_name}"}
            
            # Try common system apps first
            try:
                subprocess.Popen(app_name)
                logger.log_action("open_app", app_name, True, "System command")
                return {"success": True, "message": f"Opened {app_name}"}
            except:
                pass
            
            # Search for the app
            found_path = self._search_app(app_name)
            if found_path:
                result = self._launch(found_path)
                if result:
                    # Learn this app for next time
                    config.learn_app(app_name, found_path)
                    logger.log_action("open_app", app_name, True, f"Found at {found_path}")
                    return {"success": True, "message": f"Opened {app_name}"}
            
            # App not found
            logger.log_action("open_app", app_name, False, "App not found")
            return {
                "success": False, 
                "message": f"I don't know where {app_name} is. Tell me the path so I can remember it."
            }
            
        except Exception as e:
            logger.log_error("APP_LAUNCH", str(e), app_name)
            return {"success": False, "message": f"Error opening {app_name}: {str(e)}"}
    
    def launch_game(self, game_name):
        """Launch a game (similar to app but from games list)"""
        try:
            game_path = config.get_game_path(game_name.lower())
            
            if game_path:
                result = self._launch(game_path)
                if result:
                    logger.log_action("launch_game", game_name, True)
                    return {"success": True, "message": f"Launched {game_name}"}
            
            logger.log_action("launch_game", game_name, False, "Game not found")
            return {
                "success": False,
                "message": f"I don't know where {game_name} is. Tell me the path so I can remember it."
            }
            
        except Exception as e:
            logger.log_error("GAME_LAUNCH", str(e), game_name)
            return {"success": False, "message": f"Error launching {game_name}: {str(e)}"}
    
    def _launch(self, path):
        """Internal launch method"""
        try:
            if path.endswith('.exe'):
                subprocess.Popen(path)
            else:
                os.startfile(path)
            return True
        except Exception as e:
            logger.log_error("LAUNCH_PROCESS", str(e), path)
            return False
    
    def _search_app(self, app_name):
        """Search for application in common locations"""
        # Add .exe if not present
        if not app_name.endswith('.exe'):
            search_names = [app_name, f"{app_name}.exe"]
        else:
            search_names = [app_name]
        
        # Search common paths
        for base_path in self.common_paths:
            if not os.path.exists(base_path):
                continue
            
            for search_name in search_names:
                # Try direct path
                full_path = os.path.join(base_path, search_name)
                if os.path.exists(full_path):
                    return full_path
                
                # Search subdirectories (max depth 2)
                try:
                    for root, dirs, files in os.walk(base_path):
                        # Limit depth
                        depth = root.replace(base_path, '').count(os.sep)
                        if depth > 2:
                            continue
                        
                        for file in files:
                            if file.lower() == search_name.lower():
                                return os.path.join(root, file)
                except Exception:
                    continue
        
        return None
    
    def close_app(self, app_name):
        """Close an application by name"""
        try:
            # Find process by name
            closed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                logger.log_action("close_app", app_name, True)
                return {"success": True, "message": f"Closed {app_name}"}
            else:
                return {"success": False, "message": f"{app_name} is not running"}
                
        except Exception as e:
            logger.log_error("APP_CLOSE", str(e), app_name)
            return {"success": False, "message": f"Error closing {app_name}: {str(e)}"}
    
    def teach_app(self, name, path):
        """Teach Anna a new application"""
        if os.path.exists(path):
            config.learn_app(name, path)
            return {"success": True, "message": f"Thanks! I'll remember that {name} is at {path}"}
        else:
            return {"success": False, "message": f"I can't find anything at {path}"}
    
    def teach_game(self, name, path):
        """Teach Anna a new game"""
        if os.path.exists(path):
            config.learn_game(name, path)
            return {"success": True, "message": f"Thanks! I'll remember that {name} is at {path}"}
        else:
            return {"success": False, "message": f"I can't find anything at {path}"}


# Global app launcher instance
app_launcher = AppLauncher()
