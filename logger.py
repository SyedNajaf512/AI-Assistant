"""
Anna AI Assistant - Logging Infrastructure
Handles action logging, error tracking, and audit trails
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class AnnaLogger:
    """Centralized logging for Anna AI Assistant"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup loggers
        self.action_logger = self._setup_logger("actions", "actions.log")
        self.error_logger = self._setup_logger("errors", "errors.log")
        self.audit_logger = self._setup_logger("audit", "audit.log")
        self.debug_logger = self._setup_logger("debug", "debug.log")
    
    def _setup_logger(self, name, filename):
        """Setup individual logger with file and console handlers"""
        logger = logging.getLogger(f"anna.{name}")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(self.log_dir / filename)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler (only for errors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_action(self, action_type, target, success=True, details=None):
        """Log an automation action"""
        msg = f"Action: {action_type} | Target: {target} | Success: {success}"
        if details:
            msg += f" | Details: {details}"
        self.action_logger.info(msg)
    
    def log_error(self, error_type, message, details=None):
        """Log an error"""
        msg = f"Error: {error_type} | Message: {message}"
        if details:
            msg += f" | Details: {details}"
        self.error_logger.error(msg)
    
    def log_audit(self, event_type, user_input, action_taken, pin_verified=False):
        """Log security-relevant events"""
        msg = (f"Audit: {event_type} | Input: '{user_input}' | "
               f"Action: {action_taken} | PIN Verified: {pin_verified}")
        self.audit_logger.warning(msg)
    
    def log_debug(self, message):
        """Log debug information"""
        self.debug_logger.debug(message)


# Global logger instance
logger = AnnaLogger()
