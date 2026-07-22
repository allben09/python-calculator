        
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
            self.result_var.set(response['result'])
            if response.get('expression'):
                self.expression_var.set(response['expression'])
            self.update_history()
    
    def show_insights(self):
        """Show AI insights"""
        insights = self.controller.get_ai_insights()
        self.enable_ai_response(insights)
    
    def enable_ai_response(self, text: str):
        """Enable AI response area and set text"""
        self.ai_response.config(state=tk.NORMAL)
        self.ai_response.delete(1.0, tk.END)
        self.ai_response.insert(tk.END, text)
        self.ai_response.config(state=tk.DISABLED)
    
    def create_display(self, parent):
        """Create the display area"""
        display_frame = ttk.Frame(parent)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Expression display
        self.expression_var = tk.StringVar()
        expression_entry = tk.Entry(display_frame, textvariable=self.expression_var,
                                   font=('Arial', 12), bg=self.colors['display_bg'],
                                   fg='#888888', relief=tk.FLAT, justify='right')
        expression_entry.pack(fill=tk.X, ipady=5)
        
        # Result display
        self.result_var = tk.StringVar(value="0")
        result_entry = tk.Entry(display_frame, textvariable=self.result_var,
                               font=('Arial', 28, 'bold'), bg=self.colors['display_bg'],
                               fg=self.colors['text_normal'], relief=tk.FLAT,
                               justify='right')
        result_entry.pack(fill=tk.X, ipady=15)
        
        self.result_entry = result_entry
        
    def create_memory_buttons(self, parent):
        """Create memory operation buttons"""
        memory_frame = ttk.Frame(parent)
        memory_frame.pack(fill=tk.X, pady=(0, 10))
        
        memory_buttons = [
            ('MC', self.memory_clear),
            ('MR', self.memory_recall),
            ('MS', self.memory_store),
            ('M+', self.memory_add)
        ]
        
        for text, command in memory_buttons:
            btn = tk.Button(memory_frame, text=text, command=command,
                           bg=self.colors['btn_memory'], fg=self.colors['text_normal'],
                           font=('Arial', 10, 'bold'), relief=tk.RAISED,
                           width=6, height=1)
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
            
    def create_calculator_buttons(self, parent):
        """Create the main calculator buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            ('sin', 'function'), ('cos', 'function'), ('tan', 'function'), ('√', 'function'),
            ('ln', 'function'), ('log', 'function'), ('x²', 'function'), ('n!', 'function'),
            ('(', 'function'), (')', 'function'), ('1/x', 'function'), ('%', 'function'),
            ('7', 'number'), ('8', 'number'), ('9', 'number'), ('÷', 'operator'),
            ('4', 'number'), ('5', 'number'), ('6', 'number'), ('×', 'operator'),
            ('1', 'number'), ('2', 'number'), ('3', 'number'), ('-', 'operator'),
            ('0', 'number'), ('.', 'number'), ('⌫', 'function'), ('+', 'operator'),
            ('CE', 'function'), ('C', 'function'), ('=', 'equals')
        ]
        
        # Create grid of buttons
        row = 0
        col = 0
        for text, btn_type in buttons:
            if btn_type == 'number':
                bg = self.colors['btn_number']
                fg = self.colors['text_normal']
            elif btn_type == 'operator':
                bg = self.colors['btn_operator']
                fg = self.colors['text_normal']
            elif btn_type == 'function':
                bg = self.colors['btn_function']
                fg = self.colors['text_normal']
            elif btn_type == 'equals':
                bg = self.colors['btn_equals']
                fg = self.colors['text_normal']
            else:
                bg = self.colors['btn_number']
                fg = self.colors['text_normal']
            
            btn = tk.Button(button_frame, text=text, 
                           command=lambda t=text: self.button_click(t),
                           bg=bg, fg=fg, font=('Arial', 12, 'bold'),
                           relief=tk.RAISED, height=1)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            
            col += 1
            if col > 3:
                col = 0
                row += 1
                
        # Configure grid weights
        for i in range(8):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
            
    def create_history_panel(self, parent):
        """Create toggleable history panel"""
        self.history_visible = False
        toggle_btn = tk.Button(parent, text="📜 Show History", 
                              command=self.toggle_history,
                              bg=self.colors['btn_function'],
                              fg=self.colors['text_normal'],
                              font=('Arial', 10))
        toggle_btn.pack(pady=(5, 0))
        
        self.history_frame = ttk.Frame(parent)
        self.history_text = scrolledtext.ScrolledText(self.history_frame,
                                                     height=8,
                                                     bg=self.colors['display_bg'],
                                                     fg=self.colors['text_normal'],
                                                     font=('Courier', 10))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # History controls
        history_controls = ttk.Frame(self.history_frame)
        history_controls.pack(fill=tk.X, pady=(5, 0))
        
        clear_btn = tk.Button(history_controls, text="Clear History",
                             command=self.clear_history,
                             bg=self.colors['btn_function'],
                             fg=self.colors['text_normal'],
                             font=('Arial', 9))
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        export_btn = tk.Button(history_controls, text="Export",
                              command=self.export_history,
                              bg=self.colors['btn_function'],
                              fg=self.colors['text_normal'],
                              font=('Arial', 9))
        export_btn.pack(side=tk.LEFT, padx=2)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(self.window, textvariable=self.status_var,
                               bg=self.colors['bg'], fg='#888888',
                               font=('Arial', 9), anchor='w')
        status_label.pack(fill=tk.X, padx=10, pady=(0, 5))
        
    def setup_keyboard_bindings(self):
        """Setup keyboard shortcuts"""
        self.window.bind('<Return>', lambda e: self.button_click('='))
        self.window.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.window.bind('<Escape>', lambda e: self.button_click('C'))
        self.window.bind('<Key>', self.key_press)
        self.window.bind('<Control-h>', lambda e: self.toggle_history())
        self.window.bind('<Control-i>', lambda e: self.show_insights())
        
    def key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key in '0123456789.+-*/%()':
            self.button_click(key)
        elif key == '=':
            self.button_click('=')
            
    def button_click(self, value):
        """Handle button clicks with AI suggestions"""
        current = self.result_var.get()
        
        # If current is an AI result, start fresh
        if current.startswith("AI:") or current.startswith("❌"):
            self.result_var.set("")
            current = ""
        
        if value in '0123456789.':
            if current == "0":
                self.result_var.set(value)
            else:
                self.result_var.set(current + value)
                
        elif value in '+-×÷%()':
            self.result_var.set(current + ' ' + value + ' ')
            
        elif value == '=':
            try:
                expression = current.replace('×', '*').replace('÷', '/')
                result = self.controller.evaluate_expression(expression)
                if not result.startswith("❌"):
                    self.expression_var.set(current + " =")
                self.result_var.set(result)
                self.update_history()
                
                # Get AI suggestions for the next step
                suggestions = self.controller.get_ai_suggestions(expression)
                if suggestions:
                    self.enable_ai_response("💡 Suggestions:\n" + "\n".join([f"• {s}" for s in suggestions[:3]]))
                    
            except Exception as e:
                self.result_var.set(f"❌ Error: {str(e)}")
                
        elif value == 'C':
            self.result_var.set("0")
            self.expression_var.set("")
            
        elif value == 'CE':
            self.result_var.set("0")
            
        elif value == '⌫':
            if len(current) > 1:
                self.result_var.set(current[:-1])
            else:
                self.result_var.set("0")
                
        elif value in ['sin', 'cos', 'tan', 'ln', 'log', '√', 'x²', '1/x', 'n!']:
            try:
                num = float(current)
                result = self.controller.perform_unary_operation(num, value)
                if not result.startswith("❌"):
                    self.expression_var.set(f"{value}({num}) =")
                self.result_var.set(result)
                self.update_history()
            except ValueError:
                self.result_var.set("❌ Error: Invalid input")
                
        self.update_status()
        
    def toggle_history(self):
        """Toggle history panel visibility"""
        self.history_visible = not self.history_visible
        if self.history_visible:
            self.history_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            self.update_history()
        else:
            self.history_frame.pack_forget()
            
    def update_history(self):
        """Update the history display"""
        self.history_text.delete(1.0, tk.END)
        history = self.controller.get_history(limit=50)
        for entry in reversed(history):
            timestamp = entry.get('timestamp', '')[:16]
            expression = entry.get('expression', '')
            result = entry.get('result', '')
            self.history_text.insert(tk.END, f"{timestamp} | {expression} = {result}\n")
                
    def clear_history(self):
        """Clear history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.controller.clear_history()
            self.update_history()
            self.update_status("History cleared")
        
    def export_history(self):
        """Export history to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.controller.history.export_history(filename):
                messagebox.showinfo("Success", "History exported successfully!")
                self.update_status("History exported")
            else:
                messagebox.showerror("Error", "Failed to export history")
                
    def memory_store(self):
        """Store current value in memory"""
        try:
            value = float(self.result_var.get())
            self.controller.memory_store(value)
            self.update_status("Value stored in memory")
            self.enable_ai_response(f"💾 Stored {value} in memory")
        except ValueError:
            self.update_status("❌ Error: Invalid value")
            
    def memory_recall(self):
        """Recall memory value"""
        value = self.controller.memory_recall()
        if value != 0:
            self.result_var.set(str(value))
            self.update_status("Memory recalled")
            self.enable_ai_response(f"📤 Recalled {value} from memory")
        else:
            self.update_status("Memory is empty")
            
    def memory_clear(self):
        """Clear memory"""
        self.controller.memory_clear()
        self.update_status("Memory cleared")
        self.enable_ai_response("🗑️ Memory cleared")
        
    def memory_add(self):
        """Add current value to memory"""
        try:
            current = float(self.result_var.get())
            self.controller.memory_add(current)
            self.update_status("Added to memory")
            self.enable_ai_response(f"➕ Added {current} to memory")
        except ValueError:
            self.update_status("❌ Error: Invalid value")
            
    def update_status(self, message: Optional[str] = None):
        """Update status bar"""
        if message:
            self.status_var.set(message)
        else:
            self.status_var.set("Ready")
            
    def run(self):
        """Start the application"""
        self.window.mainloop()
