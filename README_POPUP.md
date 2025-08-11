# Modern Popup Implementation with Fade Overlay

This documentation explains the refactored popup implementation featuring a professional fade overlay for smooth content blending.

## Architecture Overview

### PopupWindow Class
The main popup window with modern design features:
- Frameless, rounded design with drop shadow
- Translucent background for professional appearance
- Responsive to system light/dark themes
- Keyboard shortcuts (Esc to close, Ctrl+C to copy)

### FadeOverlay Class
A sophisticated overlay widget that creates a gradient fade effect:

```python
class FadeOverlay(QWidget):
    def __init__(self, scroll_area: QScrollArea, fade_height: int = 64):
        super().__init__(scroll_area.viewport())
        # Attaches directly to scroll area viewport
```

## Fade Overlay Implementation

### How It Works
1. **Attachment**: The overlay is created as a child of the scroll area's viewport
2. **Transparency**: Uses `WA_TransparentForMouseEvents` to allow interaction with content below
3. **Positioning**: Automatically positions at the bottom of the visible area
4. **Gradient**: Paints a vertical gradient from transparent to background color

### Key Features

#### Automatic Scroll Tracking
```python
def connect_scroll_tracking(self):
    if self.scroll_area.verticalScrollBar():
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_position)
```

#### Theme-Aware Colors
```python
def get_background_colors(self):
    palette = self.palette()
    bg_color = palette.color(QPalette.ColorRole.Window)
    
    if bg_color.lightness() < 50:  # Dark theme
        return QColor(26, 26, 46, 255), QColor(26, 26, 46, 0)
    else:  # Light theme
        return QColor(248, 249, 250, 255), QColor(248, 249, 250, 0)
```

#### Smooth Gradient Rendering
```python
def paintEvent(self, event):
    painter = QPainter(self)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
    
    gradient = QLinearGradient(0, 0, 0, self.height())
    gradient.setColorAt(0.0, bg_transparent)  # Top: transparent
    gradient.setColorAt(0.3, QColor(..., 77))   # 30% opacity
    gradient.setColorAt(0.7, QColor(..., 204))  # 80% opacity  
    gradient.setColorAt(1.0, bg_opaque)         # Bottom: fully opaque
```

## Grammar Cards

### GrammarCard Class
Individual cards for word explanations:
- Clean, rounded design with hover effects
- Proper spacing and typography
- Word title with accent color
- Grammatical function in italics
- Clear explanation text

### Card Styling
```python
#grammarCard {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    margin-bottom: 8px;
}

#grammarCard:hover {
    border-color: #00d4ff;
    background: rgba(0, 212, 255, 0.05);
}
```

## Configuration & Customization

### Fade Height
Adjust the fade overlay height:
```python
fade_overlay = FadeOverlay(scroll_area, fade_height=80)  # Default: 64px
```

### Gradient Opacity
Modify gradient stops in `paintEvent()`:
```python
gradient.setColorAt(0.0, bg_transparent)  # Start transparency
gradient.setColorAt(0.3, QColor(..., 77))   # Early fade (30% opacity)
gradient.setColorAt(0.7, QColor(..., 204))  # Late fade (80% opacity)
gradient.setColorAt(1.0, bg_opaque)         # Full opacity
```

### Theme Colors
The overlay automatically adapts to system themes by reading `QPalette.ColorRole.Window`.

## Usage Example

### Basic Implementation
```python
# Create scroll area
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)

# Add content
content_widget = QWidget()
# ... add cards to content_widget ...
scroll_area.setWidget(content_widget)

# Add fade overlay
fade_overlay = FadeOverlay(scroll_area)
```

### Integration with PopupWindow
```python
# In create_grammar_tab()
scroll_area = QScrollArea()
# ... setup content ...

# Add fade overlay automatically
fade_overlay = FadeOverlay(scroll_area)
self.fade_overlays.append(fade_overlay)
```

## Performance Considerations

### Optimizations
- Uses `CompositionMode_SourceOver` for efficient blending
- Repaints only on scroll/resize events
- Minimal overhead with transparent background
- No blocking operations in paintEvent

### Memory Management
- Overlays are stored in popup's `fade_overlays` list
- Automatic cleanup when popup closes
- No memory leaks with proper parent-child relationships

## Testing

Run the standalone popup:
```bash
python popup_refactored.py
```

This opens a test window with sample grammar cards demonstrating the fade effect.

## Migration Notes

### From Old Implementation
The new implementation replaces:
- Old gradient overlay with timer-based positioning
- Hardcoded colors with theme-aware colors
- Fixed positioning with dynamic viewport tracking
- Multiple overlay widgets with single efficient overlay

### Benefits
- ✅ Smooth, non-blocking fade effect
- ✅ Proper scroll tracking without jank
- ✅ Theme compatibility (light/dark)
- ✅ Better performance and memory usage
- ✅ Professional, modern appearance
- ✅ High-DPI support
- ✅ Keyboard shortcuts and accessibility
