"""
Anna AI Assistant - System Control
Handles system settings and controls
"""

import subprocess
import ctypes
from logger import logger


class SystemControl:
    """Manages system settings and controls"""
    
    def __init__(self):
        # Volume control constants
        self.KEYEVENTF_EXTENDEDKEY = 0x0001
        self.KEYEVENTF_KEYUP = 0x0002
        self.VK_VOLUME_MUTE = 0xAD
        self.VK_VOLUME_DOWN = 0xAE
        self.VK_VOLUME_UP = 0xAF
    
    def volume_up(self):
        """Increase system volume"""
        try:
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_UP, 0, self.KEYEVENTF_EXTENDEDKEY, 0)
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_UP, 0, self.KEYEVENTF_EXTENDEDKEY | self.KEYEVENTF_KEYUP, 0)
            logger.log_action("volume_up", "system", True)
            return {"success": True, "message": "Volume increased"}
        except Exception as e:
            logger.log_error("VOLUME_UP", str(e))
            return {"success": False, "message": f"Error adjusting volume: {str(e)}"}
    
    def volume_down(self):
        """Decrease system volume"""
        try:
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_DOWN, 0, self.KEYEVENTF_EXTENDEDKEY, 0)
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_DOWN, 0, self.KEYEVENTF_EXTENDEDKEY | self.KEYEVENTF_KEYUP, 0)
            logger.log_action("volume_down", "system", True)
            return {"success": True, "message": "Volume decreased"}
        except Exception as e:
            logger.log_error("VOLUME_DOWN", str(e))
            return {"success": False, "message": f"Error adjusting volume: {str(e)}"}
    
    def volume_mute(self):
        """Mute/unmute system volume"""
        try:
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_MUTE, 0, self.KEYEVENTF_EXTENDEDKEY, 0)
            ctypes.windll.user32.keybd_event(self.VK_VOLUME_MUTE, 0, self.KEYEVENTF_EXTENDEDKEY | self.KEYEVENTF_KEYUP, 0)
            logger.log_action("volume_mute", "system", True)
            return {"success": True, "message": "Volume muted/unmuted"}
        except Exception as e:
            logger.log_error("VOLUME_MUTE", str(e))
            return {"success": False, "message": f"Error muting volume: {str(e)}"}
    
    def set_brightness(self, level):
        """Set screen brightness (0-100)"""
        try:
            # This is tricky on Windows, using PowerShell
            # Note: May not work on all systems
            cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            logger.log_action("set_brightness", str(level), True)
            return {"success": True, "message": f"Brightness set to {level}%"}
        except Exception as e:
            logger.log_error("SET_BRIGHTNESS", str(e), str(level))
            return {"success": False, "message": f"Error setting brightness: {str(e)}"}
    
    def run_command(self, command):
        """Run a command-line command"""
        try:
            from safety import safety
            
            # Validate command
            if not safety.validate_command(command):
                return {"success": False, "message": "Command blocked for safety reasons"}
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            logger.log_action("run_command", command, result.returncode == 0)
            
            return {
                "success": result.returncode == 0,
                "message": result.stdout if result.stdout else result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logger.log_error("CMD_TIMEOUT", "Command timed out", command)
            return {"success": False, "message": "Command timed out"}
        except Exception as e:
            logger.log_error("RUN_COMMAND", str(e), command)
            return {"success": False, "message": f"Error running command: {str(e)}"}
    
    def shutdown(self, delay_seconds=60):
        """Shutdown computer (DANGEROUS - requires PIN)"""
        try:
            subprocess.run(f"shutdown /s /t {delay_seconds}", shell=True)
            logger.log_action("shutdown", f"delay={delay_seconds}s", True)
            return {"success": True, "message": f"Shutting down in {delay_seconds} seconds"}
        except Exception as e:
            logger.log_error("SHUTDOWN", str(e))
            return {"success": False, "message": f"Error shutting down: {str(e)}"}
    
    def restart(self, delay_seconds=60):
        """Restart computer (DANGEROUS - requires PIN)"""
        try:
            subprocess.run(f"shutdown /r /t {delay_seconds}", shell=True)
            logger.log_action("restart", f"delay={delay_seconds}s", True)
            return {"success": True, "message": f"Restarting in {delay_seconds} seconds"}
        except Exception as e:
            logger.log_error("RESTART", str(e))
            return {"success": False, "message": f"Error restarting: {str(e)}"}
    
    def cancel_shutdown(self):
        """Cancel scheduled shutdown/restart"""
        try:
            subprocess.run("shutdown /a", shell=True)
            logger.log_action("cancel_shutdown", "system", True)
            return {"success": True, "message": "Shutdown cancelled"}
        except Exception as e:
            logger.log_error("CANCEL_SHUTDOWN", str(e))
            return {"success": False, "message": f"Error cancelling shutdown: {str(e)}"}
    
    def wifi_toggle(self):
        """Toggle WiFi (requires netsh)"""
        try:
            # Get WiFi interface name
            result = subprocess.run(
                "netsh interface show interface",
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Simple implementation - may need refinement
            subprocess.run("netsh interface set interface Wi-Fi toggle", shell=True)
            logger.log_action("wifi_toggle", "system", True)
            return {"success": True, "message": "WiFi toggled"}
        except Exception as e:
            logger.log_error("WIFI_TOGGLE", str(e))
            return {"success": False, "message": f"Error toggling WiFi: {str(e)}"}


# Global system control instance
system_control = SystemControl()
