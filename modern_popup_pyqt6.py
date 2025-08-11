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
        
        # Set window size and position
        self.resize(1000, 750)
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_teal']}, 
                    stop:1 rgba(69, 183, 170, 0.9));
                color: white;
                border: 1px solid rgba(78, 205, 196, 0.3);
                padding: 14px 28px;
                border-radius: 14px;
                font-weight: 600;
                font-size: 15px;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(69, 183, 170, 1.0), 
                    stop:1 rgba(61, 168, 156, 1.0));
                border: 1px solid {StyleManager.COLORS['neon_teal']};
            }}
            
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(61, 168, 156, 1.0), 
                    stop:1 rgba(53, 154, 143, 1.0));
            }}
            
            QPushButton#closeBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {StyleManager.COLORS['neon_red']}, 
                    stop:1 rgba(255, 82, 82, 0.9));
                padding: 10px 18px;
                font-size: 18px;
                border-radius: 20px;
                border: 1px solid rgba(255, 107, 107, 0.3);
            }}
            
            QPushButton#closeBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 82, 82, 1.0), 
                    stop:1 rgba(255, 68, 68, 1.0));
                border: 1px solid {StyleManager.COLORS['neon_red']};
            }}
            
            QLabel {{
                color: {StyleManager.COLORS['text_primary']};
                font-weight: 500;
                font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
            }}
            
            QLabel#title {{
                font-size: 32px;
                font-weight: 800;
                color: {StyleManager.COLORS['neon_cyan']};
                letter-spacing: 1px;
            }}
            
            QLabel#subtitle {{
                font-size: 18px;
                color: {StyleManager.COLORS['text_secondary']};
                font-weight: 400;
                letter-spacing: 0.5px;
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
        header.setFixedHeight(100)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 50))
        shadow.setOffset(0, 4)
        header.setGraphicsEffect(shadow)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 24, 32, 24)
        
        # App info
        app_info = QVBoxLayout()
        
        title = QLabel("🎯 idIAmas")
        title.setObjectName("title")
        
        subtitle = QLabel("Traducción & Aprendizaje Inteligente")
        subtitle.setObjectName("subtitle")
        
        app_info.addWidget(title)
        app_info.addWidget(subtitle)
        
        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Timestamp
        timestamp = QLabel(time.strftime("%H:%M:%S"))
        timestamp.setObjectName("timestamp")
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.setFixedSize(40, 40)
        close_btn.clicked.connect(self.close)
        
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
            "🇪🇸 Traducción", 
            self.translation_data.get('translation', ''),
            "#00d4ff"
        )
        self.tab_widget.addTab(translation_tab, "🇪🇸 Traducción")
        
        # Grammar tab
        grammar_tab = self.create_enhanced_content_tab(
            "📚 Gramática", 
            self.translation_data.get('grammar', ''),
            "#4ecdc4"
        )
        self.tab_widget.addTab(grammar_tab, "📚 Gramática")
        
        # Original tab
        original_tab = self.create_enhanced_content_tab(
            "🇮🇹 Original", 
            self.translation_data.get('original', ''),
            "#ffa726"
        )
        self.tab_widget.addTab(original_tab, "🇮🇹 Original")
        
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
        copy_btn = QPushButton("📋 Copiar")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(content))
        
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
        
    def create_enhanced_footer(self, parent_layout):
        """Create the enhanced footer section"""
        footer = QFrame()
        footer.setObjectName("footerFrame")
        footer.setFixedHeight(80)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 212, 255, 50))
        shadow.setOffset(0, -4)
        footer.setGraphicsEffect(shadow)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(32, 20, 32, 20)
        
        # Instructions
        instructions = QLabel("Presiona 'i' para traducir, 'q' para salir")
        instructions.setStyleSheet("color: #a8a8a8; font-size: 14px;")
        
        # Status
        status = QLabel("🎯 Aprendiendo Italiano")
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
    
    # Prevent rapid-fire popups (wait at least 1 second between popups)
    import time
    current_time = time.time()
    if current_time - _last_popup_time < 1.0:
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
        # Clean up any finished processes first
        _active_popup_processes = [p for p in _active_popup_processes if p.poll() is None]
        
        # Close any existing popups to prevent multiple popups
        for process in _active_popup_processes:
            try:
                process.terminate()
                process.wait(timeout=2)  # Wait up to 2 seconds for clean termination
            except:
                try:
                    process.kill()  # Force kill if terminate doesn't work
                except:
                    pass
        _active_popup_processes.clear()
        
        import subprocess
        import json
        import tempfile
        import os
        
        # Create a temporary file with the translation data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
            temp_file = f.name
        
        # Create a simple subprocess script
        popup_script = f'''
import sys
import json
import os
sys.path.insert(0, r"{os.getcwd()}")

print("=== POPUP SUBPROCESS STARTED ===")
try:
    from PyQt6.QtWidgets import QApplication
    from modern_popup_pyqt6 import ModernPyQt6Popup
    
    with open(r"{temp_file}", 'r', encoding='utf-8') as f:
        sections = json.load(f)
    
    app = QApplication(sys.argv)
    popup = ModernPyQt6Popup(sections)
    popup.show()
    popup.raise_()
    popup.activateWindow()
    
    print("✅ Popup displayed successfully!")
    result = app.exec()
    
except Exception as e:
    print(f"❌ ERROR: {{e}}")
    import traceback
    traceback.print_exc()
finally:
    try:
        os.unlink(r"{temp_file}")
    except:
        pass
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
        print("✨ Subprocess popup launched")
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
            
        # Detect section headers
        if any(keyword in line.lower() for keyword in ['texto original', 'italiano', 'original', 'frase']):
            current_section = 'original'
            continue
        elif any(keyword in line.lower() for keyword in ['traducción al español', 'español', 'traducción', 'traducida']):
            current_section = 'translation'
            continue
        elif any(keyword in line.lower() for keyword in ['explicación gramatical', 'gramática', 'explicación', 'palabras', 'función']):
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
    TEXTO ORIGINAL:
    Ciao, come stai?
    
    TRADUCCIÓN AL ESPAÑOL:
    Hola, ¿cómo estás?
    
    EXPLICACIÓN GRAMATICAL:
    - Ciao: saludo informal en italiano
    - come: cómo (adverbio interrogativo)
    - stai: segunda persona del verbo 'stare' (estar)
    """
    
    # Create QApplication and show popup
    app = QApplication(sys.argv)
    popup = mostrar_explicacion_moderna_pyqt6(test_text)
    
    # Run the event loop
    app.exec()
