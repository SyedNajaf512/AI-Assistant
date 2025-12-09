"""
Anna AI Assistant - CLI Interface
Text-based command-line interface with personality
"""

from colorama import init, Fore, Style
import sys

# Initialize colorama
init(autoreset=True)


class CLIInterface:
    """Command-line interface for Anna"""
    
    def __init__(self):
        self.colors = {
            "anna": Fore.CYAN,
            "user": Fore.GREEN,
            "system": Fore.YELLOW,
            "error": Fore.RED,
            "success": Fore.GREEN,
            "action": Fore.MAGENTA,
            "warning": Fore.YELLOW,
        }
    
    def print_banner(self):
        """Print Anna welcome banner"""
        banner = f"""
{Fore.CYAN}{'='*60}
     █████╗ ███╗   ██╗███╗   ██╗ █████╗ 
    ██╔══██╗████╗  ██║████╗  ██║██╔══██╗
    ███████║██╔██╗ ██║██╔██╗ ██║███████║
    ██╔══██║██║╚██╗██║██║╚██╗██║██╔══██║
    ██║  ██║██║ ╚████║██║ ╚████║██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═╝
    
    Advanced Local AI Assistant for Windows
    Type 'help' for commands, 'exit' to quit
{'='*60}{Style.RESET_ALL}
"""
        print(banner)
    
    def print_anna(self, message, message_type="normal"):
        """Print Anna's response"""
        color = self.colors.get(message_type, self.colors["anna"])
        print(f"{color}Anna: {Style.RESET_ALL}{message}")
    
    def print_user(self, message):
        """Print user input"""
        print(f"{self.colors['user']}You: {Style.RESET_ALL}{message}")
    
    def print_action(self, action_data):
        """Print action being executed"""
        action = action_data.get("action", "unknown")
        target = action_data.get("target", "")
        
        print(f"{self.colors['action']}[ACTION] {Style.RESET_ALL}{action}", end="")
        if target:
            print(f" → {target}", end="")
        print()
    
    def print_result(self, result):
        """Print action result"""
        if result.get("success"):
            color = self.colors["success"]
            prefix = "✓"
        else:
            color = self.colors["error"]
            prefix = "✗"
        
        message = result.get("message", "No message")
        print(f"{color}[{prefix}] {message}{Style.RESET_ALL}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"{self.colors['error']}[ERROR] {message}{Style.RESET_ALL}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"{self.colors['warning']}[WARNING] {message}{Style.RESET_ALL}")
    
    def print_system(self, message):
        """Print system message"""
        print(f"{self.colors['system']}[SYSTEM] {message}{Style.RESET_ALL}")
    
    def get_input(self, prompt="You: "):
        """Get user input"""
        try:
            user_input = input(f"{self.colors['user']}{prompt}{Style.RESET_ALL}")
            return user_input.strip()
        except KeyboardInterrupt:
            print("\n")
            return "exit"
        except EOFError:
            return "exit"
    
    def get_pin(self):
        """Get PIN input (hidden)"""
        import getpass
        try:
            pin = getpass.getpass(f"{self.colors['warning']}Enter PIN: {Style.RESET_ALL}")
            return pin.strip()
        except KeyboardInterrupt:
            print("\n")
            return ""
    
    def confirm(self, message):
        """Ask for yes/no confirmation"""
        response = self.get_input(f"{message} (yes/no): ")
        return response.lower() in ['yes', 'y']
    
    def print_help(self):
        """Print help information"""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}

{Fore.GREEN}Natural Language:{Style.RESET_ALL}
  - Just talk to Anna naturally!
  - "Open Chrome"
  - "Search Google for Python tutorials"
  - "What's the weather like?"
  - "Launch Notepad"

{Fore.GREEN}Special Commands:{Style.RESET_ALL}
  help       - Show this help message
  history    - Show conversation history
  clear      - Clear screen
  status     - Show Anna's status
  exit       - Exit Anna

{Fore.GREEN}Examples:{Style.RESET_ALL}
  "Anna, open File Explorer"
  "Search YouTube for music"
  "Type hello world"
  "Volume up"
  "What can you do?"

{Fore.YELLOW}Note:{Style.RESET_ALL} Dangerous actions will require PIN confirmation.
"""
        print(help_text)
    
    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_history(self, history):
        """Print conversation history"""
        if not history:
            self.print_system("No conversation history yet")
            return
        
        print(f"\n{Fore.CYAN}Recent Conversation History:{Style.RESET_ALL}\n")
        for i, exchange in enumerate(history, 1):
            print(f"{self.colors['user']}[{i}] You: {Style.RESET_ALL}{exchange.get('user', '')}")
            print(f"{self.colors['anna']}    Anna: {Style.RESET_ALL}{exchange.get('anna', '')}\n")


# Global CLI instance
cli = CLIInterface()
