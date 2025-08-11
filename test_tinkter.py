import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime

class ModernTranslationUI:
    def __init__(self, texto):
        self.ventana = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.parse_and_display_text(texto)
        self.setup_bindings()
        
    def setup_window(self):
        """Configure the main window"""
        self.ventana.overrideredirect(True)
        self.ventana.attributes("-topmost", True)
        self.ventana.attributes("-alpha", 0.98)
        self.ventana.configure(bg='#1a1a1a')
        
        # Window size and position
        ancho, alto = 900, 600
        x, y = 100, 100
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Store for window movement
        self.x = 0
        self.y = 0
        
    def create_widgets(self):
        """Create and configure all UI widgets"""
        # Title bar
        self.create_title_bar()
        
        # Main content area
        self.create_content_area()
        
        # Status bar
        self.create_status_bar()
        
    def create_title_bar(self):
        """Create a custom title bar"""
        title_bar = tk.Frame(self.ventana, bg='#2d2d2d', height=40)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            title_bar, 
            text="🎯 idIAmas - Traducción & Aprendizaje", 
            bg='#2d2d2d', 
            fg='#ffffff',
            font=("Segoe UI", 10, "bold")
        )
        title_label.pack(side='left', padx=15, pady=10)
        
        # Close button
        close_btn = tk.Button(
            title_bar,
            text="✕",
            command=self.ventana.destroy,
            bg='#2d2d2d',
            fg='#ff6b6b',
            bd=0,
            font=("Segoe UI", 12, "bold"),
            activebackground='#ff6b6b',
            activeforeground='white',
            highlightthickness=0,
            relief='flat',
            width=3
        )
        close_btn.pack(side='right', padx=10, pady=5)
        
        # Bind title bar for window movement
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)
        
    def create_content_area(self):
        """Create the main content area with notebook tabs"""
        # Main content frame
        content_frame = tk.Frame(self.ventana, bg='#1a1a1a')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2d2d2d', foreground='#ffffff', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#4a4a4a'), ('active', '#3a3a3a')])
        
        # Create tabs
        self.create_translation_tab()
        self.create_grammar_tab()
        self.create_original_tab()
        
    def create_translation_tab(self):
        """Create the translation tab"""
        translation_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(translation_frame, text="🇪🇸 Traducción")
        
        # Translation text area
        self.translation_text = tk.Text(
            translation_frame,
            wrap='word',
            bg='#1a1a1a',
            fg='#ffffff',
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5
        )
        
        # Scrollbar for translation
        translation_scrollbar = tk.Scrollbar(translation_frame, orient='vertical', command=self.translation_text.yview)
        self.translation_text.configure(yscrollcommand=translation_scrollbar.set)
        
        self.translation_text.pack(side='left', fill='both', expand=True)
        translation_scrollbar.pack(side='right', fill='y')
        
    def create_grammar_tab(self):
        """Create the grammar analysis tab"""
        grammar_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(grammar_frame, text="📚 Gramática")
        
        # Grammar text area
        self.grammar_text = tk.Text(
            grammar_frame,
            wrap='word',
            bg='#1a1a1a',
            fg='#87ceeb',  # Light blue for grammar
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5
        )
        
        # Scrollbar for grammar
        grammar_scrollbar = tk.Scrollbar(grammar_frame, orient='vertical', command=self.grammar_text.yview)
        self.grammar_text.configure(yscrollcommand=grammar_scrollbar.set)
        
        self.grammar_text.pack(side='left', fill='both', expand=True)
        grammar_scrollbar.pack(side='right', fill='y')
        
    def create_original_tab(self):
        """Create the original text tab"""
        original_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(original_frame, text="🇮🇹 Original")
        
        # Original text area
        self.original_text = tk.Text(
            original_frame,
            wrap='word',
            bg='#1a1a1a',
            fg='#98fb98',  # Light green for original
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5
        )
        
        # Scrollbar for original
        original_scrollbar = tk.Scrollbar(original_frame, orient='vertical', command=self.original_text.yview)
        self.original_text.configure(yscrollcommand=original_scrollbar.set)
        
        self.original_text.pack(side='left', fill='both', expand=True)
        original_scrollbar.pack(side='right', fill='y')
        
    def create_status_bar(self):
        """Create a status bar at the bottom"""
        status_frame = tk.Frame(self.ventana, bg='#2d2d2d', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_label = tk.Label(
            status_frame,
            text=f"🕒 Traducido a las {timestamp}",
            bg='#2d2d2d',
            fg='#888888',
            font=("Segoe UI", 8)
        )
        status_label.pack(side='left', padx=15, pady=5)
        
        # Instructions
        instructions = tk.Label(
            status_frame,
            text="💡 Arrastra la barra de título para mover la ventana",
            bg='#2d2d2d',
            fg='#888888',
            font=("Segoe UI", 8)
        )
        instructions.pack(side='right', padx=15, pady=5)
        
    def parse_and_display_text(self, texto):
        """Parse the AI response and display it in appropriate tabs"""
        try:
            # Split the text into sections
            sections = self.parse_ai_response(texto)
            
            # Display in appropriate tabs
            if sections.get('original'):
                self.original_text.insert('1.0', sections['original'])
                self.original_text.config(state='disabled')
                
            if sections.get('translation'):
                self.translation_text.insert('1.0', sections['translation'])
                self.translation_text.config(state='disabled')
                
            if sections.get('grammar'):
                self.grammar_text.insert('1.0', sections['grammar'])
                self.grammar_text.config(state='disabled')
                
            # If no sections found, put everything in translation tab
            if not any(sections.values()):
                self.translation_text.insert('1.0', texto)
                self.translation_text.config(state='disabled')
                
        except Exception as e:
            # Fallback: display original text
            self.translation_text.insert('1.0', texto)
            self.translation_text.config(state='disabled')
            
    def parse_ai_response(self, texto):
        """Parse the AI response into structured sections"""
        sections = {
            'original': '',
            'translation': '',
            'grammar': ''
        }
        
        # Try to find structured sections
        lines = texto.split('\n')
        current_section = 'translation'  # default
        
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
        
    def setup_bindings(self):
        """Setup keyboard shortcuts and other bindings"""
        # Escape key to close
        self.ventana.bind('<Escape>', lambda e: self.ventana.destroy())
        
        # Ctrl+Q to close
        self.ventana.bind('<Control-q>', lambda e: self.ventana.destroy())
        
        # Tab navigation
        self.ventana.bind('<Control-Tab>', self.next_tab)
        self.ventana.bind('<Control-Shift-Tab>', self.prev_tab)
        
    def next_tab(self, event=None):
        """Navigate to next tab"""
        current = self.notebook.index(self.notebook.select())
        next_tab = (current + 1) % self.notebook.index('end')
        self.notebook.select(next_tab)
        
    def prev_tab(self, event=None):
        """Navigate to previous tab"""
        current = self.notebook.index(self.notebook.select())
        prev_tab = (current - 1) % self.notebook.index('end')
        self.notebook.select(prev_tab)
        
    def start_move(self, event):
        """Start window movement"""
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        """Execute window movement"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.ventana.winfo_x() + deltax
        new_y = self.ventana.winfo_y() + deltay
        self.ventana.geometry(f"+{new_x}+{new_y}")
        
    def run(self):
        """Start the UI"""
        self.ventana.mainloop()

def mostrar_explicacion(texto):
    """Main function to display translation results"""
    app = ModernTranslationUI(texto)
    app.run()

if __name__ == "__main__":
    texto_ejemplo = (
        "Texto original: Ciao, come stai?\n\n"
        "Traducción al español: Hola, ¿cómo estás?\n\n"
        "Explicación gramatical:\n"
        "- Ciao: saludo informal en italiano\n"
        "- come: cómo (adverbio interrogativo)\n"
        "- stai: segunda persona del verbo 'stare' (estar)\n\n"
        "La frase usa la forma informal de preguntar por el estado de alguien."
    )
    mostrar_explicacion(texto_ejemplo)
