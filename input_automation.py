"""
Anna AI Assistant - Input Automation
Handles keyboard typing and mouse control
"""

import pyautogui
import time
from logger import logger


# Set pyautogui safety features
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True  # Move mouse to corner to abort


class InputAutomation:
    """Manages keyboard and mouse automation"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
    
    def type_text(self, text, interval=0.05):
        """Type text on keyboard"""
        try:
            pyautogui.write(text, interval=interval)
            logger.log_action("type_text", f"{len(text)} characters", True)
            return {"success": True, "message": f"Typed: {text[:50]}..."}
        except Exception as e:
            logger.log_error("TYPE_TEXT", str(e))
            return {"success": False, "message": f"Error typing: {str(e)}"}
    
    def press_key(self, key):
        """Press a single key or key combination"""
        try:
            # Handle key combinations (e.g., "ctrl+c", "alt+tab")
            if '+' in key:
                keys = [k.strip() for k in key.split('+')]
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key)
            
            logger.log_action("press_key", key, True)
            return {"success": True, "message": f"Pressed: {key}"}
        except Exception as e:
            logger.log_error("PRESS_KEY", str(e), key)
            return {"success": False, "message": f"Error pressing key: {str(e)}"}
    
    def move_mouse(self, x, y, duration=0.5):
        """Move mouse to coordinates"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            logger.log_action("move_mouse", f"({x}, {y})", True)
            return {"success": True, "message": f"Moved mouse to ({x}, {y})"}
        except Exception as e:
            logger.log_error("MOVE_MOUSE", str(e), f"({x}, {y})")
            return {"success": False, "message": f"Error moving mouse: {str(e)}"}
    
    def click(self, x=None, y=None, button='left', clicks=1):
        """Click at current position or specified coordinates"""
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, clicks=clicks, button=button)
            else:
                pyautogui.click(clicks=clicks, button=button)
            
            location = f"({x}, {y})" if x and y else "current position"
            logger.log_action("click", f"{button} {location}", True)
            return {"success": True, "message": f"Clicked: {button} at {location}"}
        except Exception as e:
            logger.log_error("CLICK", str(e))
            return {"success": False, "message": f"Error clicking: {str(e)}"}
    
    def double_click(self, x=None, y=None):
        """Double click at position"""
        return self.click(x, y, clicks=2)
    
    def right_click(self, x=None, y=None):
        """Right click at position"""
        return self.click(x, y, button='right')
    
    def scroll(self, amount, direction='down'):
        """Scroll up or down"""
        try:
            scroll_amount = -amount if direction == 'down' else amount
            pyautogui.scroll(scroll_amount)
            logger.log_action("scroll", f"{direction} {amount}", True)
            return {"success": True, "message": f"Scrolled {direction} {amount}"}
        except Exception as e:
            logger.log_error("SCROLL", str(e))
            return {"success": False, "message": f"Error scrolling: {str(e)}"}
    
    def get_mouse_position(self):
        """Get current mouse position"""
        try:
            x, y = pyautogui.position()
            return {"success": True, "x": x, "y": y, "message": f"Mouse at ({x}, {y})"}
        except Exception as e:
            logger.log_error("GET_MOUSE_POS", str(e))
            return {"success": False, "message": f"Error getting mouse position: {str(e)}"}
    
    def screenshot(self, filename=None):
        """Take a screenshot"""
        try:
            if filename is None:
                from datetime import datetime
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            logger.log_action("screenshot", filename, True)
            return {"success": True, "message": f"Screenshot saved: {filename}"}
        except Exception as e:
            logger.log_error("SCREENSHOT", str(e))
            return {"success": False, "message": f"Error taking screenshot: {str(e)}"}


# Global input automation instance
input_automation = InputAutomation()
