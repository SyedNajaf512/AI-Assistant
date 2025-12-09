"""
Anna AI Assistant - GUI Interface (CORE)
Modern GUI interface with dark theme
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime


class AnnaGUI:
    """Modern GUI for Anna AI Assistant"""
    
    def __init__(self, on_input_callback=None):
        self.root = tk.Tk()
        self.root.title("Anna AI Assistant")
        self.root.geometry("800x600")
        self.on_input_callback = on_input_callback
        
        # Dark theme colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#00d4ff',
            'anna': '#00d4ff',
            'user': '#4caf50',
            'system': '#ff9800',
            'error': '#f44336',
            'input_bg': '#2d2d2d',
            'button': '#0d47a1',
            'button_hover': '#1565c0'
        }
        
        self.setup_ui()
        self.voice_active = False
    
    def setup_ui(self):
        """Setup the GUI layout"""
        self.root.configure(bg=self.colors['bg'])
        
        # Header
        self.create_header()
        
        # Chat display area
        self.create_chat_area()
        
        # Input area
        self.create_input_area()
        
        # Status bar
        self.create_status_bar()
        
        # Welcome message
        self.add_message("Anna", "Hello! I'm Anna, your AI assistant. You can type commands or use voice with 'Hey Anna'.", "anna")
    
    def create_header(self):
        """Create header with title and controls"""
        header_frame = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="ANNA AI ASSISTANT",
            font=('Arial', 20, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['bg']
        )
        title_label.pack(side='left', padx=20, pady=10)
        
        # Status indicator
        self.status_indicator = tk.Label(
            header_frame,
            text="● Ready",
            font=('Arial', 12),
            bg=self.colors['accent'],
            fg='#4caf50'
        )
        self.status_indicator.pack(side='right', padx=20, pady=10)
    
    def create_chat_area(self):
        """Create chat display area"""
        chat_frame = tk.Frame(self.root, bg=self.colors['bg'])
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg=self.colors['input_bg'],
            fg=self.colors['fg'],
            font=('Consolas', 11),
            insertbackground=self.colors['fg'],
            relief='flat',
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill='both', expand=True)
        self.chat_display.config(state='disabled')
        
        # Configure tags for colored text
        self.chat_display.tag_config('anna', foreground=self.colors['anna'], font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('user', foreground=self.colors['user'], font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('system', foreground=self.colors['system'], font=('Consolas', 10, 'italic'))
        self.chat_display.tag_config('error', foreground=self.colors['error'])
        self.chat_display.tag_config('action', foreground='#bb86fc', font=('Consolas', 10, 'italic'))
    
    def create_input_area(self):
        """Create input area with text box and send button"""
        input_frame = tk.Frame(self.root, bg=self.colors['bg'])
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Input text box
        self.input_box = tk.Entry(
            input_frame,
            bg=self.colors['input_bg'],
            fg=self.colors['fg'],
            font=('Arial', 12),
            insertbackground=self.colors['fg'],
            relief='flat'
        )
        self.input_box.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 10))
        self.input_box.bind('<Return>', lambda e: self.send_message())
        self.input_box.focus()
        
        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg=self.colors['button'],
            fg=self.colors['fg'],
            font=('Arial', 11, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.send_button.pack(side='left')
        
        # Voice button
        self.voice_button = tk.Button(
            input_frame,
            text="🎤 Voice",
            command=self.toggle_voice,
            bg='#2d2d2d',
            fg=self.colors['fg'],
            font=('Arial', 11),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.voice_button.pack(side='left', padx=(10, 0))
        
        # File upload button
        self.upload_button = tk.Button(
            input_frame,
            text="📎 Upload",
            command=self.upload_file,
            bg='#6a1b9a',
            fg=self.colors['fg'],
            font=('Arial', 11),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.upload_button.pack(side='left', padx=(10, 0))
    
    def upload_file(self):
        """Handle file upload"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select a document to learn from",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            # Call callback with special file upload command
            if self.on_input_callback:
                self.add_message("You", f"📎 Uploaded: {file_path}", 'user')
                threading.Thread(target=self.on_input_callback, args=(f"UPLOAD_FILE:{file_path}",), daemon=True).start()
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = tk.Frame(self.root, bg=self.colors['input_bg'], height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to assist",
            bg=self.colors['input_bg'],
            fg=self.colors['system'],
            font=('Arial', 9),
            anchor='w'
        )
        self.status_label.pack(side='left', padx=10, pady=5)
    
    def add_message(self, sender, message, message_type='normal'):
        """Add a message to chat display"""
        self.chat_display.config(state='normal')
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format based on sender
        if sender == "Anna":
            tag = 'anna'
            prefix = f"[{timestamp}] Anna: "
        elif sender == "You":
            tag = 'user'
            prefix = f"[{timestamp}] You: "
        elif sender == "System":
            tag = 'system'
            prefix = f"[{timestamp}] System: "
        elif sender == "Action":
            tag = 'action'
            prefix = f"[{timestamp}] ⚡ Action: "
        else:
            tag = message_type
            prefix = f"[{timestamp}] {sender}: "
        
        # Insert message
        self.chat_display.insert(tk.END, prefix, tag)
        self.chat_display.insert(tk.END, message + "\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def send_message(self):
        """Send user message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        # Display user message
        self.add_message("You", message, 'user')
        
        # Clear input
        self.input_box.delete(0, tk.END)
        
        # Call callback
        if self.on_input_callback:
            threading.Thread(target=self.on_input_callback, args=(message,), daemon=True).start()
    
    def toggle_voice(self):
        """Toggle voice mode"""
        self.voice_active = not self.voice_active
        if self.voice_active:
            self.voice_button.config(bg='#4caf50', text="🎤 Listening...")
            self.update_status("Voice mode active - Say 'Hey Anna'")
        else:
            self.voice_button.config(bg='#2d2d2d', text="🎤 Voice")
            self.update_status("Voice mode inactive")
    
    def update_status(self, status_text, status_type='normal'):
        """Update status bar"""
        self.status_label.config(text=status_text)
        
        # Update indicator
        if status_type == 'listening':
            self.status_indicator.config(text="● Listening", fg='#4caf50')
        elif status_type == 'processing':
            self.status_indicator.config(text="● Processing", fg='#ff9800')
        elif status_type == 'error':
            self.status_indicator.config(text="● Error", fg='#f44336')
        else:
            self.status_indicator.config(text="● Ready", fg='#4caf50')
    
    def add_action(self, action_type, target):
        """Add action display"""
        action_text = f"{action_type} → {target}"
        self.add_message("Action", action_text, 'action')
    
    def add_result(self, success, message):
        """Add result display"""
        if success:
            self.add_message("System", f"✓ {message}", 'system')
        else:
            self.add_message("System", f"✗ {message}", 'error')
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
    
    def quit(self):
        """Close the GUI"""
        self.root.quit()


# Global GUI instance
gui = None

def initialize_gui(callback=None):
    """Initialize GUI"""
    global gui
    gui = AnnaGUI(callback)
    return gui
