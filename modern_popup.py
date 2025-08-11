#!/usr/bin/env python3
"""
Modern Desktop Popup for idIAmas
A beautiful, modern popup that appears over your content while watching
"""

import tkinter as tk
from tkinter import ttk
import time
import threading
import queue

class ModernPopup:
    def __init__(self, translation_data):
        self.translation_data = translation_data
        self.root = None
        self.popup_queue = queue.Queue()
        self.create_popup()
        
    def create_popup(self):
        """Create the modern popup window"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("🎯 idIAmas - Traducción")
        
        # Configure window properties
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Center the window
        self.center_window()
        
        # Apply modern styling with enhanced colors
        self.root.configure(bg='#0f0f23')  # Darker, more sophisticated background
        
        # Create main container with subtle border
        main_frame = tk.Frame(self.root, bg='#0f0f23', relief='flat')
        main_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Create header
        self.create_header(main_frame)
        
        # Create notebook (tabs)
        self.create_notebook(main_frame)
        
        # Create footer
        self.create_footer(main_frame)
        
        # Bind events
        self.root.bind('<Escape>', lambda e: self.close_popup())
        self.root.bind('<q>', lambda e: self.close_popup())
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
    def create_header(self, parent):
        """Create the enhanced header section"""
        header_frame = tk.Frame(parent, bg='#1a1a2e', height=90, relief='flat')
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Add subtle border effect
        border_frame = tk.Frame(header_frame, bg='#16213e', height=2)
        border_frame.pack(fill='x', side='bottom')
        
        # App info (left side)
        app_info_frame = tk.Frame(header_frame, bg='#1a1a2e')
        app_info_frame.pack(side='left', padx=28, pady=20)
        
        # Enhanced title with gradient effect simulation
        title_label = tk.Label(app_info_frame, text="🎯 idIAmas", 
                              font=('Segoe UI', 24, 'bold'), 
                              fg='#00d4ff', bg='#1a1a2e')  # Bright cyan
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(app_info_frame, text="Traducción & Aprendizaje Inteligente", 
                                 font=('Segoe UI', 14), 
                                 fg='#a8a8a8', bg='#1a1a2e')  # Softer gray
        subtitle_label.pack(anchor='w')
        
        # Right side elements
        right_frame = tk.Frame(header_frame, bg='#1a1a2e')
        right_frame.pack(side='right', padx=28, pady=20)
        
        # Enhanced timestamp with better styling
        timestamp_label = tk.Label(right_frame, text=time.strftime("%H:%M:%S"), 
                                  font=('Segoe UI', 13, 'bold'), 
                                  fg='#4ecdc4', bg='#1a1a2e')  # Teal color
        timestamp_label.pack(side='top')
        
        # Enhanced close button with hover effect
        close_btn = tk.Button(right_frame, text="✕", 
                             font=('Segoe UI', 14, 'bold'),
                             fg='#ffffff', bg='#ff6b6b',  # Modern red
                             activebackground='#ee5a52',
                             relief='flat', cursor='hand2',
                             command=self.close_popup)
        close_btn.configure(width=3, height=1)
        close_btn.pack(side='bottom')
        
        # Add hover effect
        close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#ff5252'))
        close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#ff6b6b'))
        
    def create_notebook(self, parent):
        """Create the enhanced tabbed content area"""
        # Create notebook with custom styling
        style = ttk.Style()
        style.theme_use('default')
        
        # Enhanced notebook style with better colors
        style.configure('Custom.TNotebook', background='#0f0f23', borderwidth=0)
        style.configure('Custom.TNotebook.Tab', 
                       background='#1a1a2e', 
                       foreground='#a8a8a8',
                       padding=[28, 16],
                       font=('Segoe UI', 13, 'bold'))
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', '#16213e'), ('active', '#1e1e3f')],
                  foreground=[('selected', '#00d4ff'), ('active', '#4ecdc4')])
        
        # Create notebook
        self.notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Create tabs
        self.create_translation_tab()
        self.create_grammar_tab()
        self.create_original_tab()
        
    def create_translation_tab(self):
        """Create the enhanced translation tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0f0f23')
        self.notebook.add(tab_frame, text="🇪🇸 Traducción")
        
        # Tab header with enhanced styling
        header_frame = tk.Frame(tab_frame, bg='#0f0f23')
        header_frame.pack(fill='x', padx=28, pady=28)
        
        # Enhanced title with accent color
        title_label = tk.Label(header_frame, text="🇪🇸 Traducción", 
                              font=('Segoe UI', 20, 'bold'), 
                              fg='#00d4ff', bg='#0f0f23')  # Bright cyan
        title_label.pack(side='left')
        
        # Enhanced copy button with modern styling
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 13, 'bold'),
                            fg='#ffffff', bg='#4ecdc4',  # Teal
                            activebackground='#45b7aa',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('translation', '')))
        copy_btn.pack(side='right')
        
        # Add hover effect
        copy_btn.bind('<Enter>', lambda e: copy_btn.configure(bg='#45b7aa'))
        copy_btn.bind('<Leave>', lambda e: copy_btn.configure(bg='#4ecdc4'))
        
        # Content area with enhanced styling
        content_frame = tk.Frame(tab_frame, bg='#0f0f23')
        content_frame.pack(fill='both', expand=True, padx=28, pady=0)
        
        # Enhanced text widget with better styling
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a2e',  # Darker background
                             fg='#ffffff',
                             font=('Segoe UI', 15),  # Larger font
                             relief='flat',
                             borderwidth=0,
                             padx=20, pady=20,
                             state='disabled',
                             selectbackground='#00d4ff',  # Cyan selection
                             selectforeground='#000000')
        
        # Enhanced scrollbar
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('translation', ''))
        text_widget.configure(state='disabled')
        
    def create_grammar_tab(self):
        """Create the enhanced grammar tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0f0f23')
        self.notebook.add(tab_frame, text="📚 Gramática")
        
        # Tab header with enhanced styling
        header_frame = tk.Frame(tab_frame, bg='#0f0f23')
        header_frame.pack(fill='x', padx=28, pady=28)
        
        # Enhanced title with accent color
        title_label = tk.Label(header_frame, text="📚 Gramática", 
                              font=('Segoe UI', 20, 'bold'), 
                              fg='#4ecdc4', bg='#0f0f23')  # Teal
        title_label.pack(side='left')
        
        # Enhanced copy button
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 13, 'bold'),
                            fg='#ffffff', bg='#4ecdc4', 
                            activebackground='#45b7aa',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('grammar', '')))
        copy_btn.pack(side='right')
        
        # Add hover effect
        copy_btn.bind('<Enter>', lambda e: copy_btn.configure(bg='#45b7aa'))
        copy_btn.bind('<Leave>', lambda e: copy_btn.configure(bg='#4ecdc4'))
        
        # Content area with enhanced styling
        content_frame = tk.Frame(tab_frame, bg='#0f0f23')
        content_frame.pack(fill='both', expand=True, padx=28, pady=0)
        
        # Enhanced text widget
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a2e',
                             fg='#ffffff',
                             font=('Segoe UI', 15),
                             relief='flat',
                             borderwidth=0,
                             padx=20, pady=20,
                             state='disabled',
                             selectbackground='#4ecdc4',
                             selectforeground='#000000')
        
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('grammar', ''))
        text_widget.configure(state='disabled')
        
    def create_original_tab(self):
        """Create the enhanced original text tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0f0f23')
        self.notebook.add(tab_frame, text="🇮🇹 Original")
        
        # Tab header with enhanced styling
        header_frame = tk.Frame(tab_frame, bg='#0f0f23')
        header_frame.pack(fill='x', padx=28, pady=28)
        
        # Enhanced title with accent color
        title_label = tk.Label(header_frame, text="🇮🇹 Original", 
                              font=('Segoe UI', 20, 'bold'), 
                              fg='#ffa726', bg='#0f0f23')  # Orange
        title_label.pack(side='left')
        
        # Enhanced copy button
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 13, 'bold'),
                            fg='#ffffff', bg='#4ecdc4', 
                            activebackground='#45b7aa',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('original', '')))
        copy_btn.pack(side='right')
        
        # Add hover effect
        copy_btn.bind('<Enter>', lambda e: copy_btn.configure(bg='#45b7aa'))
        copy_btn.bind('<Leave>', lambda e: copy_btn.configure(bg='#4ecdc4'))
        
        # Content area with enhanced styling
        content_frame = tk.Frame(tab_frame, bg='#0f0f23')
        content_frame.pack(fill='both', expand=True, padx=28, pady=0)
        
        # Enhanced text widget
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a2e',
                             fg='#ffffff',
                             font=('Segoe UI', 15),
                             relief='flat',
                             borderwidth=0,
                             padx=20, pady=20,
                             state='disabled',
                             selectbackground='#ffa726',
                             selectforeground='#000000')
        
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('original', ''))
        text_widget.configure(state='disabled')
        
    def create_footer(self, parent):
        """Create the enhanced footer section"""
        footer_frame = tk.Frame(parent, bg='#1a1a2e', height=70, relief='flat')
        footer_frame.pack(fill='x', padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        # Add subtle border effect
        border_frame = tk.Frame(footer_frame, bg='#16213e', height=2)
        border_frame.pack(fill='x', side='top')
        
        # Instructions (left side) with enhanced styling
        instructions_label = tk.Label(footer_frame, text="Presiona 'i' para traducir, 'q' para salir", 
                                     font=('Segoe UI', 13), 
                                     fg='#a8a8a8', bg='#1a1a2e')
        instructions_label.pack(side='left', padx=28, pady=16)
        
        # Status (right side) with enhanced styling
        status_label = tk.Label(footer_frame, text="🎯 Aprendiendo Italiano", 
                               font=('Segoe UI', 13, 'bold'), 
                               fg='#4ecdc4', bg='#1a1a2e')  # Teal accent
        status_label.pack(side='right', padx=28, pady=16)
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def start_move(self, event):
        """Start window movement"""
        self.x = event.x
        self.y = event.y
        
    def on_move(self, event):
        """Handle window movement"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        
        # Show feedback
        self.show_copy_feedback()
        
    def show_copy_feedback(self):
        """Show enhanced visual feedback for copy action"""
        # Create a modern feedback label
        feedback_label = tk.Label(self.root, text="¡Copiado! ✓", 
                                 font=('Segoe UI', 14, 'bold'),
                                 fg='#ffffff', bg='#4ecdc4',
                                 relief='flat')
        feedback_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Hide after 2 seconds
        self.root.after(2000, feedback_label.destroy)
        
    def close_popup(self):
        """Close the popup"""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None
            
    def show(self):
        """Show the popup"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
    def run(self):
        """Run the popup in its own event loop"""
        if self.root:
            self.root.mainloop()

# Global popup manager
_popup_manager = None

def mostrar_explicacion_moderna(texto: str):
    """Main function to display translation results in the modern popup"""
    global _popup_manager
    
    # Parse the AI response
    sections = parse_ai_response(texto)
    
    # Create popup in a separate thread to avoid blocking
    def create_popup():
        popup = ModernPopup(sections)
        popup.show()
        popup.run()
    
    # Start popup in background thread
    popup_thread = threading.Thread(target=create_popup, daemon=True)
    popup_thread.start()
    
    # Return immediately so main app continues
    return None

def parse_ai_response(texto: str) -> dict:
    """Parse the AI response into structured sections"""
    sections = {
        'original': '',
        'translation': '',
        'grammar': ''
    }
    
    lines = texto.split('\n')
    current_section = 'translation'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect section headers
        if any(keyword in line.lower() for keyword in ['italiano', 'original', 'frase']):
            current_section = 'original'
            continue
        elif any(keyword in line.lower() for keyword in ['español', 'traducción', 'traducida']):
            current_section = 'translation'
            continue
        elif any(keyword in line.lower() for keyword in ['gramática', 'explicación', 'palabras', 'función']):
            current_section = 'grammar'
            continue
            
        # Add line to current section
        if current_section in sections:
            sections[current_section] += line + '\n'
            
    return sections

if __name__ == "__main__":
    # Test the enhanced modern popup
    test_text = """
    TEXTO ORIGINAL:
    Ciao, come stai?
    
    TRADUCCIÓN AL ESPAÑOL:
    Hola, ¿cómo estás?
    
    EXPLICACIÓN GRAMATICAL:
    - Ciao: saludo informal en italiano
    - come: cómo (adverbio interrogativo)
    - stai: segunda persona del verbo 'stare' (estar)
    """
    
    popup = mostrar_explicacion_moderna(test_text)
    
    # For testing, we can wait a bit to see the popup
    import time
    time.sleep(5)
