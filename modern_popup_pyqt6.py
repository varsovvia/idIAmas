#!/usr/bin/env python3
"""
Modern PyQt6 Popup for idIAmas
A premium, modern popup with gradients, animations, and sleek design
"""

import sys
import time
import threading
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QTextEdit, QPushButton, 
                             QLabel, QFrame, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect,
                             QProgressBar, QGraphicsOpacityEffect, QGraphicsBlurEffect)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, 
                          QThread, pyqtSignal, QEventLoop, QParallelAnimationGroup, 
                          QSequentialAnimationGroup, QPropertyAnimation, QVariantAnimation)
from PyQt6.QtGui import (QFont, QPalette, QColor, QIcon, QPixmap, QPainter, QBrush, 
                         QLinearGradient, QPen, QGradient, QRadialGradient)

# Global QApplication manager
class QtAppManager:
    _instance = None
    _app = None
    _running = False
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_or_create_app(self):
        """Get or create QApplication instance"""
        if self._app is None:
            self._app = QApplication.instance()
            if self._app is None:
                self._app = QApplication(sys.argv)
        return self._app
    
    def start_event_processing(self):
        """Start processing events using QTimer"""
        if not self._running and self._app:
            self._running = True
            # Use QTimer to process events regularly
            self.timer = QTimer()
            self.timer.timeout.connect(self._process_events)
            self.timer.start(50)  # Process events every 50ms (less aggressive)
    
    def _process_events(self):
        """Process pending events safely"""
        try:
            if self._app:
                self._app.processEvents()
        except Exception as e:
            print(f"Event processing error: {e}")

class AnimationManager:
    """Manages all animations for the popup"""
    
    @staticmethod
    def create_fade_animation(widget, duration=300, start_opacity=0.0, end_opacity=1.0):
        """Create a fade animation for a widget"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        return animation
    
    @staticmethod
    def create_scale_animation(widget, duration=200, start_scale=0.95, end_scale=1.0):
        """Create a scale animation for button hover effects"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.OutBack)
        return animation
    
    @staticmethod
    def create_floating_animation(widget, start_pos, end_pos, duration=2000):
        """Create a floating animation for feedback elements"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.Type.OutQuart)
        return animation

class StyleManager:
    """Manages all styling for the popup"""
    
    # Premium color palette
    COLORS = {
        'primary_bg': '#0a0a0f',
        'secondary_bg': '#1a1a2e',
        'accent_bg': '#16213e',
        'glass_bg': 'rgba(26, 26, 46, 0.8)',
        'neon_cyan': '#00d4ff',
        'neon_teal': '#4ecdc4',
        'neon_orange': '#ffa726',
        'neon_red': '#ff6b6b',
        'text_primary': '#ffffff',
        'text_secondary': '#a8a8a8',
        'border_glow': '#2d2d4d',
        'success_green': '#4caf50',
        'warning_amber': '#ff9800'
    }
    
    @staticmethod
    def get_glassmorphism_style(bg_color, border_color, border_radius=16):
        """Generate glassmorphism style"""
        return f"""
            background: {bg_color};
            border: 1px solid {border_color};
            border-radius: {border_radius}px;
            backdrop-filter: blur(10px);
        """
    
    @staticmethod
    def get_premium_button_style(bg_gradient, hover_gradient, text_color='#ffffff'):
        """Generate premium button style with hover effects"""
        return f"""
            QPushButton {{
                background: {bg_gradient};
                color: {text_color};
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton:hover {{
                background: {hover_gradient};
            }}
            QPushButton:pressed {{
                transform: scale(0.98);
            }}
        """

class ModernPyQt6Popup(QMainWindow):
    def __init__(self, translation_data):
        super().__init__()
        self.translation_data = translation_data
        self.event_loop = None
        self.animation_group = QParallelAnimationGroup()
        self.floating_animations = []
        self.progress_timer = QTimer()
        self.progress_value = 0
        self.init_ui()
        self.setup_animations()
        # Temporarily disable dynamic effects to test basic functionality
        # self.setup_dynamic_effects()
        
    def init_ui(self):
        """Initialize the enhanced user interface"""
        # Set window properties
        self.setWindowTitle("🎯 idIAmas - Traducción")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |  # Always on top
            Qt.WindowType.FramelessWindowHint    # No window frame
            # Removed Tool flag to ensure it shows up
        )
        
        # Ensure the window is visible and active
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, False)
        
        # Set window size and position - make it shorter
        self.resize(900, 600)
        self.center_on_screen()
        
        # Apply premium futuristic styling
        self.setStyleSheet(self.get_premium_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Header
        self.create_enhanced_header(main_layout)
        
        # Tab widget
        self.create_enhanced_tabs(main_layout)
        
        # Footer
        self.create_enhanced_footer(main_layout)
    
    def get_premium_stylesheet(self):
        """Get the premium futuristic stylesheet"""
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {StyleManager.COLORS['primary_bg']}, 
                    stop:0.3 {StyleManager.COLORS['secondary_bg']}, 
                    stop:1 {StyleManager.COLORS['accent_bg']});
                border: 2px solid {StyleManager.COLORS['neon_cyan']};
                border-radius: 24px;
            }}
            
            QTabWidget::pane {{
                border: none;
                background: transparent;
                margin-top: 8px;
            }}
            
            QTabBar::tab {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(26, 26, 46, 0.6), 
                    stop:1 rgba(22, 33, 62, 0.6));
                color: {StyleManager.COLORS['text_secondary']};
                padding: 18px 36px;
                margin-right: 4px;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                font-weight: 600;
                font-size: 15px;
                border: 1px solid rgba(45, 45, 77, 0.5);
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }}
            
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_cyan']}, 
                    stop:1 {StyleManager.COLORS['neon_teal']});
                color: #000000;
                border: 2px solid {StyleManager.COLORS['neon_cyan']};
                font-weight: 700;
            }}
            
            QTabBar::tab:hover:!selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(30, 30, 63, 0.8), 
                    stop:1 rgba(45, 45, 79, 0.8));
                color: {StyleManager.COLORS['text_primary']};
                border: 1px solid {StyleManager.COLORS['neon_teal']};
            }}
            
            QTextEdit {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 26, 46, 0.9), 
                    stop:1 rgba(22, 33, 62, 0.9));
                color: {StyleManager.COLORS['text_primary']};
                border: 1px solid rgba(45, 45, 77, 0.6);
                border-radius: 18px;
                padding: 28px;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
                font-size: 17px;
                line-height: 1.7;
                selection-background-color: {StyleManager.COLORS['neon_cyan']};
                selection-color: #000000;
            }}
            
            QPushButton {{
                background: rgba(255, 255, 255, 0.08);
                color: #4ecdc4;
                border: 1px solid rgba(78, 205, 196, 0.3);
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 12px;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }}
            
            QPushButton:hover {{
                background: rgba(78, 205, 196, 0.15);
                border: 1px solid rgba(78, 205, 196, 0.5);
                color: #45b7aa;
            }}
            
            QPushButton:pressed {{
                background: rgba(78, 205, 196, 0.25);
                transform: scale(0.98);
            }}
            
            QPushButton#closeBtn {{
                background: rgba(255, 255, 255, 0.1);
                color: #999;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 0px;
            }}
            
            QPushButton#closeBtn:hover {{
                background: rgba(255, 70, 70, 0.8);
                color: white;
                border: 1px solid rgba(255, 70, 70, 1.0);
                transform: scale(1.05);
            }}
            
            QPushButton#closeBtn:pressed {{
                background: rgba(200, 50, 50, 0.9);
                transform: scale(0.95);
            }}
            
            QLabel {{
                color: {StyleManager.COLORS['text_primary']};
                font-weight: 500;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }}
            
            QLabel#titlePrefix {{
                font-size: 28px;
                font-weight: 300;
                color: {StyleManager.COLORS['text_primary']};
                letter-spacing: 1px;
                margin: 0px;
                padding: 0px;
            }}
            
            QLabel#titleAccent {{
                font-size: 28px;
                font-weight: 900;
                color: {StyleManager.COLORS['neon_cyan']};
                letter-spacing: 1px;
                margin: 0px;
                padding: 0px;
                text-shadow: 0px 0px 10px {StyleManager.COLORS['neon_cyan']};
            }}
            
            QLabel#titleSuffix {{
                font-size: 28px;
                font-weight: 300;
                color: {StyleManager.COLORS['text_primary']};
                letter-spacing: 1px;
                margin: 0px;
                padding: 0px;
            }}
            
            QLabel#subtitle {{
                font-size: 14px;
                color: {StyleManager.COLORS['text_secondary']};
                font-weight: 400;
                letter-spacing: 0.5px;
                margin-top: 4px;
            }}
            
            QLabel#timestamp {{
                font-size: 16px;
                font-weight: 600;
                color: {StyleManager.COLORS['neon_teal']};
                letter-spacing: 0.5px;
            }}
            
            QLabel#tabTitle {{
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }}
            
            QFrame#headerFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(26, 26, 46, 0.85), 
                    stop:1 rgba(22, 33, 62, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(45, 45, 77, 0.6);
            }}
            
            QFrame#footerFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(26, 26, 46, 0.85), 
                    stop:1 rgba(22, 33, 62, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(45, 45, 77, 0.6);
            }}
            
            QProgressBar {{
                background: rgba(26, 26, 46, 0.6);
                border: 1px solid rgba(45, 45, 77, 0.6);
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                color: {StyleManager.COLORS['text_primary']};
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_cyan']}, 
                    stop:1 {StyleManager.COLORS['neon_teal']});
                border-radius: 6px;
            }}
            
            QScrollBar:vertical {{
                background-color: rgba(26, 26, 46, 0.4);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_teal']}, 
                    stop:1 rgba(69, 183, 170, 0.8));
                border-radius: 6px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(69, 183, 170, 1.0), 
                    stop:1 rgba(61, 168, 156, 1.0));
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """
        
    def create_enhanced_header(self, parent_layout):
        """Create the enhanced header section with gradients"""
        header = QFrame()
        header.setObjectName("headerFrame")
        header.setFixedHeight(80)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 50))
        shadow.setOffset(0, 4)
        header.setGraphicsEffect(shadow)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        # App info with cooler design
        app_info = QVBoxLayout()
        
        # Create a horizontal layout for the title with accent
        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)  # No spacing between title parts
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main title with modern styling
        title = QLabel("id")
        title.setObjectName("titlePrefix")
        
        title_accent = QLabel("IA")
        title_accent.setObjectName("titleAccent")
        
        title_suffix = QLabel("mas")
        title_suffix.setObjectName("titleSuffix")
        
        title_layout.addWidget(title)
        title_layout.addWidget(title_accent)
        title_layout.addWidget(title_suffix)
        title_layout.addStretch()  # Push everything to the left
        
        subtitle = QLabel("AI-Powered Language Learning")
        subtitle.setObjectName("subtitle")
        
        app_info.addLayout(title_layout)
        app_info.addWidget(subtitle)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Timestamp
        timestamp = QLabel(time.strftime("%H:%M:%S"))
        timestamp.setObjectName("timestamp")
        
        # Close button with professional styling
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeBtn")
        close_btn.setFixedSize(32, 32)
        close_btn.clicked.connect(self.close)
        close_btn.setToolTip("Close")
        
        header_layout.addLayout(app_info)
        header_layout.addWidget(spacer)
        header_layout.addWidget(timestamp)
        header_layout.addWidget(close_btn)
        
        parent_layout.addWidget(header)
        
    def create_enhanced_tabs(self, parent_layout):
        """Create the enhanced tabbed content area"""
        self.tab_widget = QTabWidget()
        
        # Translation tab
        translation_tab = self.create_enhanced_content_tab(
            "ES | Traducción", 
            self.translation_data.get('translation', ''),
            "#00d4ff"
        )
        self.tab_widget.addTab(translation_tab, "ES | Traducción")
        
        # Grammar tab (special handling for word-by-word breakdown)
        grammar_tab = self.create_grammar_tab(
            self.translation_data.get('grammar', '')
        )
        self.tab_widget.addTab(grammar_tab, "※ Gramática")
        
        # Original tab
        original_tab = self.create_enhanced_content_tab(
            "IT | Original", 
            self.translation_data.get('original', ''),
            "#ffa726"
        )
        self.tab_widget.addTab(original_tab, "IT | Original")
        
        parent_layout.addWidget(self.tab_widget)
        
    def create_enhanced_content_tab(self, title, content, accent_color):
        """Create an enhanced content tab with modern styling"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Tab header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("tabTitle")
        title_label.setStyleSheet(f"""
            QLabel#tabTitle {{
                color: {accent_color};
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }}
        """)
        
        # Copy button
        copy_btn = QPushButton("⧉ Copy")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(content))
        copy_btn.setToolTip("Copy to clipboard")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(copy_btn)
        
        layout.addLayout(header_layout)
        
        # Content area with enhanced styling
        content_area = QTextEdit()
        content_area.setPlainText(content)
        content_area.setReadOnly(True)
        content_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Set custom scrollbar styling
        content_area.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #1a1a2e;
                width: 16px;
                border-radius: 8px;
                margin: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4ecdc4, stop:1 #45b7aa);
                border-radius: 8px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45b7aa, stop:1 #3da89c);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        layout.addWidget(content_area)
        
        return tab
    
    def create_grammar_tab(self, content):
        """Create a special grammar tab with word-by-word breakdown"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Tab header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("※ Gramática")
        title_label.setObjectName("tabTitle")
        title_label.setStyleSheet(f"""
            QLabel#tabTitle {{
                color: #4ecdc4;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }}
        """)
        
        # Copy button
        copy_btn = QPushButton("⧉ Copy")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(content))
        copy_btn.setToolTip("Copy to clipboard")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(copy_btn)
        
        layout.addLayout(header_layout)
        
        # Create grammar content with word cards
        grammar_content = self.create_grammar_content(content)
        layout.addWidget(grammar_content)
        
        return tab
    
    def create_grammar_content(self, content: str) -> QWidget:
        """Create grammar explanation content with individual word cards and gradient fade"""
        # Create container widget with relative positioning
        container = QWidget()
        container.setMinimumHeight(400)  # Ensure minimum height for overlay
        
        # Create scroll area
        scroll_area = QScrollArea(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Use a layout to properly manage the scroll area
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll_area)
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)  # Normal margins
        layout.setSpacing(15)
        
        if not content.strip():
            label = QLabel("No grammar explanation available.")
            label.setStyleSheet("color: #666; font-style: italic; font-size: 14px;")
            layout.addWidget(label)
            layout.addStretch()
            scroll_area.setWidget(widget)
            # Add gradient overlay
            gradient_overlay = self.create_gradient_overlay(container)
            return container
        
        # Parse the grammar content into word explanations
        word_explanations = self.parse_word_explanations(content)
        
        if not word_explanations:
            # Fallback to original formatting if parsing fails
            fallback_content = self.create_fallback_grammar_content(content)
            scroll_area.setWidget(fallback_content)
            # Add gradient overlay
            gradient_overlay = self.create_gradient_overlay(container)
            return container
        
        # Create word cards
        for word_data in word_explanations:
            word_card = self.create_word_card(word_data)
            layout.addWidget(word_card)
        
        # Add gradient fade widget at the end
        gradient_fade = self.create_gradient_fade_widget()
        layout.addWidget(gradient_fade)
        
        layout.addStretch()
        scroll_area.setWidget(widget)
        
        # Style the scroll area
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background-color: rgba(26, 26, 46, 0.3);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4ecdc4, stop:1 #45b7aa);
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45b7aa, stop:1 #3d9991);
            }
        """)
        
        return container
    
    def create_gradient_fade_widget(self) -> QWidget:
        """Create a gradient fade widget to place at the end of content"""
        fade_widget = QWidget()
        fade_widget.setFixedHeight(60)
        fade_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(248, 249, 250, 1.0),
                    stop:0.3 rgba(26, 26, 46, 0.3),
                    stop:0.7 rgba(26, 26, 46, 0.8),
                    stop:1.0 rgba(26, 26, 46, 1.0));
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        return fade_widget
    
    def create_gradient_overlay(self, parent: QWidget) -> QWidget:
        """Create a gradient overlay that fades content into the background"""
        overlay = QWidget(parent)
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Allow clicks through
        overlay.setGeometry(0, parent.height() - 80, parent.width(), 80)  # Position at bottom
        overlay.raise_()  # Ensure it's on top
        
        # Create gradient style that matches the tab background and fades from transparent to opaque
        overlay.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 26, 46, 0),
                    stop:0.2 rgba(26, 26, 46, 0.1),
                    stop:0.5 rgba(26, 26, 46, 0.4),
                    stop:0.8 rgba(26, 26, 46, 0.8),
                    stop:1.0 rgba(26, 26, 46, 1.0));
                border: none;
                border-radius: 0px;
            }
        """)
        
        # Position the gradient at the bottom of the visible content area
        def update_overlay_position():
            if parent and overlay:
                # Get the actual scroll area height and position gradient there
                scroll_widget = parent.findChild(QScrollArea)
                if scroll_widget:
                    scroll_height = scroll_widget.height()
                    overlay.setGeometry(0, scroll_height - 80, parent.width(), 80)
                else:
                    # Fallback positioning
                    overlay.setGeometry(0, parent.height() - 80, parent.width(), 80)
                overlay.raise_()
        
        # Connect to resize event (using QTimer for better performance)
        from PyQt6.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(update_overlay_position)
        timer.start(100)  # Update every 100ms
        
        # Initial positioning
        update_overlay_position()
        
        return overlay
    
    def parse_word_explanations(self, content: str) -> list:
        """Parse grammar content into individual word explanations"""
        word_explanations = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for pattern: "word: explanation" or "- word: explanation"
            line = line.lstrip('-•').strip()
            
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    word = parts[0].strip()
                    explanation = parts[1].strip()
                    
                    # Extract grammatical function if in parentheses
                    function = ""
                    if '(' in explanation and ')' in explanation:
                        start = explanation.find('(')
                        end = explanation.find(')', start)
                        if start != -1 and end != -1:
                            function = explanation[start+1:end]
                            explanation = explanation[:start].strip() + explanation[end+1:].strip()
                    
                    word_explanations.append({
                        'word': word,
                        'explanation': explanation,
                        'function': function
                    })
        
        return word_explanations
    
    def create_word_card(self, word_data: dict) -> QWidget:
        """Create a visual card for a single word explanation"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #e9ecef;
                border-radius: 12px;
                margin: 5px;
                padding: 15px;
            }
            QWidget:hover {
                border-color: #4CAF50;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8fffa, stop:1 #f0f8f0);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Word title
        word_label = QLabel(word_data['word'])
        word_label.setStyleSheet("""
            color: #2E7D32;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        layout.addWidget(word_label)
        
        # Grammatical function (if available)
        if word_data['function']:
            function_label = QLabel(f"({word_data['function']})")
            function_label.setStyleSheet("""
                color: #666;
                font-size: 12px;
                font-style: italic;
                margin-bottom: 8px;
            """)
            layout.addWidget(function_label)
        
        # Explanation
        explanation_label = QLabel(word_data['explanation'])
        explanation_label.setStyleSheet("""
            color: #333;
            font-size: 14px;
            line-height: 1.4;
        """)
        explanation_label.setWordWrap(True)
        layout.addWidget(explanation_label)
        
        return card
    
    def create_fallback_grammar_content(self, content: str) -> QWidget:
        """Fallback grammar content if parsing fails"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Split content into lines and process each
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('-') or line.startswith('•'):
                # Bullet point
                line = line.lstrip('-•').strip()
                bullet_widget = QWidget()
                bullet_layout = QHBoxLayout(bullet_widget)
                bullet_layout.setContentsMargins(0, 5, 0, 5)
                
                bullet_label = QLabel("•")
                bullet_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16px;")
                bullet_label.setFixedWidth(20)
                
                text_label = QLabel(line)
                text_label.setStyleSheet("color: #333; font-size: 14px; line-height: 1.6;")
                text_label.setWordWrap(True)
                
                bullet_layout.addWidget(bullet_label)
                bullet_layout.addWidget(text_label)
                layout.addWidget(bullet_widget)
            else:
                # Regular text
                label = QLabel(line)
                label.setStyleSheet("color: #333; font-size: 14px; line-height: 1.6; margin: 5px 0px;")
                label.setWordWrap(True)
                layout.addWidget(label)
        
        layout.addStretch()
        return widget
        
    def create_enhanced_footer(self, parent_layout):
        """Create the enhanced footer section"""
        footer = QFrame()
        footer.setObjectName("footerFrame")
        footer.setFixedHeight(60)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 50))
        shadow.setOffset(0, -4)
        footer.setGraphicsEffect(shadow)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(32, 20, 32, 20)
        
        # Instructions
        instructions = QLabel("Press 'i' to translate, 'q' to exit")
        instructions.setStyleSheet("color: #a8a8a8; font-size: 14px;")
        
        # Status
        status = QLabel("⬢ Learning Italian")
        status.setStyleSheet("color: #4ecdc4; font-size: 14px; font-weight: 600;")
        
        footer_layout.addWidget(instructions)
        footer_layout.addStretch()
        footer_layout.addWidget(status)
        
        parent_layout.addWidget(footer)
        
    def setup_animations(self):
        """Setup enhanced entrance and exit animations"""
        # Simple fade in effect (reduced complexity to avoid crashes)
        try:
            self.setWindowOpacity(0.8)
            fade_anim = QPropertyAnimation(self, b"windowOpacity")
            fade_anim.setDuration(300)
            fade_anim.setStartValue(0.8)
            fade_anim.setEndValue(1.0)
            fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            fade_anim.start()
        except Exception as e:
            print(f"Animation setup error: {e}")
            # Fallback to no animation
            self.setWindowOpacity(1.0)
    
    def setup_dynamic_effects(self):
        """Setup dynamic effects and animations"""
        try:
            # Add enhanced copy feedback animations
            self.setup_enhanced_feedback()
            
            # Add progress indicator in footer if needed
            self.setup_progress_indicator()
            
            # Start any ambient animations
            self.start_ambient_effects()
            
        except Exception as e:
            print(f"Dynamic effects setup error: {e}")
    
    def setup_enhanced_feedback(self):
        """Setup enhanced feedback animations"""
        # This will be used for copy feedback
        pass
    
    def setup_progress_indicator(self):
        """Setup progress indicator in footer"""
        # Add a subtle progress bar for future use
        pass
    
    def start_ambient_effects(self):
        """Start subtle ambient effects"""
        # Add subtle pulsing to accent elements
        try:
            # Find elements with neon colors and add subtle glow animation
            pass
        except Exception as e:
            print(f"Ambient effects error: {e}")
        
    def center_on_screen(self):
        """Center the popup on the screen"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        print(f"Centering popup at: {x}, {y}")
        print(f"Screen size: {screen.width()}x{screen.height()}")
        print(f"Popup size: {self.width()}x{self.height()}")
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard with enhanced feedback"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Show enhanced feedback
        self.show_enhanced_copy_feedback()
        
    def show_enhanced_copy_feedback(self):
        """Show enhanced visual feedback for copy action with floating animation"""
        # Create a premium feedback label
        feedback = QLabel("✨ ¡Copiado! ✓")
        feedback.setParent(self)
        feedback.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_teal']}, 
                    stop:1 {StyleManager.COLORS['success_green']});
                color: white;
                padding: 20px 40px;
                border-radius: 25px;
                font-weight: 700;
                font-size: 18px;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
                letter-spacing: 1px;
                border: 2px solid rgba(78, 205, 196, 0.3);
            }}
        """)
        feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add premium shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(78, 205, 196, 150))
        shadow.setOffset(0, 10)
        feedback.setGraphicsEffect(shadow)
        
        # Position feedback in the center
        feedback.setFixedSize(250, 80)
        start_x = (self.width() - feedback.width()) // 2
        start_y = (self.height() - feedback.height()) // 2
        end_y = start_y - 60  # Float upward
        
        feedback.move(start_x, start_y)
        feedback.show()
        
        # Create animation group for complex effects
        animation_group = QParallelAnimationGroup()
        
        # 1. Floating animation
        float_anim = AnimationManager.create_floating_animation(
            feedback, 
            feedback.pos(), 
            feedback.pos() + QRect(0, -60, 0, 0).topLeft(),
            duration=2500
        )
        
        # 2. Fade out animation
        fade_anim = QPropertyAnimation(feedback, b"windowOpacity")
        fade_anim.setDuration(2500)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        fade_anim.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        # 3. Scale animation for premium effect
        scale_anim = QPropertyAnimation(feedback, b"geometry")
        scale_anim.setDuration(400)
        current_geo = feedback.geometry()
        scaled_geo = QRect(
            current_geo.x() - 10, 
            current_geo.y() - 5, 
            current_geo.width() + 20, 
            current_geo.height() + 10
        )
        scale_anim.setStartValue(current_geo)
        scale_anim.setEndValue(scaled_geo)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # Add animations to group
        animation_group.addAnimation(float_anim)
        animation_group.addAnimation(fade_anim)
        
        # Clean up after animation
        animation_group.finished.connect(feedback.deleteLater)
        
        # Start animations
        scale_anim.start()
        QTimer.singleShot(200, animation_group.start)  # Slight delay for scale effect
        
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)
            
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def closeEvent(self, event):
        """Handle window close event"""
        print("Popup closing...")
        event.accept()

# Global variables to track active popups and prevent rapid triggers
_active_popup_processes = []
_last_popup_time = 0

def mostrar_explicacion_moderna_pyqt6(texto: str):
    """Main function to display translation results in the modern PyQt6 popup"""
    global _active_popup_processes, _last_popup_time
    
    # Prevent rapid-fire popups (wait at least 2 seconds between popups)
    import time
    current_time = time.time()
    if current_time - _last_popup_time < 2.0:
        print("⏰ Popup request too soon, ignoring...")
        return None
    _last_popup_time = current_time
    
    print("🚀 Starting popup display...")
    
    try:
        # Parse the AI response
        sections = parse_ai_response(texto)
        print(f"📄 Parsed sections: {list(sections.keys())}")
        
        # Check if we're in the main thread
        import threading
        is_main_thread = threading.current_thread() is threading.main_thread()
        print(f"🧵 Running in main thread: {is_main_thread}")
        
        if not is_main_thread:
            print("🔄 Not in main thread, using subprocess approach...")
            return _create_subprocess_popup(sections)
        
        # Try direct approach first (simpler and more reliable)
        print("🎯 Attempting direct popup creation...")
        
        # Check if QApplication exists
        app = QApplication.instance()
        if app is None:
            print("📱 Creating new QApplication...")
            app = QApplication(sys.argv)
        else:
            print("📱 Using existing QApplication...")
        
        # Create and show popup directly
        popup = ModernPyQt6Popup(sections)
        popup.show()
        popup.raise_()
        popup.activateWindow()
        
        print("✅ Direct popup created successfully!")
        return popup
        
    except Exception as direct_error:
        print(f"❌ Direct approach failed: {direct_error}")
        print("🔄 Falling back to subprocess approach...")
        
        # Fallback to subprocess approach
        return _create_subprocess_popup(sections)

def _create_subprocess_popup(sections: dict):
    """Create popup using subprocess approach as fallback"""
    global _active_popup_processes
    
    try:
        # Aggressively clean up any existing processes
        print(f"🧹 Cleaning up {len(_active_popup_processes)} existing popup processes...")
        
        # Force kill all existing popup processes immediately
        for process in _active_popup_processes:
            try:
                process.kill()  # Force kill immediately
                print(f"💀 Killed process PID {process.pid}")
            except:
                pass
        
        # Clear the list and also kill any python processes that might be popup subprocesses
        _active_popup_processes.clear()
        
        # Additional cleanup: kill any python processes that might be hanging around
        try:
            import subprocess
            subprocess.run(['taskkill', '/f', '/im', 'python.exe', '/fi', 'WINDOWTITLE eq *'], 
                          capture_output=True, check=False)
        except:
            pass
        
        import subprocess
        import json
        import tempfile
        import os
        
        # Create a temporary file with the translation data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
            temp_file = f.name
        
        # Create unique popup identifier
        import uuid
        popup_id = str(uuid.uuid4())[:8]
        
        # Create a simple subprocess script with unique identification
        popup_script = f'''
import sys
import json
import os
sys.path.insert(0, r"{os.getcwd()}")

# Unique popup identifier
POPUP_ID = "{popup_id}"
print(f"=== POPUP SUBPROCESS STARTED [{{POPUP_ID}}] ===")

try:
    from PyQt6.QtWidgets import QApplication
    from modern_popup_pyqt6 import ModernPyQt6Popup
    
    with open(r"{temp_file}", 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    app = QApplication(sys.argv)
    popup = ModernPyQt6Popup(sections)
    popup.setWindowTitle(f"idIAmas [{{POPUP_ID}}]")  # Set unique title
    popup.show()
    popup.raise_()
    popup.activateWindow()
    
    print(f"✅ Popup [{{POPUP_ID}}] displayed successfully!")
    result = app.exec()
    print(f"📄 Popup [{{POPUP_ID}}] closed with result: {{result}}")
    
except Exception as e:
    print(f"❌ ERROR in popup [{{POPUP_ID}}]: {{e}}")
    import traceback
    traceback.print_exc()
finally:
    try:
        os.unlink(r"{temp_file}")
    except:
        pass
    print(f"🗑️ Popup [{{POPUP_ID}}] cleanup completed")
'''
        
        # Write and launch script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(popup_script)
            script_file = f.name
        
        if sys.platform == 'win32':
            # Hide the console window for a cleaner experience
            process = subprocess.Popen([sys.executable, script_file], 
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen([sys.executable, script_file])
        
        _active_popup_processes.append(process)
        print(f"✨ Subprocess popup launched [PID: {process.pid}, ID: {popup_id}]")
        
        # Wait a moment to ensure the process starts
        import time
        time.sleep(0.5)
        
        if process.poll() is not None:
            print(f"⚠️ Popup process exited immediately with code: {process.returncode}")
            _active_popup_processes.remove(process)
        
        return None
        
    except Exception as e:
        print(f"❌ Subprocess creation failed: {e}")
        return None

def parse_ai_response(texto: str) -> dict:
    """Parse the AI response into structured sections"""
    print(f"🔍 Parsing AI response:\n{texto}\n" + "="*50)
    
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
            
        # Detect section headers (support both English and Spanish for compatibility)
        if any(keyword in line.lower() for keyword in ['original text', 'texto original', 'italiano', 'original', 'frase']):
            current_section = 'original'
            continue
        elif any(keyword in line.lower() for keyword in ['translation to', 'traducción al español', 'español', 'traducción', 'traducida', 'translation']):
            current_section = 'translation'
            continue
        elif any(keyword in line.lower() for keyword in ['grammar explanation', 'explicación gramatical', 'gramática', 'explicación', 'palabras', 'función']):
            current_section = 'grammar'
            continue
            
        # Add line to current section
        if current_section in sections:
            sections[current_section] += line + '\n'
    
    # Debug output
    print(f"🎯 Parsed sections:")
    for section_name, content in sections.items():
        content_preview = content[:100] + "..." if len(content) > 100 else content
        print(f"  {section_name}: {len(content)} chars - {content_preview.strip()}")
            
    return sections

if __name__ == "__main__":
    # Test the modern PyQt6 popup
    test_text = """
    ORIGINAL TEXT:
    Ciao, come stai?
    
    TRANSLATION TO SPANISH:
    Hola, ¿cómo estás?
    
    GRAMMAR EXPLANATION:
    - Ciao: informal greeting in Italian
    - come: how (interrogative adverb)
    - stai: second person of the verb 'stare' (to be/stay)
    """
    
    # Import new popup implementation
    try:
        from popup_refactored import PopupWindow
        USE_NEW_POPUP = True
    except ImportError:
        USE_NEW_POPUP = False
        print("⚠️ New popup implementation not found, using old implementation")
    
    # Create QApplication and show popup
    app = QApplication(sys.argv)
    
    if USE_NEW_POPUP:
        sections = parse_ai_response(test_text)
        popup = PopupWindow(sections)
        popup.show()
    else:
        popup = mostrar_explicacion_moderna_pyqt6(test_text)
    
    # Run the event loop
    app.exec()


def show_modern_popup(texto: str):
    """
    New main function to display translation results using subprocess approach.
    Always uses subprocess to avoid threading issues with QApplication.
    """
    global _active_popup_processes, _last_popup_time
    
    # Prevent rapid-fire popups (wait at least 2 seconds between popups)
    import time
    current_time = time.time()
    if current_time - _last_popup_time < 2.0:
        print("⏰ Popup request too soon, ignoring...")
        return None
    _last_popup_time = current_time
    
    print("🚀 Starting modern popup display...")
    
    try:
        # Parse the AI response
        sections = parse_ai_response(texto)
        print(f"📄 Parsed sections: {list(sections.keys())}")
        
        # Always use subprocess approach to avoid threading issues
        return _create_modern_subprocess_popup(sections)
        
    except Exception as error:
        print(f"❌ Error creating modern popup: {error}")
        print("🔄 Falling back to old implementation...")
        return _create_subprocess_popup(sections)


def _create_modern_subprocess_popup(sections: dict):
    """Create modern popup using subprocess approach"""
    global _active_popup_processes
    
    try:
        # Aggressively clean up any existing processes
        print(f"🧹 Cleaning up {len(_active_popup_processes)} existing popup processes...")
        
        # Force kill all existing popup processes immediately
        for process in _active_popup_processes:
            try:
                process.kill()  # Force kill immediately
                print(f"💀 Killed process PID {process.pid}")
            except:
                pass
        
        # Clear the list
        _active_popup_processes.clear()
        
        import subprocess
        import json
        import tempfile
        import os
        import uuid
        
        # Create a temporary file with the translation data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
            temp_file = f.name
        
        # Create unique popup identifier
        popup_id = str(uuid.uuid4())[:8]
        
        # Create a subprocess script using the new popup implementation
        popup_script = f'''
import sys
import json
import os
sys.path.insert(0, r"{os.getcwd()}")

# Unique popup identifier
POPUP_ID = "{popup_id}"
print(f"=== MODERN POPUP SUBPROCESS STARTED [{{POPUP_ID}}] ===")

try:
    from PyQt6.QtWidgets import QApplication
    from popup_refactored import PopupWindow
    
    with open(r"{temp_file}", 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    app = QApplication(sys.argv)
    popup = PopupWindow(sections)
    popup.setWindowTitle(f"idIAmas [{{POPUP_ID}}]")  # Set unique title
    popup.show()
    popup.raise_()
    popup.activateWindow()
    
    print(f"✅ Modern Popup [{{POPUP_ID}}] displayed successfully!")
    result = app.exec()
    print(f"📄 Modern Popup [{{POPUP_ID}}] closed with result: {{result}}")
    
except Exception as e:
    print(f"❌ ERROR in modern popup [{{POPUP_ID}}]: {{e}}")
    import traceback
    traceback.print_exc()
finally:
    try:
        os.unlink(r"{temp_file}")
    except:
        pass
    print(f"🗑️ Modern Popup [{{POPUP_ID}}] cleanup completed")
'''
        
        # Write and launch script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(popup_script)
            script_file = f.name
        
        if sys.platform == 'win32':
            # Hide the console window for a cleaner experience
            process = subprocess.Popen([sys.executable, script_file], 
                                     creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            process = subprocess.Popen([sys.executable, script_file])
        
        _active_popup_processes.append(process)
        print(f"✨ Modern subprocess popup launched [PID: {process.pid}, ID: {popup_id}]")
        
        # Wait a moment to ensure the process starts
        import time
        time.sleep(0.5)
        
        if process.poll() is not None:
            print(f"⚠️ Modern popup process exited immediately with code: {process.returncode}")
            return None
        
        return process
        
    except Exception as e:
        print(f"❌ Error creating modern subprocess popup: {e}")
        return None
