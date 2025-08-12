#!/usr/bin/env python3
"""
Modern, professional PyQt6 popup with proper fade overlay implementation.
Implements non-blocking bottom fade for grammar cards display.
"""

import sys
import json
import tempfile
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QLabel, QPushButton, QTabWidget, QFrame, QTextEdit,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import (
    QPainter, QLinearGradient, QColor, QPalette, QBrush, QPen,
    QKeySequence, QFont, QPixmap, QShortcut
)


class FadeOverlay(QWidget):
    """
    Transparent overlay widget that creates a gradient fade effect on all sides.
    Attaches to scroll area viewport and tracks scrolling automatically.
    """
    
    def __init__(self, scroll_area: QScrollArea, fade_height: int = 64, background_color: str = "#0b0b0b"):
        super().__init__(scroll_area.viewport())
        self.scroll_area = scroll_area
        self.fade_height = fade_height
        self.background_color = background_color
        self.setup_overlay()
        self.connect_scroll_tracking()
    
    def setup_overlay(self):
        """Initialize overlay properties and attributes"""
        # Make transparent for mouse events but visible for painting
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        # Position overlay initially
        self.update_position()
        
        # Ensure overlay is on top
        self.raise_()
        self.show()
    
    def connect_scroll_tracking(self):
        """Connect to scroll events for position updates"""
        # Track vertical scrolling
        if self.scroll_area.verticalScrollBar():
            self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_position)
        
        # Track resize events
        self.scroll_area.viewport().resizeEvent = self.on_viewport_resize
    
    def on_viewport_resize(self, event):
        """Handle viewport resize events"""
        super(QWidget, self.scroll_area.viewport()).resizeEvent(event)
        self.update_position()
    
    def update_position(self):
        """Update overlay position and size to cover entire viewport"""
        if not self.scroll_area or not self.scroll_area.viewport():
            return
            
        viewport = self.scroll_area.viewport()
        viewport_rect = viewport.rect()
        
        # Cover the entire viewport for bottom fade
        self.setGeometry(viewport_rect)
    
    def paintEvent(self, event):
        """Paint bottom gradient fade to popup background color"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set composition mode for proper blending
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        
        rect = self.rect()
        fade_size = self.fade_height
        
        # Parse the background color
        bg_color = QColor(self.background_color)
        
        # Bottom gradient: fade from transparent to popup background color
        bottom_gradient = QLinearGradient(0, rect.height() - fade_size, 0, rect.height())
        bottom_gradient.setColorAt(0.0, QColor(bg_color.red(), bg_color.green(), bg_color.blue(), 0))      # Start: transparent
        bottom_gradient.setColorAt(0.5, QColor(bg_color.red(), bg_color.green(), bg_color.blue(), 128))   # Middle: semi-transparent
        bottom_gradient.setColorAt(1.0, QColor(bg_color.red(), bg_color.green(), bg_color.blue(), 255))   # End: solid popup background
        
        bottom_rect = rect
        bottom_rect.setTop(rect.height() - fade_size)
        painter.fillRect(bottom_rect, QBrush(bottom_gradient))


class GrammarCard(QWidget):
    """Individual card widget for grammar explanations with hover animations and enhanced details"""
    
    def __init__(self, word_data: dict):
        super().__init__()
        self.word_data = word_data
        self.shine_animation = None
        self.hover_animation = None
        self.is_hovered = False
        self.setup_card()
        self.setup_animations()
    
    def setup_card(self):
        """Setup card appearance and content with enhanced details"""
        self.setObjectName("grammarCard")
        
        # Create layout with better spacing
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Word title with larger, more prominent display
        word_label = QLabel(self.word_data.get('word', ''))
        word_label.setObjectName("wordTitle")
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(word_label)
        
        # Difficulty indicator if available
        if self.word_data.get('difficulty'):
            difficulty_label = QLabel(f"🎯 {self.word_data['difficulty'].upper()}")
            difficulty_label.setObjectName("difficultyIndicator")
            difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(difficulty_label)
        
        # Separator line for visual division
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("cardSeparator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Grammatical function with enhanced styling
        if self.word_data.get('function'):
            function_label = QLabel(f"📚 {self.word_data['function']}")
            function_label.setObjectName("grammarFunction")
            function_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(function_label)
        
        # Explanation with better formatting
        explanation_label = QLabel(self.word_data.get('explanation', ''))
        explanation_label.setObjectName("grammarExplanation")
        explanation_label.setWordWrap(True)
        explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(explanation_label)
        
        # Additional details section if available
        if self.word_data.get('additional_info'):
            details_label = QLabel(f"ℹ️ {self.word_data['additional_info']}")
            details_label.setObjectName("grammarDetails")
            details_label.setWordWrap(True)
            details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(details_label)
        
        # Usage examples if available
        if self.word_data.get('examples'):
            examples_label = QLabel(f"💡 Ejemplos: {self.word_data['examples']}")
            examples_label.setObjectName("grammarExamples")
            examples_label.setWordWrap(True)
            examples_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(examples_label)
    
    def setup_animations(self):
        """Setup hover and shine animations"""
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
        from PyQt6.QtWidgets import QGraphicsOpacityEffect, QGraphicsDropShadowEffect
        
        # Create shadow effect for hover glow
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setColor(QColor(76, 175, 80, 0))
        self.shadow_effect.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow_effect)
        
        # Hover animations
        self.shadow_animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.shadow_animation.setDuration(250)
        self.shadow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.color_animation = QPropertyAnimation(self.shadow_effect, b"color")
        self.color_animation.setDuration(250)
        self.color_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def enterEvent(self, event):
        """Handle mouse enter - start hover animation"""
        super().enterEvent(event)
        self.is_hovered = True
        
        # Start glow effect
        if self.shadow_animation:
            self.shadow_animation.stop()
            self.shadow_animation.setStartValue(0)
            self.shadow_animation.setEndValue(15)
            self.shadow_animation.start()
        
        if self.color_animation:
            self.color_animation.stop()
            self.color_animation.setStartValue(QColor(76, 175, 80, 0))
            self.color_animation.setEndValue(QColor(76, 175, 80, 80))
            self.color_animation.start()
        
        # Trigger shine effect
        self.start_shine_effect()
    
    def leaveEvent(self, event):
        """Handle mouse leave - reverse hover animation"""
        super().leaveEvent(event)
        self.is_hovered = False
        
        # Stop glow effect
        if self.shadow_animation:
            self.shadow_animation.stop()
            self.shadow_animation.setStartValue(15)
            self.shadow_animation.setEndValue(0)
            self.shadow_animation.start()
        
        if self.color_animation:
            self.color_animation.stop()
            self.color_animation.setStartValue(QColor(76, 175, 80, 80))
            self.color_animation.setEndValue(QColor(76, 175, 80, 0))
            self.color_animation.start()
    
    def start_shine_effect(self):
        """Start a subtle shine animation across the card"""
        if not self.is_hovered:
            return
            
        # Create a shine timer for periodic effect
        from PyQt6.QtCore import QTimer
        
        def create_shine():
            if self.is_hovered:  # Only shine if still hovered
                self.update()  # Trigger repaint for shine
                
        if not hasattr(self, 'shine_timer'):
            self.shine_timer = QTimer()
            self.shine_timer.timeout.connect(create_shine)
            self.shine_timer.setSingleShot(True)
            
        self.shine_timer.start(100)  # Delay shine slightly
    
    def paintEvent(self, event):
        """Custom paint event with shine effect"""
        super().paintEvent(event)
        
        if self.is_hovered:
            from PyQt6.QtGui import QPainter, QLinearGradient, QBrush
            
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Create subtle shine gradient
            shine_gradient = QLinearGradient(0, 0, self.width(), 0)
            shine_gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
            shine_gradient.setColorAt(0.3, QColor(76, 175, 80, 30))  # Green shine
            shine_gradient.setColorAt(0.7, QColor(76, 175, 80, 30))
            shine_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
            
            # Paint shine effect
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Overlay)
            painter.fillRect(self.rect(), QBrush(shine_gradient))


class PopupWindow(QMainWindow):
    """
    Modern, minimal popup window for displaying translation results.
    Features frameless design, rounded corners, shadow, and proper fade overlay.
    """
    
    closed = pyqtSignal()
    
    def __init__(self, translation_data: dict):
        super().__init__()
        self.translation_data = translation_data
        self.fade_overlays = []
        
        # Debug: Print what data we received
        print(f"🔍 PopupWindow received data: {list(translation_data.keys())}")
        for key, value in translation_data.items():
            if isinstance(value, str):
                print(f"  {key}: {len(value)} chars - {value[:100]}{'...' if len(value) > 100 else ''}")
            elif isinstance(value, list):
                print(f"  {key}: {len(value)} items - {value[:3]}{'...' if len(value) > 3 else ''}")
            else:
                print(f"  {key}: {type(value)} - {value}")
        
        self.setup_window()
        self.setup_ui()
        self.setup_shortcuts()
        self.apply_styles()
    
    def setup_window(self):
        """Configure window properties for modern appearance"""
        self.setWindowTitle("idIAmas - AI Translation")
        
        # Frameless, shadowed popup
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint  # We'll add our own shadow
        )
        
        # Enable translucent background for rounded corners
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Window size and positioning
        self.resize(900, 600)
        self.center_on_screen()
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
    
    def setup_ui(self):
        """Create and setup the user interface"""
        # Central widget with rounded background
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Root layout with consistent spacing
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)
        
        # Header
        self.create_header(root_layout)
        
        # Tab widget for content
        self.create_tabs(root_layout)
        
        # Footer with status (copy moved to header)
        self.create_footer(root_layout)
    
    def create_header(self, parent_layout):
        """Create header with title and close button"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title section
        title_layout = QVBoxLayout()
        
        # App title with modern styling
        title_widget = QWidget()
        title_row = QHBoxLayout(title_widget)
        title_row.setSpacing(0)
        title_row.setContentsMargins(0, 0, 0, 0)
        
        title_prefix = QLabel("id")
        title_prefix.setObjectName("titlePrefix")
        title_accent = QLabel("IA")
        title_accent.setObjectName("titleAccent")
        title_suffix = QLabel("mas")
        title_suffix.setObjectName("titleSuffix")
        
        title_row.addWidget(title_prefix)
        title_row.addWidget(title_accent)
        title_row.addWidget(title_suffix)
        title_row.addStretch()
        
        subtitle = QLabel("AI-Powered Language Learning")
        subtitle.setObjectName("subtitle")
        
        title_layout.addWidget(title_widget)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        # Spacer
        header_layout.addStretch()

        # Header actions: Copy + Close
        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)
        copy_btn = QPushButton("⧉ Copy")
        copy_btn.setObjectName("copyButton")
        copy_btn.setFixedHeight(32)
        copy_btn.clicked.connect(self.copy_content)
        actions.addWidget(copy_btn)

        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self.close)
        actions.addWidget(close_btn)

        header_layout.addLayout(actions)
        
        parent_layout.addWidget(header_frame)
    
    def create_tabs(self, parent_layout):
        """Create tab widget with translation content"""
        tab_widget = QTabWidget()
        tab_widget.setObjectName("mainTabs")
        
        # Original text tab
        original_content = self.translation_data.get('original', '')
        if original_content and original_content.strip():
            original_tab = self.create_text_tab(original_content)
            tab_widget.addTab(original_tab, "IT | Original")
        else:
            # Fallback: show raw data if original is empty
            fallback_content = str(self.translation_data.get('original', 'No original text available'))
            if fallback_content == 'No original text available':
                # Try to show the raw translation data for debugging
                fallback_content = f"Debug: Raw data keys: {list(self.translation_data.keys())}\n\nRaw content:\n{str(self.translation_data)}"
            fallback_tab = self.create_text_tab(fallback_content)
            tab_widget.addTab(fallback_tab, "IT | Original")
        
        # Translation tab
        translation_content = self.translation_data.get('translation', '')
        if translation_content and translation_content.strip():
            translation_tab = self.create_text_tab(translation_content)
            tab_widget.addTab(translation_tab, "ES | Translation")
        else:
            # Fallback: show raw data if translation is empty
            fallback_content = str(self.translation_data.get('translation', 'No translation available'))
            if fallback_content == 'No translation available':
                # Try to show the raw translation data for debugging
                fallback_content = f"Debug: Raw data keys: {list(self.translation_data.keys())}\n\nRaw content:\n{str(self.translation_data)}"
            fallback_tab = self.create_text_tab(fallback_content)
            tab_widget.addTab(fallback_tab, "ES | Translation")
        
        # Grammar tab with cards and fade overlay
        grammar_content = None
        if 'grammar_json' in self.translation_data:
            grammar_content = self.translation_data.get('grammar_json')
        elif 'grammar' in self.translation_data:
            grammar_content = self.translation_data.get('grammar')

        if grammar_content is not None:
            grammar_tab = self.create_grammar_tab(grammar_content)
            tab_widget.addTab(grammar_tab, "※ Grammar")
        else:
            # Fallback: show raw grammar data if available
            raw_grammar = self.translation_data.get('grammar', '')
            if raw_grammar:
                grammar_tab = self.create_grammar_tab(raw_grammar)
                tab_widget.addTab(grammar_tab, "※ Grammar")
        
        parent_layout.addWidget(tab_widget)
    
    def create_text_tab(self, content: str) -> QWidget:
        """Create a simple text display tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        
        text_edit = QTextEdit()
        text_edit.setObjectName("textDisplay")
        text_edit.setPlainText(content)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        return tab
    
    def get_background_color(self) -> str:
        """Get the primary background color from the stylesheet"""
        # Extract the background color from the stylesheet
        # This matches the bg_primary color defined in apply_styles
        return "#0b0b0b"
    
    def create_grammar_tab(self, content) -> QWidget:
        """Create grammar tab with scrollable cards and fade overlay"""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName("grammarScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)
        
        # Parse and create grammar cards
        # If content is already a JSON array/list, prefer that
        word_explanations = []
        try:
            import json
            if isinstance(content, list):
                for item in content:
                    word_explanations.append({
                        'word': item.get('word', ''),
                        'explanation': item.get('explanation', ''),
                        'function': item.get('function', ''),
                        'additional_info': item.get('additional_info', ''),
                        'examples': item.get('examples', ''),
                        'difficulty': item.get('difficulty', ''),
                    })
            elif isinstance(content, str):
                c = content.strip()
                if c.startswith('[') and c.endswith(']'):
                    grammar_items = json.loads(c)
                    for item in grammar_items:
                        word_explanations.append({
                            'word': item.get('word', ''),
                            'explanation': item.get('explanation', ''),
                            'function': item.get('function', ''),
                            'additional_info': item.get('additional_info', ''),
                            'examples': item.get('examples', ''),
                            'difficulty': item.get('difficulty', ''),
                        })
        except Exception:
            # Fall back to text parsing
            pass

        if not word_explanations:
            # Only attempt string parsing if the content is a string
            if isinstance(content, str):
                word_explanations = self.parse_grammar_content(content)
            else:
                word_explanations = []
        
        if word_explanations:
            for word_data in word_explanations:
                card = GrammarCard(word_data)
                content_layout.addWidget(card)
        else:
            # Fallback for unparseable content
            message = "No grammar explanation available."
            if isinstance(content, str) and content.strip():
                message = content
            fallback_label = QLabel(message)
            fallback_label.setWordWrap(True)
            fallback_label.setObjectName("fallbackText")
            content_layout.addWidget(fallback_label)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        tab_layout.addWidget(scroll_area)
        
        # Add fade overlay to scroll area
        # Use the exact background color from stylesheet for perfect blending
        fade_overlay = FadeOverlay(scroll_area, background_color=self.get_background_color())
        self.fade_overlays.append(fade_overlay)
        
        return tab
    
    def create_footer(self, parent_layout):
        """Create footer with copy button and status"""
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, 8, 0, 0)
        
        # Status text
        status_label = QLabel("Press Esc to close")
        status_label.setObjectName("statusText")
        footer_layout.addWidget(status_label)
        
        footer_layout.addStretch()
        
        parent_layout.addWidget(footer_frame)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Esc to close
        close_shortcut = QShortcut(QKeySequence("Escape"), self)
        close_shortcut.activated.connect(self.close)
        
        # Ctrl+C to copy
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        copy_shortcut.activated.connect(self.copy_content)
    
    def copy_content(self):
        """Copy current tab content to clipboard"""
        # Implementation for copying content
        pass
    
    def parse_grammar_content(self, content: str) -> list:
        """Parse grammar content into word explanation data"""
        word_explanations = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Handle lines that start with dash or just contain the word explanations
            if line.startswith('-'):
                line = line.lstrip('- ')
            
            # Parse "word: explanation (function)" format or similar variations
            if ':' in line:
                parts = line.split(':', 1)
                word = parts[0].strip()
                rest = parts[1].strip()
                
                # Extract function from parentheses - look for patterns like (sustantivo), (verbo), etc.
                function = ''
                explanation = rest
                
                # Look for parentheses containing grammatical function
                if '(' in rest and ')' in rest:
                    func_start = rest.rfind('(')
                    func_end = rest.rfind(')')
                    if func_start < func_end:
                        potential_function = rest[func_start+1:func_end]
                        # Only treat as function if it looks like a grammatical term
                        if any(term in potential_function.lower() for term in [
                            'sustantivo', 'verbo', 'adjetivo', 'adverbio', 'preposición', 
                            'conjunción', 'pronombre', 'artículo', 'presente', 'pasado',
                            'participio', 'infinitivo', 'singular', 'plural', 'femenino', 'masculino'
                        ]):
                            function = potential_function
                            explanation = rest[:func_start].strip()
                
                # Clean up the explanation - remove extra quotes or formatting
                explanation = explanation.strip('"\'""')
                
                if word and explanation:  # Only add if we have both word and explanation
                    word_explanations.append({
                        'word': word,
                        'explanation': explanation,
                        'function': function
                    })
        
        return word_explanations
    
    def center_on_screen(self):
        """Center the window on the screen"""
        if QApplication.primaryScreen():
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def apply_styles(self):
        """Apply modern styling to the popup"""
        # Get colors from palette for theme compatibility
        palette = self.palette()
        
        # High-contrast palette: almost black/white with blue accents
        bg_primary = "#0b0b0b"          # near black
        bg_secondary = "#111111"        # slightly lighter black
        text_primary = "#f4f4f4"        # near white
        text_secondary = "#b9b9b9"      # muted grey
        accent_color = "#2aa3ff"       # vivid blue
        card_bg = "#1a1a1a"            # dark card background
        border_color = "#2a2a2a"       # subtle dark border
        
        style = f"""
        QMainWindow {{
            background: transparent;
        }}
        
        #centralWidget {{
            background: {bg_primary};
            border-radius: 12px;
            border: none;
        }}
        
        #headerFrame {{
            background: transparent;
            border: none;
            padding: 8px 0px;
        }}
        
        #titlePrefix, #titleSuffix {{
            font-size: 24px;
            font-weight: 300;
            color: {text_primary};
        }}
        
        #titleAccent {{
            font-size: 24px;
            font-weight: 900;
            color: {accent_color};
        }}
        
        #subtitle {{
            font-size: 12px;
            color: {text_secondary};
            font-weight: 400;
        }}
        
        #closeButton {{
            background: transparent;
            border: none;
            border-radius: 16px;
            color: {text_secondary};
            font-size: 18px;
            font-weight: bold;
        }}
        
        #closeButton:hover {{
            background: rgba(255, 0, 0, 0.15);
            border: none;
            color: #ff6b6b;
        }}
        
        #closeButton:pressed {{
            background: rgba(255, 0, 0, 0.25);
        }}
        
        #mainTabs {{
            background: transparent;
            border: none;
        }}
        
        #mainTabs::pane {{
            border: none;
            border-radius: 8px;
            background: {bg_secondary};
        }}
        
        #mainTabs::tab-bar {{
            /* alignment: center; */
        }}
        
        #mainTabs QTabBar::tab {{
            background: {bg_secondary};
            border: none;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            color: {text_secondary};
        }}
        
        #mainTabs QTabBar::tab:hover {{
            background: rgba(42, 163, 255, 0.12);
            color: {accent_color};
        }}
        
        #mainTabs QTabBar::tab:selected {{
            background: {bg_primary};
            color: {accent_color};
            border: none;
        }}
        
        #textDisplay {{
            background: transparent;
            border: none;
            color: {text_primary};
            font-size: 14px;
            padding: 8px;
        }}
        
        #grammarScrollArea {{
            background: transparent;
            border: none;
        }}
        
        #grammarCard {{
            background: {card_bg};
            border: 2px solid {border_color};
            border-radius: 16px;
            margin-bottom: 16px;
            padding: 8px;
        }}
        
        #grammarCard:hover {{
            background: rgba(76, 175, 80, 0.15);
            border: 2px solid rgba(76, 175, 80, 0.5);
        }}
        
        #wordTitle {{
            color: {accent_color};
            font-size: 20px;
            font-weight: 900;
        }}
        
        #difficultyIndicator {{
            color: {accent_color};
            font-size: 14px;
            font-weight: 700;
        }}
        
        #grammarFunction {{
            color: {text_secondary};
            font-size: 14px;
            font-style: italic;
            font-weight: 600;
        }}
        
        #grammarExplanation {{
            color: {text_primary};
            font-size: 16px;
            font-weight: 500;
        }}
        
        #grammarDetails {{
            color: {text_secondary};
            font-size: 13px;
            font-style: italic;
        }}
        
        #grammarExamples {{
            color: {accent_color};
            font-size: 13px;
            font-weight: 500;
        }}
        
        #cardSeparator {{
            background: {accent_color};
            opacity: 0.6;
        }}
        
        #fallbackText {{
            color: {text_primary};
            font-size: 14px;
        }}
        
        #footerFrame {{
            background: transparent;
            border: none;
        }}
        
        #statusText {{
            color: {text_secondary};
            font-size: 12px;
        }}
        
        #copyButton {{
            background: {accent_color};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: 600;
        }}
        
        #copyButton:hover {{
            background: rgba(0, 212, 255, 0.9);
        }}
        
        #copyButton:pressed {{
            background: rgba(0, 212, 255, 0.7);
        }}
        
        QScrollBar:vertical {{
            background: {bg_secondary};
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {border_color};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {accent_color};
        }}
        
        QScrollBar::handle:vertical:pressed {{
            background: rgba(0, 212, 255, 0.8);
        }}
        """
        
        self.setStyleSheet(style)
    
    def paintEvent(self, event):
        """Custom paint event for rounded background"""
        # Let the base paint event handle the translucent background
        super().paintEvent(event)
    
    def closeEvent(self, event):
        """Handle close event"""
        self.closed.emit()
        event.accept()


def create_sample_data():
    """Create sample translation data for testing"""
    return {
        'original': 'Che poi ti vengo a cercare',
        'translation': 'Que luego vengo a buscarte',
        'grammar': '''- Che: que (conjunción)
- poi: luego (adverbio)
- ti: a ti (pronombre de objeto indirecto)
- vengo: vengo (verbo venir en primera persona del singular, presente indicativo)
- a: a (preposición que introduce el complemento de régimen)
- cercare: buscar (verbo en infinitivo)'''
    }


def main():
    """Main function for testing the popup"""
    # Enable high DPI support (Qt6 handles high DPI automatically)
    app = QApplication(sys.argv)
    
    # Create and show popup with sample data
    sample_data = create_sample_data()
    popup = PopupWindow(sample_data)
    popup.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
