"""
Anna AI Assistant - Safety Layer
Security controls and dangerous action detection
"""

import re
from logger import logger
from config import config


class Safety:
    """Safety and security controls for Anna"""
    
    # Dangerous keywords that require PIN
    DANGEROUS_KEYWORDS = [
        r'\bdelete\b', r'\bremove\b', r'\berase\b', r'\bwipe\b',
        r'\bdestroy\b', r'\bformat\b', r'\bshutdown\b', r'\brestart\b',
        r'\breboot\b', r'\bkill\b.*\bprocess\b', r'\bterminate\b.*\bprocess\b',
        r'\bedit\b.*\bsystem\b', r'\bmodify\b.*\bregistry\b',
        r'\buninstall\b', r'\binstall\b', r'\brm\b\s+-rf',
        r'\bdel\b\s+/[fqs]', r'\bformat\b\s+[a-z]:', 
    ]
    
    # Dangerous actions that always require confirmation
    DANGEROUS_ACTIONS = [
        'delete_file', 'delete_folder', 'format_drive',
        'kill_process', 'modify_registry', 'install_software',
        'uninstall_software', 'run_script', 'shutdown', 'restart'
    ]
    
    def __init__(self):
        self.pending_dangerous_action = None
        self.pin_attempts = 0
        self.max_pin_attempts = 3
    
    def is_dangerous(self, user_input, action_type=None):
        """Check if input or action is dangerous"""
        # Check action type
        if action_type in self.DANGEROUS_ACTIONS:
            return True
        
        # Check keywords in input
        user_input_lower = user_input.lower()
        for pattern in self.DANGEROUS_KEYWORDS:
            if re.search(pattern, user_input_lower):
                return True
        
        return False
    
    def requires_pin(self, user_input, action_type=None):
        """Check if action requires PIN verification"""
        return self.is_dangerous(user_input, action_type)
    
    def verify_pin(self, pin_input):
        """Verify PIN and handle attempts"""
        if config.verify_pin(pin_input):
            self.pin_attempts = 0
            logger.log_audit("PIN_VERIFIED", "User PIN", "Access granted", True)
            return True
        else:
            self.pin_attempts += 1
            logger.log_audit("PIN_FAILED", "User PIN", f"Attempt {self.pin_attempts}", False)
            
            if self.pin_attempts >= self.max_pin_attempts:
                logger.log_audit("PIN_LOCKED", "User PIN", "Max attempts reached", False)
                self.pin_attempts = 0  # Reset for next time
                return "LOCKED"
            
            return False
    
    def request_pin_confirmation(self, user_input, action_data):
        """Store pending action and request PIN"""
        self.pending_dangerous_action = {
            "input": user_input,
            "action": action_data
        }
        logger.log_audit("PIN_REQUESTED", user_input, str(action_data), False)
        return True
    
    def get_pending_action(self):
        """Get and clear pending action"""
        action = self.pending_dangerous_action
        self.pending_dangerous_action = None
        return action
    
    def clear_pending_action(self):
        """Clear pending action"""
        self.pending_dangerous_action = None
    
    def has_pending_action(self):
        """Check if there's a pending dangerous action"""
        return self.pending_dangerous_action is not None
    
    def sanitize_path(self, path):
        """Sanitize file paths to prevent directory traversal"""
        # Remove dangerous patterns
        dangerous_patterns = ['..', '~', '$', '|', '&', ';']
        for pattern in dangerous_patterns:
            if pattern in path:
                logger.log_error("PATH_SANITIZE", f"Dangerous pattern in path: {pattern}")
                return None
        return path
    
    def validate_command(self, command):
        """Validate command-line commands"""
        # Block dangerous shell commands
        dangerous_commands = [
            'rm -rf /', 'del /f /s /q', 'format c:', 
            'rd /s /q', ':(){:|:&};:', 'dd if='
        ]
        
        cmd_lower = command.lower().strip()
        for dangerous in dangerous_commands:
            if dangerous in cmd_lower:
                logger.log_error("CMD_BLOCKED", f"Dangerous command blocked: {command}")
                return False
        return True


# Global safety instance
safety = Safety()
