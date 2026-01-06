from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QStackedWidget, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
from src.screens.pos_screen import POSScreen
from src.screens.products_screen import ProductsScreen
from src.screens.orders_screen import OrdersScreen
from src.screens.reports_screen import ReportsScreen
from src.screens.settings_screen import SettingsScreen
from src.screens.price_management_screen import PriceManagementScreen
from src.screens.stock_management_screen import StockManagementScreen
from src.screens.tables_screen import TablesScreen
from src.database import Database
import os

class MainWindow(QMainWindow):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.allowed_indices = {0} if (current_user and current_user['role'] == 'employé') else set(range(8))
        self.init_ui()
        self.setWindowTitle("Café 216 - POS System")
        self.setGeometry(0, 0, 1400, 900)
        self.showMaximized()

    def init_ui(self):
        self.primary_color = "#C8A882"  # Warm beige/coffee
        self.secondary_color = "#2C2C2C"  # Dark charcoal
        self.accent_color = "#D4A574"  # Gold accent
        self.background_color = "#F8F6F3"  # Off-white
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (sidebar + contenu)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar de navigation
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 0)
        
        # Stack widget pour les écrans
        self.stacked_widget = QStackedWidget()
        
        self.pos_screen = POSScreen(self.db, self.current_user)
        self.products_screen = ProductsScreen(self.db)
        self.price_management_screen = PriceManagementScreen(self.db)
        self.stock_management_screen = StockManagementScreen(self.db)
        self.tables_screen = TablesScreen(self.db)
        self.orders_screen = OrdersScreen(self.db)
        self.reports_screen = ReportsScreen(self.db)
        self.settings_screen = SettingsScreen(self.db)
        
        self.stacked_widget.addWidget(self.pos_screen)
        self.stacked_widget.addWidget(self.products_screen)
        self.stacked_widget.addWidget(self.price_management_screen)
        self.stacked_widget.addWidget(self.stock_management_screen)
        self.stacked_widget.addWidget(self.tables_screen)
        self.stacked_widget.addWidget(self.orders_screen)
        self.stacked_widget.addWidget(self.reports_screen)
        self.stacked_widget.addWidget(self.settings_screen)
        
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Afficher l'écran POS par défaut
        self.stacked_widget.setCurrentIndex(0)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(10, 15, 10, 15)
        
        title = QLabel("CAFÉ 216")
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {self.accent_color}; font-weight: bold;")
        logo_layout.addWidget(title)
        
        subtitle = QLabel("POS System")
        subtitle_font = QFont("Arial", 9)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: white;")
        logo_layout.addWidget(subtitle)
        
        logo_container.setStyleSheet(f"background-color: {self.secondary_color}; padding: 5px;")
        sidebar_layout.addWidget(logo_container)
        
        nav_buttons = [
            ("Ventes", 0, "☕"),
            ("Produits", 1, "📦"),
            ("Prix & Produits", 2, "💰"),
            ("Stock", 3, "📊"),
            ("Tables", 4, "🪑"),
            ("Commandes", 5, "📋"),
            ("Rapports", 6, "📈"),
            ("Paramètres", 7, "⚙️")
        ]
        
        for btn_text, index, icon in nav_buttons:
            btn = QPushButton(f"{icon}\n{btn_text}")
            btn.setFixedHeight(70)
            btn.setFont(QFont("Arial", 10, QFont.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.secondary_color};
                    border: none;
                    color: white;
                    border-left: 4px solid transparent;
                }}
                QPushButton:hover {{
                    background-color: #3a3a3a;
                    border-left: 4px solid {self.accent_color};
                }}
                QPushButton:pressed {{
                    background-color: {self.accent_color};
                    color: {self.secondary_color};
                }}
                QPushButton:disabled {{
                    background-color: #444444;
                    color: #AAAAAA;
                }}
            """)
            if index in self.allowed_indices:
                btn.clicked.connect(lambda checked, i=index: self.navigate(i))
            else:
                btn.setDisabled(True)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()

        if self.current_user:
            user_info = QLabel(f"Connecté: {self.current_user['username']}\nRôle: {self.current_user['role']}")
            user_info.setAlignment(Qt.AlignCenter)
            user_info.setStyleSheet("color: white; padding: 8px;")
            sidebar_layout.addWidget(user_info)
        
        # Bouton déconnexion
        logout_btn = QPushButton("Déconnexion")
        logout_btn.setFixedHeight(50)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #CC3333;
                color: white;
                border: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #992222;
            }}
        """)
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn)
        
        sidebar.setStyleSheet(f"background-color: {self.secondary_color};")
        return sidebar

    def navigate(self, index: int):
        if index in self.allowed_indices:
            self.stacked_widget.setCurrentIndex(index)
