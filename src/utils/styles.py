"""
Modern Design Styles for Café 216 POS System
"""

class ModernStyles:
    """Modern button and UI styles with contemporary design"""
    
    # Color Palette
    PRIMARY = "#6B4CE6"        # Modern purple
    SECONDARY = "#1F2937"      # Dark gray
    SUCCESS = "#10B981"        # Green
    DANGER = "#EF4444"         # Red
    WARNING = "#F59E0B"        # Amber
    INFO = "#3B82F6"           # Blue
    LIGHT_BG = "#F9FAFB"       # Very light gray
    BORDER = "#E5E7EB"         # Light border
    TEXT_PRIMARY = "#111827"   # Dark text
    TEXT_SECONDARY = "#6B7280" # Gray text
    CARD_BG = "#FFFFFF"        # White card
    
    @staticmethod
    def card_style():
        """Modern card container with shadow"""
        return f"""
            QWidget {{
                background-color: {ModernStyles.CARD_BG};
                border-radius: 12px;
                border: 1px solid {ModernStyles.BORDER};
            }}
        """
    
    @staticmethod
    def modern_table():
        """Enhanced table styling with better visuals"""
        return f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {ModernStyles.BORDER};
                border-radius: 8px;
                gridline-color: {ModernStyles.BORDER};
                selection-background-color: {ModernStyles.PRIMARY};
                selection-color: white;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {ModernStyles.PRIMARY};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {ModernStyles.SECONDARY};
                color: white;
                padding: 12px;
                font-weight: 600;
                font-size: 12px;
                border: none;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 8px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 8px;
            }}
        """
    
    @staticmethod
    def modern_input():
        """Modern input field styling"""
        return f"""
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                padding: 10px 12px;
                border: 2px solid {ModernStyles.BORDER};
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                color: {ModernStyles.TEXT_PRIMARY};
            }}
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {ModernStyles.PRIMARY};
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {ModernStyles.TEXT_SECONDARY};
                margin-right: 8px;
            }}
        """
    
    @staticmethod
    def modern_label(size="normal"):
        """Modern label styling"""
        font_size = "14px" if size == "normal" else "18px" if size == "large" else "12px"
        font_weight = "600" if size == "large" else "500"
        
        return f"""
            QLabel {{
                color: {ModernStyles.TEXT_PRIMARY};
                font-size: {font_size};
                font-weight: {font_weight};
                padding: 4px 0;
            }}
        """
    
    @staticmethod
    def modern_button(color=None, size="normal"):
        """Modern button style with smooth animations and shadows"""
        if color is None:
            color = ModernStyles.PRIMARY
        
        padding = "12px 24px" if size == "normal" else "8px 16px" if size == "small" else "14px 28px"
        height = "40px" if size == "normal" else "32px" if size == "small" else "48px"
        
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: {padding};
                font-weight: 600;
                font-size: 12px;
                letter-spacing: 0.5px;
                min-height: {height};
            }}
            QPushButton:hover {{
                background-color: {ModernStyles._lighten(color, 10)};
                border: 1px solid {ModernStyles._lighten(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles._darken(color, 10)};
            }}
            QPushButton:disabled {{
                background-color: #D1D5DB;
                color: #9CA3AF;
            }}
        """
    
    @staticmethod
    def modern_button_outline(color=None):
        """Outline button style"""
        if color is None:
            color = ModernStyles.PRIMARY
        
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: 2px solid {color};
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles._lighten(color, 95)};
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles._lighten(color, 85)};
            }}
            QPushButton:disabled {{
                border-color: #D1D5DB;
                color: #9CA3AF;
            }}
        """
    
    @staticmethod
    def sidebar_button():
        """Modern sidebar button with left border indicator"""
        return f"""
            QPushButton {{
                background-color: {ModernStyles.SECONDARY};
                color: white;
                border: none;
                border-left: 3px solid transparent;
                padding: 12px 16px;
                text-align: left;
                font-weight: 500;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #374151;
                border-left: 3px solid {ModernStyles.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles.PRIMARY};
                color: white;
                border-left: 3px solid {ModernStyles.PRIMARY};
            }}
            QPushButton:disabled {{
                background-color: #4B5563;
                color: #9CA3AF;
            }}
        """
    
    @staticmethod
    def table_button(style="edit"):
        """Modern table action button"""
        if style == "edit":
            color = ModernStyles.INFO
        elif style == "delete":
            color = ModernStyles.DANGER
        elif style == "add":
            color = ModernStyles.SUCCESS
        else:
            color = ModernStyles.PRIMARY
        
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
                font-size: 11px;
                min-width: 60px;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles._lighten(color, 10)};
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles._darken(color, 10)};
            }}
        """
    
    @staticmethod
    def icon_button(size="normal"):
        """Icon-only button style"""
        return f"""
            QPushButton {{
                background-color: {ModernStyles.LIGHT_BG};
                color: {ModernStyles.TEXT_PRIMARY};
                border: 1px solid {ModernStyles.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles.BORDER};
                border: 1px solid {ModernStyles.PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles.PRIMARY};
                color: white;
            }}
        """
    
    @staticmethod
    def large_action_button(color=None):
        """Large primary action button"""
        if color is None:
            color = ModernStyles.PRIMARY
        
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 28px;
                font-weight: 700;
                font-size: 14px;
                letter-spacing: 0.5px;
                min-height: 48px;
            }}
            QPushButton:hover {{
                background-color: {ModernStyles._lighten(color, 10)};
                border: none;
            }}
            QPushButton:pressed {{
                background-color: {ModernStyles._darken(color, 15)};
            }}
        """
    
    @staticmethod
    def dialog_button(is_primary=True):
        """Dialog/Modal button style"""
        if is_primary:
            color = ModernStyles.PRIMARY
            return f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: 600;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: {ModernStyles._lighten(color, 10)};
                }}
                QPushButton:pressed {{
                    background-color: {ModernStyles._darken(color, 10)};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: {ModernStyles.LIGHT_BG};
                    color: {ModernStyles.TEXT_PRIMARY};
                    border: 1px solid {ModernStyles.BORDER};
                    border-radius: 6px;
                    padding: 10px 20px;
                    font-weight: 600;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: #F3F4F6;
                    border: 1px solid {ModernStyles.PRIMARY};
                }}
            """
    
    @staticmethod
    def _lighten(color, percent):
        """Lighten a hex color by a percentage"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(int(min(255, c + (255 - c) * percent / 100)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    @staticmethod
    def _darken(color, percent):
        """Darken a hex color by a percentage"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(int(c * (100 - percent) / 100) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
