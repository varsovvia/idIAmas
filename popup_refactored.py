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
    Transparent overlay widget that creates a gradient fade effect.
    Attaches to scroll area viewport and tracks scrolling automatically.
    """
    
    def __init__(self, scroll_area: QScrollArea, fade_height: int = 64):
        super().__init__(scroll_area.viewport())
        self.scroll_area = scroll_area
        self.fade_height = fade_height
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
        """Update overlay position and size based on viewport"""
        if not self.scroll_area or not self.scroll_area.viewport():
            return
            
        viewport = self.scroll_area.viewport()
        viewport_rect = viewport.rect()
        
        # Position overlay to cover bottom of viewport
        bottom_fade_rect = viewport_rect
        bottom_fade_rect.setTop(max(0, viewport_rect.height() - self.fade_height))
        
        self.setGeometry(bottom_fade_rect)
        
        # Check if we need top fade (when scrolled down)
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar and scroll_bar.value() > 0:
            # Could implement top fade here if needed
            pass
    
    def get_background_colors(self):
        """Get background colors from application palette"""
        palette = self.palette()
        
        # Try to get the popup background color
        bg_color = palette.color(QPalette.ColorRole.Window)
        
        # If it's too dark/light, use a reasonable default
        if bg_color.lightness() < 50:  # Dark theme
            return QColor(26, 26, 46, 255), QColor(26, 26, 46, 0)
        else:  # Light theme
            return QColor(248, 249, 250, 255), QColor(248, 249, 250, 0)
    
    def paintEvent(self, event):
        """Paint the gradient fade overlay"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set composition mode for proper blending
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        
        # Get background colors
        bg_opaque, bg_transparent = self.get_background_colors()
        
        # Create vertical gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, bg_transparent)  # Top: transparent
        gradient.setColorAt(0.3, QColor(bg_opaque.red(), bg_opaque.green(), bg_opaque.blue(), 77))  # 30% opacity
        gradient.setColorAt(0.7, QColor(bg_opaque.red(), bg_opaque.green(), bg_opaque.blue(), 204))  # 80% opacity
        gradient.setColorAt(1.0, bg_opaque)  # Bottom: fully opaque
        
        # Apply gradient as brush and fill the rect
        painter.fillRect(self.rect(), QBrush(gradient))


class GrammarCard(QWidget):
    """Individual card widget for grammar explanations"""
    
    def __init__(self, word_data: dict):
        super().__init__()
        self.word_data = word_data
        self.setup_card()
    
    def setup_card(self):
        """Setup card appearance and content"""
        self.setObjectName("grammarCard")
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Word title
        word_label = QLabel(self.word_data.get('word', ''))
        word_label.setObjectName("wordTitle")
        layout.addWidget(word_label)
        
        # Grammatical function
        if self.word_data.get('function'):
            function_label = QLabel(f"({self.word_data['function']})")
            function_label.setObjectName("grammarFunction")
            layout.addWidget(function_label)
        
        # Explanation
        explanation_label = QLabel(self.word_data.get('explanation', ''))
        explanation_label.setObjectName("grammarExplanation")
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)


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
        
        # Footer with copy button and status
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
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        parent_layout.addWidget(header_frame)
    
    def create_tabs(self, parent_layout):
        """Create tab widget with translation content"""
        tab_widget = QTabWidget()
        tab_widget.setObjectName("mainTabs")
        
        # Original text tab
        if 'original' in self.translation_data:
            original_tab = self.create_text_tab(self.translation_data['original'])
            tab_widget.addTab(original_tab, "IT | Original")
        
        # Translation tab
        if 'translation' in self.translation_data:
            translation_tab = self.create_text_tab(self.translation_data['translation'])
            tab_widget.addTab(translation_tab, "ES | Translation")
        
        # Grammar tab with cards and fade overlay
        if 'grammar' in self.translation_data:
            grammar_tab = self.create_grammar_tab(self.translation_data['grammar'])
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
    
    def create_grammar_tab(self, content: str) -> QWidget:
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
        word_explanations = self.parse_grammar_content(content)
        
        if word_explanations:
            for word_data in word_explanations:
                card = GrammarCard(word_data)
                content_layout.addWidget(card)
        else:
            # Fallback for unparseable content
            fallback_label = QLabel(content)
            fallback_label.setWordWrap(True)
            fallback_label.setObjectName("fallbackText")
            content_layout.addWidget(fallback_label)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        tab_layout.addWidget(scroll_area)
        
        # Add fade overlay to scroll area
        fade_overlay = FadeOverlay(scroll_area)
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
        
        # Copy button
        copy_btn = QPushButton("⧉ Copy")
        copy_btn.setObjectName("copyButton")
        copy_btn.clicked.connect(self.copy_content)
        footer_layout.addWidget(copy_btn)
        
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
            if not line or line.startswith('-') is False:
                continue
                
            # Remove the leading dash
            line = line.lstrip('- ')
            
            # Parse "word: explanation (function)" format
            if ':' in line:
                parts = line.split(':', 1)
                word = parts[0].strip()
                rest = parts[1].strip()
                
                # Extract function from parentheses
                function = ''
                explanation = rest
                
                if '(' in rest and ')' in rest:
                    func_start = rest.rfind('(')
                    func_end = rest.rfind(')')
                    if func_start < func_end:
                        function = rest[func_start+1:func_end]
                        explanation = rest[:func_start].strip()
                
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
        
        # Define colors based on theme
        if palette.color(QPalette.ColorRole.Window).lightness() < 128:
            # Dark theme colors
            bg_primary = "rgba(26, 26, 46, 0.95)"
            bg_secondary = "rgba(16, 16, 32, 0.9)"
            text_primary = "#ffffff"
            text_secondary = "#a8a8a8"
            accent_color = "#00d4ff"
            card_bg = "rgba(255, 255, 255, 0.1)"
            border_color = "rgba(255, 255, 255, 0.2)"
        else:
            # Light theme colors
            bg_primary = "rgba(248, 249, 250, 0.95)"
            bg_secondary = "rgba(255, 255, 255, 0.9)"
            text_primary = "#2c3e50"
            text_secondary = "#6c757d"
            accent_color = "#007bff"
            card_bg = "rgba(255, 255, 255, 0.8)"
            border_color = "rgba(0, 0, 0, 0.1)"
        
        style = f"""
        QMainWindow {{
            background: transparent;
        }}
        
        #centralWidget {{
            background: {bg_primary};
            border-radius: 12px;
            border: 1px solid {border_color};
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
            letter-spacing: 1px;
        }}
        
        #titleAccent {{
            font-size: 24px;
            font-weight: 900;
            color: {accent_color};
            letter-spacing: 1px;
        }}
        
        #subtitle {{
            font-size: 12px;
            color: {text_secondary};
            font-weight: 400;
            margin-top: 2px;
        }}
        
        #closeButton {{
            background: transparent;
            border: 1px solid {border_color};
            border-radius: 16px;
            color: {text_secondary};
            font-size: 18px;
            font-weight: bold;
        }}
        
        #closeButton:hover {{
            background: rgba(255, 0, 0, 0.1);
            border-color: #ff6b6b;
            color: #ff6b6b;
        }}
        
        #mainTabs {{
            background: transparent;
            border: none;
        }}
        
        #mainTabs::pane {{
            border: 1px solid {border_color};
            border-radius: 8px;
            background: {bg_secondary};
        }}
        
        #mainTabs::tab-bar {{
            alignment: center;
        }}
        
        #mainTabs QTabBar::tab {{
            background: {bg_secondary};
            border: 1px solid {border_color};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            color: {text_secondary};
        }}
        
        #mainTabs QTabBar::tab:selected {{
            background: {bg_primary};
            color: {accent_color};
            border-bottom: 1px solid {bg_primary};
        }}
        
        #textDisplay {{
            background: transparent;
            border: none;
            color: {text_primary};
            font-size: 14px;
            line-height: 1.5;
            padding: 8px;
        }}
        
        #grammarScrollArea {{
            background: transparent;
            border: none;
        }}
        
        #grammarCard {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 8px;
            margin-bottom: 8px;
        }}
        
        #grammarCard:hover {{
            border-color: {accent_color};
            background: rgba(0, 212, 255, 0.05);
        }}
        
        #wordTitle {{
            color: {accent_color};
            font-size: 16px;
            font-weight: bold;
        }}
        
        #grammarFunction {{
            color: {text_secondary};
            font-size: 12px;
            font-style: italic;
        }}
        
        #grammarExplanation {{
            color: {text_primary};
            font-size: 14px;
            line-height: 1.4;
        }}
        
        #fallbackText {{
            color: {text_primary};
            font-size: 14px;
            line-height: 1.5;
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
            background: rgba(0, 212, 255, 0.8);
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
