"""
Anna AI Assistant - Windows Auto-Start Setup
Creates a shortcut in Windows Startup folder
"""

import os
import sys
from pathlib import Path


def create_startup_shortcut():
    """Create a shortcut in Windows Startup folder"""
    try:
        import win32com.client
        
        # Get paths
        startup_folder = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        
        # Current script directory
        script_dir = Path(__file__).parent.absolute()
        target_path = str(script_dir / "main.py")
        python_exe = sys.executable
        
        # Create shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut_path = os.path.join(startup_folder, "Anna AI Assistant.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        
        # Configure shortcut
        shortcut.TargetPath = python_exe
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = str(script_dir)
        shortcut.IconLocation = python_exe
        shortcut.Description = "Anna AI Assistant - Voice & GUI"
        shortcut.WindowStyle = 1  # Normal window
        
        # Save
        shortcut.save()
        
        return True, f"Startup shortcut created at: {shortcut_path}"
        
    except ImportError:
        return False, "pywin32 not installed. Run: pip install pywin32"
    except Exception as e:
        return False, f"Error creating shortcut: {str(e)}"


def remove_startup_shortcut():
    """Remove Anna from Windows Startup"""
    try:
        startup_folder = os.path.join(
            os.getenv('APPDATA'),
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        shortcut_path = os.path.join(startup_folder, "Anna AI Assistant.lnk")
        
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            return True, "Startup shortcut removed"
        else:
            return False, "No startup shortcut found"
            
    except Exception as e:
        return False, f"Error removing shortcut: {str(e)}"


def is_auto_start_enabled():
    """Check if auto-start is enabled"""
    startup_folder = os.path.join(
        os.getenv('APPDATA'),
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    shortcut_path = os.path.join(startup_folder, "Anna AI Assistant.lnk")
    return os.path.exists(shortcut_path)


if __name__ == "__main__":
    # Command-line tool
    import argparse
    
    parser = argparse.ArgumentParser(description="Anna Auto-Start Manager")
    parser.add_argument('action', choices=['enable', 'disable', 'status'],
                       help='Action to perform')
    args = parser.parse_args()
    
    if args.action == 'enable':
        success, message = create_startup_shortcut()
        print(message)
        sys.exit(0 if success else 1)
    
    elif args.action == 'disable':
        success, message = remove_startup_shortcut()
        print(message)
        sys.exit(0 if success else 1)
    
    elif args.action == 'status':
        if is_auto_start_enabled():
            print("Auto-start: ENABLED")
        else:
            print("Auto-start: DISABLED")
