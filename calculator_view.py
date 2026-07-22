"""
Calculator View - Professional GUI with AI Integration
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional, List, Dict
import threading
import queue
import math

class CalculatorView:
    """Professional calculator GUI with AI assistant"""
    
    def __init__(self, controller):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("🤖 AI Professional Calculator")
        self.window.geometry("750x900")
        self.window.resizable(False, False)
        
        # AI message queue
        self.message_queue = queue.Queue()
        
        # Color scheme - Modern dark theme
        self.colors = {
            'bg': '#1a1a1a',
            'display_bg': '#2d2d2d',
            'ai_bg': '#1e2d3d',
            'btn_number': '#3d3d3d',
            'btn_operator': '#ff6b6b',
            'btn_function': '#4d4d4d',
            'btn_equals': '#4a90e2',
            'btn_ai': '#2ecc71',
            'btn_memory': '#5d5d5d',
            'text_normal': '#ffffff',
            'text_operator': '#ff6b6b',
            'text_ai': '#a8d8ea'
        }
        
        self.setup_ui()
        self.setup_keyboard_bindings()
        self.check_ai_messages()
        
    def setup_ui(self):
        """Initialize the UI components"""
        self.window.configure(bg=self.colors['bg'])
        
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # AI Assistant Panel
        self.create_ai_panel(main_frame)
        
        # Display area
        self.create_display(main_frame)
        
        # Memory and function buttons
        self.create_memory_buttons(main_frame)
        
        # Main calculator buttons
        self.create_calculator_buttons(main_frame)
        
        # History panel
        self.create_history_panel(main_frame)
        
        # Status bar
        self.create_status_bar()
        
    def create_ai_panel(self, parent):
        """Create AI assistant panel"""
        ai_frame = ttk.Frame(parent)
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        
        # AI Header
        ai_header = tk.Frame(ai_frame, bg=self.colors['bg'])
        ai_header.pack(fill=tk.X)
        
        ai_label = tk.Label(ai_header, text="🤖 AI Assistant", 
                           bg=self.colors['bg'], fg=self.colors['text_ai'],
                           font=('Arial', 11, 'bold'))
        ai_label.pack(side=tk.LEFT)
        
        # Insights button
        insights_btn = tk.Button(ai_header, text="📊 Insights", 
                                command=self.show_insights,
                                bg=self.colors['btn_function'],
                                fg=self.colors['text_normal'],
                                font=('Arial', 9))
        insights_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # AI Input
        ai_input_frame = ttk.Frame(ai_frame)
        ai_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.ai_input = tk.Entry(ai_input_frame, 
                                font=('Arial', 11),
                                bg=self.colors['ai_bg'],
                                fg=self.colors['text_normal'],
                                relief=tk.FLAT)
        self.ai_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.ai_input.bind('<Return>', lambda e: self.process_ai_command())
        
        ai_btn = tk.Button(ai_input_frame, text="Ask AI", 
                          command=self.process_ai_command,
                          bg=self.colors['btn_ai'], 
                          fg='white',
                          font=('Arial', 10, 'bold'),
                          relief=tk.RAISED)
        ai_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # AI Response area
        self.ai_response = scrolledtext.ScrolledText(ai_frame,
                                                    height=3,
                                                    bg=self.colors['ai_bg'],
                                                    fg=self.colors['text_ai'],
                                                    font=('Arial', 10),
                                                    wrap=tk.WORD,
                                                    relief=tk.FLAT)
        self.ai_response.pack(fill=tk.X, pady=(5, 0))
        self.ai_response.insert(tk.END, "💡 Ask me anything about math!\n")
        self.ai_response.insert(tk.END, "Try: 'What's 20% of 50?' or 'Square root of 144'")
        self.ai_response.config(state=tk.DISABLED)
        
    def process_ai_command(self):
        """Process AI command from user"""
        command = self.ai_input.get().strip()
        if not command:
            return
        
        self.ai_input.delete(0, tk.END)
        
        # Show thinking indicator
        self.enable_ai_response("🤔 Thinking...")
        
        # Process in background thread
        threading.Thread(target=self._process_ai_async, args=(command,), daemon=True).start()
    
    def _process_ai_async(self, command: str):
        """Process AI command in background"""
        try:
            result = self.controller.process_input(command)
            self.message_queue.put(('ai_response', result))
        except Exception as e:
            self.message_queue.put(('ai_response', {'type': 'error', 'response': f"❌ Error: {str(e)}"}))
    
    def check_ai_messages(self):
        """Check for AI responses in queue"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                if msg_type == 'ai_response':
                    self.display_ai_response(data)
        except queue.Empty:
            pass
        finally:
            self.window.after(100, self.check_ai_messages)
    
    def display_ai_response(self, response: Dict):
        """Display AI response"""
        self.enable_ai_response("")
        
        response_text = ""
        if response.get('type') == 'calculation':
            response_text = f"🧮 {response.get('expression', '')}\n"
            response_text += f"📊 Answer: {response.get('result', '')}"
        elif response.get('type') == 'greeting':
            response_text = f"👋 {response.get('response', '')}"
        elif response.get('type') == 'help':
            response_text = response.get('response', '')
        elif response.get('type') == 'error':
            response_text = f"❌ {response.get('response', '')}"
        elif response.get('type') == 'suggestion':
            response_text = f"💡 {response.get('message', '')}\n"
            for suggestion in response.get('suggestions', []):
                response_text += f"• {suggestion}\n"
        else:
            response_text = response.get('response', "I processed your request.")
        
        self.enable_ai_response(response_text)
        
        # If there's a result, update the calculator display
        if response.get('type') == 'calculation' and response.get('result'):
            self.result_var
