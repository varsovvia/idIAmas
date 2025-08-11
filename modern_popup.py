#!/usr/bin/env python3
"""
Modern Desktop Popup for idIAmas
A beautiful, modern popup that appears over your content while watching
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class ModernPopup:
    def __init__(self, translation_data):
        self.translation_data = translation_data
        self.root = None
        self.create_popup()
        
    def create_popup(self):
        """Create the modern popup window"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("🎯 idIAmas - Traducción")
        
        # Configure window properties
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Center the window
        self.center_window()
        
        # Apply modern styling
        self.root.configure(bg='#0a0a0a')
        
        # Create main container
        main_frame = tk.Frame(self.root, bg='#0a0a0a', relief='flat')
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
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
        """Create the header section"""
        header_frame = tk.Frame(parent, bg='#1a1a1a', height=80, relief='flat')
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # App info (left side)
        app_info_frame = tk.Frame(header_frame, bg='#1a1a1a')
        app_info_frame.pack(side='left', padx=24, pady=16)
        
        title_label = tk.Label(app_info_frame, text="🎯 idIAmas", 
                              font=('Segoe UI', 20, 'bold'), 
                              fg='#ffffff', bg='#1a1a1a')
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(app_info_frame, text="Traducción & Aprendizaje", 
                                 font=('Segoe UI', 14), 
                                 fg='#888888', bg='#1a1a1a')
        subtitle_label.pack(anchor='w')
        
        # Right side elements
        right_frame = tk.Frame(header_frame, bg='#1a1a1a')
        right_frame.pack(side='right', padx=24, pady=16)
        
        # Timestamp
        timestamp_label = tk.Label(right_frame, text=time.strftime("%H:%M:%S"), 
                                  font=('Segoe UI', 12), 
                                  fg='#666666', bg='#1a1a1a')
        timestamp_label.pack(side='top')
        
        # Close button
        close_btn = tk.Button(right_frame, text="✕", 
                             font=('Segoe UI', 12, 'bold'),
                             fg='#ffffff', bg='#ef4444', 
                             activebackground='#dc2626',
                             relief='flat', cursor='hand2',
                             command=self.close_popup)
        close_btn.configure(width=3, height=1)
        close_btn.pack(side='bottom')
        
    def create_notebook(self, parent):
        """Create the tabbed content area"""
        # Create notebook with custom styling
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure notebook style
        style.configure('Custom.TNotebook', background='#0a0a0a', borderwidth=0)
        style.configure('Custom.TNotebook.Tab', 
                       background='#1a1a1a', 
                       foreground='#888888',
                       padding=[24, 12],
                       font=('Segoe UI', 12, 'bold'))
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', '#2d2d2d'), ('active', '#2d2d2d')],
                  foreground=[('selected', '#ffffff'), ('active', '#cccccc')])
        
        # Create notebook
        self.notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Create tabs
        self.create_translation_tab()
        self.create_grammar_tab()
        self.create_original_tab()
        
    def create_translation_tab(self):
        """Create the translation tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0a0a0a')
        self.notebook.add(tab_frame, text="🇪🇸 Traducción")
        
        # Tab header
        header_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        header_frame.pack(fill='x', padx=24, pady=24)
        
        title_label = tk.Label(header_frame, text="🇪🇸 Traducción", 
                              font=('Segoe UI', 18, 'bold'), 
                              fg='#3b82f6', bg='#0a0a0a')
        title_label.pack(side='left')
        
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 12, 'bold'),
                            fg='#ffffff', bg='#10b981', 
                            activebackground='#059669',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('translation', '')))
        copy_btn.pack(side='right')
        
        # Content area
        content_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        content_frame.pack(fill='both', expand=True, padx=24, pady=0)
        
        # Text widget with scrollbar
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a1a', 
                             fg='#ffffff',
                             font=('Segoe UI', 14),
                             relief='flat',
                             borderwidth=1,
                             padx=16, pady=16,
                             state='disabled')
        
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('translation', ''))
        text_widget.configure(state='disabled')
        
    def create_grammar_tab(self):
        """Create the grammar tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0a0a0a')
        self.notebook.add(tab_frame, text="📚 Gramática")
        
        # Tab header
        header_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        header_frame.pack(fill='x', padx=24, pady=24)
        
        title_label = tk.Label(header_frame, text="📚 Gramática", 
                              font=('Segoe UI', 18, 'bold'), 
                              fg='#10b981', bg='#0a0a0a')
        title_label.pack(side='left')
        
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 12, 'bold'),
                            fg='#ffffff', bg='#10b981', 
                            activebackground='#059669',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('grammar', '')))
        copy_btn.pack(side='right')
        
        # Content area
        content_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        content_frame.pack(fill='both', expand=True, padx=24, pady=0)
        
        # Text widget with scrollbar
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a1a', 
                             fg='#ffffff',
                             font=('Segoe UI', 14),
                             relief='flat',
                             borderwidth=1,
                             padx=16, pady=16,
                             state='disabled')
        
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('grammar', ''))
        text_widget.configure(state='disabled')
        
    def create_original_tab(self):
        """Create the original text tab"""
        tab_frame = tk.Frame(self.notebook, bg='#0a0a0a')
        self.notebook.add(tab_frame, text="🇮🇹 Original")
        
        # Tab header
        header_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        header_frame.pack(fill='x', padx=24, pady=24)
        
        title_label = tk.Label(header_frame, text="🇮🇹 Original", 
                              font=('Segoe UI', 18, 'bold'), 
                              fg='#f59e0b', bg='#0a0a0a')
        title_label.pack(side='left')
        
        copy_btn = tk.Button(header_frame, text="📋 Copiar", 
                            font=('Segoe UI', 12, 'bold'),
                            fg='#ffffff', bg='#10b981', 
                            activebackground='#059669',
                            relief='flat', cursor='hand2',
                            command=lambda: self.copy_to_clipboard(self.translation_data.get('original', '')))
        copy_btn.pack(side='right')
        
        # Content area
        content_frame = tk.Frame(tab_frame, bg='#0a0a0a')
        content_frame.pack(fill='both', expand=True, padx=24, pady=0)
        
        # Text widget with scrollbar
        text_widget = tk.Text(content_frame, 
                             wrap='word', 
                             bg='#1a1a1a', 
                             fg='#ffffff',
                             font=('Segoe UI', 14),
                             relief='flat',
                             borderwidth=1,
                             padx=16, pady=16,
                             state='disabled')
        
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert content
        text_widget.configure(state='normal')
        text_widget.insert('1.0', self.translation_data.get('original', ''))
        text_widget.configure(state='disabled')
        
    def create_footer(self, parent):
        """Create the footer section"""
        footer_frame = tk.Frame(parent, bg='#1a1a1a', height=60, relief='flat')
        footer_frame.pack(fill='x', padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        # Instructions (left side)
        instructions_label = tk.Label(footer_frame, text="Presiona 'i' para traducir, 'q' para salir", 
                                     font=('Segoe UI', 12), 
                                     fg='#666666', bg='#1a1a1a')
        instructions_label.pack(side='left', padx=24, pady=12)
        
        # Status (right side)
        status_label = tk.Label(footer_frame, text="🎯 Aprendiendo Italiano", 
                               font=('Segoe UI', 12), 
                               fg='#666666', bg='#1a1a1a')
        status_label.pack(side='right', padx=24, pady=12)
        
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
        """Show visual feedback for copy action"""
        feedback_label = tk.Label(self.root, text="¡Copiado! ✓", 
                                 font=('Segoe UI', 12, 'bold'),
                                 fg='#ffffff', bg='#10b981',
                                 relief='flat')
        feedback_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Hide after 2 seconds
        self.root.after(2000, feedback_label.destroy)
        
    def close_popup(self):
        """Close the popup"""
        if self.root:
            self.root.destroy()
            self.root = None
            
    def show(self):
        """Show the popup"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

def mostrar_explicacion_moderna(texto: str):
    """Main function to display translation results in the modern popup"""
    # Parse the AI response
    sections = parse_ai_response(texto)
    
    # Create and show the popup
    popup = ModernPopup(sections)
    popup.show()
    
    # Return the popup instance
    return popup

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
    # Test the modern popup
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
    
    # For testing, run the main loop
    if popup.root:
        popup.root.mainloop()
